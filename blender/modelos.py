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
    'puntera_t': (0.36, 0.11),            # puntera en T: altura a los lados y ancho del tallo
    'ojalera': (11.8, 0.8),
    'talon': (0.05, 0.5),
}


def variante_de(origen, **cambios):
    nuevo = {**origen, **cambios}
    if 'puntera' in cambios and 'puntera_t' not in cambios:
        nuevo.pop('puntera_t', None)
    return nuevo


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
    rayas={**SAMBA['rayas'], 'x_abajo': 10.0, 'x_arriba': 13.6, 'paso_abajo': 2.1, 'paso_arriba': 1.55, 'v0': 0.05, 'v1': 0.82,
           'dientes': 0.14},
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

SIN_RAYAS = {**SAMBA['rayas'], 'n': 0}
SUELA_BOOST = [(0, -0.2), (0.05, 0.1), (0.22, 0.16), (0.25, 0.1), (0.28, 0.2), (0.6, 0.4), (0.9, 0.28),
               (1.0, 0.1), (1.03, -0.15)]
ABERTURA_CALCETIN = [(3.4, 0), (4.0, -1.9), (6.4, -2.5), (9.2, -2.2), (12.8, -1.5), (17, -1.3),
                     (20.3, -0.9), (21.3, 0), (20.3, 0.9), (17, 1.3), (12.8, 1.5), (9.2, 2.2),
                     (6.4, 2.5), (4.0, 1.9)]

STAN = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_REDONDO, 0.98),
    borde=[(2, 11.4), (4.5, 10.1), (7, 9.3), (10, 10.2), (13, 10.3), (17, 8.6), (21.5, 6.2)],
    base=[(0, 2.9), (12, 2.7), (22, 2.4), (30, 2.4)],
    suela=SUELA_COPA,
    punta=(19, 0.9),
    puntera=None,
    rayas=SIN_RAYAS,
    perfora=[(9.6, 13.5, 7, 0.14, 0.76), (11.5, 15.0, 7, 0.14, 0.76), (13.4, 16.5, 7, 0.14, 0.76)],
    talon=(0.06, 0.58),
)

FORUM = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_REDONDO, 1.07),
    abertura=ancho(ABERTURA, 1.05),
    borde=[(2, 13.0), (4.5, 12.2), (7, 11.8), (10, 12.2), (13, 11.6), (17, 9.4), (21.5, 6.9)],
    base=[(0, 3.3), (12, 3.1), (22, 2.8), (30, 2.8)],
    suela=SUELA_COPA,
    punta=(19, 1.0),
    puntera=None,
    guardia=('puntera', 0.2),
    perfora_punta=True,
    collar=0.62,
    cordon=(0.38, 0.12),
    cordones=(14.2, 19.8, 5),
    correa=(12.2, 1.0, 0.55),
    rayas={**SAMBA['rayas'], 'x_abajo': 13.2, 'x_arriba': 15.4, 'ancho': 0.85, 'paso_abajo': 1.7, 'paso_arriba': 1.15, 'v0': 0.22, 'v1': 0.72},
    paneles=[{'parte': 'puntera', 'x': (3.5, 8.5), 'v': (0.18, 0.62), 'inclina': 1.5}],
    talon=(0.06, 0.2),
)

ULTRABOOST = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_FINO, 1.03),
    abertura=ABERTURA_CALCETIN,
    borde=[(3, 14.8), (5, 14.0), (7.5, 13.8), (10, 13.4), (13, 12.0), (17, 9.0), (21.5, 6.2)],
    base=[(0, 4.5), (12, 3.8), (22, 2.8), (30, 2.3)],
    suela=SUELA_BOOST,
    corte=3,
    ondas=(0.13, 38),
    punta=(15, 2.8),
    puntera=None,
    collar=0.22,
    cordones=(13.4, 19.6, 6),
    cordon=(0.2, 0.08),
    rayas=SIN_RAYAS,
    paneles=[{'parte': 'rayas', 'x': (10.4, 12.6), 'v': (0.06, 0.76), 'inclina': 3.0, 'alto': 0.14},
             {'parte': 'rayas', 'x': (13.6, 15.4), 'v': (0.06, 0.76), 'inclina': 2.2, 'alto': 0.14},
             {'parte': 'rayas', 'x': (16.4, 18.0), 'v': (0.06, 0.76), 'inclina': 1.4, 'alto': 0.14}],
    talon=(0.11, 0.04),
)

PREDATOR = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_FINO, 0.97),
    borde=[(2, 8.9), (4.5, 7.7), (7, 7.1), (10, 7.9), (13, 8.1), (17, 6.8), (21.5, 4.9)],
    base=[(0, 1.2), (12, 1.05), (22, 0.95), (30, 0.95)],
    suela=[(0, -0.1), (0.2, 0.04), (0.8, 0.1), (1.0, 0.08), (1.03, -0.15)],
    punta=(17, 0.8),
    elevar=1.7,
    tacos=[(3, -2.1, 0.8), (3, 2.1, 0.8), (7.3, -2.4, 0.8), (7.3, 2.4, 0.8), (17.5, -3.7, 0.75), (17.5, 3.1, 0.75),
           (22, 0, 0.75), (25.2, -3.1, 0.75), (25.2, 2.6, 0.75), (28, -0.3, 0.7)],
    puntera=(21.5, 0.92, 0.62, 0.12),
    solapa=(10.8, 19.4, 3.3),
    cordones=(12.6, 19.0, 5),
    paneles=[{'parte': 'puntera', 'x': (22, 27), 'v': (0.42, 0.5), 'alto': 0.2, 'forma': 'recto'},
             {'parte': 'puntera', 'x': (22, 27), 'v': (0.58, 0.66), 'alto': 0.2, 'forma': 'recto'}],
    rayas={**SAMBA['rayas'], 'x_abajo': 7.6, 'x_arriba': 10.6, 'paso_abajo': 2.0, 'paso_arriba': 1.5, 'ancho': 0.95, 'v0': 0.08, 'v1': 0.72},
    talon=(0.075, 0.08),
)

