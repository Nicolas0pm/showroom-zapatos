import { useRef } from 'react'
import { useSearchParams } from 'react-router'
import catalogo from '../catalogo.json'
import Tarjeta from '../componentes/Tarjeta.jsx'
import { usarAparicion } from '../aparicion.js'

const TODOS = Object.keys(catalogo.productos)

export default function Catalogo() {
  const [parametros, setParametros] = useSearchParams()
  const filtro = parametros.get('estante')
  const estante = catalogo.estantes.find((e) => e.id === filtro)
  const claves = estante ? estante.zapatos : TODOS
  const raiz = useRef(null)
  usarAparicion(raiz, filtro)

  return (
    <div className="contenido" ref={raiz}>
      <title>Catálogo | Showroom de zapatos</title>
      <header className="encabezado">
        <p className="linea">Catálogo</p>
        <h1>{estante ? estante.nombre : 'Todos los zapatos'}</h1>
      </header>
      <div className="filtros" role="group" aria-label="Filtrar por estantería">
        <button type="button" aria-pressed={!estante} onClick={() => setParametros({})}>Todos</button>
        {catalogo.estantes.map((e) => (
          <button key={e.id} type="button" aria-pressed={filtro === e.id} onClick={() => setParametros({ estante: e.id })}>
            {e.nombre}
          </button>
        ))}
      </div>
      <p className="oculto" aria-live="polite">{claves.length} productos</p>
      <ul className="rejilla">
        {claves.map((clave, i) => (
          <Tarjeta key={clave} clave={clave} producto={catalogo.productos[clave]} prioridad={i < 2} />
        ))}
      </ul>
    </div>
  )
}
