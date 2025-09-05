# src/main.py
from __future__ import annotations

from typing import Optional, Tuple, List
from .manager import GestorVentas
from .models import Producto


def _input_str(msg: str) -> str:
    return input(msg).strip()


def _input_int(msg: str, minimo: Optional[int] = None) -> int:
    while True:
        try:
            val = int(input(msg).strip())
            if minimo is not None and val < minimo:
                print(f"Debe ser >= {minimo}.")
                continue
            return val
        except ValueError:
            print("Ingrese un número entero válido.")


def _input_float(msg: str, minimo: Optional[float] = None) -> float:
    while True:
        try:
            raw = input(msg).strip().replace(",", ".")  # permite 11,50 o 11.50
            val = float(raw)
            if minimo is not None and val < minimo:
                print(f"Debe ser >= {minimo}.")
                continue
            return val
        except ValueError:
            print("Ingrese un número válido.")


def _menu() -> None:
    print("\n=== Mercado Ventas ===")
    print("1) Cargar productos desde CSV")
    print("2) Guardar productos a CSV")
    print("3) Agregar producto")
    print("4) Listar productos")
    print("5) Registrar venta")
    print("6) Listar ventas")
    print("7) Resumen por producto")
    print("8) Exportar ventas a JSON")
    print("0) Salir")


def main() -> None:
    g = GestorVentas()

    while True:
        _menu()
        opcion = _input_str("Opción: ").lower()

        try:
            if opcion == "1":
                path = _input_str("Ruta CSV (ej: data/productos.csv): ")
                n = g.cargar_productos_desde_csv(path)
                print(f"Cargados/actualizados {n} productos.")

            elif opcion == "2":
                path = _input_str("Ruta destino CSV: ")
                n = g.guardar_productos_csv(path)
                print(f"Exportados {n} productos a {path}.")

            elif opcion == "3":
                pid = _input_str("ID: ")
                nombre = _input_str("Nombre: ")
                precio = _input_float("Precio: ", minimo=0.0)
                stock = _input_int("Stock: ", minimo=0)
                g.agregar_producto(Producto(id=pid, nombre=nombre, precio=precio, stock=stock))
                print("✅ Producto agregado.")

            elif opcion == "4":
                productos = g.listar_productos()
                if not productos:
                    print("No hay productos.")
                else:
                    print("\nID | Nombre | Precio | Stock")
                    for p in productos:
                        print(f"{p.id} | {p.nombre} | ${p.precio} | {p.stock}")

            elif opcion == "5":
                print("Ingrese items de la venta. Deje ID vacío para finalizar.")
                items: List[Tuple[str, int]] = []
                while True:
                    pid = _input_str("Producto ID: ")
                    if not pid:
                        break
                    cant = _input_int("Cantidad: ", minimo=1)
                    items.append((pid, cant))
                if not items:
                    print("Venta cancelada (sin items).")
                else:
                    v = g.registrar_venta(items)
                    print(f"✅ Venta registrada. Total: ${v.total}")

            elif opcion == "6":
                ventas = g.listar_ventas()
                if not ventas:
                    print("No hay ventas.")
                else:
                    for i, v in enumerate(ventas, start=1):
                        print(f"Venta #{i} - total ${v.total} - items: {len(v.items)}")

            elif opcion == "7":
                resumen = g.resumen_por_producto()
                if not resumen:
                    print("Sin datos para resumen.")
                else:
                    print("\nproducto_id | cantidad_total | ingresos")
                    for r in resumen:
                        print(f"{r.producto_id} | {r.cantidad_total} | ${r.ingresos}")

            elif opcion == "8":
                path = _input_str("Ruta JSON destino (ej: data/ventas.json): ")
                n = g.exportar_ventas_json(path)
                print(f"Exportadas {n} ventas a {path}.")

            elif opcion == "0":
                print("¡Hasta luego!")
                break

            else:
                print("Opción inválida.")

        except KeyboardInterrupt:
            print("\nOperación cancelada por el usuario.")
        except Exception as e:
            # 👇 Esto asegura que siempre veas el tipo y el detalle del error
            import traceback, sys
            print(f"\n❌ Error: {type(e).__name__}: {e}")
            traceback.print_exc(file=sys.stdout)


if __name__ == "__main__":
    main()
