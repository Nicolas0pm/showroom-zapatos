import { useLayoutEffect } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { usarSinMovimiento } from './usarSinMovimiento.js'

gsap.registerPlugin(ScrollTrigger)

// Los elementos .aparece suben y se revelan al entrar en pantalla.
export function usarAparicion(raiz, dependencia) {
  const sinMovimiento = usarSinMovimiento()
  useLayoutEffect(() => {
    if (sinMovimiento) return
    const contexto = gsap.context(() => {
      gsap.set('.aparece', { y: 28, autoAlpha: 0 })
      ScrollTrigger.batch('.aparece', {
        start: 'top 92%',
        once: true,
        onEnter: (lote) => gsap.to(lote, { y: 0, autoAlpha: 1, duration: 0.6, ease: 'power3.out', stagger: 0.07 }),
      })
    }, raiz)
    return () => contexto.revert()
  }, [raiz, sinMovimiento, dependencia])
}
