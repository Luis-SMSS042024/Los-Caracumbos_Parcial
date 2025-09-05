# Sistema de Ventas - Mercado Local
Proyecto para el parcial de Programación Computacional III.
 Luis Alexander Rivera Alvarez - SMSS042024
 Walter Jose Ramirez Perez - SMSS034824

📌 1. ¿Qué ventajas tiene en comparación con poner todo el código en un solo archivo o utilizar módulos?
Ventajas de separar en módulos:
Organización y legibilidad: en lugar de tener cientos de líneas en un solo archivo, separamos responsabilidades en models.py, manager.py, main.py. Así cada archivo cumple un rol específico y es más fácil de entender.
Mantenimiento: si aparece un error en la lógica de ventas, sabemos que está en manager.py; si es un problema de modelo de datos, está en models.py. Esto reduce el tiempo de depuración.
Reutilización: las clases (Producto, Venta, GestorVentas) pueden reutilizarse en otros proyectos o interfaces (por ejemplo, pasar de CLI a web) sin reescribir todo.
Escalabilidad: el programa puede crecer fácilmente agregando nuevos módulos (por ejemplo, un reportes.py o un usuarios.py).
Trabajo en equipo: permite que dos personas trabajen en paralelo en archivos distintos sin pisarse.

📌 2. ¿Cómo aplicaron la Programación Orientada a Objetos en su solución? Describan el papel de las clases creadas.
Aplicación de POO:
Producto: representa la entidad básica (con atributos como id, nombre, precio, stock).
→ Encapsula validaciones como no permitir precios negativos.
ItemVenta: une un producto con una cantidad vendida y calcula su subtotal.
→ Aplica la idea de composición (una venta está compuesta por items).
Venta: agrupa varios ItemVenta y calcula el total de la compra.
→ Modela una transacción concreta.
ResumenProducto: resume estadísticas de ventas por producto (cantidad total vendida e ingresos generados).
→ Es útil para reportes.
GestorVentas: actúa como controlador central. Maneja la lista de productos, valida stock, registra ventas y exporta datos.
→ Aplica encapsulación al ocultar la lógica de gestión y exponer solo métodos seguros (agregar_producto, registrar_venta, etc.).
👉 En conjunto, usamos clases para modelar objetos reales (productos, ventas) y un gestor para administrar la lógica del negocio, lo que es un diseño típico orientado a objetos.

📌 3. ¿De qué manera el uso de GitHub facilitó el trabajo colaborativo en equipo? Den un ejemplo concreto.
Ventajas del uso de GitHub:
Control de versiones: cada cambio quedó registrado con un commit, lo que permite volver atrás si algo falla.
Trabajo en paralelo: mientras uno implementaba los modelos (models.py), el otro trabajaba en la lógica de gestión (manager.py) sin esperar a que el primero terminara.
Revisiones cruzadas (Pull Requests): cada integrante subió sus cambios en una rama y el otro revisó antes de hacer merge. Ejemplo:
Luis creó un PR para agregar las validaciones en models.py.
Tú revisaste el código, dejaste un comentario, y luego lo aprobaste.
Así se asegura que ambos aportaron y aprendieron de los cambios.
Evidencia de participación: el docente puede ver en el historial de commits quién hizo qué y cómo se integraron los cambios.