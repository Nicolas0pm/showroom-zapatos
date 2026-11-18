# Showroom de zapatos

Tienda virtual en 3D hecha para el proyecto de motion design. En vez de una cuadrícula de productos, el usuario entra a una sala con estilo urbano, recorre tres estanterías, toma un zapato, lo gira y elige su color y talla.

**Sitio publicado:** https://showroom-zapatos.vercel.app

> Proyecto universitario sin fines comerciales y sin relación con las marcas o personas mencionadas. No se vende nada: precios, tallas y modelos son simulados, y los modelos 3D son aproximaciones hechas por el equipo.

## Tecnologías

| Uso | Herramienta |
|---|---|
| Interfaz y páginas | React 19, React Router |
| 3D en el navegador | Three.js con React Three Fiber y Drei |
| Animación | GSAP y su complemento ScrollTrigger |
| Empaquetado | Vite |
| Modelos 3D y fotos | Blender 5 con scripts en Python |
| Compresión de modelos | glTF-Transform (meshopt) |
| Publicación | Vercel |

## Ejecutar

```bash
npm install
npm run dev        # servidor de desarrollo
npm run build      # versión de producción en dist/
npm run preview    # sirve la versión de producción
```

## Estructura

```
blender/                   Producción de contenido (corre fuera del navegador)
  modelos.py               Medidas de cada zapato, colores, precios y estanterías
  zapato.py                Construye un zapato pieza por pieza, lo renderiza y lo exporta
  generar_catalogo.py      Escribe src/catalogo.json a partir de modelos.py
  exportar.sh              Exporta todos los modelos, los comprime y genera las fotos
public/
  modelos/*.glb            Zapato completo y versión liviana para las repisas
  fotos/*.webp             Una foto por producto y color
src/
  main.jsx                 Punto de entrada
  App.jsx                  Rutas, cabecera y carga diferida de páginas
  paginas/                 Inicio (sala), Catálogo, Producto, Carrito, Nosotros, Contacto
  componentes/             Panel, Opciones (color y talla), Tarjeta, VisorZapato
  Sala.jsx                 Escena 3D: cámara, sala, estanterías y zapato elegido
  texturas.js              Ladrillo, concreto, grafiti, piso, neón y cortina dibujados en canvas
  carrito.jsx              Estado del carrito compartido por todas las páginas
  transicion.jsx           Transición de franjas entre páginas
  aparicion.js             Aparición de elementos al hacer scroll
  usarSinMovimiento.js     Detecta si el usuario pide reducir el movimiento
  catalogo.json            Generado: no se edita a mano
  estilos.css              Estilos de toda la aplicación
```

## Arquitectura

Es una aplicación de una sola página (SPA) basada en componentes y publicada como sitio estático: no tiene servidor ni base de datos. Se divide en dos partes que solo se comunican por archivos.

```
          BLENDER (Python)                               NAVEGADOR (React)
  modelos.py ──► zapato.py ──► exportar.sh     catalogo.json ──► páginas y componentes
      │                          │                  modelos/*.glb ──► Sala.jsx, VisorZapato
      └──► generar_catalogo.py   ├─► public/modelos      fotos/*.webp ──► Catálogo, Producto, Carrito
                                 └─► public/fotos
```

- **Una sola fuente de datos.** Todo el catálogo vive en `blender/modelos.py`. De ahí salen los modelos 3D, las fotos y el `catalogo.json` de la web. Para cambiar un precio o un color se edita un solo lugar.
- **Presentación.** Cada página y cada pieza de la interfaz es un componente de React. Las páginas se cargan solo cuando se visitan (`React.lazy`), así que la portada pesa poco.
- **Estado compartido.** El carrito y la transición usan contextos de React. El carrito se guarda en `localStorage`.
- **Escena 3D.** `Sala.jsx` reúne la cámara, la sala, las repisas y el zapato elegido. Es el archivo más grande, y separarlo en varios es una mejora pendiente.

## Cómo se construyen los zapatos

Los modelos no se esculpen a mano: `zapato.py` los genera a partir de números. Cada zapato es un diccionario en `modelos.py` con medidas en centímetros. El eje x va del talón (0) a la punta (30).

1. **Horma.** La clase `Horma` define la capellada como una superficie `S(u, v)`. `u` recorre el contorno del pie y `v` sube desde la suela hasta la abertura del cuello. La sección es una superelipse, así que la pared sube casi recta y luego se curva. Con `cupula()` la punta baja suavemente hacia la nariz, como en un zapato real.
2. **Piezas.** Cada parte es una malla con su propio material: suela, capellada, puntera, rayas, contrafuerte, ojalera, lengua, cordones cruzados con moño, costuras, perforaciones, correas, tacos y demás. Los paneles se dibujan como parches sobre la misma superficie `S(u, v)`, por eso quedan pegados al zapato.
3. **Variantes de forma.** Cada modelo cambia solo lo que lo distingue. Por ejemplo, el Superstar tiene puntera de concha y rayas dentadas, el Predator lleva tacos, el Megaride tiene suela de columnas y la Adilette se arma con la función `chancla()`.
4. **Materiales.** Cada pieza tiene un acabado (cuero, gamuza, malla, tela, goma o plástico) que define su rugosidad y su brillo aterciopelado. No se usan texturas.
5. **Exportación.** `exportar.sh` genera para cada modelo un GLB completo, uno liviano para las repisas (`--lod 0.1`) y una foto transparente por color. Después comprime los GLB con meshopt y convierte las fotos a WebP.

