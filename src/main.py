# src/manager.py
from __future__ import annotations

from typing import Dict, List, Tuple
from datetime import datetime
import csv
import json

from .models import Producto, ItemVenta, Venta, ResumenProducto


class GestorVentas:
    def __init__(self) -> None:
        self.productos: Dict[str, Producto] = {}
        self.ventas: List[Venta] = []

    # ---------- Productos ----------
    def agregar_producto(self, producto: Producto) -> None:
        if producto.id in self.productos:
            raise ValueError(f"Ya existe un producto con id '{producto.id}'.")
        self.productos[producto.id] = producto

    def listar_productos(self) -> List[Producto]:
        return sorted(self.productos.values(), key=lambda p: p.nombre.lower())

    # ---------- Ventas ----------
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
            disponible = self.productos[prod_id].stock
            if disponible < cant:
                raise ValueError(
                    f"Stock insuficiente para '{prod_id}'. "
                    f"Disponible: {disponible}, solicitado: {cant}"
                )

        # Construcción de items y descuento de stock
        items: List[ItemVenta] = []
        for prod_id, cant in items_solicitados:
            prod = self.productos[prod_id]
            items.append(ItemVenta(producto_id=prod.id, cantidad=cant, precio_unitario=prod.precio))
            prod.stock -= cant  # descontar stock

        venta = Venta(fecha=datetime.now(), items=items)
        self.ventas.append(venta)
        return venta

    def listar_ventas(self) -> List[Venta]:
        return list(self.ventas)

    # ---------- IO CSV / JSON ----------
    def cargar_productos_desde_csv(self, path: str) -> int:
        """
        CSV con encabezados: id,nombre,precio,stock
        Si el id existe, se ACTUALIZA (precio/stock/nombre).
        Devuelve cuántos productos fueron creados/actualizados.
        """
        count = 0
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pid = (row.get("id") or "").strip()
                nombre = (row.get("nombre") or "").strip()
                precio = float((row.get("precio") or "0").strip() or 0)
                stock = int((row.get("stock") or "0").strip() or 0)
                prod = Producto(id=pid, nombre=nombre, precio=precio, stock=stock)
                self.productos[pid] = prod  # inserta o actualiza
                count += 1
        return count

    def guardar_productos_csv(self, path: str) -> int:
        """
        Guarda todos los productos al CSV. Devuelve la cantidad de filas escritas.
        """
        productos = list(self.listar_productos())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "nombre", "precio", "stock"])
            writer.writeheader()
            for p in productos:
                writer.writerow({"id": p.id, "nombre": p.nombre, "precio": p.precio, "stock": p.stock})
        return len(productos)

    def exportar_ventas_json(self, path: str) -> int:
        """
        Exporta todas las ventas a JSON. Devuelve cantidad de ventas exportadas.
        """
        data = []
        for v in self.ventas:
            data.append({
                "fecha": v.fecha.isoformat(timespec="seconds"),
                "total": v.total,
                "items": [
                    {
                        "producto_id": it.producto_id,
                        "cantidad": it.cantidad,
                        "precio_unitario": it.precio_unitario,
                        "subtotal": it.subtotal,
                    }
                    for it in v.items
                ],
            })
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return len(self.ventas)

    def resumen_por_producto(self) -> List[ResumenProducto]:
        """
        Recorre las ventas y consolida cantidades/ingresos por producto_id.
        """
        acumulado: Dict[str, ResumenProducto] = {}
        for v in self.ventas:
            for it in v.items:
                r = acumulado.get(it.producto_id)
                if r is None:
                    acumulado[it.producto_id] = ResumenProducto(
                        producto_id=it.producto_id,
                        cantidad_total=it.cantidad,
                        ingresos=it.subtotal,
                    )
                else:
                    r.cantidad_total += it.cantidad
                    r.ingresos = round(r.ingresos + it.subtotal, 2)

        return sorted(acumulado.values(), key=lambda r: r.producto_id)
