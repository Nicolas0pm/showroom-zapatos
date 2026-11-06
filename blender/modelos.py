"""Medidas de cada modelo y catalogo de la tienda. Medidas en centimetros;
x va del talon (0) a la punta (30). Precios y tallas son simulados."""


def ancho(puntos, f):
    return [(x, y * f) for x, y in puntos]


CONTORNO_FINO = [(0, 0), (0.7, -2.7), (4.5, -3.9), (11, -4.1), (18, -4.9), (24, -4.8),
                 (28.3, -3.1), (30, -0.4), (29.4, 1.9), (26, 3.7), (20, 4.1), (13, 3.0),
                 (6, 3.4), (1.1, 2.6)]
CONTORNO_REDONDO = [(0, 0), (0.7, -2.9), (4.5, -4.1), (11, -4.3), (18, -5.1), (24.5, -5.1),
                    (28.8, -3.9), (30, -1.0), (29.7, 2.0), (27, 4.2), (20, 4.4), (13, 3.2),
                    (6, 3.6), (1.1, 2.8)]
ABERTURA = [(2.4, 0), (3.2, -2.3), (6.3, -3.0), (9.8, -2.6), (12.8, -1.75), (17, -1.45),
            (20.3, -0.95), (21.3, 0), (20.3, 0.95), (17, 1.45), (12.8, 1.75), (9.8, 2.6),
            (6.3, 3.0), (3.2, 2.3)]
SUELA_PLANA = [(0, -0.35), (0.06, -0.02), (0.45, 0.14), (0.5, 0.05), (0.56, 0.05), (0.62, 0.16),
               (1.0, 0.1), (1.03, -0.15)]
SUELA_COPA = [(0, -0.3), (0.05, 0), (0.3, 0.12), (0.34, 0.04), (0.38, 0.04), (0.42, 0.14),
              (0.68, 0.16), (0.72, 0.06), (0.76, 0.06), (0.8, 0.16), (1.0, 0.12), (1.03, -0.15)]
SUELA_CUNA = [(0, -0.2), (0.05, 0.12), (0.3, 0.2), (0.33, 0.1), (0.36, 0.22), (0.8, 0.3),
              (1.0, 0.12), (1.03, -0.15)]

SAMBA = {
    'contorno': CONTORNO_FINO,            # huella; empieza en el talon, primero y negativa
    'abertura': ABERTURA,                 # cuello y garganta de los cordones
    'borde': [(2, 10.9), (4.5, 9.5), (7, 8.7), (10, 9.6), (13, 9.7), (17, 8.0), (21.5, 5.7)],
    'base': [(0, 2.4), (12, 2.15), (22, 1.75), (30, 1.65)],
    'punta': (17, 1.5),
    'cuello': (10.5, 15.5),
    'suela': SUELA_PLANA,                 # anillos: fraccion de altura y salida
    'corte': None,                        # desde que anillo empieza la entresuela
    'lengua': (21.2, 8.4),
    'cordones': (12.6, 19.7, 7),
    'cordon': (0.3, 0.1),
    'collar': 0.34,
    'rayas': {'n': 3, 'x_abajo': 9.6, 'paso_abajo': 2.05, 'x_arriba': 13.6, 'paso_arriba': 1.5,
              'ancho': 1.0, 'v0': 0.07, 'v1': 0.8},
    'puntera': (22.2, 0.98, 1.15, 0.07),  # x, altura, forma, grosor
    'ojalera': (11.8, 0.8),
    'talon': (0.05, 0.5),
}


def variante_de(origen, **cambios):
    return {**origen, **cambios}


GAZELLE = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_REDONDO, 0.97),
    borde=[(2, 10.5), (4.5, 9.2), (7, 8.4), (10, 9.3), (13, 9.3), (17, 7.6), (21.5, 5.4)],
    base=[(0, 2.15), (12, 1.95), (22, 1.6), (30, 1.5)],
    puntera=None,
    rayas={**SAMBA['rayas'], 'x_abajo': 10.2, 'x_arriba': 14.2, 'ancho': 1.15, 'paso_abajo': 2.2, 'paso_arriba': 1.6},
    talon=(0.052, 0.42),
)

