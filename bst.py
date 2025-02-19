import json
from models import Producto

class NodoProducto:
    def __init__(self, producto: Producto):
        self.producto = producto
        self.izquierda = None
        self.derecha = None

class BSTProductos:
    def __init__(self):
        self.raiz = None
        self.cargar_productos()

    def insertar(self, producto: Producto):
        if not self.raiz:
            self.raiz = NodoProducto(producto)
        else:
            self._insertar(self.raiz, producto)
        self.guardar_productos()

    def _insertar(self, nodo, producto):
        if producto.id < nodo.producto.id:
            if nodo.izquierda is None:
                nodo.izquierda = NodoProducto(producto)
            else:
                self._insertar(nodo.izquierda, producto)
        else:
            if nodo.derecha is None:
                nodo.derecha = NodoProducto(producto)
            else:
                self._insertar(nodo.derecha, producto)

    def buscar(self, id_producto):
        return self._buscar(self.raiz, id_producto)

    def _buscar(self, nodo, id_producto):
        if nodo is None:
            return None
        if nodo.producto.id == id_producto:
            return nodo.producto
        elif id_producto < nodo.producto.id:
            return self._buscar(nodo.izquierda, id_producto)
        else:
            return self._buscar(nodo.derecha, id_producto)

    def guardar_productos(self):
        productos = []
        self._guardar_productos(self.raiz, productos)
        with open("productos.json", "w") as f:
            json.dump([p.dict() for p in productos], f)

    def _guardar_productos(self, nodo, productos):
        if nodo:
            productos.append(nodo.producto)
            self._guardar_productos(nodo.izquierda, productos)
            self._guardar_productos(nodo.derecha, productos)

    def cargar_productos(self):
        try:
            with open("productos.json", "r") as f:
                productos = json.load(f)
                for p in productos:
                    self.insertar(Producto(**p))
        except FileNotFoundError:
            pass
