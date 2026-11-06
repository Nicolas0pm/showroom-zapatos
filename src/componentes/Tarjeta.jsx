import { Enlace } from '../transicion.jsx'

export const foto = (clave, variante) => `/fotos/${clave}-${variante}.webp`

export default function Tarjeta({ clave, producto, prioridad }) {
  const desde = Math.min(...producto.variantes.map((v) => v.precio))
  return (
    <li className="tarjeta aparece">
      <Enlace to={`/producto/${clave}`}>
        <img
          src={foto(clave, 0)}
          alt={`${producto.nombre}, ${producto.variantes[0].nombre}`}
          width="680"
          height="440"
          loading={prioridad ? 'eager' : 'lazy'}
          fetchPriority={prioridad ? 'high' : 'auto'}
        />
        <h2>{producto.nombre}</h2>
        <p>Desde ${desde} · {producto.variantes.length} colores</p>
      </Enlace>
    </li>
  )
}
