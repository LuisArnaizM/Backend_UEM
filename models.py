from pydantic import BaseModel
from typing import List

class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int

class Pedido(BaseModel):
    id: int
    productos: List[int]  # Lista de IDs de productos
