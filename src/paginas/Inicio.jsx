import { Suspense, lazy, useCallback, useLayoutEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import catalogo from '../catalogo.json'
import Panel from '../componentes/Panel.jsx'
import { usarSinMovimiento } from '../usarSinMovimiento.js'

const Sala = lazy(() => import('../Sala.jsx'))
const SIN_SELECCION = { estante: null, ranura: null }

export default function Inicio() {
  const sinMovimiento = usarSinMovimiento()
  // En celular la sala 3D se carga al entrar, para no gastar datos sin pedirlo.
  const [dentro, setDentro] = useState(() => window.matchMedia('(min-width: 861px)').matches)
  const [vista, setVista] = useState(SIN_SELECCION)
  const [abierto, setAbierto] = useState(false)
  const [clave, setClave] = useState(null)
  const [variante, setVariante] = useState(null)
  const panel = useRef(null)

  const irAEstante = useCallback((estante) => {
    setAbierto(false)
    setVista({ estante, ranura: null })
  }, [])

  const elegirRanura = useCallback((ranura) => {
    setVista((v) => {
      const id = catalogo.estantes[v.estante].zapatos[ranura]
      setClave(id)
      setVariante(catalogo.productos[id].variantes[0])
      return { ...v, ranura }
    })
    setAbierto(true)
  }, [])

  const cerrarDetalle = useCallback(() => setAbierto(false), [])
  const detalleCerrado = useCallback(() => setVista((v) => ({ ...v, ranura: null })), [])
  const alListo = useCallback(() => {}, [])

  useLayoutEffect(() => {
    if (!abierto || sinMovimiento || !panel.current) return
    const entrada = gsap.fromTo(
      panel.current,
      { y: 24, autoAlpha: 0 },
      { y: 0, autoAlpha: 1, duration: 0.6, ease: 'power3.out', delay: 0.35 },
    )
    return () => entrada.revert()
  }, [abierto, sinMovimiento])

  const estante = vista.estante === null ? null : catalogo.estantes[vista.estante]
  const producto = clave ? catalogo.productos[clave] : null

  return (
    <div className="inicio">
      <title>Showroom de zapatos</title>
      <div className="lienzo">
        {dentro && (
          <Suspense fallback={<p className="cargando">Preparando la sala…</p>}>
            <Sala
              catalogo={catalogo}
              vista={vista}
              producto={producto}
              colores={variante?.colores}
              abierto={abierto}
              sinMovimiento={sinMovimiento}
              alElegirEstante={irAEstante}
              alElegirRanura={elegirRanura}
              alCerrar={detalleCerrado}
              alListo={alListo}
            />
          </Suspense>
        )}
      </div>

      {!dentro && (
        <div className="portada">
          <p className="linea">Showroom virtual</p>
          <h1>Entra a la sala</h1>
          <p>Recorre las estanterías y gira cada zapato en 3D.</p>
          <button type="button" className="agregar" onClick={() => setDentro(true)}>Entrar a la sala</button>
        </div>
      )}

      {dentro && (
        <nav className="menu" aria-label="Secciones de la sala">
          <button type="button" aria-pressed={vista.estante === null} onClick={() => { setAbierto(false); setVista(SIN_SELECCION) }}>Sala</button>
          {catalogo.estantes.map((e, i) => (
            <button key={e.id} type="button" aria-pressed={vista.estante === i} onClick={() => irAEstante(i)}>{e.nombre}</button>
          ))}
        </nav>
      )}

      {estante && vista.ranura === null && (
        <ul className="lista-teclado" aria-label={`Zapatos de ${estante.nombre}`}>
          {estante.zapatos.map((id, i) => (
            <li key={id}>
              <button type="button" onClick={() => elegirRanura(i)}>{catalogo.productos[id].nombre}</button>
            </li>
          ))}
        </ul>
      )}

      <p className="aviso-sala">Proyecto universitario sin fines comerciales, sin relación con la marca.</p>

      {abierto && (
        <Panel
          key={`${vista.estante}-${vista.ranura}`}
          ref={panel}
          clave={clave}
          producto={producto}
          estante={estante.nombre}
          variante={variante}
          alCambiar={setVariante}
          alCerrar={cerrarDetalle}
        />
      )}
    </div>
  )
}