TAEKWONDO = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_REDONDO, 0.92),
    borde=[(2, 8.2), (4.5, 6.8), (7, 5.9), (10, 6.2), (13, 6.6), (17, 5.8), (21.5, 3.9)],
    base=[(0, 1.1), (12, 1.0), (22, 0.9), (30, 0.9)],
    suela=[(0, -0.05), (0.15, 0.06), (0.85, 0.1), (1.0, 0.08), (1.03, -0.1)],
    punta=(19, 0.6),
    puntera=None,
    collar=0.16,
    cordon=(0.17, 0.07),
    cordones=(13.4, 19.8, 6),
    lengua=(21.2, 11),
    rayas={**SAMBA['rayas'], 'ancho': 0.62, 'paso_abajo': 1.25, 'paso_arriba': 1.1, 'x_abajo': 11.8, 'x_arriba': 13.8, 'v0': 0.1, 'v1': 0.72},
    talon=(0.035, 0.45),
)

ADILETTE = variante_de(
    SAMBA,
    tipo='chancla',
    contorno=ancho(CONTORNO_REDONDO, 1.02),
    base=[(0, 2.9), (12, 2.4), (22, 2.0), (30, 1.8)],
    suela=[(0, -0.2), (0.08, 0.05), (0.8, 0.1), (1.0, 0.0), (1.02, -0.4)],
    punta=(20, 0.8),
    tira=(13.5, 24.0, 5.6),
)

ADIZERO = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_FINO, 0.98),
    borde=[(2, 13.2), (4.5, 12.1), (7, 11.7), (10, 12.1), (13, 11.7), (17, 9.8), (21.5, 7.2)],
    base=[(0, 3.5), (9, 5.4), (18, 5.2), (25, 3.4), (30, 1.6)],
    suela=[(0, -0.02), (0.05, 0.08), (0.12, 0.14), (0.5, 0.34), (0.82, 0.22), (1.0, 0.08), (1.03, -0.15)],
    corte=1,
    punta=(13, 3.8),
    arco_talon=(9, 1.5),
    puntera=None,
    collar=0.14,
    cordon=(0.17, 0.07),
    cordones=(13.4, 19.8, 6),
    rayas={**SAMBA['rayas'], 'x_abajo': 8.0, 'x_arriba': 12.6, 'paso_abajo': 2.9, 'paso_arriba': 1.9, 'ancho': 1.65, 'v0': 0.05, 'v1': 0.84},
    talon=(0.03, 0.72),
)

GRAND_COURT = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_REDONDO, 1.0),
    borde=[(2, 11.2), (4.5, 9.9), (7, 9.1), (10, 10.0), (13, 10.1), (17, 8.4), (21.5, 6.0)],
    base=[(0, 2.6), (12, 2.45), (22, 2.2), (30, 2.2)],
    suela=SUELA_COPA,
    punta=(19, 0.9),
    puntera=None,
    perfora_punta=True,
    paneles=[{'parte': 'puntera', 'x': (2.5, 6.6), 'v': (0.05, 0.9), 'inclina': 1.4},
             {'parte': 'puntera', 'x': (22.5, 26.5), 'v': (0.05, 0.24), 'inclina': -1}],
    rayas={**SAMBA['rayas'], 'ancho': 1.3, 'paso_abajo': 2.35, 'paso_arriba': 1.95, 'x_abajo': 10.6, 'x_arriba': 12.6, 'v0': 0.08, 'v1': 0.8},
    talon=(0.04, 0.68),
)

SUPERNOVA = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_FINO, 1.05),
    borde=[(2, 13.6), (4.5, 12.2), (7, 11.6), (10, 12.2), (13, 11.9), (17, 9.8), (21.5, 7.0)],
    base=[(0, 4.5), (12, 4.0), (22, 3.2), (30, 2.3)],
    suela=[(0, 0.0), (0.05, 0.12), (0.2, 0.2), (0.23, 0.08), (0.27, 0.24), (0.55, 0.36), (0.6, 0.18), (0.66, 0.34), (1.0, 0.16), (1.03, -0.15)],
    corte=2,
    punta=(14, 3.0),
    arco_talon=(6, 0.8),
    puntera=None,
    guardia=('puntera', 0.2),
    collar=0.46,
    cordon=(0.22, 0.09),
    paneles=[{'parte': 'puntera', 'x': (3.2, 8.2), 'v': (0.16, 0.82), 'inclina': 2.2}],
    rayas={**SAMBA['rayas'], 'ancho': 1.05, 'paso_abajo': 2.0, 'paso_arriba': 1.5, 'x_abajo': 11.4, 'x_arriba': 14.0, 'v0': 0.16, 'v1': 0.76},
    talon=(0.03, 0.72),
)

MEGARIDE = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_FINO, 1.02),
    borde=[(2, 14.6), (4.5, 13.4), (7, 12.9), (10, 13.2), (13, 12.5), (17, 10.0), (21.5, 7.0)],
    base=[(0, 5.8), (12, 5.2), (22, 3.6), (30, 2.5)],
    suela=SUELA_PLANA,
    columnas=([(0, -0.1), (0.05, 0.08), (0.2, 0.14), (0.24, 0.05)],
              [(0.6, 0.05), (0.64, 0.18), (0.9, 0.2), (1.0, 0.1), (1.03, -0.15)], 54, 0.2),
    punta=(15, 2.4),
    puntera=(22.5, 0.82, 0.7, 0.1),
    guardia=('puntera', 0.14),
    collar=0.4,
    paneles=[{'parte': 'puntera', 'x': (4, 9), 'v': (0.12, 0.88), 'inclina': 2.5}],
    rayas={**SAMBA['rayas'], 'ancho': 0.95, 'paso_abajo': 1.9, 'paso_arriba': 1.5, 'x_abajo': 11.0, 'x_arriba': 13.6, 'v0': 0.14, 'v1': 0.76},
    talon=(0.09, 0.12),
)

HAWAII = variante_de(
    GAZELLE,
    base=[(0, 2.9), (12, 2.6), (22, 2.2), (30, 2.1)],
    suela=SUELA_COPA,
    punta=(19, 1.0),
    guardia=('puntera', 0.16),
    paneles=[{'parte': 'puntera', 'x': (21, 26), 'v': (0.16, 0.5), 'inclina': -1}],
    rayas={**GAZELLE['rayas'], 'ancho': 0.9, 'x_abajo': 12.0, 'x_arriba': 14.4, 'paso_abajo': 1.7, 'paso_arriba': 1.4, 'v0': 0.2},
    talon=(0.06, 0.3),
)

