import { createContext, useCallback, useContext, useMemo, useRef } from 'react'
import { Link, useNavigate } from 'react-router'
import gsap from 'gsap'
import { usarSinMovimiento } from './usarSinMovimiento.js'

const Contexto = createContext(null)

// Tres franjas diagonales cubren la pantalla, cambia la pagina y se retiran.
export function TransicionProvider({ children }) {
  const navegar = useNavigate()
  const sinMovimiento = usarSinMovimiento()
  const velo = useRef(null)
  const activa = useRef(false)

  const irA = useCallback((ruta) => {
    if (sinMovimiento) {
      navegar(ruta)
      return
    }
    if (activa.current) return
    activa.current = true
    const franjas = velo.current.children
    gsap.timeline({ onComplete: () => { activa.current = false } })
      .set(velo.current, { autoAlpha: 1 })
      .fromTo(franjas, { yPercent: 115 }, { yPercent: 0, duration: 0.38, ease: 'power3.in', stagger: 0.06 })
      .add(() => navegar(ruta))
      .to(franjas, { yPercent: -115, duration: 0.42, ease: 'power3.out', stagger: 0.06 }, '+=0.06')
      .set(velo.current, { autoAlpha: 0 })
  }, [navegar, sinMovimiento])

  const valor = useMemo(() => ({ irA }), [irA])

  return (
    <Contexto.Provider value={valor}>
      {children}
      <div className="velo" ref={velo} aria-hidden="true">
        <span /><span /><span />
      </div>
    </Contexto.Provider>
  )
}

export const usarTransicion = () => useContext(Contexto)

export function Enlace({ to, onClick, ...props }) {
  const { irA } = usarTransicion()
  return (
    <Link
      to={to}
      {...props}
      onClick={(e) => {
        onClick?.(e)
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return
        e.preventDefault()
        irA(to)
      }}
    />
  )
}
