import { useEffect, useState } from 'react'

export function usarSinMovimiento() {
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