ALBRECHT = variante_de(
    SPEZIAL,
    borde=[(2, 13.4), (4.5, 12.8), (7, 12.4), (10, 12.2), (13, 10.9), (17, 8.4), (21.5, 5.6)],
    cordones=(11.6, 19.6, 8),
    collar=0.48,
    puntera=(23.4, 0.8, 0.8, 0.09),
    paneles=[{'parte': 'puntera', 'x': (2.6, 7.4), 'v': (0.05, 0.96), 'inclina': 1.8}],
    rayas={**SPEZIAL['rayas'], 'ancho': 0.7, 'paso_abajo': 1.6, 'paso_arriba': 1.2, 'x_abajo': 11.4, 'x_arriba': 12.6, 'v1': 0.78},
    talon=(0.03, 0.75),
)

CLOT_SAMBA = variante_de(
    SAMBA,
    base=[(0, 3.3), (12, 3.0), (22, 2.7), (30, 2.6)],
    suela=[(0, -0.05), (0.1, 0.12), (0.9, 0.16), (1.0, 0.08), (1.03, -0.15)],
    ondas=(0.09, 90),
    punta=(19, 0.9),
    puntera=(21.0, 0.98, 0.5, 0.1),
    rayas={**SAMBA['rayas'], 'ancho': 0.8, 'paso_abajo': 1.8, 'paso_arriba': 1.3, 'x_abajo': 11.0, 'x_arriba': 13.4},
    talon=(0.07, 0.3),
)

SAMBA_LX = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_FINO, 0.93),
    borde=[(2, 9.7), (4.5, 8.2), (7, 7.3), (10, 8.2), (13, 8.4), (17, 7.0), (21.5, 5.0)],
    base=[(0, 1.9), (12, 1.7), (22, 1.4), (30, 1.3)],
    puntera=(24.5, 0.55, 0.9, 0.09),
    guardia=('puntera', 0.12),
    rayas={**SAMBA['rayas'], 'n': 2, 'ancho': 1.5, 'paso_abajo': 3.0, 'paso_arriba': 2.3, 'x_abajo': 10.2, 'x_arriba': 13.4},
    talon=(0.04, 0.6),
)

TOKYO = variante_de(
    TAEKWONDO,
    borde=[(2, 9.0), (4.5, 7.6), (7, 6.8), (10, 7.2), (13, 7.5), (17, 6.3), (21.5, 4.3)],
    guardia=('puntera', 0.1),
    cordones=(13.0, 19.8, 6),
    rayas={**TAEKWONDO['rayas'], 'x_abajo': 9.2, 'x_arriba': 10.6},
    talon=(0.06, 0.1),
)

ATMOS_ZX = {**ZX, 'guardia': ('puntera', 0.13),
            'puntera': (21.6, 0.9, 0.55, 0.1),
            'paneles': [{'parte': 'talon', 'x': (2.4, 7.6), 'v': (0.1, 0.86), 'inclina': 1.6}],
            'rayas': {**ZX['rayas'], 'ancho': 0.9, 'paso_abajo': 1.9, 'paso_arriba': 1.45, 'x_abajo': 10.6, 'x_arriba': 13.2,
                      'v0': 0.14, 'v1': 0.78},
            'talon': (0.05, 0.4)}

BORDE_ALTO = [(2, 15.6), (4.5, 15.2), (7, 15.0), (10, 14.8), (13, 12.8), (17, 9.8), (21.5, 6.9)]

HOOPS_MID = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_REDONDO, 1.05),
    borde=BORDE_ALTO,
    base=[(0, 3.2), (12, 3.0), (22, 2.7), (30, 2.7)],
    suela=SUELA_COPA,
    punta=(19, 1.0),
    puntera=None,
    guardia=('puntera', 0.14),
    collar=0.62,
    cordones=(11.4, 19.7, 7),
    paneles=[{'parte': 'correa', 'x': (2.8, 10.6), 'v': (0.8, 0.96), 'alto': 0.16, 'forma': 'recto'},
             {'parte': 'correa', 'x': (2.8, 10.6), 'v': (0.62, 0.77), 'alto': 0.16, 'forma': 'recto'}],
    rayas={**SAMBA['rayas'], 'ancho': 1.2, 'paso_abajo': 2.3, 'paso_arriba': 1.9, 'x_abajo': 9.4, 'x_arriba': 13.0, 'v0': 0.14, 'v1': 0.58},
    talon=(0.06, 0.14),
)

FORUM_MID = variante_de(
    FORUM,
    borde=[(2, 16.0), (4.5, 15.6), (7, 15.4), (10, 15.2), (13, 13.0), (17, 9.9), (21.5, 7.0)],
    correa=(11.6, 1.05, 0.6),
    cordones=(12.0, 19.8, 6),
    paneles=[{'parte': 'puntera', 'x': (3.0, 8.0), 'v': (0.16, 0.56), 'inclina': 1.5},
             {'parte': 'talon', 'x': (2.6, 7.2), 'v': (0.72, 0.96), 'alto': 0.14}],
    rayas={**FORUM['rayas'], 'x_abajo': 12.0, 'x_arriba': 15.2, 'ancho': 1.0, 'paso_abajo': 1.95, 'paso_arriba': 1.5, 'v1': 0.6},
)

BREAKNET_MID = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_REDONDO, 1.02),
    borde=[(2, 14.6), (4.5, 14.2), (7, 14.0), (10, 13.8), (13, 12.0), (17, 9.4), (21.5, 6.6)],
    base=[(0, 2.9), (12, 2.7), (22, 2.4), (30, 2.4)],
    suela=SUELA_COPA,
    punta=(19, 0.9),
    puntera=None,
    collar=0.3,
    cordones=(11.0, 19.7, 8),
    rayas={**SAMBA['rayas'], 'ancho': 1.65, 'paso_abajo': 2.9, 'paso_arriba': 2.6, 'x_abajo': 8.8, 'x_arriba': 11.6, 'v0': 0.08, 'v1': 0.62},
    talon=(0.04, 0.72),
)

