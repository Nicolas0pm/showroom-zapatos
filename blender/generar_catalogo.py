"""Escribe src/catalogo.json a partir de modelos.py: python3 generar_catalogo.py"""
import json
import os

from modelos import ESTANTES, PRODUCTOS

TALLAS = [36, 37, 38, 39, 40, 41, 42, 43, 44]
productos = {}
for clave, (nombre, base, variantes) in PRODUCTOS.items():
    productos[clave] = {
        'nombre': nombre,
        'base': base,
        'tallas': TALLAS,
        'variantes': [{'id': str(i), **x} for i, x in enumerate(variantes)],
    }
destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'catalogo.json')
with open(destino, 'w') as f:
    json.dump({'productos': productos, 'estantes': ESTANTES}, f, indent=2, ensure_ascii=False)
