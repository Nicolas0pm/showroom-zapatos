#!/bin/bash
# Exporta todos los modelos a la web, los comprime y renderiza las fotos del catalogo.
cd "$(dirname "$0")"
# Con argumentos solo procesa esos modelos: ./exportar.sh terrex forummid
MODELOS=${*:-$(python3 -c "from modelos import MODELOS; print(' '.join(MODELOS))")}
[ $# -eq 0 ] && rm -f renders/fotos/*.png ../public/fotos/*.webp
mkdir -p renders/fotos ../public/fotos
for m in $MODELOS; do
  blender -b -P zapato.py -- --modelo $m --glb --lod 0.1 --fotos 2>&1 | grep -E 'Traceback|Error:'
done
cd ..
for m in $MODELOS; do for f in public/modelos/$m.glb public/modelos/$m-repisa.glb; do
  npx -y @gltf-transform/cli meshopt "$f" "${f%.glb}.opt.glb" 2>&1 | grep -i error
  mv "${f%.glb}.opt.glb" "$f"
done; done
cd blender
for f in renders/fotos/*.png; do
  magick "$f" -trim +repage -resize 640x400 -background none -gravity center -extent 680x440 -quality 78 "../public/fotos/$(basename "${f%.png}").webp"
done
python3 generar_catalogo.py
ls ../public/fotos | wc -l
du -sh ../public/fotos ../public/modelos