TERREX = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_FINO, 1.07),
    borde=[(2, 15.2), (4.5, 14.7), (7, 14.5), (10, 14.2), (13, 12.4), (17, 9.8), (21.5, 7.0)],
    base=[(0, 3.9), (12, 3.5), (22, 3.1), (30, 3.1)],
    suela=[(0, 0.0), (0.04, 0.2), (0.3, 0.26), (0.34, 0.04), (0.42, 0.26), (0.78, 0.2), (1.0, 0.1), (1.03, -0.15)],
    corte=3,
    ondas=(0.24, 30),
    punta=(18, 2.0),
    puntera=(23.2, 0.86, 0.5, 0.18),
    guardia=('puntera', 0.14),
    collar=0.3,
    cordon=(0.17, 0.08),
    cordones=(11.2, 19.4, 8),
    lazos=True,
    rayas={**SAMBA['rayas'], 'ancho': 1.0, 'paso_abajo': 2.0, 'paso_arriba': 1.5, 'x_abajo': 10.0, 'x_arriba': 12.8, 'v0': 0.16, 'v1': 0.68},
    talon=(0.09, 0.08),
)

BADBO = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_REDONDO, 1.06),
    borde=[(2, 13.4), (4.5, 12.4), (7, 11.9), (10, 12.5), (13, 12.0), (17, 9.8), (21.5, 7.1)],
    base=[(0, 3.8), (12, 3.5), (22, 3.1), (30, 3.0)],
    suela=SUELA_COPA,
    punta=(19, 1.1),
    puntera=(23.0, 0.8, 0.45, 0.14),
    collar=0.55,
    cordones=(11.8, 19.6, 7),
    paneles=[{'parte': 'talon', 'x': (2.8, 8.4), 'v': (0.2, 0.8), 'inclina': 2.0}],
    rayas={**SAMBA['rayas'], 'ancho': 0.8, 'paso_abajo': 1.5, 'paso_arriba': 1.3, 'x_abajo': 10.2, 'x_arriba': 11.8, 'v0': 0.2, 'v1': 0.76},
    talon=(0.04, 0.72),
)

WC_MEGARIDE = {**MEGARIDE,
               'columnas': (MEGARIDE['columnas'][0], MEGARIDE['columnas'][1], 28, 0.36),
               'puntera': None, 'guardia': ('puntera', 0.26),
               'rayas': {**MEGARIDE['rayas'], 'ancho': 1.4, 'paso_abajo': 2.4, 'paso_arriba': 2.0, 'x_abajo': 9.6, 'x_arriba': 12.4},
               'paneles': [{'parte': 'talon', 'x': (2.8, 6.8), 'v': (0.26, 0.96), 'inclina': 1.5}]}

WB_ARMY = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_FINO, 0.93),
    borde=[(2, 9.8), (4.5, 8.4), (7, 7.6), (10, 8.4), (13, 8.5), (17, 7.1), (21.5, 5.0)],
    base=[(0, 1.9), (12, 1.6), (22, 1.3), (30, 1.25)],
    puntera=(25.0, 0.5, 0.7, 0.08),
    cordon=(0.2, 0.08),
    paneles=[{'parte': 'puntera', 'x': (3.0, 7.0), 'v': (0.05, 0.94), 'inclina': 1.6}],
    rayas={**SAMBA['rayas'], 'ancho': 0.55, 'paso_abajo': 1.2, 'paso_arriba': 1.05, 'x_abajo': 12.8, 'x_arriba': 14.6, 'v0': 0.1, 'v1': 0.76},
    talon=(0.03, 0.75),
)

Y3_EVO = variante_de(
    SUPERNOVA,
    base=[(0, 4.6), (10, 5.5), (20, 4.6), (30, 1.9)],
    suela=[(0, 0.0), (0.05, 0.12), (0.14, 0.18), (0.55, 0.3), (0.62, 0.2), (0.68, 0.3), (1.0, 0.1), (1.03, -0.15)],
    corte=1,
    punta=(14, 3.4),
    arco_talon=(8, 1.3),
    guardia=('puntera', 0.1),
    collar=0.18,
    paneles=[],
    borde=[(2, 13.8), (4.5, 12.8), (7, 12.4), (10, 12.8), (13, 12.3), (17, 10.2), (21.5, 7.5)],
    rayas={**SUPERNOVA['rayas'], 'ancho': 0.6, 'paso_abajo': 1.3, 'paso_arriba': 1.15, 'x_abajo': 12.6, 'x_arriba': 14.2, 'v0': 0.14, 'v1': 0.72},
    talon=(0.1, 0.5),
)

SATISFY_ADIZERO = {**ADIZERO,
                   'base': [(0, 3.2), (9, 4.6), (18, 4.5), (25, 3.0), (30, 1.5)],
                   'borde': [(2, 12.5), (4.5, 11.3), (7, 10.8), (10, 11.2), (13, 10.9), (17, 9.0), (21.5, 6.6)],
                   'guardia': ('puntera', 0.12),
                   'rayas': {**ADIZERO['rayas'], 'ancho': 0.9, 'paso_abajo': 1.7, 'paso_arriba': 1.4, 'x_abajo': 10.6, 'x_arriba': 13.8},
                   'perfora_punta': True}

BAPE_ADISTAR = variante_de(
    SUPERNOVA,
    base=[(0, 5.4), (12, 4.7), (22, 3.7), (30, 2.8)],
    suela=[(0, 0.0), (0.06, 0.16), (0.3, 0.24), (0.33, 0.08), (0.4, 0.3), (0.66, 0.36), (0.7, 0.14), (0.76, 0.3), (1.0, 0.14), (1.03, -0.15)],
    ondas=(0.13, 16),
    corte=2,
    collar=0.6,
    guardia=('puntera', 0.24),
    paneles=[{'parte': 'correa', 'x': (3.2, 7.8), 'v': (0.26, 0.92), 'inclina': 2.2},
             {'parte': 'correa', 'x': (17.5, 21.5), 'v': (0.26, 0.56), 'inclina': -1.5}],
    rayas={**SUPERNOVA['rayas'], 'ancho': 0.95, 'x_abajo': 10.4, 'x_arriba': 12.4, 'v0': 0.26},
    talon=(0.05, 0.62),
)

COCA_SUPERSTAR = {**SUPERSTAR,
                  'base': [(0, 3.1), (12, 2.9), (22, 2.7), (30, 2.7)],
                  'puntera': (21.6, 0.8, 0.26, 0.24),
                  'aros': (0.16, 0.24, 0.32, 0.4, 0.48, 0.56),
                  'paneles': [{'parte': 'talon', 'x': (2.8, 7.4), 'v': (0.08, 0.5), 'inclina': 1.2}],
                  'rayas': {**SUPERSTAR['rayas'], 'ancho': 1.3, 'paso_abajo': 2.3, 'paso_arriba': 1.8}}

