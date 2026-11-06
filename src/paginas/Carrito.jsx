import { useRef, useState } from 'react'
import gsap from 'gsap'
import catalogo from '../catalogo.json'
import { usarCarrito } from '../carrito.jsx'
import { foto } from '../componentes/Tarjeta.jsx'
import { Enlace } from '../transicion.jsx'
import { usarSinMovimiento } from '../usarSinMovimiento.js'

function Linea({ item }) {
  const { cambiarCantidad, quitar } = usarCarrito()
  const sinMovimiento = usarSinMovimiento()
  const fila = useRef(null)
  const producto = catalogo.productos[item.producto]
  const variante = producto?.variantes.find((v) => v.id === item.variante)
  if (!variante) return null

  function eliminar() {
    if (sinMovimiento) {
      quitar(item)
      return
    }
    gsap.to(fila.current, { x: -30, autoAlpha: 0, height: 0, paddingBlock: 0, duration: 0.3, ease: 'power2.in', onComplete: () => quitar(item) })
  }

  return (
    <li className="linea-carrito" ref={fila}>
      <img src={foto(item.producto, item.variante)} alt="" width="136" height="88" />
      <div className="linea-datos">
        <h2>{producto.nombre}</h2>
        <p>{variante.nombre} · Talla {item.talla}</p>
        <button type="button" className="quitar" onClick={eliminar}>Quitar</button>
      </div>
      <div className="cantidad">
        <button type="button" aria-label={`Quitar una unidad de ${producto.nombre}`} disabled={item.cantidad === 1} onClick={() => cambiarCantidad(item, item.cantidad - 1)}>−</button>
        <span aria-live="polite">{item.cantidad}</span>
        <button type="button" aria-label={`Agregar una unidad de ${producto.nombre}`} onClick={() => cambiarCantidad(item, item.cantidad + 1)}>+</button>
      </div>
      <p className="subtotal">${item.precio * item.cantidad}</p>
    </li>
  )
}

export default function Carrito() {
  const { items, total, vaciar } = usarCarrito()
  const [comprado, setComprado] = useState(false)

  function simularCompra() {
    vaciar()
    setComprado(true)
  }

  return (
    <div className="contenido estrecho">
      <title>Bolsa | Showroom de zapatos</title>
      <header className="encabezado">
        <p className="linea">Compra simulada</p>
        <h1>Tu bolsa</h1>
      </header>
      {comprado ? (
        <div className="estado" role="status">
          <h2>Compra simulada completada</h2>
          <p>No se hizo ningún cobro ni se enviará ningún pedido. Esta tienda es un proyecto universitario.</p>
          <Enlace className="boton" to="/catalogo">Seguir viendo zapatos</Enlace>
        </div>
      ) : items.length === 0 ? (
        <div className="estado">
          <h2>Tu bolsa está vacía</h2>
          <p>Elige un zapato en la sala o en el catálogo.</p>
          <Enlace className="boton" to="/catalogo">Ir al catálogo</Enlace>
        </div>
      ) : (
        <>
          <ul className="lista-carrito">
            {items.map((item) => <Linea key={`${item.producto}-${item.variante}-${item.talla}`} item={item} />)}
          </ul>
          <div className="resumen">
            <p>Total <strong>${total}</strong></p>
            <button type="button" className="agregar" onClick={simularCompra}>Simular compra</button>
            <p className="simulado">No se pide ningún dato de pago.</p>
          </div>
        </>
      )}
    </div>
  )
}
