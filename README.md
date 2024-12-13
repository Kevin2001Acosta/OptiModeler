Problema de Optimización
Una empresa produce n productos químico diferentes mezclando varias materias primas. Cada producto
químico se vende a un precio específico. El objetivo
de la empresa es determinar cuántas unidades de cada
producto químico se deben producir para maximizar
los ingresos totales, teniendo en cuenta la disponibilidad de las materias primas. Es importante aclarar que
cada producto químico requiere una cantidad diferente
de materias primas para su producción.
Cada producto químico se caracteriza por su precio de
venta por unidad (pi) y la cantidad de cada materia
prima requerida para su producción (aij , donde i
representa el producto químico y j la materia prima).
Además, existe una restricción de disponibilidad de
materias primas (Aj ). Por último, de cada producto
químico existe una demanda mínima/máxima a
cumplir (Di)
Objetivo:
Maximizar las ganancias por venta de productos
químico (Z).
El programa Python toma ciertos los datos necesarios del problema, (N,M, disponibilidad de cada material, etc) separados por espacios entre lineas, y retorna código minizinc,
que puede ser pegado y ejecutado en minizinc, sin ningún cambio.
