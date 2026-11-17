"""Genera un zapato estilizado por partes, cada una con su material.

Uso:
  blender -b -P zapato.py -- --modelo samba --variante clasico --render --glb

La capellada es una superficie S(u, v): u recorre el contorno del pie y
v sube desde la suela hasta la abertura. Los paneles (rayas, puntera,
talon) son parches sobre esa misma superficie, por eso quedan pegados.
"""
import argparse
import math
import os
import sys

import addon_utils
import bmesh
import bpy
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from modelos import MODELOS, PRODUCTOS  # noqa: E402


# --- curvas ---------------------------------------------------------------

def catmull_cerrada(puntos, pasos=60):
    p = np.array(puntos, float)
    n = len(p)
    salida = []
    for i in range(n):
        p0, p1, p2, p3 = p[i - 1], p[i], p[(i + 1) % n], p[(i + 2) % n]
        for t in np.linspace(0, 1, pasos, endpoint=False):
            salida.append(0.5 * (2 * p1 + (p2 - p0) * t
                                 + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                                 + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3))
    return np.array(salida)


class Lazo:
    """Curva cerrada parametrizada por longitud de arco, u en [0, 1)."""

    def __init__(self, puntos):
        d = catmull_cerrada(puntos)
        d = np.vstack([d, d[:1]])
        s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(d, axis=0), axis=1))])
        self.s = s / s[-1]
        self.d = d

    def __call__(self, u):
        u = np.mod(u, 1.0)
        return np.stack([np.interp(u, self.s, self.d[:, 0]),
                         np.interp(u, self.s, self.d[:, 1])], axis=-1)

    def normal(self, u):
        t = self(u + 1e-3) - self(u - 1e-3)
        t = t / np.linalg.norm(t, axis=-1, keepdims=True)
        return np.stack([t[..., 1], -t[..., 0]], axis=-1)


def perfil(puntos, suavizado=1.2):
    """Interpolacion suave de z en funcion de x."""
    xs, zs = zip(*puntos)
    x = np.linspace(min(xs) - 12, max(xs) + 12, 800)
    z = np.interp(x, xs, zs)
    paso = x[1] - x[0]
    k = np.arange(-40, 41) * paso
    g = np.exp(-(k / suavizado) ** 2 / 2)
    z = np.convolve(np.pad(z, 40, mode='edge'), g / g.sum(), mode='valid')
    return lambda q: np.interp(q, x, z)


