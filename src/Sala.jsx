import { Suspense, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react'
import { Canvas, useThree } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { CanvasTexture, Color, DoubleSide, Euler, Matrix4, Quaternion, SRGBColorSpace, Vector3 } from 'three'
import gsap from 'gsap'

// Medidas en centimetros, igual que los modelos de Blender.
const MEDIO = 220
const LARGO_ZAPATO = 30
const ESCALA_REPISA = 1.45
const EJE_Y = new Vector3(0, 1, 0)
const PAREDES = [
  { pos: [0, 0, -MEDIO], rot: 0 },
  { pos: [-MEDIO, 0, 0], rot: Math.PI / 2 },
  { pos: [MEDIO, 0, 0], rot: -Math.PI / 2 },
]

function aMundo(pared, x, y, z) {
  return new Vector3(x, y, z).applyAxisAngle(EJE_Y, pared.rot).add(new Vector3(...pared.pos))
}

// En pantallas verticales las repisas se apilan para que quepan.
function distribucion(vertical, cantidad) {
  if (vertical) {
    return { filas: cantidad > 4 ? [52, 100, 148] : [76, 130], columnas: [-29, 29], ancho: 118 }
  }
  return cantidad > 4
    ? { filas: [84, 140], columnas: [-58, 0, 58], ancho: 180 }
    : { filas: [84, 140], columnas: [-40, 40], ancho: 180 }
}

function ranuras(estantes, productos, vertical) {
  return estantes.flatMap((estante, e) =>
    estante.zapatos.map((clave, i) => {
      const { filas, columnas } = distribucion(vertical, estante.zapatos.length)
      const fila = Math.floor(i / columnas.length)
      const x = columnas[i % columnas.length]
      const pared = PAREDES[e]
      return {
        estante: e,
        indice: i,
        base: productos[clave].base,
        colores: productos[clave].variantes[0].colores,
        pos: aMundo(pared, x, filas[fila] + 1.2, 2),
        giro: pared.rot - 0.45,
      }
    }),
  )
}

function estacion(e, cantidad, aspecto, fov) {
  const { ancho } = distribucion(aspecto < 0.8, cantidad)
  const tangente = Math.tan((fov * Math.PI) / 360)
  const distancia = Math.min(400, Math.max(190, (ancho / 2 + 16) / (tangente * aspecto)))
  const pared = PAREDES[e]
  return { pos: aMundo(pared, 0, 128, distancia), mira: aMundo(pared, 0, 122, 0) }
}

const GENERAL = { pos: new Vector3(0, 138, 345), mira: new Vector3(0, 118, -80) }

function Camara({ vista, cantidades, sinMovimiento, intro, alTerminarIntro }) {
  const camera = useThree((s) => s.camera)
  const size = useThree((s) => s.size)
  const invalidate = useThree((s) => s.invalidate)
  const mira = useRef(GENERAL.mira.clone())
  const aspecto = size.width / size.height

  useEffect(() => {
    camera.fov = aspecto < 1 ? 62 : 46
    camera.updateProjectionMatrix()
    invalidate()
  }, [camera, aspecto, invalidate])

  useEffect(() => {
    const fov = aspecto < 1 ? 62 : 46
    const destino = vista.estante === null ? GENERAL : estacion(vista.estante, cantidades[vista.estante], aspecto, fov)
    const aplicar = () => {
      camera.lookAt(mira.current)
      invalidate()
    }
    // Elegir una seccion durante la entrada la cancela.
    if (vista.estante !== null) intro.current = false
    if (sinMovimiento || !intro.current) {
      if (sinMovimiento) {
        camera.position.copy(destino.pos)
        mira.current.copy(destino.mira)
        aplicar()
        intro.current = false
        alTerminarIntro()
        return
      }
      const t = gsap.timeline({ defaults: { duration: 1.5, ease: 'power3.inOut' }, onUpdate: aplicar })
      t.to(camera.position, { x: destino.pos.x, y: destino.pos.y, z: destino.pos.z }, 0)
      t.to(mira.current, { x: destino.mira.x, y: destino.mira.y, z: destino.mira.z }, 0)
      return () => t.kill()
    }
    // Entrada: barre las paredes laterales y termina en la vista general.
    camera.position.set(0, 128, 60)
    mira.current.copy(aMundo(PAREDES[1], 0, 122, 0))
    aplicar()
    const derecha = aMundo(PAREDES[2], 0, 122, 0)
    const t = gsap.timeline({ onUpdate: aplicar, onComplete: () => { intro.current = false; alTerminarIntro() } })
    t.to(mira.current, { x: derecha.x, y: derecha.y, z: derecha.z, duration: 2.2, ease: 'sine.inOut' }, 0.9)
    t.to(mira.current, { x: GENERAL.mira.x, y: GENERAL.mira.y, z: GENERAL.mira.z, duration: 1.5, ease: 'power2.inOut' }, 3.1)
    t.to(camera.position, { x: GENERAL.pos.x, y: GENERAL.pos.y, z: GENERAL.pos.z, duration: 1.5, ease: 'power2.inOut' }, 3.1)
    return () => t.kill()
  }, [vista.estante, cantidades, aspecto, camera, sinMovimiento, invalidate, intro, alTerminarIntro])

  return null
}

function rotulo(texto, claro) {
  const c = document.createElement('canvas')
  c.width = 1024
  c.height = 128
  const x = c.getContext('2d')
  x.font = '800 84px system-ui, sans-serif'
  x.textAlign = 'center'
  x.textBaseline = 'middle'
  x.fillStyle = claro ? '#f3f1ea' : '#141414'
  x.fillText(texto.toUpperCase(), 512, 66)
  const t = new CanvasTexture(c)
  t.colorSpace = SRGBColorSpace
  return t
}

function Estante({ estante, pared, vertical, encendido }) {
  const { filas, ancho } = distribucion(vertical, estante.zapatos.length)
  const textura = useMemo(() => rotulo(estante.nombre, estante.oscuro), [estante])
  return (
    <group position={pared.pos} rotation={[0, pared.rot, 0]}>
      {estante.oscuro && (
        <mesh position={[0, 150, 0.4]}>
          <planeGeometry args={[300, 300]} />
          <meshStandardMaterial color="#1b1b1e" roughness={0.8} />
        </mesh>
      )}
      <mesh position={[0, 190, 1]}>
        <planeGeometry args={[120, 15]} />
        <meshBasicMaterial map={textura} transparent toneMapped={false} />
      </mesh>
      {filas.map((y) => (
        <group key={y} position={[0, y, 0]}>
          <mesh position={[0, -1.6, 19]}>
            <boxGeometry args={[ancho, 3.2, 38]} />
            <meshStandardMaterial color={estante.oscuro ? '#3a3a3f' : '#c9a071'} roughness={0.6} />
          </mesh>
          <mesh position={[0, -3.5, 36]}>
            <boxGeometry args={[ancho - 8, 0.7, 1]} />
            <meshBasicMaterial ref={(m) => { encendido.current[`${estante.id}${y}`] = m }} color="#000" toneMapped={false} />
          </mesh>
        </group>
      ))}
    </group>
  )
}

function Cuarto({ estantes, vertical, alElegirEstante, vista, sinMovimiento, intro }) {
  const invalidate = useThree((s) => s.invalidate)
  const ambiente = useRef()
  const focos = useRef([])
  const franjas = useRef([])
  const leds = useRef({})

  useEffect(() => {
    const aplicar = (niveles) => {
      ambiente.current.intensity = 0.1 + 0.8 * niveles.sala
      estantes.forEach((estante, i) => {
        const n = niveles[`e${i}`]
        focos.current[i].intensity = 1.25 * n
        franjas.current[i].color.set(estante.color).multiplyScalar(n * 1.1)
        Object.entries(leds.current)
          .filter(([k]) => k.startsWith(estante.id))
          .forEach(([, m]) => m?.color.set(estante.color).multiplyScalar(n))
      })
      invalidate()
    }
    const niveles = { sala: 0, e0: 0, e1: 0, e2: 0 }
    if (sinMovimiento || !intro.current) {
      aplicar({ sala: 1, e0: 1, e1: 1, e2: 1 })
      return
    }
    aplicar(niveles)
    const t = gsap.timeline({ onUpdate: () => aplicar(niveles) })
    t.to(niveles, { e1: 1, duration: 0.5, ease: 'power2.out' }, 0.3)
    t.to(niveles, { e0: 1, duration: 0.5, ease: 'power2.out' }, 1.2)
    t.to(niveles, { e2: 1, duration: 0.5, ease: 'power2.out' }, 2.1)
    t.to(niveles, { sala: 1, duration: 1.2, ease: 'power1.inOut' }, 2.6)
    return () => t.kill()
  }, [estantes, invalidate, sinMovimiento, intro])

  const cielo = [
    { pos: [0, 299, -60], tam: [9, 1, 300] },
    { pos: [-110, 299, 90], tam: [210, 1, 9] },
    { pos: [110, 299, 90], tam: [210, 1, 9] },
  ]
  const orden = [0, 1, 2]

  return (
    <>
      <ambientLight ref={ambiente} intensity={0.1} />
      {PAREDES.map((pared, i) => {
        const p = aMundo(pared, 0, 240, 150)
        return (
          <pointLight
            key={i}
            ref={(l) => { focos.current[i] = l }}
            position={p}
            color={estantes[i].color}
            decay={0}
            distance={420}
            intensity={0}
          />
        )
      })}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 100]}>
        <planeGeometry args={[MEDIO * 2, 640]} />
        <meshStandardMaterial color="#cfccc4" roughness={0.45} />
      </mesh>
      <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, 300, 100]}>
        <planeGeometry args={[MEDIO * 2, 640]} />
        <meshStandardMaterial color="#e9e7e1" />
      </mesh>
      <mesh position={[0, 150, -MEDIO]}>
        <planeGeometry args={[MEDIO * 2, 300]} />
        <meshStandardMaterial color="#efece5" />
      </mesh>
      {[-1, 1].map((s) => (
        <mesh key={s} position={[s * MEDIO, 150, 100]} rotation={[0, -s * Math.PI / 2, 0]}>
          <planeGeometry args={[640, 300]} />
          <meshStandardMaterial color="#efece5" />
        </mesh>
      ))}
      {cielo.map((f, i) => (
        <mesh key={i} position={f.pos}>
          <boxGeometry args={f.tam} />
          <meshBasicMaterial ref={(m) => { if (m) franjas.current[orden[i]] = m }} color="#000" toneMapped={false} />
        </mesh>
      ))}
      {estantes.map((estante, i) => (
        <Estante key={estante.id} estante={estante} pared={PAREDES[i]} vertical={vertical} encendido={leds} />
      ))}
      {vista.estante === null && PAREDES.map((pared, i) => (
        <mesh
          key={i}
          position={aMundo(pared, 0, 130, 3)}
          rotation={[0, pared.rot, 0]}
          onClick={(e) => { e.stopPropagation(); alElegirEstante(i) }}
          onPointerOver={() => { document.body.style.cursor = 'pointer' }}
          onPointerOut={() => { document.body.style.cursor = '' }}
        >
          <planeGeometry args={[300, 240]} />
          <meshBasicMaterial transparent opacity={0} depthWrite={false} />
        </mesh>
      ))}
    </>
  )
}