SPEZIAL = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_FINO, 0.95),
    base=[(0, 2.3), (12, 2.0), (22, 1.55), (30, 1.45)],
    borde=[(2, 10.3), (4.5, 9.0), (7, 8.1), (10, 9.0), (13, 9.1), (17, 7.5), (21.5, 5.2)],
    rayas={**SAMBA['rayas'], 'ancho': 0.8, 'paso_abajo': 2.3, 'paso_arriba': 1.7, 'x_abajo': 9.9, 'x_arriba': 13.8},
    puntera=(24.2, 0.62, 1.0, 0.07),
    talon=(0.04, 0.55),
)

SUPERSTAR = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_REDONDO, 1.03),
    borde=[(2, 12.1), (4.5, 10.8), (7, 10.0), (10, 10.9), (13, 11.0), (17, 9.2), (21.5, 6.9)],
    base=[(0, 3.5), (12, 3.3), (22, 3.0), (30, 3.0)],
    suela=SUELA_COPA,
    punta=(19, 0.9),
    puntera=(21.6, 0.74, 0.3, 0.2),
    aros=(0.18, 0.27, 0.36, 0.45, 0.54),
    collar=0.42,
    rayas={**SAMBA['rayas'], 'x_abajo': 10.0, 'x_arriba': 13.6, 'paso_abajo': 2.1, 'paso_arriba': 1.55, 'v0': 0.05, 'v1': 0.82},
    talon=(0.05, 0.56),
)

CAMPUS = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_REDONDO, 1.08),
    abertura=ancho(ABERTURA, 1.06),
    borde=[(2, 11.9), (4.5, 10.8), (7, 10.0), (10, 10.8), (13, 10.9), (17, 9.0), (21.5, 6.8)],
    base=[(0, 3.2), (12, 3.0), (22, 2.8), (30, 2.8)],
    suela=SUELA_COPA,
    punta=(19, 1.0),
    puntera=None,
    cordon=(0.42, 0.13),
    cordones=(12.6, 19.7, 6),
    collar=0.62,
    rayas={**SAMBA['rayas'], 'ancho': 1.3, 'paso_abajo': 2.3, 'paso_arriba': 1.75, 'x_abajo': 9.6, 'x_arriba': 13.2},
    talon=(0.055, 0.5),
)

SL72 = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_FINO, 0.96),
    borde=[(2, 11.3), (4.5, 10.3), (7, 9.5), (10, 10.2), (13, 10.0), (17, 8.0), (21.5, 5.6)],
    base=[(0, 3.7), (12, 3.0), (22, 2.0), (30, 1.7)],
    suela=SUELA_CUNA,
    corte=3,
    punta=(16, 2.4),
    puntera=(21.6, 0.9, 0.75, 0.08),
    collar=0.4,
    rayas={**SAMBA['rayas'], 'ancho': 0.72, 'paso_abajo': 1.7, 'paso_arriba': 1.3, 'x_abajo': 10.8, 'x_arriba': 14.2, 'v0': 0.09},
    talon=(0.075, 0.2),
)

ZX = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_REDONDO, 1.05),
    borde=[(2, 13.2), (4.5, 12.0), (7, 11.2), (10, 11.8), (13, 11.3), (17, 9.0), (21.5, 6.5)],
    base=[(0, 4.6), (12, 3.8), (22, 2.7), (30, 2.3)],
    suela=SUELA_CUNA,
    corte=3,
    punta=(16, 2.6),
    puntera=(21.2, 0.88, 0.6, 0.1),
    collar=0.55,
    cordon=(0.34, 0.11),
    rayas={**SAMBA['rayas'], 'ancho': 0.85, 'paso_abajo': 1.85, 'paso_arriba': 1.4, 'x_abajo': 11.0, 'x_arriba': 13.6, 'v0': 0.16, 'v1': 0.78},
    talon=(0.115, 0.08),
)

MODELOS = {'samba': SAMBA, 'gazelle': GAZELLE, 'spezial': SPEZIAL, 'superstar': SUPERSTAR,
           'campus': CAMPUS, 'sl72': SL72, 'zx': ZX}

