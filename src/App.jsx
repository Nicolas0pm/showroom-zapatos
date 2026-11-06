import { Suspense, lazy, useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import catalogo from './catalogo.json'
import Panel from './Panel.jsx'

const Sala = lazy(() => import('./Sala.jsx'))
const CLAVE_CARRITO = 'showroom-carrito'
const SIN_SELECCION = { estante: null, ranura: null }

function leerCarrito() {
  try {
    return JSON.parse(localStorage.getItem(CLAVE_CARRITO)) ?? []
  } catch {
    return []
  }
}

function guardarCarrito(carrito) {
  try {
    localStorage.setItem(CLAVE_CARRITO, JSON.stringify(carrito))
  } catch {
    // Sin almacenamiento el carrito dura solo esta visita.
  }
}

function usarSinMovimiento() {
  const [activo, setActivo] = useState(
    () => window.matchMedia('(prefers-reduced-motion: reduce)').matches,
  )
  useEffect(() => {
    const consulta = window.matchMedia('(prefers-reduced-motion: reduce)')
    const cambiar = (e) => setActivo(e.matches)
    consulta.addEventListener('change', cambiar)
    return () => consulta.removeEventListener('change', cambiar)
  }, [])
  return activo
}

export default function App() {
  const sinMovimiento = usarSinMovimiento()
  // En celular la sala 3D se carga al entrar, para no gastar datos sin pedirlo.
  const [dentro, setDentro] = useState(() => window.matchMedia('(min-width: 861px)').matches)
  const [vista, setVista] = useState(SIN_SELECCION)
  const [abierto, setAbierto] = useState(false)
  const [clave, setClave] = useState(null)
  const [variante, setVariante] = useState(null)
  const [carrito, setCarrito] = useState(leerCarrito)
  const contador = useRef(null)
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

  function agregar(item) {
    const nuevo = [...carrito, item]
    setCarrito(nuevo)
    guardarCarrito(nuevo)
    if (!sinMovimiento) {
      gsap.fromTo(contador.current, { scale: 1.5 }, { scale: 1, duration: 0.5, ease: 'back.out(3)' })
    }
  }

  const estante = vista.estante === null ? null : catalogo.estantes[vista.estante]
  const producto = clave ? catalogo.productos[clave] : null

  return (
    <div className="pagina">
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

      <header className="cabecera">
        <span className="marca">Showroom</span>
        <span className="bolsa">
          Bolsa <b ref={contador}>{carrito.length}</b>
          <span className="oculto"> productos</span>
        </span>
      </header>

      {!dentro && (
        <main className="portada">
          <p className="linea">Showroom virtual</p>
          <h1>Entra a la sala</h1>
          <p>Recorre las estanterías y gira cada zapato en 3D.</p>
          <button type="button" className="agregar" onClick={() => setDentro(true)}>Entrar a la sala</button>
        </main>
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
              <button type="button" onClick={() => elegirRanura(i)}>
                {catalogo.productos[id].nombre}
              </button>
            </li>
          ))}
        </ul>
      )}

      <footer className="pie">Proyecto universitario sin fines comerciales, sin relación con la marca.</footer>

      {abierto && (
        <Panel
          key={`${vista.estante}-${vista.ranura}`}
          ref={panel}
          clave={clave}
          producto={producto}
          estante={estante.nombre}
          variante={variante}
          sinMovimiento={sinMovimiento}
          alCambiar={setVariante}
          alAgregar={agregar}
          alCerrar={cerrarDetalle}
        />
      )}
    </div>
  )
}
