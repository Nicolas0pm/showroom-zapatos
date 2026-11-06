import { useRef } from 'react'
import { usarAparicion } from '../aparicion.js'
import { Enlace } from '../transicion.jsx'

const ROLES = [
  ['Líder de proyecto y UX', 'Planeación, entregas, investigación y wireframes.'],
  ['Diseño visual', 'Identidad, interfaz y piezas gráficas.'],
  ['Motion design', 'Guía de movimiento y animaciones originales.'],
  ['Desarrollo', 'Implementación, animaciones y publicación.'],
]

const PASOS = [
  ['Modelar', 'Cada zapato se genera en Blender por partes, para poder cambiar su color en la web.'],
  ['Construir', 'La sala funciona en tiempo real con Three.js y React.'],
  ['Animar', 'GSAP mueve la cámara, las luces y las transiciones. Cada movimiento guía la compra.'],
  ['Cuidar', 'Las animaciones se apagan si el usuario prefiere reducir el movimiento.'],
]

export default function Nosotros() {
  const raiz = useRef(null)
  usarAparicion(raiz)

  return (
    <div className="contenido estrecho" ref={raiz}>
      <title>Nosotros | Showroom de zapatos</title>
      <header className="encabezado">
        <p className="linea">Nosotros</p>
        <h1>Una tienda que se recorre</h1>
        <p className="entrada">
          Quisimos cambiar la cuadrícula de productos por una sala. Aquí el usuario camina entre
          estanterías, toma un zapato y lo gira antes de decidir.
        </p>
      </header>

      <section className="bloque">
        <h2 className="aparece">Cómo lo hicimos</h2>
        <ol className="pasos">
          {PASOS.map(([titulo, texto]) => (
            <li key={titulo} className="aparece"><h3>{titulo}</h3><p>{texto}</p></li>
          ))}
        </ol>
      </section>

      <section className="bloque">
        <h2 className="aparece">El equipo</h2>
        <ul className="roles">
          {ROLES.map(([rol, texto]) => (
            <li key={rol} className="aparece"><h3>{rol}</h3><p>{texto}</p></li>
          ))}
        </ul>
      </section>

      <section className="bloque aviso aparece">
        <h2>Aviso</h2>
        <p>
          Este es un proyecto universitario sin fines comerciales y no tiene relación con las marcas
          o personas mencionadas. No se vende ningún producto. Los precios, las tallas y los modelos
          son simulados, y los modelos 3D son aproximaciones hechas por el equipo.
        </p>
      </section>

      <Enlace className="boton aparece" to="/">Volver a la sala</Enlace>
    </div>
  )
}
