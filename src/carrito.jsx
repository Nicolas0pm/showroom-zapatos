import { createContext, useCallback, useContext, useMemo, useState } from 'react'

const CLAVE = 'showroom-carrito'
const Contexto = createContext(null)

function leer() {
  try {
    const lista = JSON.parse(localStorage.getItem(CLAVE)) ?? []
    return lista.map((item) => ({ ...item, cantidad: item.cantidad ?? 1 }))
  } catch {
    return []
  }
}

function guardar(lista) {
  try {
    localStorage.setItem(CLAVE, JSON.stringify(lista))
  } catch {
    // Sin almacenamiento el carrito dura solo esta visita.
  }
}

const mismo = (a, b) => a.producto === b.producto && a.variante === b.variante && a.talla === b.talla

export function CarritoProvider({ children }) {
  const [items, setItems] = useState(leer)

  const actualizar = useCallback((cambio) => {
    setItems((actual) => {
      const nuevo = cambio(actual)
      guardar(nuevo)
      return nuevo
    })
  }, [])

  const valor = useMemo(() => ({
    items,
    unidades: items.reduce((total, i) => total + i.cantidad, 0),
    total: items.reduce((total, i) => total + i.cantidad * i.precio, 0),
    agregar: (item) => actualizar((lista) => (
      lista.some((i) => mismo(i, item))
        ? lista.map((i) => (mismo(i, item) ? { ...i, cantidad: i.cantidad + 1 } : i))
        : [...lista, { ...item, cantidad: 1 }]
    )),
    cambiarCantidad: (item, cantidad) => actualizar((lista) => (
      lista.map((i) => (mismo(i, item) ? { ...i, cantidad: Math.max(1, cantidad) } : i))
    )),
    quitar: (item) => actualizar((lista) => lista.filter((i) => !mismo(i, item))),
    vaciar: () => actualizar(() => []),
  }), [items, actualizar])

  return <Contexto.Provider value={valor}>{children}</Contexto.Provider>
}

export const usarCarrito = () => useContext(Contexto)