def suave(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


# --- la horma -------------------------------------------------------------

class Horma:
    def __init__(self, m):
        self.m = m
        self.contorno = Lazo(m['contorno'])
        self.abertura = Lazo(m['abertura'])
        self.borde = perfil(m['borde'])
        self.base = perfil(m['base'], 2.5)
        self.signo = 1.0
        # ancho del pie en cada x, para la cupula de la punta
        xs = np.linspace(0, 30, 160)
        ext = self.contorno(np.linspace(0.0, 0.5, 400))
        intr = self.contorno(np.linspace(1.0, 0.5, 400))
        self.x_lado = xs
        self.y_ext = np.interp(xs, *self._monotono(ext))
        self.y_int = np.interp(xs, *self._monotono(intr))
        # techo de la punta: un cuarto de elipse desde la garganta hasta la nariz,
        # y una subida suave hacia atras para no tocar el resto del zapato
        garganta = self.garganta = float(np.max(np.array(m['abertura'])[:, 0]))
        alto = float(self.borde(garganta)) + 0.4 - float(self.base(garganta))
        largo = 30.7 - garganta

        def altura_punta(q):
            t = np.clip((q - garganta) / largo, 0, 1)
            elipse = np.sqrt(np.clip(1 - t ** 2, 0, 1)) ** 0.85
            subida = 8 * np.logaddexp(0, (garganta - q) / 1.2)
            return self.base(q) + alto * elipse + subida

        self.altura_punta = altura_punta

    @staticmethod
    def _monotono(puntos):
        """Ordena (x, y) por x para poder interpolar y en funcion de x."""
        orden = np.argsort(puntos[:, 0])
        return puntos[orden, 0], puntos[orden, 1]

    def curvar(self, p):
        """Levanta la punta (toe spring)."""
        p = np.array(p, float)
        x0, alto = self.m['punta']
        t = np.clip((p[..., 0] - x0) / (30 - x0), 0, None)
        p[..., 2] += alto * t ** 2 + self.m.get('elevar', 0)
        if 'arco_talon' in self.m:
            x1, subida = self.m['arco_talon']
            p[..., 2] += subida * np.clip((x1 - p[..., 0]) / x1, 0, None) ** 2
        return p

    def plano(self, u, v):
        """Superficie sin curvar, con u y v escalares o arreglos."""
        u, v = np.asarray(u, float), np.asarray(v, float)
        c, o = self.contorno(u), self.abertura(u)
        cuello = 1 - suave(*self.m['cuello'], o[..., 0])
        ang = v * math.pi / 2
        exp = 2 / self.m.get('caja', 2.7)
        f = (1 - cuello) * (1 - np.cos(ang) ** exp) + cuello * v ** 1.7
        g = (1 - cuello) * np.sin(ang) ** exp + cuello * v ** 0.9
        # en la punta la capellada baja en pendiente, no en curva abombada
        xy = c + (o - c) * f[..., None]
        zb, zt = self.base(c[..., 0]) - 0.45, self.borde(o[..., 0])
        z = zb + (zt - zb) * g
        z = self.cupula(xy, z)
        return np.concatenate([xy, z[..., None]], axis=-1)

    def cupula(self, xy, z, suavidad=0.35):
        """Baja la punta con una cupula: alta hacia los cordones, baja en la punta."""
        x, y = xy[..., 0], xy[..., 1]
        centro = (np.interp(x, self.x_lado, self.y_ext) + np.interp(x, self.x_lado, self.y_int)) / 2
        medio = np.maximum((np.interp(x, self.x_lado, self.y_int) - np.interp(x, self.x_lado, self.y_ext)) / 2, 0.5)
        r = np.clip(np.abs(y - centro) / medio, 0, 1)
        # junto a la garganta la cupula aun no redondea los lados
        w = suave(self.garganta, self.garganta + 4.5, x)
        # la pared de la punta sube un poco recta antes de curvarse
        labio = self.base(x) + 0.9
        techo = labio + (self.altura_punta(x) - labio) * (1 - w * r ** 2.4) ** 0.45
        return -suavidad * np.logaddexp(-z / suavidad, -techo / suavidad)

    def S(self, u, v):
        return self.curvar(self.plano(u, v))

    def normal(self, u, v):
        e = 2e-3
        du = self.S(u + e, v) - self.S(u - e, v)
        dv = self.S(u, np.clip(v + e, 0, 1)) - self.S(u, np.clip(v - e, 0, 1))
        n = np.cross(du, dv) * self.signo
        return n / np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-9)

    def u_de_x(self, x, v, lado):
        """Halla u para una x del mundo; lado -1 externo (y<0), +1 interno."""
        us = np.linspace(0.02, 0.48, 400) if lado < 0 else np.linspace(0.98, 0.52, 400)
        xs = self.S(us, np.full_like(us, v))[:, 0]
        return float(np.interp(x, xs, us))


# --- mallas ---------------------------------------------------------------

def malla(nombre, verts, caras, material):
    me = bpy.data.meshes.new(nombre)
    me.from_pydata([tuple(map(float, v)) for v in verts], [], caras)
    me.update()
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.collection.objects.link(ob)
    me.materials.append(mat(material))
    ob['parte'] = material
    return ob


def rejilla(nu, nv, cerrada_u=False, base=0):
    caras = []
    for i in range(nu if cerrada_u else nu - 1):
        for j in range(nv - 1):
            a, b = i * nv + j, ((i + 1) % nu) * nv + j
            caras.append((base + a, base + b, base + b + 1, base + a + 1))
    return caras


_mats = {}


def mat(nombre):
    if nombre not in _mats:
        m = bpy.data.materials.new(nombre)
        m.use_nodes = True
        _mats[nombre] = m
    return _mats[nombre]


def parche(h, nombre, material, uv, na, nb, alto=0.09):
    """Panel con grosor sobre la capellada. uv(a, b) devuelve (u, v)."""
    A, B = np.meshgrid(np.linspace(0, 1, na), np.linspace(0, 1, nb), indexing='ij')
    U, V = uv(A, B)
    S, N = h.S(U, V), h.normal(U, V)
    arriba = (S + N * alto).reshape(-1, 3)
    verts = list(arriba)
    caras = rejilla(na, nb)
    borde = ([(i, 0) for i in range(na)] + [(na - 1, j) for j in range(1, nb)]
             + [(i, nb - 1) for i in range(na - 2, -1, -1)]
             + [(0, j) for j in range(nb - 2, 0, -1)])
    base = len(verts)
    for i, j in borde:
        verts.append(S[i, j] - N[i, j] * 0.03)
    n = len(borde)
    for k, (i, j) in enumerate(borde):
        i2, j2 = borde[(k + 1) % n]
        caras.append((i * nb + j, base + k, base + (k + 1) % n, i2 * nb + j2))
    return malla(nombre, verts, caras, material)


