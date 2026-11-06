import { Enlace } from '../transicion.jsx'

export default function NoEncontrada() {
  return (
    <div className="contenido estrecho">
      <title>Página no encontrada | Showroom de zapatos</title>
      <div className="estado">
        <h1>Esta página no existe</h1>
        <Enlace className="boton" to="/">Volver a la sala</Enlace>
      </div>
    </div>
  )
}
