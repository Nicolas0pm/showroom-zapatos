import { useRef, useState } from 'react'
import gsap from 'gsap'
import { usarCarrito } from '../carrito.jsx'
import { usarSinMovimiento } from '../usarSinMovimiento.js'

// Precio, color, talla y boton de compra; se usa en la sala y en el detalle.
export default function Opciones({ clave, producto, variante, alCambiar }) {
  const { agregar } = usarCarrito()
  const sinMovimiento = usarSinMovimiento()
  const [talla, setTalla] = useState(null)
  const [agregado, setAgregado] = useState(false)
  const precio = useRef(null)
  const temporizador = useRef(null)

  function elegir(nueva) {
    if (nueva.id === variante.id) return
    alCambiar(nueva)
    if (!nueva.tallas.includes(talla)) setTalla(null)
    setAgregado(false)
    if (!sinMovimiento) {
      gsap.fromTo(precio.current, { y: 10, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: 0.35, ease: 'power2.out' })
    }
  }

  function comprar() {
    agregar({ producto: clave, variante: variante.id, talla, precio: variante.precio })
    setAgregado(true)
    clearTimeout(temporizador.current)
    temporizador.current = setTimeout(() => setAgregado(false), 1800)
  }

  return (
    <>
      <p className="precio" ref={precio} aria-live="polite">${variante.precio}</p>

      <fieldset>
        <legend>Color: <span>{variante.nombre}</span></legend>
        <div className="colores">
          {producto.variantes.map((v) => (
            <button
              key={v.id}
              type="button"
              className="color"
              aria-label={v.nombre}
              aria-pressed={v.id === variante.id}
              style={{ '--a': v.muestra[0], '--b': v.muestra[1] }}
              onClick={() => elegir(v)}
            />
          ))}
        </div>
      </fieldset>

      <fieldset>
        <legend>Talla <span>{talla ?? 'sin elegir'}</span></legend>
        <div className="tallas">
          {producto.tallas.map((t) => (
            <button
              key={t}
              type="button"
              className="talla"
              disabled={!variante.tallas.includes(t)}
              aria-pressed={t === talla}
              onClick={() => setTalla(t)}
            >
              {t}
            </button>
          ))}
        </div>
      </fieldset>

      <button type="button" className={`agregar ${agregado ? 'listo' : ''}`} disabled={!talla} onClick={comprar}>
        {agregado ? 'Agregado ✓' : talla ? 'Agregar a la bolsa' : 'Elige una talla'}
      </button>
      <p className="simulado">Precios, tallas y modelos provisionales.</p>
    </>
  )
}
