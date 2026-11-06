import { forwardRef } from 'react'
import Opciones from './Opciones.jsx'
import { Enlace } from '../transicion.jsx'

const Panel = forwardRef(function Panel({ clave, producto, estante, variante, alCambiar, alCerrar }, ref) {
  return (
    <aside className="panel" ref={ref}>
      <button type="button" className="cerrar" aria-label="Volver a la estantería" onClick={alCerrar}>×</button>
      <p className="linea">{estante}</p>
      <h1>{producto.nombre}</h1>
      <Opciones clave={clave} producto={producto} variante={variante} alCambiar={alCambiar} />
      <Enlace className="enlace-detalle" to={`/producto/${clave}`}>Ver detalle completo</Enlace>
    </aside>
  )
})

export default Panel
