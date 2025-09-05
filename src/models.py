from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Producto:
    id: str
    nombre: str
    precio: float
    stock: int

    def __post_init__(self) -> None:
        if not self.id or not self.id.strip():
            raise ValueError("El id de producto no puede estar vacío.")
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de producto no puede estar vacío.")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")

@dataclass
class ItemVenta:
    producto_id: str
    cantidad: int
    precio_unitario: float  # precio del producto al momento de la venta

    def __post_init__(self) -> None:
        if not self.producto_id or not self.producto_id.strip():
            raise ValueError("El producto_id no puede estar vacío.")
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser >= 1.")
        if self.precio_unitario < 0:
            raise ValueError("El precio_unitario no puede ser negativo.")

    @property
    def subtotal(self) -> float:
        return round(self.cantidad * self.precio_unitario, 2)

@dataclass
class Venta:
    fecha: datetime
    items: List[ItemVenta]

    def __post_init__(self) -> None:
        if not self.items:
            raise ValueError("Una venta debe tener al menos un item.")

    @property
    def total(self) -> float:
        return round(sum(it.subtotal for it in self.items), 2)

@dataclass
class ResumenProducto:
    producto_id: str
    cantidad_total: int
    ingresos: float
