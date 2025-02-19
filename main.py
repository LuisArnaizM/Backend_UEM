from fastapi import FastAPI, HTTPException
from bst import BSTProductos
from linked_list import ListaPedidos
from models import Producto, Pedido

app = FastAPI()
bst_productos = BSTProductos()
lista_pedidos = ListaPedidos()

@app.post("/productos")
def crear_producto(producto: Producto):
    bst_productos.insertar(producto)
    return {"mensaje": "Producto agregado"}

@app.get("/productos/{id}")
def obtener_producto(id: int):
    producto = bst_productos.buscar(id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.post("/pedidos")
def crear_pedido(pedido: Pedido):
    lista_pedidos.agregar_pedido(pedido)
    return {"mensaje": "Pedido creado"}

@app.get("/pedidos/{id}")
def obtener_pedido(id: int):
    pedido = lista_pedidos.buscar_pedido(id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@app.put("/pedidos/{id}")
def actualizar_pedido(id: int, pedido: Pedido):
    actualizado = lista_pedidos.actualizar_pedido(id, pedido.productos)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return actualizado

@app.delete("/pedidos/{id}")
def eliminar_pedido(id: int):
    if not lista_pedidos.eliminar_pedido(id):
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"mensaje": "Pedido eliminado"}

@app.get("/pedidos")
def listar_pedidos():
    return lista_pedidos.listar_pedidos()
