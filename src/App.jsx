import { Suspense, lazy, useEffect, useRef } from 'react'
import { BrowserRouter, NavLink, Route, Routes, useLocation } from 'react-router'
import gsap from 'gsap'
import { CarritoProvider, usarCarrito } from './carrito.jsx'
import { Enlace, TransicionProvider, usarTransicion } from './transicion.jsx'
import { usarSinMovimiento } from './usarSinMovimiento.js'
import Inicio from './paginas/Inicio.jsx'

const Catalogo = lazy(() => import('./paginas/Catalogo.jsx'))
const Producto = lazy(() => import('./paginas/Producto.jsx'))
const Carrito = lazy(() => import('./paginas/Carrito.jsx'))
const Nosotros = lazy(() => import('./paginas/Nosotros.jsx'))
const Contacto = lazy(() => import('./paginas/Contacto.jsx'))
const NoEncontrada = lazy(() => import('./paginas/NoEncontrada.jsx'))

const SECCIONES = [['/', 'Sala'], ['/catalogo', 'Catálogo'], ['/nosotros', 'Nosotros'], ['/contacto', 'Contacto']]

function Cabecera() {
  const { unidades } = usarCarrito()
  const { irA } = usarTransicion()
  const sinMovimiento = usarSinMovimiento()
  const contador = useRef(null)
  const previo = useRef(unidades)

  useEffect(() => {
    if (unidades > previo.current && !sinMovimiento) {
      gsap.fromTo(contador.current, { scale: 1.5 }, { scale: 1, duration: 0.5, ease: 'back.out(3)' })
    }
    previo.current = unidades
  }, [unidades, sinMovimiento])

  return (
    <header className="cabecera">
      <Enlace className="marca" to="/">Showroom</Enlace>
      <nav className="secciones" aria-label="Principal">
        {SECCIONES.map(([ruta, nombre]) => (
          <NavLink
            key={ruta}
            to={ruta}
            end
            onClick={(e) => {
              if (e.metaKey || e.ctrlKey || e.shiftKey) return
              e.preventDefault()
              irA(ruta)
            }}
          >
            {nombre}
          </NavLink>
        ))}
      </nav>
      <Enlace className="bolsa" to="/carrito">
        Bolsa <b ref={contador}>{unidades}</b>
        <span className="oculto"> productos</span>
      </Enlace>
    </header>
  )
}

function Paginas() {
  const { pathname } = useLocation()
  const principal = useRef(null)
  const primera = useRef(true)

  useEffect(() => {
    if (primera.current) {
      primera.current = false
      return
    }
    window.scrollTo(0, 0)
    principal.current?.focus({ preventScroll: true })
  }, [pathname])

  const esInicio = pathname === '/'

  return (
    <div className={esInicio ? 'pagina en-sala' : 'pagina'}>
      <Cabecera />
      <main ref={principal} tabIndex={-1}>
        <Suspense fallback={<p className="cargando-pagina">Cargando…</p>}>
          <Routes>
            <Route path="/" element={<Inicio />} />
            <Route path="/catalogo" element={<Catalogo />} />
            <Route path="/producto/:id" element={<Producto />} />
            <Route path="/carrito" element={<Carrito />} />
            <Route path="/nosotros" element={<Nosotros />} />
            <Route path="/contacto" element={<Contacto />} />
            <Route path="*" element={<NoEncontrada />} />
          </Routes>
        </Suspense>
      </main>
      {!esInicio && (
        <footer className="pie">Proyecto universitario sin fines comerciales, sin relación con la marca.</footer>
      )}
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <CarritoProvider>
        <TransicionProvider>
          <Paginas />
        </TransicionProvider>
      </CarritoProvider>
    </BrowserRouter>
  )
}