ABERTURA_LARGA = [(2.4, 0), (3.2, -2.3), (6.3, -3.0), (9.8, -2.6), (12.8, -1.6), (18, -1.15), (23.6, -0.8),
                  (25.2, 0), (23.6, 0.8), (18, 1.15), (12.8, 1.6), (9.8, 2.6), (6.3, 3.0), (3.2, 2.3)]

GUIDE_TENNIE = variante_de(
    SAMBA,
    contorno=ancho(CONTORNO_REDONDO, 1.0),
    abertura=ABERTURA_LARGA,
    borde=[(2, 11.4), (4.5, 10.4), (7, 9.8), (10, 10.4), (13, 10.2), (18, 8.2), (22, 6.7), (25.5, 5.4)],
    base=[(0, 2.6), (12, 2.3), (22, 2.0), (30, 2.0)],
    suela=[(0, -0.05), (0.08, 0.1), (0.5, 0.16), (0.55, 0.06), (0.6, 0.16), (1.0, 0.1), (1.03, -0.15)],
    punta=(18, 1.6),
    puntera=None,
    guardia=('suela', 0.26),
    lengua=(25.0, 8.2),
    cordones=(12.4, 24.2, 11),
    cordon=(0.17, 0.08),
    ojalera=(11.8, 0.84),
    lazos=True,
    rayas={**SAMBA['rayas'], 'ancho': 0.6, 'paso_abajo': 1.25, 'paso_arriba': 1.1, 'x_abajo': 8.6, 'x_arriba': 10.4, 'v0': 0.3, 'v1': 0.72},
    talon=(0.07, 0.12),
)

SL72 = {**SL72, 'paneles': [{'parte': 'puntera', 'x': (3.0, 7.6), 'v': (0.16, 0.92), 'inclina': 1.6}]}
ZX = {**ZX, 'guardia': ('puntera', 0.16),
      'paneles': [{'parte': 'talon', 'x': (17.5, 20.5), 'v': (0.3, 0.8), 'inclina': -1.5}]}

for _modelo in (SUPERSTAR, CAMPUS, STAN, FORUM, GRAND_COURT, HOOPS_MID, FORUM_MID, BREAKNET_MID,
                BADBO, COCA_SUPERSTAR, HAWAII):
    _modelo['costura_suela'] = 0.84
ADILETTE['contrafuerte'] = False
PREDATOR['contrafuerte'] = (8.0, 0.5)
ULTRABOOST['contrafuerte'] = False

MODELOS = {'samba': SAMBA, 'gazelle': GAZELLE, 'spezial': SPEZIAL, 'superstar': SUPERSTAR,
           'campus': CAMPUS, 'sl72': SL72, 'zx': ZX, 'stansmith': STAN, 'forum': FORUM,
           'ultraboost': ULTRABOOST, 'predator': PREDATOR, 'taekwondo': TAEKWONDO, 'adilette': ADILETTE,
           'adizero': ADIZERO, 'grandcourt': GRAND_COURT, 'supernova': SUPERNOVA, 'megaride': MEGARIDE,
           'hawaii': HAWAII, 'albrecht': ALBRECHT, 'clot': CLOT_SAMBA, 'sambalx': SAMBA_LX, 'tokyo': TOKYO,
           'atmoszx': ATMOS_ZX, 'hoopsmid': HOOPS_MID, 'forummid': FORUM_MID, 'breaknetmid': BREAKNET_MID,
           'terrex': TERREX, 'badbo': BADBO, 'wcmegaride': WC_MEGARIDE, 'wbarmy': WB_ARMY, 'y3evo': Y3_EVO,
           'satisfyadizero': SATISFY_ADIZERO, 'bapeadistar': BAPE_ADISTAR, 'cocasuperstar': COCA_SUPERSTAR,
           'guidetennie': GUIDE_TENNIE}

BLANCO, NEGRO, GOMA = '#f3f1ea', '#17171a', '#b57f4c'


