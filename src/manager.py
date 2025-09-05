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

    # ---- Productos ----
    def agregar_producto(self, producto: Producto) -> None:
        if producto.id in self.productos:
            raise ValueError(f"Ya existe un producto con id '{producto.id}'.")
        self.productos[producto.id] = producto

    def listar_productos(self) -> List[Producto]:
        return sorted(self.productos.values(), key=lambda p: p.nombre.lower())

    # ---- Ventas ----
    def registrar_venta(self, items_solicitados: List[Tuple[str, int]]) -> Venta:
        if not items_solicitados:
            raise ValueError("Debe registrar al menos un item.")

        # Validaciones
        for pid, cant in items_solicitados:
            if pid not in self.productos:
                raise ValueError(f"Producto '{pid}' no existe.")
            if cant <= 0:
                raise ValueError("La cantidad debe ser >= 1.")
            if self.productos[pid].stock < cant:
                raise ValueError(
                    f"Stock insuficiente para '{pid}'. "
                    f"Disponible: {self.productos[pid].stock}, solicitado: {cant}"
                )

        # Construcción de items y descuento de stock
        items: List[ItemVenta] = []
        for pid, cant in items_solicitados:
            p = self.productos[pid]
            items.append(ItemVenta(producto_id=p.id, cantidad=cant, precio_unitario=p.precio))
            p.stock -= cant

        venta = Venta(fecha=datetime.now(), items=items)
        self.ventas.append(venta)
        return venta

    def listar_ventas(self) -> List[Venta]:
        return list(self.ventas)

    # ---- IO CSV / JSON ----
    def cargar_productos_desde_csv(self, path: str) -> int:
        """
        CSV con encabezados: id,nombre,precio,stock
        Inserta o actualiza productos por id. Devuelve la cantidad procesada.
        """
        if not path:
            raise ValueError("Debes indicar la ruta del CSV (ej: data/productos.csv).")

        count = 0
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                esperados = {"id", "nombre", "precio", "stock"}
                if set(reader.fieldnames or []) != esperados:
                    raise ValueError(f"Encabezados esperados: {sorted(esperados)}. "
                                     f"Encontrados: {reader.fieldnames}")

                for row in reader:
                    pid = (row.get("id") or "").strip()
                    nombre = (row.get("nombre") or "").strip()
                    precio = float((row.get("precio") or "0").strip() or 0)
                    stock = int((row.get("stock") or "0").strip() or 0)
                    prod = Producto(id=pid, nombre=nombre, precio=precio, stock=stock)
                    self.productos[pid] = prod  # inserta o actualiza
                    count += 1
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
        return count

    def guardar_productos_csv(self, path: str) -> int:
        """
        Guarda todos los productos a CSV. Devuelve la cantidad de filas escritas.
        """
        if not path:
            raise ValueError("Debes indicar la ruta destino del CSV.")
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
        if not path:
            raise ValueError("Debes indicar la ruta destino del JSON.")
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
        Consolida cantidades e ingresos por producto.
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
