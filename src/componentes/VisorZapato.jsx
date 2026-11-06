import { useEffect, useMemo, useRef } from 'react'
import { Canvas, useThree } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { Color } from 'three'
import gsap from 'gsap'

function Zapato({ url, colores, sinMovimiento }) {
  const { scene } = useGLTF(url)
  const gl = useThree((s) => s.gl)
  const invalidate = useThree((s) => s.invalidate)
  const grupo = useRef()
  const primera = useRef(true)

  const materiales = useMemo(() => {
    const m = {}
    scene.traverse((o) => { if (o.isMesh) m[o.material.name] = o.material })
    return m
  }, [scene])

  useEffect(() => {
    const instantaneo = primera.current || sinMovimiento
    primera.current = false
    const tweens = Object.entries(colores).map(([parte, hex]) => {
      const { r, g, b } = new Color(hex)
      return materiales[parte] && gsap.to(materiales[parte].color, {
        r, g, b, duration: instantaneo ? 0 : 0.45, ease: 'power2.out', onUpdate: invalidate,
      })
    })
    return () => tweens.forEach((t) => t?.kill())
  }, [colores, materiales, sinMovimiento, invalidate])

  useEffect(() => {
    const lienzo = gl.domElement
    let previo = null
    const bajar = (e) => { previo = e.clientX }
    const mover = (e) => {
      if (previo === null) return
      grupo.current.rotation.y += (e.clientX - previo) * 0.012
      previo = e.clientX
      invalidate()
    }
    const subir = () => { previo = null }
    lienzo.addEventListener('pointerdown', bajar)
    window.addEventListener('pointermove', mover)
    window.addEventListener('pointerup', subir)
    return () => {
      lienzo.removeEventListener('pointerdown', bajar)
      window.removeEventListener('pointermove', mover)
      window.removeEventListener('pointerup', subir)
    }
  }, [gl, invalidate])

  return (
    <group ref={grupo} rotation={[0, -0.55, 0]}>
      <primitive object={scene} position={[-15, -5, 0]} />
    </group>
  )
}

export default function VisorZapato({ url, colores, sinMovimiento }) {
  return (
    <Canvas flat frameloop="demand" dpr={[1, 1.75]} camera={{ position: [0, 10, 46], fov: 34 }}>
      <ambientLight intensity={1.05} />
      <directionalLight position={[12, 30, 24]} intensity={1.5} />
      <directionalLight position={[-20, 8, -10]} intensity={0.5} />
      <Zapato url={url} colores={colores} sinMovimiento={sinMovimiento} />
    </Canvas>
  )
}