def tubo(nombre, material, camino, ancho, grueso, arriba=(0, 0, 1), lados=8):
    """Barre una elipse por un camino; se usa para cordones."""
    camino = np.array(camino, float)
    t = np.gradient(camino, axis=0)
    t /= np.linalg.norm(t, axis=1, keepdims=True)
    lat = np.cross(t, arriba)
    lat /= np.linalg.norm(lat, axis=1, keepdims=True)
    sup = np.cross(lat, t)
    verts = []
    for p, l, s in zip(camino, lat, sup):
        for k in range(lados):
            a = 2 * math.pi * k / lados
            verts.append(p + l * math.cos(a) * ancho + s * math.sin(a) * grueso)
    caras = []
    n = len(camino)
    for i in range(n - 1):
        for k in range(lados):
            a, b = i * lados + k, i * lados + (k + 1) % lados
            caras.append((a, a + lados, b + lados, b))
    caras.append(tuple(range(lados - 1, -1, -1)))
    caras.append(tuple((n - 1) * lados + k for k in range(lados)))
    return malla(nombre, verts, caras, material)


# --- partes ---------------------------------------------------------------

def banda(h, nombre, material, anillos, tapa_abajo, tapa_arriba):
    us = np.linspace(0, 1, 170, endpoint=False)
    c, n = h.contorno(us), h.contorno.normal(us)
    if np.dot(n[len(us) // 4], (0, -1)) < 0:
        n = -n
    alto = h.base(c[:, 0])
    verts = []
    amplitud, ondas = h.m.get('ondas', (0, 0))
    for fr, sal in anillos:
        bulto = amplitud * np.sin(us * 2 * math.pi * ondas) * math.sin(min(fr, 1) * math.pi)
        verts += list(np.column_stack([c + n * (sal + bulto)[:, None], alto * fr]))
    v = h.curvar(np.array(verts))
    nv = len(anillos)
    # los vertices van por anillo, la rejilla los espera por columna
    v = v[np.arange(len(v)).reshape(nv, len(us)).T.reshape(-1)]
    caras = rejilla(len(us), nv, cerrada_u=True)
    if tapa_abajo:
        caras.append(tuple(i * nv for i in range(len(us) - 1, -1, -1)))
    if tapa_arriba:
        caras.append(tuple(i * nv + nv - 1 for i in range(len(us))))
    return malla(nombre, v, caras, material)


def columnas(h):
    """Suela hueca: base y entresuela unidas por columnas a lo largo del borde."""
    abajo, arriba, cantidad, radio = h.m['columnas']
    obs = [banda(h, 'suela', 'suela', abajo, True, True),
           banda(h, 'entresuela', 'entresuela', arriba, True, True),
           banda(h, 'nucleo', 'forro', [(abajo[-1][0], -0.9), (arriba[0][0], -0.9)], False, False)]
    us = np.linspace(0.04, 0.96, cantidad)
    c, n = h.contorno(us), h.contorno.normal(us)
    if np.dot(h.contorno.normal(0.25), (0, -1)) < 0:
        n = -n
    for i, (p, d) in enumerate(zip(c, n)):
        if 26 < p[0]:
            continue
        xy = p - d * 0.25
        alto = float(h.base(p[0]))
        camino = h.curvar([(xy[0], xy[1], alto * f) for f in np.linspace(abajo[-1][0] - 0.03, arriba[0][0] + 0.03, 4)])
        obs.append(tubo(f'columna_{i}', 'correa', camino, radio, radio, arriba=(1, 0, 0), lados=6))
    return obs


def suela(h):
    if 'columnas' in h.m:
        return columnas(h)
    anillos, corte = h.m['suela'], h.m['corte']
    if corte is None:
        return [banda(h, 'suela', 'suela', anillos, True, True)]
    return [banda(h, 'suela', 'suela', anillos[:corte + 1], True, False),
            banda(h, 'entresuela', 'entresuela', anillos[corte:], False, True)]


def capellada(h):
    nu, nv = 200, 30
    U, V = np.meshgrid(np.linspace(0, 1, nu, endpoint=False), np.linspace(0, 1, nv), indexing='ij')
    return malla('capellada', h.S(U, V).reshape(-1, 3), rejilla(nu, nv, cerrada_u=True), 'capellada')


def interior(h):
    """Forro: baja desde la abertura hasta la plantilla."""
    us = np.linspace(0, 1, 120, endpoint=False)
    borde = h.S(us, np.ones_like(us))
    centro = np.array([11.0, 0.0])
    pasos = np.linspace(0, 1, 6)
    verts = []
    for p in borde:
        for t in pasos:
            xy = p[:2] + (centro - p[:2]) * 0.16 * t
            verts.append((xy[0], xy[1], p[2] + (h.base(xy[0]) + 0.5 - p[2]) * t))
    n = len(pasos)
    caras = rejilla(len(us), n, cerrada_u=True)
    caras.append(tuple(i * n + n - 1 for i in range(len(us))))
    forro = malla('forro', verts, caras, 'forro')
    # acolchado del borde
    us = np.linspace(0, 1, 140, endpoint=False)
    camino = h.S(us, np.ones_like(us))
    r = h.m['collar']
    lados = 8
    tan = np.roll(camino, -1, 0) - np.roll(camino, 1, 0)
    tan /= np.linalg.norm(tan, axis=1, keepdims=True)
    lat = np.cross(tan, (0, 0, 1))
    lat /= np.maximum(np.linalg.norm(lat, axis=1, keepdims=True), 1e-6)
    sup = np.cross(lat, tan)
    verts = []
    for p, l, s in zip(camino, lat, sup):
        for k in range(lados + 1):
            a = 2 * math.pi * k / lados
            verts.append(p + (l * math.cos(a) + s * math.sin(a)) * r)
    return forro, malla('collar', verts, rejilla(len(us), lados + 1, cerrada_u=True), 'forro')


def lengua(h):
    m = h.m
    x0, x1 = m['lengua']
    na, nb = 11, 26
    arriba, abajo = [], []
    for b in np.linspace(0, 1, nb):
        x = x0 + (x1 - x0) * b
        z = h.borde(x) - 0.55 + 2.1 * b ** 3
        w = 2.1 + 0.7 * math.sin(b * math.pi) if b < .9 else 2.1 + 0.7 * math.sin(.9 * math.pi)
        fin = math.sqrt(max(1 - (max(b - .8, 0) / .205) ** 2, 0.02))
        for a in np.linspace(-1, 1, na):
            y = a * w * fin
            p = (x, y, z - 0.5 * a * a)
            arriba.append(p)
            abajo.append((p[0], p[1], p[2] - 0.22))
    arriba, abajo = h.curvar(arriba), h.curvar(abajo)
    n = nb * na
    caras = rejilla(nb, na)
    caras += [tuple(c + n for c in reversed(f)) for f in rejilla(nb, na)]
    for i in range(nb - 1):
        for j, jj in ((0, 0), (na - 1, na - 1)):
            a, b = i * na + j, (i + 1) * na + j
            caras.append((a, a + n, b + n, b) if j == 0 else (b, b + n, a + n, a))
    for j in range(na - 1):
        a = (nb - 1) * na + j
        caras.append((a, a + n, a + 1 + n, a + 1))
    etiqueta = arriba.reshape(nb, na, 3)[int(nb * 0.74):int(nb * 0.9), 3:na - 3].copy()
    etiqueta += np.array((0, 0, 0.05))
    f, c = etiqueta.shape[:2]
    return [malla('lengua', np.vstack([arriba, abajo]), caras, 'lengua'),
            malla('etiqueta', etiqueta.reshape(-1, 3), rejilla(f, c), 'talon')]


def cordones(h):
    """Cordones cruzados en X, con una barra al frente y ojales en cada fila."""
    m = h.m
    x_fin, x_ini, filas = m['cordones']
    externos, internos = [], []
    for x in np.linspace(x_ini, x_fin, filas):
        ue, ui = h.u_de_x(x, 0.9, -1), h.u_de_x(x, 0.9, 1)
        externos.append((ue, h.S(ue, 0.9)))
        internos.append((ui, h.S(ui, 0.9)))

    def tramo(nombre, a, b, alza):
        camino = []
        for t in np.linspace(0, 1, 14):
            p = a + (b - a) * t
            p[2] += alza * math.sin(t * math.pi) ** 0.7 + 0.12
            camino.append(p)
        return tubo(nombre, 'cordones', camino, *m['cordon'])

    obs = [tramo('cordon_frente', externos[0][1], internos[0][1], 0.3)]
    for i in range(filas - 1):
        obs.append(tramo(f'cordon_{i}_a', externos[i][1], internos[i + 1][1], 0.36))
        obs.append(tramo(f'cordon_{i}_b', internos[i][1], externos[i + 1][1], 0.46))
    for i, (u, _) in enumerate(externos + internos):
        obs.append(punto(h, f'ojal_{i}', u, 0.9, radio=0.22, alto=0.09, material='costuras'))
    return obs


def rayas(h):
    m = h.m['rayas']
    dientes = m.get('dientes', 0)
    obs = []
    for lado, nombre in ((-1, 'ext'), (1, 'int')):
        for i in range(m['n']):
            x_abajo = m['x_abajo'] + i * m['paso_abajo']
            x_arriba = m['x_arriba'] + i * m['paso_arriba']
            ancho = m['ancho']

            def uv(A, B, xa=x_abajo, xb=x_arriba):
                V = m['v0'] + (m['v1'] - m['v0']) * B
                U = np.zeros_like(A)
                for idx in np.ndindex(A.shape):
                    b = B[idx]
                    borde = A[idx] - 0.5
                    x = xa + (xb - xa) * b + borde * ancho
                    if dientes and abs(borde) == 0.5:
                        x += math.copysign(dientes, borde) * abs((b * 16) % 2 - 1)
                    U[idx] = h.u_de_x(x, V[idx], lado)
                return U, V

            obs.append(parche(h, f'raya_{nombre}_{i}', 'rayas', uv, 5, 48 if dientes else 22, alto=0.11))
    return obs


def costura(h, nombre, U, V, alto=0.13):
    camino = h.S(U, V) + h.normal(U, V) * alto
    return tubo(nombre, 'costuras', camino, 0.045, 0.03, lados=5)


def puntera(h):
    x, vmax, forma, grosor = h.m['puntera']
    ua, ub = h.u_de_x(x, 0.02, -1), h.u_de_x(x, 0.02, 1)

    def uv(A, B):
        U = ua + (ub - ua) * A
        tope = 0.03 + (vmax - 0.03) * np.sin(A * math.pi) ** forma
        if 'puntera_t' in h.m:
            bajo, tallo = h.m['puntera_t']
            tope = np.maximum(0.03 + bajo * np.sin(A * math.pi) ** 0.45,
                              0.03 + (vmax - 0.03) * np.exp(-((A - 0.5) / tallo) ** 4))
        return U, B * tope

    a = np.linspace(0.02, 0.98, 120)
    U, V = uv(a, np.full_like(a, 0.97))
    obs = [parche(h, 'puntera', 'puntera', uv, 120, 14, alto=grosor),
           costura(h, 'costura_puntera', U, V, alto=grosor + 0.06)]
    for i, altura in enumerate(h.m.get('aros', ())):
        Ua = ua + (ub - ua) * np.linspace(0.3, 0.7, 40)
        obs.append(costura(h, f'aro_{i}', Ua, np.full_like(Ua, altura), alto=grosor + 0.03))
    return obs


def ojalera(h):
    x, v0 = h.m['ojalera']
    ua, ub = h.u_de_x(x, 0.95, -1), h.u_de_x(x, 0.95, 1)
    a = np.linspace(0, 1, 70)
    return [parche(h, 'ojalera', 'ojalera',
                   lambda A, B: (ua + (ub - ua) * A, v0 + (0.995 - v0) * B), 70, 6, alto=0.08),
            costura(h, 'costura_ojalera', ua + (ub - ua) * a, np.full_like(a, v0 + 0.02))]


def contrafuerte(h):
    """Refuerzo curvo del talon, con su costura."""
    x, altura = h.m.get('contrafuerte', (7.2, 0.6))
    ue, ui = h.u_de_x(x, 0.3, -1), h.u_de_x(x, 0.3, 1)

    def uv(A, B):
        U = np.mod(ui + (ue + 1 - ui) * A, 1)
        tope = 0.06 + (altura - 0.06) * np.sin(A * math.pi) ** 0.55
        return U, B * tope

    a = np.linspace(0.01, 0.99, 60)
    U, V = uv(a, np.full_like(a, 0.96))
    return [parche(h, 'contrafuerte', 'contrafuerte', uv, 60, 10, alto=0.07),
            costura(h, 'costura_talon', U, V, alto=0.12)]


def costura_suela(h):
    fraccion = h.m['costura_suela']
    us = np.linspace(0, 1, 240)
    c, n = h.contorno(us), h.contorno.normal(us)
    if np.dot(n[len(us) // 4], (0, -1)) < 0:
        n = -n
    salida = np.interp(fraccion, *zip(*h.m['suela'])) + 0.03
    camino = h.curvar(np.column_stack([c + n * salida, h.base(c[:, 0]) * fraccion]))
    return [tubo('costura_suela', 'costuras', camino, 0.06, 0.06, arriba=(1, 0, 0), lados=5)]


def talon(h):
    ancho, v0 = h.m['talon']

    def uv(A, B):
        return (A - 0.5) * 2 * ancho * (1 - 0.35 * B), v0 + (0.995 - v0) * B

    return parche(h, 'talon', 'talon', uv, 14, 12, alto=0.1)


def punto(h, nombre, u, v, radio=0.17, alto=0.1, material='rayas'):
    """Disco pequeno sobre la capellada, para perforaciones."""
    p, n = h.S(u, v), h.normal(u, v)
    t = h.S(u + 2e-3, v) - h.S(u - 2e-3, v)
    t /= np.linalg.norm(t)
    b = np.cross(n, t)
    verts = [p + n * alto + (t * math.cos(a) + b * math.sin(a)) * radio
             for a in np.linspace(0, 2 * math.pi, 7, endpoint=False)]
    return malla(nombre, verts, [tuple(range(7))], material)


def perforaciones(h):
    obs = []
    for i, (x_abajo, x_arriba, n, v0, v1) in enumerate(h.m.get('perfora', ())):
        for lado in (-1, 1):
            for k, t in enumerate(np.linspace(0, 1, n)):
                v = v0 + (v1 - v0) * t
                u = h.u_de_x(x_abajo + (x_arriba - x_abajo) * t, v, lado)
                obs.append(punto(h, f'perfora_{i}_{lado}_{k}', u, v))
    if h.m.get('perfora_punta'):
        ua, ub = h.u_de_x(24, 0.02, -1), h.u_de_x(24, 0.02, 1)
        for i, v in enumerate((0.42, 0.56, 0.7)):
            for k, a in enumerate(np.linspace(0.36, 0.64, 7 - i)):
                obs.append(punto(h, f'punta_{i}_{k}', ua + (ub - ua) * a, v, radio=0.14))
    return obs


def paneles(h):
    obs = []
    for i, p in enumerate(h.m.get('paneles', ())):
        x0, x1 = p['x']
        v0, v1 = p['v']
        inclina = p.get('inclina', 0)
        redondo = p.get('forma', 'redondo') == 'redondo'
        for lado in (-1, 1):
            def uv(A, B):
                # borde superior en arco: los paneles reales no son rectangulos
                perfil = 0.3 + 0.7 * np.sin(A * math.pi) ** 0.5 if redondo else 1
                V = v0 + (v1 - v0) * B * perfil
                U = np.zeros_like(A)
                for idx in np.ndindex(A.shape):
                    U[idx] = h.u_de_x(x0 + (x1 - x0) * A[idx] + inclina * B[idx], V[idx], lado)
                return U, V
            obs.append(parche(h, f'panel_{i}_{lado}', p['parte'], uv, 24, 10, alto=p.get('alto', 0.08)))
            a = np.linspace(0.03, 0.97, 30)
            U, V = uv(a, np.full_like(a, 0.94))
            obs.append(costura(h, f'costura_panel_{i}_{lado}', U, V, alto=p.get('alto', 0.08) + 0.05))
    return obs


def guardia(h):
    parte, tope = h.m['guardia']
    return [parche(h, 'guardia', parte, lambda A, B: (A, B * tope), 200, 4, alto=0.09)]


def correa(h):
    x, ancho, v = h.m['correa']
    ue, ui = h.u_de_x(x, 0.9, -1), h.u_de_x(x, 0.9, 1)
    camino = [h.S(ue, a) + h.normal(ue, a) * 0.16 for a in np.linspace(v, 0.97, 8)]
    a, b = camino[-1], h.S(ui, 0.97) + h.normal(ui, 0.97) * 0.16
    for t in np.linspace(0, 1, 12)[1:-1]:
        p = a + (b - a) * t
        p[2] += 0.45 * math.sin(t * math.pi)
        camino.append(p)
    camino += [h.S(ui, a) + h.normal(ui, a) * 0.16 for a in np.linspace(0.97, v, 8)]
    return [tubo('correa', 'correa', camino, 0.12, ancho, arriba=(1, 0, 0), lados=6)]


def solapa(h):
    """Lengueta ancha que tapa los cordones, como en las botas de futbol."""
    x0, x1, medio = h.m['solapa']
    filas, cols = 12, 9
    verts = []
    for b in np.linspace(0, 1, filas):
        x = x0 + (x1 - x0) * b
        for a in np.linspace(-1, 1, cols):
            verts.append((x, a * medio * (1 - 0.35 * b ** 2), h.borde(x) + 0.75 - 0.9 * a * a))
    return [malla('solapa', h.curvar(verts), rejilla(filas, cols), 'puntera')]


def tacos(h):
    obs = []
    alto = h.m['elevar']
    for i, (x, y, r) in enumerate(h.m['tacos']):
        verts = []
        for altura, f in ((alto + 0.3, 1), (0.01, 0.72)):
            verts += [(x + math.cos(a) * r * f, y + math.sin(a) * r * f, altura)
                      for a in np.linspace(0, 2 * math.pi, 8, endpoint=False)]
        caras = [(k, (k + 1) % 8, 8 + (k + 1) % 8, 8 + k) for k in range(8)]
        caras.append(tuple(range(15, 7, -1)))
        obs.append(malla(f'taco_{i}', verts, caras, 'suela'))
    return obs


def lazos(h):
    """Tiradores de tela en el talon y la lengua."""
    x_lengua = h.m['lengua'][1]
    bases = [h.S(0.0, 1.0), h.curvar((x_lengua, 0.0, float(h.borde(x_lengua)) + 1.4))]
    obs = []
    for i, p in enumerate(bases):
        camino = [p + np.array((-0.25 * math.sin(t), 0.42 * math.cos(t), 1.9 * math.sin(t)))
                  for t in np.linspace(0, math.pi, 12)]
        obs.append(tubo(f'lazo_{i}', 'cordones', camino, 0.07, 0.2, arriba=(1, 0, 0), lados=6))
    return obs


def chancla(h):
    """Suela contorneada y una tira ancha con tres rayas."""
    obs = suela(h)
    x0, x1, altura = h.m['tira']
    filas, cols = 24, 30
    arriba, abajo = [], []
    for b in np.linspace(0, 1, filas):
        x = x0 + (x1 - x0) * b
        ye, yi = h.S(h.u_de_x(x, 0.0, -1), 0.0)[1], h.S(h.u_de_x(x, 0.0, 1), 0.0)[1]
        centro, medio = (ye + yi) / 2, (yi - ye) / 2 + 0.05
        for a in np.linspace(-1, 1, cols):
            z = h.base(x) - 0.2 + altura * (1 - abs(a) ** 2.6) ** 0.62
            arriba.append((x, centro + a * medio, z))
            abajo.append((x, centro + a * medio * 0.97, z - 0.3))
    arriba = h.curvar(arriba)
    abajo = h.curvar(abajo)
    n = len(arriba)
    caras = rejilla(filas, cols) + [tuple(c + n for c in reversed(f)) for f in rejilla(filas, cols)]
    obs.append(malla('tira', np.vstack([arriba, abajo]), caras, 'capellada'))
    grilla = arriba.reshape(filas, cols, 3)
    for i, fila in enumerate((5, 11, 17)):
        p = grilla[fila:fila + 4, 2:-2].copy()
        p[..., 2] += 0.07
        f, c = p.shape[:2]
        obs.append(malla(f'raya_{i}', p.reshape(-1, 3), rejilla(f, c), 'rayas'))
    return obs


def suavizar(ob, angulo=0.6):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    for f in bm.faces:
        f.smooth = True
    for e in bm.edges:
        if len(e.link_faces) == 2 and e.calc_face_angle(0) > angulo:
            e.smooth = False
    bm.to_mesh(ob.data)
    bm.free()


def unir_por_material(obs):
    """Una malla por material: menos llamadas de dibujo en la web."""
    grupos = {}
    for ob in obs:
        grupos.setdefault(ob['parte'], []).append(ob)
    for parte, lista in grupos.items():
        bpy.ops.object.select_all(action='DESELECT')
        for ob in lista:
            ob.select_set(True)
        bpy.context.view_layer.objects.active = lista[0]
        if len(lista) > 1:
            bpy.ops.object.join()
        bpy.context.object.name = parte


def construir(m):
    h = Horma(m)
    if m.get('tipo') == 'chancla':
        obs = chancla(h)
    else:
        obs = suela(h) + [capellada(h), talon(h)] + lengua(h)
        obs += (puntera(h) if m['puntera'] else []) + ojalera(h) + list(interior(h)) + rayas(h) + cordones(h)
        obs += paneles(h) + perforaciones(h)
        if h.m.get('contrafuerte', True):
            obs += contrafuerte(h)
        if 'costura_suela' in h.m:
            obs += costura_suela(h)
        for clave, parte in (('guardia', guardia), ('correa', correa), ('solapa', solapa), ('tacos', tacos), ('lazos', lazos)):
            if clave in m:
                obs += parte(h)
    for ob in obs:
        suavizar(ob)
    unir_por_material(obs)


# --- color ----------------------------------------------------------------

def hex_rgb(c):
    c = c.lstrip('#')
    srgb = [int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in srgb] + [1]


def aplicar_variante(m, nombre):
    pintar(m['variantes'][nombre])


def pintar(colores):
    for parte, material in _mats.items():
        bsdf = material.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = hex_rgb(colores.get(parte, '#ffffff'))
        bsdf.inputs['Roughness'].default_value = 0.62 if parte != 'suela' else 0.45


# --- render y exportacion ---------------------------------------------------

def preparar_escena():
    addon_utils.enable('cycles')
    s = bpy.context.scene
    s.render.engine = 'CYCLES'
    s.cycles.samples = 48
    s.cycles.use_denoising = True
    s.render.resolution_x, s.render.resolution_y = 900, 600
    s.view_settings.view_transform = 'Standard'
    mundo = bpy.data.worlds.new('estudio')
    mundo.use_nodes = True
    mundo.node_tree.nodes['Background'].inputs[0].default_value = (0.9, 0.9, 0.9, 1)
    mundo.node_tree.nodes['Background'].inputs[1].default_value = 0.42
    s.world = mundo
    bpy.ops.mesh.primitive_plane_add(size=300, location=(15, 0, -0.01))
    piso = bpy.context.object
    pm = bpy.data.materials.new('piso')
    pm.use_nodes = True
    pm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.86, 0.86, 0.86, 1)
    piso.data.materials.append(pm)
    bpy.ops.object.light_add(type='AREA', location=(15, -25, 45))
    luz = bpy.context.object
    luz.data.size = 40
    luz.data.energy = 9000
    luz.rotation_euler = (0.45, 0, 0)
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
    bpy.context.collection.objects.link(cam)
    cam.data.lens = 70
    s.camera = cam
    return cam


def mirar(cam, pos, objetivo=(15, 0, 4.5)):
    from mathutils import Vector
    cam.location = pos
    cam.rotation_euler = (Vector(objetivo) - Vector(pos)).to_track_quat('-Z', 'Y').to_euler()


VISTAS = {
    'cerca': (52, -30, 14),
    'frente': (70, -6, 16),
    'lado': (15, -88, 7),
    'tres_cuartos': (72, -62, 34),
    'arriba': (15, -6, 95),
    'atras': (-48, -42, 26),
}


def renderizar(cam, prefijo, vistas):
    for v in vistas:
        mirar(cam, VISTAS[v])
        bpy.context.scene.render.filepath = f'{AQUI}/renders/{prefijo}_{v}.png'
        bpy.ops.render.render(write_still=True)


def main():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument('--modelo', default='samba')
    ap.add_argument('--variante', default=None)
    ap.add_argument('--vistas', default='lado,tres_cuartos,arriba,atras')
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--glb', action='store_true')
    ap.add_argument('--fotos', action='store_true', help='foto transparente de cada producto y color')
    ap.add_argument('--lod', type=float, default=0, help='exporta tambien una version reducida')
    a = ap.parse_args(argv)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    m = MODELOS[a.modelo]
    construir(m)
    variantes = a.variante.split(',') if a.variante else [next(iter(m['variantes']))]
    aplicar_variante(m, variantes[0])
    bpy.ops.wm.save_as_mainfile(filepath=f'{AQUI}/{a.modelo}.blend')

    if a.glb:
        bpy.ops.export_scene.gltf(filepath=f'{AQUI}/../public/modelos/{a.modelo}.glb',
                                  export_format='GLB', export_apply=True)
    if a.lod:
        for ob in bpy.context.scene.objects:
            ob.modifiers.new('reducir', 'DECIMATE').ratio = a.lod
        bpy.ops.export_scene.gltf(filepath=f'{AQUI}/../public/modelos/{a.modelo}-repisa.glb',
                                  export_format='GLB', export_apply=True)
        for ob in bpy.context.scene.objects:
            ob.modifiers.clear()
    if a.fotos:
        cam = preparar_escena()
        s = bpy.context.scene
        s.render.film_transparent = True
        s.render.resolution_x, s.render.resolution_y = 1000, 700
        s.cycles.samples = 32
        bpy.data.objects['Plane'].hide_render = True
        mirar(cam, (66, -70, 24))
        for clave, (_, base, lista) in PRODUCTOS.items():
            if base != a.modelo:
                continue
            for i, x in enumerate(lista):
                pintar(x['colores'])
                s.render.filepath = f'{AQUI}/renders/fotos/{clave}-{i}.png'
                bpy.ops.render.render(write_still=True)
        return
    if a.render:
        cam = preparar_escena()
        for v in variantes:
            aplicar_variante(m, v)
            renderizar(cam, f'{a.modelo}_{v}', a.vistas.split(','))


main()
