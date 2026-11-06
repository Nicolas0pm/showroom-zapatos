import { Suspense, lazy, useEffect, useRef, useState } from 'react'
import { useParams } from 'react-router'
import catalogo from '../catalogo.json'
import Opciones from '../componentes/Opciones.jsx'
import Tarjeta, { foto } from '../componentes/Tarjeta.jsx'
import { Enlace } from '../transicion.jsx'
import { usarAparicion } from '../aparicion.js'
import { usarSinMovimiento } from '../usarSinMovimiento.js'
import NoEncontrada from './NoEncontrada.jsx'

const VisorZapato = lazy(() => import('../componentes/VisorZapato.jsx'))

function Contenido({ clave, producto }) {
  const sinMovimiento = usarSinMovimiento()
  const [variante, setVariante] = useState(producto.variantes[0])
  const [en3d, setEn3d] = useState(false)
  const raiz = useRef(null)
  usarAparicion(raiz, clave)

  const estante = catalogo.estantes.find((e) => e.zapatos.includes(clave))
  const relacionados = estante.zapatos.filter((id) => id !== clave).slice(0, 3)

  return (
    <div className="contenido" ref={raiz}>
      <title>{`${producto.nombre} | Showroom de zapatos`}</title>
      <Enlace className="volver" to="/catalogo">← Volver al catálogo</Enlace>
      <div className="ficha">
        <div className="vitrina">
          {en3d ? (
            <Suspense fallback={<p className="cargando-3d">Cargando modelo…</p>}>
              <VisorZapato url={`/modelos/${producto.base}.glb`} colores={variante.colores} sinMovimiento={sinMovimiento} />
              <p className="ayuda">Arrastra para girar</p>
            </Suspense>
          ) : (
            <>
              <img
                src={foto(clave, variante.id)}
                alt={`${producto.nombre}, ${variante.nombre}`}
                width="680"
                height="440"
                fetchPriority="high"
              />
              <button type="button" className="ver-3d" onClick={() => setEn3d(true)}>Ver en 3D</button>
            </>
          )}
        </div>
        <div className="datos">
          <p className="linea">{estante.nombre}</p>
          <h1>{producto.nombre}</h1>
          <p className="descripcion">{producto.descripcion}</p>
          <Opciones clave={clave} producto={producto} variante={variante} alCambiar={setVariante} />
        </div>
      </div>
      <section className="relacionados">
        <h2 className="aparece">También en {estante.nombre}</h2>
        <ul className="rejilla">
          {relacionados.map((id) => <Tarjeta key={id} clave={id} producto={catalogo.productos[id]} />)}
        </ul>
      </section>
    </div>
  )
}

export default function Producto() {
  const { id } = useParams()
  const producto = catalogo.productos[id]
  useEffect(() => { window.scrollTo(0, 0) }, [id])
  if (!producto) return <NoEncontrada />
  return <Contenido key={id} clave={id} producto={producto} />
}
