# Showroom de zapatos

Tienda virtual en 3D para el proyecto de motion design. El usuario recorre una sala con tres estanterías, elige un zapato y cambia su color y talla.

Proyecto universitario sin fines comerciales, sin relación con las marcas mencionadas. Precios y tallas simulados.

## Ejecutar

```bash
npm install
npm run dev
```

## Modelos 3D

Los modelos se generan con Blender desde `blender/zapato.py`. Las medidas y el catálogo están en `blender/modelos.py`.

```bash
cd blender
blender -b -P zapato.py -- --modelo samba --glb --lod 0.1
python3 generar_catalogo.py
```
