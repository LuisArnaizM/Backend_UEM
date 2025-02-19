import json
from models import Pedido

class NodoPedido:
    def __init__(self, pedido: Pedido):
        self.pedido = pedido
        self.siguiente = None

class ListaPedidos:
    def __init__(self):
        self.cabeza = None
        self.cargar_pedidos()

    def agregar_pedido(self, pedido: Pedido):
        nuevo_nodo = NodoPedido(pedido)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.guardar_pedidos()

    def buscar_pedido(self, id_pedido):
        actual = self.cabeza
        while actual:
            if actual.pedido.id == id_pedido:
                return actual.pedido
            actual = actual.siguiente
        return None

    def actualizar_pedido(self, id_pedido, productos):
        actual = self.cabeza
        while actual:
            if actual.pedido.id == id_pedido:
                actual.pedido.productos = productos
                self.guardar_pedidos()
                return actual.pedido
            actual = actual.siguiente
        return None

    def eliminar_pedido(self, id_pedido):
        if not self.cabeza:
            return False
        if self.cabeza.pedido.id == id_pedido:
            self.cabeza = self.cabeza.siguiente
            self.guardar_pedidos()
            return True
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.pedido.id == id_pedido:
                actual.siguiente = actual.siguiente.siguiente
                self.guardar_pedidos()
                return True
            actual = actual.siguiente
        return False

    def listar_pedidos(self):
        pedidos = []
        actual = self.cabeza
        while actual:
            pedidos.append(actual.pedido)
            actual = actual.siguiente
        return pedidos

    def guardar_pedidos(self):
        with open("pedidos.json", "w") as f:
            json.dump([p.dict() for p in self.listar_pedidos()], f)

    def cargar_pedidos(self):
        try:
            with open("pedidos.json", "r") as f:
                pedidos = json.load(f)
                for p in pedidos:
                    self.agregar_pedido(Pedido(**p))
        except FileNotFoundError:
            pass