```bash
cd blender
./exportar.sh                    # todos los modelos (unos 15 minutos)
./exportar.sh samba gazelle      # solo algunos
blender -b -P zapato.py -- --modelo samba --render --vistas lado,tres_cuartos   # revisar un modelo
```

### Agregar un zapato

1. En `modelos.py`, crear el modelo con `variante_de(SAMBA, ...)` cambiando solo lo necesario, y agregarlo al diccionario `MODELOS`.
2. Agregar el producto en `PRODUCTOS`, con su nombre, su modelo base y sus colores (`v(...)`), y su texto en `DESCRIPCIONES`.
3. Ubicarlo en una estantería dentro de `ESTANTES`.
4. Ejecutar `./exportar.sh nombre-del-modelo`.

## La sala 3D

- **Cámara en polares.** La cámara se describe por hacia dónde mira (ángulo), qué tan lejos del centro está (radio) y a qué altura. Por eso pasar de una pared a otra es un giro en arco y no un deslizamiento. Entre paredes opuestas siempre gira pasando por el fondo.
- **Repisas livianas.** Todos los zapatos de un mismo modelo se dibujan con una `InstancedMesh` por pieza, lo que reduce mucho las llamadas de dibujo. Cada repisa usa el modelo liviano y su color sale de la primera variante del producto.
- **Zapato elegido.** Al hacer clic se carga el GLB completo, que sale de la repisa hacia la cámara mientras un velo oscurece el fondo. El zapato se gira arrastrando, y el color cambia con una transición.
- **Texturas dibujadas.** El ladrillo, el concreto, el grafiti, el piso de cancha, el neón y la cortina metálica se dibujan en `canvas` al cargar, sin descargar imágenes. Se crean una por una en pausas libres del navegador, para no congelar la carga.

## Animaciones y su intención

| Animación | Para qué sirve |
|---|---|
| Vuelta de 360° al entrar, con neón que parpadea | Presenta la sala completa y muestra dónde está cada sección |
| Giro en arco entre paredes | Mantiene la orientación del usuario dentro de la sala |
| Zapato que sale de la repisa y fondo que se oscurece | Pone el foco en el producto elegido |
| Cambio de color con transición | Confirma la elección sin recargar nada |
| Contador de la bolsa que salta | Confirma que el producto se agregó |
| Franjas diagonales entre páginas | Da continuidad a la marca al navegar |
| Tarjetas que aparecen al hacer scroll | Guía la lectura del catálogo |

## Accesibilidad

- Con la preferencia del sistema "reducir movimiento" activa, no hay vuelta de entrada ni transiciones: la sala y los cambios de pared aparecen directamente.
- Los zapatos de cada estantería también son botones accesibles con teclado, que aparecen al recibir el foco.
- Los controles tienen nombres accesibles, los formularios marcan sus errores con `aria-invalid` y el precio se anuncia con `aria-live`.

## Rendimiento

- **Portada liviana en celular.** La sala 3D se carga solo al tocar "Entrar a la sala", y la portada transfiere unos 120 KB.
- **Modelos comprimidos.** Los modelos usan meshopt: cada zapato completo pesa entre 130 y 190 KB, y la versión de repisa unos 30 KB.
- **3D bajo demanda.** El visor 3D de la ficha de producto solo carga al pulsar "Ver en 3D"; antes se muestra la foto.

Lighthouse en móvil, medido el 10 de noviembre de 2026 antes de los últimos cambios de materiales:

| Medición | Rendimiento |
|---|---|
| Portada | 99 |
| Escritorio con la sala | 69 |
| Móvil simulado con la sala | 67 |

La parte más pesada es arrancar la sala 3D. Para mejorarla habría que unir los modelos de repisa en un solo archivo o cargar solo la pared visible.

## Publicación

El sitio se publica en Vercel. `vercel.json` redirige todas las rutas a `index.html`, para que enlaces como `/catalogo` funcionen al abrirlos directamente.

```bash
npx vercel deploy --prod
```

## Material y licencias

- Los modelos 3D, las fotos de producto y las texturas los genera el propio proyecto con código. No se usan imágenes, modelos ni fuentes de terceros: las letras son las del sistema.
- Las librerías usadas (React, Three.js, React Three Fiber, Drei, React Router y Vite) tienen licencia MIT. GSAP se usa bajo su licencia estándar gratuita.
- Las marcas y los nombres de modelos pertenecen a sus dueños y se mencionan solo con fines académicos.