def paleta(cuerpo, rayas, suela=GOMA, puntera=None, talon=None, entresuela=None, cordones=None, forro=None, correa=None):
    oscuro = int(cuerpo[1:3], 16) < 90
    return {
        'capellada': cuerpo, 'ojalera': cuerpo, 'lengua': cuerpo, 'rayas': rayas, 'suela': suela,
        'puntera': puntera or cuerpo, 'talon': talon or rayas, 'entresuela': entresuela or BLANCO,
        'cordones': cordones or (cuerpo if oscuro else BLANCO),
        'forro': forro or ('#2b2b2f' if oscuro else '#e6e2d8'),
        'costuras': '#55555c' if oscuro else '#b9b4a6',
        'correa': correa or rayas,
        'contrafuerte': cuerpo,
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
    'hawaii': ('Hawaii SPZL', 'hawaii', [
        v('Marrón tono a tono', 130, [40, 41, 42], '#6a4a33', '#54392a', suela=GOMA),
        v('Verde', 130, [39, 41, 43], '#3d5a3d', '#e8dcc4', suela=GOMA),
    ]),
    'albrecht': ('Albrecht II SPZL', 'albrecht', [
        v('Marrón', 140, [40, 41, 42, 44], '#7a5436', '#e8dcc4', puntera='#6b4930'),
        v('Azul marino', 140, [39, 41, 43], '#1f2c4f', '#d6d4cd', puntera='#1b2644'),
    ]),
    'zx8000': ('ZX 8000', 'zx', [
        v('Azul y amarillo', 120, [40, 41, 42, 43], '#d8d9dc', '#2352a3', suela='#2352a3', puntera='#2f6fb5', talon='#e6c229', entresuela='#f3f1ea'),
        v('Blanco y gris', 120, [38, 39, 41], BLANCO, '#8a8c92', suela='#8a8c92', puntera='#c9c9cc', talon='#8a8c92'),
    ]),
    'stansmith': ('Stan Smith', 'stansmith', [
        v('Blanco y verde', 100, [37, 38, 40, 41, 42], BLANCO, '#b8b5ab', suela=BLANCO, talon='#1f6b45'),
        v('Blanco y azul', 100, [38, 39, 41, 43], BLANCO, '#b8b5ab', suela=BLANCO, talon='#1f3f8a'),
        v('Blanco y dorado', 110, [39, 40, 41], BLANCO, '#b8b5ab', suela=BLANCO, talon='#b9933f'),
    ]),
    'forum': ('Forum Low', 'forum', [
        v('Blanco y azul', 110, [39, 40, 41, 42, 44], BLANCO, '#1f3f8a', suela=BLANCO, puntera='#e4e2db', talon='#1f3f8a', correa='#1f3f8a'),
        v('Blanco y rojo', 110, [38, 41, 42, 43], BLANCO, '#b3261e', suela=BLANCO, puntera='#e4e2db', talon='#b3261e', correa='#b3261e'),
        v('Negro total', 120, [40, 41, 43], '#1e1e22', '#3a3a40', suela='#1e1e22', puntera='#2b2b30', talon='#3a3a40', correa='#3a3a40', cordones='#1e1e22'),
    ]),
    'ultraboost': ('Ultraboost', 'ultraboost', [
        v('Negro y blanco', 180, [39, 40, 41, 42, 43], '#26262b', '#3f3f46', suela='#26262b', talon='#3f3f46', entresuela=BLANCO, cordones='#26262b'),
        v('Blanco total', 180, [38, 40, 41, 42], '#e7e6e1', '#cfcfca', suela='#c9c9c4', talon='#cfcfca', entresuela=BLANCO, cordones=BLANCO),
        v('Azul y naranja', 190, [40, 41, 44], '#1f3f8a', '#e8703a', suela='#1f3f8a', talon='#e8703a', entresuela=BLANCO, cordones=BLANCO),
    ]),
    'adilette': ('Adilette', 'adilette', [
        v('Negro y blanco', 45, [38, 39, 40, 41, 42, 43, 44], NEGRO, BLANCO, suela=NEGRO),
        v('Azul y blanco', 45, [38, 40, 42, 43], '#1f3f8a', BLANCO, suela='#1f3f8a'),
        v('Blanco y negro', 45, [37, 38, 39, 41], BLANCO, '#141414', suela=BLANCO),
    ]),
    'predator': ('Predator 96 FG', 'predator', [
        v('Negro y rojo', 300, [39, 40, 41, 42, 43], NEGRO, BLANCO, suela='#b3261e', puntera='#26262b', talon='#b3261e', entresuela=BLANCO),
        v('Blanco y negro', 300, [40, 41, 42], BLANCO, '#141414', suela='#141414', puntera='#e4e2db', talon='#141414'),
    ]),
    'taekwondo': ('Taekwondo', 'taekwondo', [
        v('Blanco y negro', 90, [36, 37, 38, 39, 40], BLANCO, '#141414', suela=GOMA, forro=BLANCO),
        v('Negro y blanco', 90, [37, 38, 39, 41], NEGRO, BLANCO, suela=GOMA),
        v('Rojo y blanco', 95, [36, 37, 38], '#b3261e', BLANCO, suela=GOMA),
    ]),
    'adizero': ('Adizero Adios Pro', 'adizero', [
        v('Rosa y negro', 250, [39, 40, 41, 42], '#ec2f5b', '#16161a', suela='#16161a', talon='#16161a', entresuela='#f6f4ee', cordones='#ec2f5b'),
        v('Negro y gris', 250, [40, 41, 42, 43], '#1c1c20', '#55555c', suela='#1c1c20', talon='#55555c', entresuela='#8f9096', cordones='#1c1c20'),
        v('Blanco y azul', 250, [38, 39, 41], '#eceae4', '#1f3f8a', suela='#1f3f8a', talon='#1f3f8a', entresuela=BLANCO, cordones=BLANCO),
    ]),
    'grandcourt': ('Grand Court Base', 'grandcourt', [
        v('Blanco y negro', 75, [37, 38, 39, 40, 41, 42, 43], BLANCO, '#141414', suela=BLANCO, puntera='#e6e4dd', talon='#141414'),
        v('Blanco y verde', 75, [38, 40, 41, 42], BLANCO, '#1f5a3c', suela=BLANCO, puntera='#e6e4dd', talon='#1f5a3c'),
        v('Negro y blanco', 75, [39, 41, 43], NEGRO, BLANCO, suela=BLANCO, puntera='#26262b', talon=BLANCO),
    ]),
    'supernova': ('Supernova', 'supernova', [
        v('Gris y azul', 130, [39, 40, 41, 42], '#b9bbc0', '#8f9096', suela='#3b3c88', puntera='#8f9096', talon='#3b3c88', entresuela='#e8e7e2', cordones=BLANCO),
        v('Negro y blanco', 130, [40, 41, 43], '#1c1c20', '#4a4a50', suela='#1c1c20', puntera='#2c2c31', talon='#4a4a50', entresuela=BLANCO),
        v('Blanco y naranja', 135, [38, 39, 41], BLANCO, '#e8703a', suela='#e8703a', puntera='#d9d7cf', talon='#e8703a', entresuela=BLANCO),
    ]),
    'megaride': ('Megaride', 'megaride', [
        v('Negro y rojo', 180, [40, 41, 42, 43], '#17231d', '#1f5a3c', suela='#141416', puntera='#222a26', talon='#c2a82f', entresuela='#17231d', correa='#b3261e', forro='#0e0e10'),
        v('Plata y negro', 180, [39, 41, 42], '#bfc1c6', '#35353b', suela='#141416', puntera='#8f9096', talon='#35353b', entresuela='#d9d9d6', correa='#141416', forro='#0e0e10'),
    ]),
    'hoopsmid': ('Hoops Mid', 'hoopsmid', [
        v('Negro y blanco', 85, [39, 40, 41, 42, 43], '#1b1b1f', BLANCO, suela='#1b1b1f', puntera='#2a2a2f', talon='#2a2a2f', correa=BLANCO, cordones='#1b1b1f'),
        v('Blanco y negro', 85, [38, 40, 41, 42], BLANCO, '#141414', suela=BLANCO, puntera='#dedcd5', talon='#141414', correa='#dedcd5'),
        v('Blanco y azul', 85, [39, 41, 43], BLANCO, '#1f3f8a', suela=BLANCO, puntera='#dedcd5', talon='#1f3f8a', correa='#1f3f8a'),
    ]),
    'forummid': ('Forum Mid', 'forummid', [
        v('Blanco y azul', 120, [39, 40, 41, 42], BLANCO, '#1f45c4', suela='#1f45c4', puntera='#e4e2db', talon='#1f45c4', correa=BLANCO, entresuela=BLANCO),
        v('Crema y negro', 125, [40, 41, 43], BLANCO, '#232326', suela='#232326', puntera='#d8cbb0', talon='#232326', correa='#d8cbb0'),
        v('Negro total', 125, [41, 42, 44], '#1e1e22', '#3a3a40', suela='#1e1e22', puntera='#2b2b30', talon='#3a3a40', correa='#3a3a40', cordones='#1e1e22'),
    ]),
    'breaknetmid': ('Breaknet Mid', 'breaknetmid', [
        v('Blanco y negro', 80, [38, 39, 40, 41, 42], BLANCO, '#141414', suela=BLANCO, talon='#141414'),
        v('Negro y blanco', 80, [40, 41, 43], NEGRO, BLANCO, suela=BLANCO, talon=BLANCO),
        v('Blanco y verde', 80, [38, 41, 42], BLANCO, '#1f5a3c', suela=BLANCO, talon='#1f5a3c'),
    ]),
    'terrex': ('Terrex', 'terrex', [
        v('Negro total', 160, [40, 41, 42, 43, 44], '#1a1a1d', '#2e2e33', suela='#111113', puntera='#232327', talon='#2e2e33', entresuela='#232327', cordones='#111113'),
        v('Verde y naranja', 165, [39, 41, 42], '#44513a', '#2d3626', suela='#111113', puntera='#2d3626', talon='#e8703a', entresuela='#6a6a63', cordones='#e8703a'),
        v('Arena y negro', 165, [40, 42, 43], '#b9a888', '#3a342a', suela='#1a1a1d', puntera='#7b6d55', talon='#3a342a', entresuela='#e0d9c8', cordones='#3a342a'),
    ]),
    'badbo': ('Bad Bunny BadBo 1.0', 'badbo', [
        v('Blanco, rojo y azul', 160, [39, 40, 41, 42, 43], BLANCO, '#c8102e', suela=BLANCO, puntera='#1f3f8a', talon='#1f3f8a', correa='#c8102e'),
        v('Negro y rojo', 160, [40, 41, 43], NEGRO, '#c8102e', suela='#1b1b1f', puntera='#2a2a2f', talon='#c8102e', correa='#c8102e'),
    ]),
    'chavarria-megaride': ('Willy Chavarria × Megaride', 'wcmegaride', [
        v('Negro y plata', 200, [40, 41, 42, 43], '#1a1a1d', '#c9cbd0', suela='#111113', puntera='#2a2a2f', talon='#c9cbd0', entresuela='#1a1a1d', correa='#c9cbd0', forro='#0e0e10'),
        v('Blanco y rojo', 200, [39, 41, 42], BLANCO, '#b3261e', suela='#141416', puntera='#d9d7cf', talon='#b3261e', entresuela=BLANCO, correa='#b3261e', forro='#0e0e10'),
    ]),
    'wb-army': ('Wales Bonner × BW Army', 'wbarmy', [
        v('Marrón y crema', 190, [38, 40, 41, 42], '#6b4a31', '#e8dcc4', suela=GOMA, puntera='#58391f', talon='#e8dcc4'),
        v('Crema y verde', 190, [39, 41, 43], '#e4d6bd', '#2c5a3f', suela=GOMA, puntera='#d6c6a8', talon='#2c5a3f'),
    ]),
    'y3-evo': ('Y-3 Evo SL', 'y3evo', [
        v('Blanco y negro', 240, [39, 41, 42], '#e7e6e1', '#141414', suela='#141414', puntera='#d9d7cf', talon='#141414', entresuela=BLANCO),
        v('Negro total', 240, [40, 41, 42, 43], '#141416', '#2d2d32', suela='#141416', puntera='#232327', talon='#2d2d32', entresuela='#55555c', cordones='#141416'),
    ]),
    'satisfy-adizero': ('Satisfy × Adizero Adios Pro 4', 'satisfyadizero', [
        v('Gris y lima', 280, [39, 40, 41, 42], '#b5b7ba', '#c7e03a', suela='#2c2c31', puntera='#8f9096', talon='#c7e03a', entresuela='#e0e0da', cordones='#c7e03a'),
        v('Negro y lima', 280, [40, 41, 43], '#1c1c20', '#c7e03a', suela='#1c1c20', puntera='#2c2c31', talon='#c7e03a', entresuela='#35353b', cordones='#1c1c20'),
    ]),
    'bape-adistar': ('BAPE × Adistar HRMY', 'bapeadistar', [
        v('Verde militar', 220, [40, 41, 42], '#5d6b4a', '#2a3324', suela='#2a3324', puntera='#3f4b33', talon='#2a3324', entresuela='#d9d5c5', correa='#8a9470'),
        v('Azul y blanco', 220, [39, 41, 43], '#3a5fa8', BLANCO, suela='#1f3f8a', puntera='#27437a', talon=BLANCO, entresuela=BLANCO, correa='#7f9bd0'),
    ]),
    'coca-superstar': ('Coca-Cola × Superstar', 'cocasuperstar', [
        v('Rojo y blanco', 150, [38, 40, 41, 42, 43], '#c8102e', BLANCO, suela=BLANCO, puntera=BLANCO, talon=BLANCO),
        v('Blanco y rojo', 150, [39, 41, 42], BLANCO, '#c8102e', suela=BLANCO, puntera='#e9e7df', talon='#c8102e'),
    ]),
    'braindead-guide': ('Brain Dead × Guide Tennie', 'guidetennie', [
        v('Mostaza y negro', 170, [40, 41, 42, 43], '#b08a2e', '#2b2b2b', suela='#1e1e22', talon='#2b2b2b', cordones='#1e1e22'),
        v('Violeta y negro', 170, [39, 41, 43], '#5c4a86', '#2b2b2b', suela='#1e1e22', talon='#d8d24b', cordones='#d8d24b'),
    ]),
    'clot-samba': ('CLOT × Samba', 'clot', [
        v('Crema y yute', 180, [40, 41, 42], '#e4d6bd', '#3a2c20', suela='#c8a877', puntera='#d6c6a8'),
        v('Negro y yute', 180, [41, 42, 43], '#232326', '#c8a877', suela='#c8a877', puntera='#2e2e33'),
    ]),
    'sftm-samba': ('Song for the Mute × Samba LX', 'sambalx', [
        v('Gris desgastado', 170, [39, 41, 42], '#8e8a80', '#3d3b37', suela='#9c8866', puntera='#7f7b72'),
        v('Marrón desgastado', 170, [40, 42, 44], '#6e5a48', '#d5ccb9', suela='#9c8866', puntera='#604e3f'),
    ]),
    'sftm-tokyo': ('Song for the Mute × Tokyo', 'tokyo', [
        v('Verde desgastado', 170, [39, 40, 41], '#59604b', '#d5ccb9', puntera='#4e5442'),
        v('Negro desgastado', 170, [40, 41, 43], '#2d2c2a', '#a9a497', puntera='#3a3936'),
    ]),
    'atmos-zx': ('atmos × ZX 8000', 'atmoszx', [
        v('Blanco, gris y rojo', 160, [40, 41, 42], '#efeeea', '#111114', suela='#d23a2e', puntera='#c9c8c3', talon='#d23a2e', entresuela='#efeeea'),
        v('Negro y rojo', 160, [41, 42, 43], '#1b1b1f', '#d23a2e', suela='#d23a2e', puntera='#2c2c31', talon='#2c2c31', entresuela='#e8e6df'),
    ]),
}