const matriz = new Matrix4()
const compuesta = new Matrix4()
const giroQ = new Quaternion()
const centro = new Matrix4().makeTranslation(-LARGO_ZAPATO / 2, 0, 0)

function matrizDe(r, escala, alza) {
  giroQ.setFromEuler(new Euler(0, r.giro, 0))
  const p = r.pos.clone()
  p.y += alza
  matriz.compose(p, giroQ, new Vector3(escala, escala, escala)).multiply(centro)
  return matriz
}

function sombraSuave() {
  const c = document.createElement('canvas')
  c.width = c.height = 128
  const x = c.getContext('2d')
  const g = x.createRadialGradient(64, 64, 8, 64, 64, 64)
  g.addColorStop(0, 'rgba(0,0,0,.5)')
  g.addColorStop(1, 'rgba(0,0,0,0)')
  x.fillStyle = g
  x.fillRect(0, 0, 128, 128)
  return new CanvasTexture(c)
}

// Cada modelo se dibuja con una InstancedMesh por parte, en todas sus repisas.
function Repisas({ base, slots, oculto, vista, alElegir }) {
  const { scene } = useGLTF(`/modelos/${base}-repisa.glb`)
  const invalidate = useThree((s) => s.invalidate)
  const refs = useRef({})
  const realce = useRef(slots.map(() => ({ n: 0 })))
  const sombras = useRef()
  const texturaSombra = useMemo(sombraSuave, [])

  const partes = useMemo(() => {
    const lista = []
    scene.updateMatrixWorld(true)
    scene.traverse((o) => {
      if (o.isMesh) {
        const material = o.material.clone()
        material.color.set('#fff')
        // La compresion guarda la escala en el nodo, no en los vertices.
        lista.push({ nombre: o.material.name, geometria: o.geometry, material, local: o.matrixWorld.clone() })
      }
    })
    return lista
  }, [scene])

  const dibujar = (i) => {
    const r = slots[i]
    const n = realce.current[i]?.n ?? 0
    const escala = i === oculto ? 0 : ESCALA_REPISA * (1 + 0.08 * n)
    const m = matrizDe(r, escala, 2 * n)
    partes.forEach((p) => {
      const instancia = refs.current[p.nombre]
      if (!instancia) return
      instancia.setMatrixAt(i, compuesta.multiplyMatrices(m, p.local))
      instancia.instanceMatrix.needsUpdate = true
    })
    const piso = sombras.current
    if (piso) {
      giroQ.setFromEuler(new Euler(-Math.PI / 2, 0, -r.giro, 'YXZ'))
      const e = i === oculto ? 0 : 1
      piso.setMatrixAt(i, matriz.compose(r.pos.clone().setY(r.pos.y + 0.15), giroQ, new Vector3(e * 58, e * 26, 1)))
      piso.instanceMatrix.needsUpdate = true
    }
  }

  useLayoutEffect(() => {
    const color = new Color()
    partes.forEach((p) => {
      const instancia = refs.current[p.nombre]
      slots.forEach((r, i) => {
        instancia.setColorAt(i, color.set(r.colores[p.nombre]))
      })
      instancia.instanceColor.needsUpdate = true
      instancia.computeBoundingSphere()
    })
    slots.forEach((_, i) => dibujar(i))
    invalidate()
  }, [partes, slots, oculto])

  const resaltar = (i, n) => {
    gsap.to(realce.current[i], {
      n,
      duration: 0.25,
      ease: 'power2.out',
      onUpdate: () => { dibujar(i); invalidate() },
    })
  }

  return (
    <>
      {partes.map((p) => (
        <instancedMesh
          key={p.nombre}
          ref={(m) => { refs.current[p.nombre] = m }}
          args={[p.geometria, p.material, slots.length]}
          frustumCulled={false}
          raycast={() => null}
        />
      ))}
      <instancedMesh ref={sombras} args={[undefined, undefined, slots.length]} frustumCulled={false} raycast={() => null}>
        <planeGeometry />
        <meshBasicMaterial map={texturaSombra} transparent depthWrite={false} toneMapped={false} />
      </instancedMesh>
      {slots.map((r, i) => (
        r.estante === vista.estante && vista.ranura === null && (
          <mesh
            key={i}
            position={[r.pos.x, r.pos.y + 10, r.pos.z]}
            rotation={[0, r.giro, 0]}
            onClick={(e) => { e.stopPropagation(); document.body.style.cursor = ''; alElegir(r.indice) }}
            onPointerOver={(e) => { e.stopPropagation(); resaltar(i, 1); document.body.style.cursor = 'pointer' }}
            onPointerOut={() => { resaltar(i, 0); document.body.style.cursor = '' }}
          >
            <boxGeometry args={[48, 22, 20]} />
            <meshBasicMaterial transparent opacity={0} depthWrite={false} />
          </mesh>
        )
      ))}
    </>
  )
}

