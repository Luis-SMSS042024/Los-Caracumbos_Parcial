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

    def agregar_producto(self, producto: Producto) -> None:
        raise NotImplementedError

    def listar_productos(self) -> List[Producto]:
        raise NotImplementedError

    def registrar_venta(self, items_solicitados: List[Tuple[str, int]]) -> Venta:
        raise NotImplementedError

    def listar_ventas(self) -> List[Venta]:
        raise NotImplementedError

    def cargar_productos_desde_csv(self, path: str) -> int:
        raise NotImplementedError

    def guardar_productos_csv(self, path: str) -> int:
        raise NotImplementedError

    def exportar_ventas_json(self, path: str) -> int:
        raise NotImplementedError

    def resumen_por_producto(self) -> List[ResumenProducto]:
        raise NotImplementedError