DESCRIPCIONES = {
    'samba': 'Silueta baja de inspiración futbolera, con puntera en T y suela de goma.',
    'gazelle': 'Clásico de perfil bajo y líneas limpias, pensado para el uso diario.',
    'superstar': 'Puntera de concha y suela de copa, una silueta reconocible al instante.',
    'hawaii': 'Silueta de terraza con suela de copa y refuerzo bajo en la capellada.',
    'albrecht': 'Corte alto para tobillo, con muchos ojales y rayas finas.',
    'clot': 'Versión con suela alta de textura trenzada y puntera ampliada.',
    'sambalx': 'Perfil muy bajo, con dos franjas anchas y materiales desgastados.',
    'tokyo': 'Silueta delgada con correa sobre el empeine.',
    'atmoszx': 'Running en capas, con correa y paneles de contraste.',
    'hoopsmid': 'Bota media de baloncesto, con cuello acolchado en franjas.',
    'forummid': 'Bota media con correa en el tobillo y puntera perforada.',
    'breaknetmid': 'Bota media limpia, con rayas anchas y suela de copa.',
    'terrex': 'Bota de senderismo con suela de tacos, puntera reforzada y tiradores.',
    'badbo': 'Versión aproximada: silueta de cancha con correa y colores de bandera.',
    'wcmegaride': 'Suela de columnas gruesas y capellada envolvente.',
    'wbarmy': 'Perfil bajo y delgado con rayas finas y suela de goma.',
    'y3evo': 'Running elevado de líneas limpias, con suela curva.',
    'satisfyadizero': 'Zapatilla de competición con suela curva y puntera perforada.',
    'bapeadistar': 'Running voluminoso con suela en capas y paneles de contraste.',
    'cocasuperstar': 'Superstar de puntera marcada y paneles en el talón.',
    'guidetennie': 'Zapatilla de aproximación con cordones hasta la punta y borde de goma.',
    'adizero': 'Zapatilla de competición con suela curva muy alta y rayas anchas.',
    'grandcourt': 'Tenis de cancha sencillo, con talón y puntera en capas.',
    'supernova': 'Running de uso diario con suela acolchada en capas.',
    'megaride': 'Suela hueca con columnas a la vista y capellada envolvente.',
    'stansmith': 'Tenis limpio, sin rayas: tres líneas de perforaciones y talón de color.',
    'forum': 'Bota baja de baloncesto con correa en el tobillo y puntera perforada.',
    'ultraboost': 'Tejido tipo calcetín, jaula lateral y una suela alta y abultada.',
    'adilette': 'Chancla de tira ancha y suela contorneada, para antes y después de entrenar.',
    'predator': 'Bota de fútbol con lengüeta sobre los cordones y tacos en la suela.',
    'taekwondo': 'Silueta muy delgada y flexible, con suela casi plana.',
    'campus': 'Proporciones anchas, cuello acolchado y cordones gruesos.',
    'spezial': 'Perfil estilizado de inspiración deportiva, con suela de goma.',
    'sl72': 'Silueta de running retro con suela en cuña y rayas finas.',
    'zx': 'Zapatilla de running de volumen generoso, con refuerzo en el talón.',
}