function Detalle({ url, ranura, colores, abierto, sinMovimiento, alCerrar }) {
  const { scene } = useGLTF(url)
  const camera = useThree((s) => s.camera)
  const gl = useThree((s) => s.gl)
  const size = useThree((s) => s.size)
  const invalidate = useThree((s) => s.invalidate)
  const grupo = useRef()
  const velo = useRef()
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

  useLayoutEffect(() => {
    const vertical = size.width / size.height < 1
    const frente = camera.getWorldDirection(new Vector3())
    const lado = new Vector3().crossVectors(frente, camera.up).normalize()
    const arriba = new Vector3().crossVectors(lado, frente)
    const destino = camera.position.clone()
      .addScaledVector(frente, vertical ? 82 : 60)
      .addScaledVector(lado, vertical ? 0 : -11)
      .addScaledVector(arriba, vertical ? 20 : 0)
    const velado = camera.position.clone().addScaledVector(frente, 92)
    velo.current.position.copy(velado)
    velo.current.quaternion.copy(camera.quaternion)
    const g = grupo.current
    const duracion = sinMovimiento ? 0 : 0.9
    const miraAl = Math.atan2(-frente.x, -frente.z) - 0.55
    const t = gsap.timeline({ onUpdate: invalidate })
    if (abierto) {
      g.position.copy(ranura.pos)
      g.rotation.y = ranura.giro
      g.scale.setScalar(ESCALA_REPISA)
      t.to(g.scale, { x: 1, y: 1, z: 1, duration: duracion, ease: 'power3.inOut' }, 0)
      t.to(g.position, { x: destino.x, y: destino.y - 5, z: destino.z, duration: duracion, ease: 'power3.inOut' }, 0)
      t.to(g.rotation, { y: miraAl, duration: duracion, ease: 'power3.inOut' }, 0)
      t.to(velo.current.material, { opacity: 0.62, duration: duracion * 0.8 }, 0)
    } else {
      t.to(g.position, { x: ranura.pos.x, y: ranura.pos.y, z: ranura.pos.z, duration: duracion * 0.8, ease: 'power3.inOut' }, 0)
      t.to(g.rotation, { y: ranura.giro, duration: duracion * 0.8, ease: 'power3.inOut' }, 0)
      t.to(g.scale, { x: ESCALA_REPISA, y: ESCALA_REPISA, z: ESCALA_REPISA, duration: duracion * 0.8, ease: 'power3.inOut' }, 0)
      t.to(velo.current.material, { opacity: 0, duration: duracion * 0.6 }, 0)
      t.eventCallback('onComplete', alCerrar)
    }
    return () => t.kill()
  }, [abierto, ranura, camera, size, sinMovimiento, invalidate, alCerrar])

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
    <>
      <mesh ref={velo} renderOrder={1}>
        <planeGeometry args={[900, 900]} />
        <meshBasicMaterial color="#0d0d0f" transparent opacity={0} side={DoubleSide} depthWrite={false} />
      </mesh>
      <group ref={grupo}>
        <directionalLight position={[10, 40, 30]} intensity={1.1} />
        <primitive object={scene} position={[-LARGO_ZAPATO / 2, 0, 0]} />
      </group>
    </>
  )
}

