import { useState } from 'react'

const VACIO = { nombre: '', correo: '', mensaje: '' }

function validar({ nombre, correo, mensaje }) {
  const errores = {}
  if (!nombre.trim()) errores.nombre = 'Escribe tu nombre.'
  if (!/^\S+@\S+\.\S+$/.test(correo)) errores.correo = 'Escribe un correo válido.'
  if (mensaje.trim().length < 10) errores.mensaje = 'Escribe al menos 10 caracteres.'
  return errores
}

function Campo({ id, etiqueta, error, children }) {
  return (
    <div className={`campo ${error ? 'con-error' : ''}`}>
      <label htmlFor={id}>{etiqueta}</label>
      {children}
      {error && <p className="error" id={`${id}-error`}>{error}</p>}
    </div>
  )
}

export default function Contacto() {
  const [datos, setDatos] = useState(VACIO)
  const [errores, setErrores] = useState({})
  const [enviado, setEnviado] = useState(false)

  const cambiar = (e) => setDatos({ ...datos, [e.target.name]: e.target.value })
  const propiedades = (nombre) => ({
    id: nombre,
    name: nombre,
    value: datos[nombre],
    onChange: cambiar,
    'aria-invalid': Boolean(errores[nombre]),
    'aria-describedby': errores[nombre] ? `${nombre}-error` : undefined,
  })

  function enviar(e) {
    e.preventDefault()
    const encontrados = validar(datos)
    setErrores(encontrados)
    if (Object.keys(encontrados).length === 0) {
      setEnviado(true)
      setDatos(VACIO)
    }
  }

  return (
    <div className="contenido estrecho">
      <title>Contacto | Showroom de zapatos</title>
      <header className="encabezado">
        <p className="linea">Contacto</p>
        <h1>Escríbenos</h1>
        <p className="entrada">Este formulario es una simulación: no envía ni guarda tus datos.</p>
      </header>
      {enviado ? (
        <div className="estado" role="status">
          <h2>Mensaje simulado</h2>
          <p>No se envió ni se guardó nada.</p>
          <button type="button" className="boton" onClick={() => setEnviado(false)}>Escribir otro</button>
        </div>
      ) : (
        <form className="formulario" onSubmit={enviar} noValidate>
          <Campo id="nombre" etiqueta="Nombre" error={errores.nombre}>
            <input type="text" autoComplete="off" {...propiedades('nombre')} />
          </Campo>
          <Campo id="correo" etiqueta="Correo" error={errores.correo}>
            <input type="email" autoComplete="off" {...propiedades('correo')} />
          </Campo>
          <Campo id="mensaje" etiqueta="Mensaje" error={errores.mensaje}>
            <textarea rows="5" {...propiedades('mensaje')} />
          </Campo>
          <button type="submit" className="agregar">Simular envío</button>
        </form>
      )}
    </div>
  )
}