ESTANTES = [
    {'id': 'vendidos', 'nombre': 'Más vendidos', 'color': '#ffe2bd', 'oscuro': False,
     'zapatos': ['samba', 'gazelle', 'superstar', 'adilette', 'ultraboost', 'stansmith', 'forum', 'campus',
                 'spezial', 'sl72', 'taekwondo', 'grandcourt']},
    {'id': 'novedades', 'nombre': 'Novedades', 'color': '#cfe4ff', 'oscuro': False,
     'zapatos': ['predator', 'adizero', 'hawaii', 'zx8000', 'supernova', 'megaride', 'albrecht',
                 'hoopsmid', 'forummid', 'breaknetmid', 'terrex']},
    {'id': 'colaboraciones', 'nombre': 'Colaboraciones', 'color': '#ffffff', 'oscuro': True,
     'zapatos': ['badbo', 'chavarria-megaride', 'clot-samba', 'wb-army', 'y3-evo', 'satisfy-adizero',
                 'bape-adistar', 'coca-superstar', 'braindead-guide', 'sftm-samba', 'sftm-tokyo', 'atmos-zx']},
]

for _modelo in MODELOS.values():
    _quedan = []
    for _p in _modelo.get('paneles', ()):
        if _p.get('forma', 'redondo') == 'recto' or _p['parte'] == 'rayas':
            _quedan.append(_p)
        elif _p['x'][0] < 4.5 and 'contrafuerte_como' not in _modelo and _modelo.get('contrafuerte') is not False:
            _modelo['contrafuerte'] = (_p['x'][1] + 0.5 * _p.get('inclina', 0), min(max(_p['v'][1], 0.5), 0.86))
            _modelo['contrafuerte_como'] = _p['parte']
    _modelo['paneles'] = _quedan

for _nombre, _base, _lista in PRODUCTOS.values():
    _como = MODELOS[_base].get('contrafuerte_como')
    if _como:
        for _x in _lista:
            _x['colores']['contrafuerte'] = _x['colores'][_como]

for _clave, _modelo in MODELOS.items():
    _lista = next(x[2] for x in PRODUCTOS.values() if x[1] == _clave)
    _modelo['variantes'] = {str(i): x['colores'] for i, x in enumerate(_lista)}
