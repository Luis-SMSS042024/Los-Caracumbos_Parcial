# src/models.py
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

@dataclass
class ItemVenta:
    producto_id: str
    cantidad: int
    precio_unitario: float
    @property
    def subtotal(self) -> float:
        return round(self.cantidad * self.precio_unitario, 2)

@dataclass
class Venta:
    fecha: datetime
    items: List[ItemVenta]
    @property
    def total(self) -> float:
        return round(sum(it.subtotal for it in self.items), 2)

@dataclass
class ResumenProducto:
    producto_id: str
    cantidad_total: int
    ingresos: float
