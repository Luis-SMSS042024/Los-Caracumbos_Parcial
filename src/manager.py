# src/manager.py
from __future__ import annotations
from typing import Dict, List, Tuple
from datetime import datetime
from .models import Producto, ItemVenta, Venta, ResumenProducto

class GestorVentas:
    """
    Gestor en memoria de productos y ventas.
    """
    def __init__(self) -> None:
        self.productos: Dict[str, Producto] = {}
        self.ventas: List[Venta] = []
        self._venta_seq: int = 1

    # ---- Productos ----
    def agregar_producto(self, producto: Producto) -> None:
        if producto.id in self.productos:
            raise ValueError(f"Ya existe un producto con id '{producto.id}'.")
        self.productos[producto.id] = producto

    def listar_productos(self) -> List[Producto]:
        return sorted(self.productos.values(), key=lambda p: p.nombre.lower())

    # ---- Ventas ----
    def registrar_venta(self, items_solicitados: List[Tuple[str, int]]) -> Venta:
        """
        items_solicitados: lista de (producto_id, cantidad)
        - Verifica existencia y stock
        - Descuenta stock
        - Crea venta con precios “congelados”
        """
        if not items_solicitados:
            raise ValueError("Debe registrar al menos un item.")

        # Validaciones previas sin mutar estado
        for prod_id, cant in items_solicitados:
            if prod_id not in self.productos:
                raise ValueError(f"Producto '{prod_id}' no existe.")
            if cant <= 0:
                raise ValueError("La cantidad debe ser >= 1.")
            if self.productos[prod_id].stock < cant:
                raise ValueError(
                    f"Stock insuficiente para '{prod_id}'. "
                    f"Disponible: {self.productos[prod_id].stock}, solicitado: {cant}"
                )

        # Construcción de items y descuento de stock
        items: List[ItemVenta] = []
        for prod_id, cant in items_solicitados:
            prod = self.productos[prod_id]
            items.append(ItemVenta(producto_id=prod.id, cantidad=cant, precio_unitario=prod.precio))
            prod.stock -= cant  # descontar stock

        venta = Venta(fecha=datetime.now(), items=items)
        self.ventas.append(venta)
        self._venta_seq += 1
        return venta

    def listar_ventas(self) -> List[Venta]:
        return list(self.ventas)
