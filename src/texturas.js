// Texturas de la sala urbana, dibujadas en canvas al cargar: no se descarga ninguna imagen.
import { CanvasTexture, RepeatWrapping, SRGBColorSpace } from 'three'

// Numeros pseudoaleatorios con semilla, para que la sala se vea igual en cada visita.
function azar(semilla) {
  let s = semilla >>> 0
  return () => {
    s = (s + 0x6d2b79f5) >>> 0
    let t = Math.imul(s ^ (s >>> 15), 1 | s)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

function lienzo(ancho, alto) {
  const c = document.createElement('canvas')
  c.width = ancho
  c.height = alto
  return [c, c.getContext('2d')]
}

function textura(c, repetir = [1, 1]) {
  const t = new CanvasTexture(c)
  t.colorSpace = SRGBColorSpace
  t.wrapS = t.wrapT = RepeatWrapping
  t.repeat.set(...repetir)
  t.anisotropy = 4
  return t
}

function grano(x, ancho, alto, r, cantidad, tono) {
  for (let i = 0; i < cantidad; i++) {
    x.fillStyle = `rgba(${tono},${0.03 + r() * 0.07})`
    x.fillRect(r() * ancho, r() * alto, 1 + r() * 3, 1 + r() * 3)
  }
}

export function ladrillo(repetir, oscuro = false) {
  const [c, x] = lienzo(512, 512)
  const r = azar(oscuro ? 7 : 3)
  x.fillStyle = oscuro ? '#1c1c1f' : '#8f8a82'
  x.fillRect(0, 0, 512, 512)
  const alto = 32
  const largo = 96
  for (let fila = 0; fila < 512 / alto; fila++) {
    const corrido = fila % 2 ? largo / 2 : 0
    for (let col = -1; col < 512 / largo + 1; col++) {
      const tono = oscuro ? 34 + r() * 16 : 0
      x.fillStyle = oscuro
        ? `rgb(${tono},${tono},${tono + 3})`
        : `hsl(${10 + r() * 14}, ${38 + r() * 18}%, ${30 + r() * 12}%)`
      x.fillRect(col * largo + corrido + 3, fila * alto + 3, largo - 6, alto - 6)
    }
  }
  grano(x, 512, 512, r, 2600, oscuro ? '255,255,255' : '0,0,0')
  return textura(c, repetir)
}

export function concreto(repetir, base = '#9a9893') {
  const [c, x] = lienzo(512, 512)
  const r = azar(11)
  x.fillStyle = base
  x.fillRect(0, 0, 512, 512)
  for (let i = 0; i < 70; i++) {
    const g = x.createRadialGradient(r() * 512, r() * 512, 0, r() * 512, r() * 512, 40 + r() * 120)
    g.addColorStop(0, `rgba(0,0,0,${r() * 0.06})`)
    g.addColorStop(1, 'rgba(0,0,0,0)')
    x.fillStyle = g
    x.fillRect(0, 0, 512, 512)
  }
  grano(x, 512, 512, r, 5000, '0,0,0')
  grano(x, 512, 512, r, 2000, '255,255,255')
  return textura(c, repetir)
}

// Mural con letras de burbuja, manchas y chorreados. Todo original.
export function grafiti() {
  const [c, x] = lienzo(1024, 512)
  const r = azar(23)
  x.drawImage(concreto([1, 1], '#8e8c87').image, 0, 0, 1024, 512)
  const colores = ['#ff3d7f', '#2ec4ff', '#ffd23f', '#7cff6b', '#9b5cff', '#ff7a2e']
  for (let i = 0; i < 9; i++) {
    const cx = 60 + r() * 900
    const cy = 120 + r() * 300
    const rad = 50 + r() * 90
    x.beginPath()
    for (let a = 0; a <= Math.PI * 2 + 0.01; a += Math.PI / 6) {
      const d = rad * (0.7 + r() * 0.5)
      x.lineTo(cx + Math.cos(a) * d * 1.4, cy + Math.sin(a) * d)
    }
    x.closePath()
    const color = colores[i % colores.length]
    x.fillStyle = color
    x.globalAlpha = 0.85
    x.fill()
    x.globalAlpha = 1
    x.lineWidth = 7
    x.strokeStyle = '#111'
    x.stroke()
    x.strokeStyle = color
    x.lineWidth = 4
    for (let k = 0; k < 4; k++) {
      const gx = cx - rad + r() * rad * 2
      x.beginPath()
      x.moveTo(gx, cy + rad * 0.5)
      x.lineTo(gx, cy + rad * 0.5 + 30 + r() * 90)
      x.stroke()
    }
  }
  x.font = '900 190px Impact, "Arial Black", system-ui, sans-serif'
  x.textAlign = 'center'
  x.textBaseline = 'middle'
  x.lineJoin = 'round'
  x.save()
  x.translate(512, 250)
  x.rotate(-0.08)
  x.lineWidth = 34
  x.strokeStyle = '#111'
  x.strokeText('CALLE', 8, 10)
  const g = x.createLinearGradient(0, -90, 0, 90)
  g.addColorStop(0, '#ffd23f')
  g.addColorStop(0.5, '#ff3d7f')
  g.addColorStop(1, '#9b5cff')
  x.lineWidth = 18
  x.strokeStyle = '#fff'
  x.strokeText('CALLE', 0, 0)
  x.fillStyle = g
  x.fillText('CALLE', 0, 0)
  x.restore()
  x.strokeStyle = '#111'
  x.lineWidth = 5
  for (let i = 0; i < 6; i++) {
    x.beginPath()
    let px = r() * 1000
    let py = 40 + r() * 440
    x.moveTo(px, py)
    for (let k = 0; k < 5; k++) {
      px += 20 + r() * 40
      py += (r() - 0.5) * 50
      x.quadraticCurveTo(px - 10, py - 40 * r(), px, py)
    }
    x.stroke()
  }
  return textura(c)
}

// Piso de concreto pulido con lineas de cancha pintadas.
export function piso(ancho, largo) {
  const escala = 2
  const [c, x] = lienzo(ancho * escala, largo * escala)
  const r = azar(5)
  const base = concreto([1, 1], '#6f6d69').image
  for (let i = 0; i < c.width; i += 512) {
    for (let j = 0; j < c.height; j += 512) x.drawImage(base, i, j)
  }
  x.strokeStyle = 'rgba(255,255,255,0.75)'
  x.lineWidth = 5 * escala
  const cx = c.width / 2
  // la pared del fondo queda arriba del lienzo
  x.beginPath()
  x.arc(cx, 0, 150 * escala, 0, Math.PI)
  x.stroke()
  x.strokeRect(cx - 50 * escala, 0, 100 * escala, 190 * escala)
  x.beginPath()
  x.arc(cx, 190 * escala, 50 * escala, 0, Math.PI)
  x.stroke()
  x.beginPath()
  x.arc(cx, c.height * 0.72, 60 * escala, 0, Math.PI * 2)
  x.stroke()
  x.strokeStyle = 'rgba(255,196,40,0.8)'
  x.lineWidth = 8 * escala
  x.setLineDash([30 * escala, 22 * escala])
  x.beginPath()
  x.moveTo(30 * escala, c.height)
  x.lineTo(30 * escala, 40 * escala)
  x.moveTo(c.width - 30 * escala, c.height)
  x.lineTo(c.width - 30 * escala, 40 * escala)
  x.stroke()
  x.setLineDash([])
  for (let i = 0; i < 14; i++) {
    x.strokeStyle = 'rgba(20,20,20,0.35)'
    x.lineWidth = 1.5
    x.beginPath()
    let px = r() * c.width
    let py = r() * c.height
    x.moveTo(px, py)
    for (let k = 0; k < 8; k++) {
      px += (r() - 0.5) * 60
      py += (r() - 0.3) * 50
      x.lineTo(px, py)
    }
    x.stroke()
  }
  return textura(c)
}

// Letrero de neon: tubo blanco con halo de color.
export function neon(texto, color, ancho = 1024, alto = 160) {
  const [c, x] = lienzo(ancho, alto)
  x.font = `600 ${alto * 0.5}px "Trebuchet MS", "Segoe UI", system-ui, sans-serif`
  x.textAlign = 'center'
  x.textBaseline = 'middle'
  x.shadowColor = color
  for (const [blur, ancho2] of [[38, 10], [18, 7], [6, 4]]) {
    x.shadowBlur = blur
    x.lineWidth = ancho2
    x.strokeStyle = color
    x.strokeText(texto, ancho / 2, alto / 2)
  }
  x.shadowBlur = 4
  x.lineWidth = 2.2
  x.strokeStyle = '#fff'
  x.strokeText(texto, ancho / 2, alto / 2)
  return textura(c)
}

export function reja() {
  const [c, x] = lienzo(256, 256)
  x.strokeStyle = '#b9bcc2'
  x.lineWidth = 3
  for (let i = -256; i < 512; i += 32) {
    x.beginPath()
    x.moveTo(i, 0)
    x.lineTo(i + 256, 256)
    x.moveTo(i + 256, 0)
    x.lineTo(i, 256)
    x.stroke()
  }
  return textura(c, [4, 2])
}