export default function Sala({ catalogo, vista, producto, colores, abierto, sinMovimiento, alElegirEstante, alElegirRanura, alCerrar, alListo }) {
  const [vertical, setVertical] = useState(() => window.innerWidth / window.innerHeight < 0.8)
  const intro = useRef(!sinMovimiento)
  const { estantes, productos } = catalogo
  const cantidades = useMemo(() => estantes.map((e) => e.zapatos.length), [estantes])
  const slots = useMemo(() => ranuras(estantes, productos, vertical), [estantes, productos, vertical])
  const grupos = useMemo(() => {
    const porBase = {}
    slots.forEach((r) => { (porBase[r.base] ??= []).push(r) })
    return Object.entries(porBase)
  }, [slots])
  const elegida = vista.ranura === null ? null : slots.find((r) => r.estante === vista.estante && r.indice === vista.ranura)

  useEffect(() => {
    const medir = () => setVertical(window.innerWidth / window.innerHeight < 0.8)
    window.addEventListener('resize', medir)
    return () => window.removeEventListener('resize', medir)
  }, [])

  useEffect(() => {
    if (vista.estante === null) return
    slots.filter((r) => r.estante === vista.estante).forEach((r) => useGLTF.preload(`/modelos/${r.base}.glb`))
  }, [vista.estante, slots])

  return (
    <Canvas
      flat
      frameloop="demand"
      dpr={[1, 1.75]}
      camera={{ position: GENERAL.pos.toArray(), fov: 46, near: 4, far: 1400 }}
      gl={{ antialias: true, powerPreference: 'high-performance' }}
    >
      <color attach="background" args={['#0b0b0c']} />
      <Camara vista={vista} cantidades={cantidades} sinMovimiento={sinMovimiento} intro={intro} alTerminarIntro={alListo} />
      <Cuarto
        estantes={estantes}
        vertical={vertical}
        vista={vista}
        alElegirEstante={alElegirEstante}
        sinMovimiento={sinMovimiento}
        intro={intro}
      />
      {grupos.map(([base, lista]) => (
        <Suspense key={base} fallback={null}>
          <Repisas
            base={base}
            slots={lista}
            oculto={elegida ? lista.indexOf(elegida) : -1}
            vista={vista}
            alElegir={alElegirRanura}
          />
        </Suspense>
      ))}
      <Suspense fallback={null}>
        {elegida && producto && (
          <Detalle
            key={`${elegida.estante}-${elegida.indice}`}
            url={`/modelos/${producto.base}.glb`}
            ranura={elegida}
            colores={colores}
            abierto={abierto}
            sinMovimiento={sinMovimiento}
            alCerrar={alCerrar}
          />
        )}
      </Suspense>
    </Canvas>
  )
}