BLANCO, NEGRO, GOMA = '#f3f1ea', '#17171a', '#b57f4c'


def paleta(cuerpo, rayas, suela=GOMA, puntera=None, talon=None, entresuela=None, cordones=None, forro=None):
    oscuro = int(cuerpo[1:3], 16) < 90
    return {
        'capellada': cuerpo, 'ojalera': cuerpo, 'lengua': cuerpo, 'rayas': rayas, 'suela': suela,
        'puntera': puntera or cuerpo, 'talon': talon or rayas, 'entresuela': entresuela or BLANCO,
        'cordones': cordones or (cuerpo if oscuro else BLANCO),
        'forro': forro or ('#2b2b2f' if oscuro else '#e6e2d8'),
        'costuras': '#55555c' if oscuro else '#b9b4a6',
    }


def v(nombre, precio, tallas, *args, **kwargs):
    colores = paleta(*args, **kwargs)
    return {'nombre': nombre, 'precio': precio, 'tallas': tallas,
            'muestra': [colores['capellada'], colores['rayas']], 'colores': colores}


# id: (nombre, modelo 3D base, variantes). La primera variante es la de la repisa.
PRODUCTOS = {
    'samba': ('Samba', 'samba', [
        v('Blanco y negro', 120, [37, 38, 39, 41, 42, 44], BLANCO, '#141414', puntera='#e2ded2'),
        v('Negro y blanco', 130, [38, 40, 41, 42, 43], NEGRO, BLANCO, puntera='#222226'),
        v('Blanco y verde', 135, [40, 41], BLANCO, '#1f5a3c', puntera='#e2ded2'),
    ]),
    'gazelle': ('Gazelle', 'gazelle', [
        v('Azul y blanco', 110, [38, 39, 40, 42], '#27407c', BLANCO, suela=BLANCO),
        v('Verde y blanco', 110, [39, 41, 42, 43], '#25604a', BLANCO, suela=BLANCO),
        v('Rosa y blanco', 115, [36, 37, 38, 39], '#d9a3ad', BLANCO, suela=GOMA),
    ]),
    'superstar': ('Superstar', 'superstar', [
        v('Blanco y negro', 110, [37, 38, 40, 41, 42, 44], BLANCO, '#141414', suela=BLANCO, puntera='#e9e7df'),
        v('Negro y blanco', 110, [39, 40, 41, 43], NEGRO, BLANCO, suela=BLANCO, puntera='#e9e7df'),
        v('Blanco y dorado', 125, [38, 41, 42], BLANCO, '#b9933f', suela=BLANCO, puntera='#e9e7df'),
    ]),
    'campus': ('Campus 00s', 'campus', [
        v('Gris y blanco', 115, [38, 39, 40, 41], '#7d7f85', BLANCO, suela=BLANCO, cordones=BLANCO),
        v('Negro y blanco', 115, [39, 41, 42, 43], '#1e1e22', BLANCO, suela=BLANCO, cordones=BLANCO),
        v('Marrón y crema', 120, [40, 41, 44], '#6d4a30', '#e8dcc4', suela='#e8dcc4', cordones='#e8dcc4'),
    ]),
    'spezial': ('Handball Spezial', 'spezial', [
        v('Azul y gris', 115, [38, 40, 41, 42], '#2f4f8f', '#d6d4cd', puntera='#27437a'),
        v('Burdeos y crema', 115, [37, 39, 41], '#6d2233', '#e8dcc4', puntera='#5c1c2b'),
        v('Beige y marrón', 120, [39, 40, 42, 43], '#cdb896', '#6b4326', puntera='#bda785'),
    ]),
    'sl72': ('SL 72', 'sl72', [
        v('Azul y blanco', 95, [38, 39, 41, 42], '#2b56a8', BLANCO, suela='#c9463d', puntera='#d9d7cf'),
        v('Negro y dorado', 100, [40, 41, 43], NEGRO, '#b9933f', suela=GOMA, puntera='#2c2c31'),
        v('Rojo y blanco', 95, [37, 38, 39], '#b3261e', BLANCO, suela=BLANCO, puntera='#d9d7cf'),
    ]),
    'hawaii': ('Hawaii SPZL', 'gazelle', [
        v('Marrón tono a tono', 130, [40, 41, 42], '#6a4a33', '#54392a', suela=GOMA),
        v('Verde', 130, [39, 41, 43], '#3d5a3d', '#e8dcc4', suela=GOMA),
    ]),
    'albrecht': ('Albrecht II SPZL', 'spezial', [
        v('Marrón', 140, [40, 41, 42, 44], '#7a5436', '#e8dcc4', puntera='#6b4930'),
        v('Azul marino', 140, [39, 41, 43], '#1f2c4f', '#d6d4cd', puntera='#1b2644'),
    ]),
    'zx8000': ('ZX 8000', 'zx', [
        v('Azul y amarillo', 120, [40, 41, 42, 43], '#d8d9dc', '#2352a3', suela='#2352a3', puntera='#2f6fb5', talon='#e6c229', entresuela='#f3f1ea'),
        v('Blanco y gris', 120, [38, 39, 41], BLANCO, '#8a8c92', suela='#8a8c92', puntera='#c9c9cc', talon='#8a8c92'),
    ]),
    'campus-nuevo': ('Campus 00s', 'campus', [
        v('Crema y verde', 120, [38, 40, 41], '#e8dcc4', '#2c5a3f', suela=BLANCO, cordones='#2c5a3f'),
        v('Lila y blanco', 120, [36, 37, 38], '#b7a7d3', BLANCO, suela=BLANCO, cordones=BLANCO),
    ]),
    'clot-samba': ('CLOT × Samba', 'samba', [
        v('Crema y yute', 180, [40, 41, 42], '#e4d6bd', '#3a2c20', suela='#c8a877', puntera='#d6c6a8'),
        v('Negro y yute', 180, [41, 42, 43], '#232326', '#c8a877', suela='#c8a877', puntera='#2e2e33'),
    ]),
    'sftm-samba': ('Song for the Mute × Samba LX', 'samba', [
        v('Gris desgastado', 170, [39, 41, 42], '#8e8a80', '#3d3b37', suela='#9c8866', puntera='#7f7b72'),
        v('Marrón desgastado', 170, [40, 42, 44], '#6e5a48', '#d5ccb9', suela='#9c8866', puntera='#604e3f'),
    ]),
    'sftm-tokyo': ('Song for the Mute × Tokyo', 'spezial', [
        v('Verde desgastado', 170, [39, 40, 41], '#59604b', '#d5ccb9', puntera='#4e5442'),
        v('Negro desgastado', 170, [40, 41, 43], '#2d2c2a', '#a9a497', puntera='#3a3936'),
    ]),
    'atmos-zx': ('atmos × ZX 8000', 'zx', [
        v('Edición atmos', 160, [40, 41, 42], '#efeeea', '#111114', suela='#d23a2e', puntera='#d23a2e', talon='#111114'),
        v('Negro y rojo', 160, [41, 42, 43], '#1b1b1f', '#d23a2e', suela='#d23a2e', puntera='#2c2c31', talon='#d23a2e', entresuela='#e8e6df'),
    ]),
}

ESTANTES = [
    {'id': 'vendidos', 'nombre': 'Más vendidos', 'color': '#ffe2bd', 'oscuro': False,
     'zapatos': ['samba', 'gazelle', 'superstar', 'campus', 'spezial', 'sl72']},
    {'id': 'novedades', 'nombre': 'Novedades', 'color': '#cfe4ff', 'oscuro': False,
     'zapatos': ['hawaii', 'albrecht', 'zx8000', 'campus-nuevo']},
    {'id': 'colaboraciones', 'nombre': 'Colaboraciones', 'color': '#ffffff', 'oscuro': True,
     'zapatos': ['clot-samba', 'sftm-samba', 'sftm-tokyo', 'atmos-zx']},
]

for _m, _p in zip(MODELOS.values(), ('samba', 'gazelle', 'spezial', 'superstar', 'campus', 'sl72', 'zx8000')):
    _m['variantes'] = {str(i): x['colores'] for i, x in enumerate(PRODUCTOS[_p][2])}
