#!/usr/bin/env python3
"""Conteo y medición de complejidad.

Producto punto:
- n multiplicaciones y n - 1 sumas.
- Total: 2n - 1 flops = O(n).

Producto de matrices n x n:
- Hay n^2 productos punto.
- Total: n^2 (2n - 1) = 2n^3 - n^2 flops = O(n^3).
"""

import math
import time
from pathlib import Path

from fiscomp.matrices import Matrix, LowerTriangularMatrix
from fiscomp.algebra_lineal import SistemaTriangular

CARPETA = Path(__file__).resolve().parent
CARPETA_DATOS = CARPETA / "datos"
CARPETA_DATOS.mkdir(exist_ok=True)


def producto_punto_contando(x, y):
    """Regresa el producto punto y el número de flops."""
    suma = x[0] * y[0]
    flops = 1

    for i in range(1, len(x)):
        suma += x[i] * y[i]
        flops += 2

    return suma, flops


def mat_vec_contando(A, x):
    """Regresa A x y el número de flops."""
    resultado = []
    flops = 0

    for renglon in A:
        valor, flops_renglon = producto_punto_contando(renglon, x)
        resultado.append(valor)
        flops += flops_renglon

    return resultado, flops


def mat_mat_contando(A, B):
    """Regresa A B y el número de flops."""
    n = len(A)
    resultado = []
    flops = 0

    for i in range(n):
        renglon = []
        for j in range(n):
            columna = [B[k][j] for k in range(n)]
            valor, flops_producto = producto_punto_contando(A[i], columna)
            renglon.append(valor)
            flops += flops_producto
        resultado.append(renglon)

    return resultado, flops


def matriz_normal(n):
    """Matriz sencilla n x n."""
    return [
        [float(i + j + 1) for j in range(n)]
        for i in range(n)
    ]


def matriz_triangular(n):
    """Matriz triangular inferior no singular."""
    return LowerTriangularMatrix(
        [
            [2.0 if i == j else (1.0 if j < i else 0.0) for j in range(n)]
            for i in range(n)
        ]
    )


def medir(funcion, repeticiones=3):
    """Regresa el tiempo mínimo de varias ejecuciones."""
    mejor = None

    for _ in range(repeticiones):
        inicio = time.perf_counter()
        funcion()
        tiempo = time.perf_counter() - inicio

        if mejor is None or tiempo < mejor:
            mejor = tiempo

    return mejor


print("--- Conteo de flops ---")
print(f"{'n':>5} {'punto':>10} {'mat_vec':>10} {'mat_mat':>12} {'sustitucion':>14}")

ruta_flops = CARPETA_DATOS / "conteo_flops.dat"

with open(ruta_flops, "w", encoding="utf-8") as archivo:
    archivo.write("# n producto_punto mat_vec mat_mat sustitucion\n")

    for n in [1, 2, 4, 8, 16, 32, 64]:
        A = matriz_normal(n)
        B = matriz_normal(n)
        x = [1.0] * n

        _, flops_punto = producto_punto_contando(x, x)
        _, flops_mat_vec = mat_vec_contando(A, x)
        _, flops_mat_mat = mat_mat_contando(A, B)

        sistema = SistemaTriangular(matriz_triangular(n), [1.0] * n)
        sistema.resolver()
        flops_sustitucion = sistema.flops

        print(
            f"{n:>5} {flops_punto:>10} {flops_mat_vec:>10} "
            f"{flops_mat_mat:>12} {flops_sustitucion:>14}"
        )

        archivo.write(
            f"{n} {flops_punto} {flops_mat_vec} "
            f"{flops_mat_mat} {flops_sustitucion}\n"
        )

print("\n--- Tiempos ---")
print(f"{'n':>5} {'sustitución (s)':>18} {'mat_mat (s)':>15}")

ruta_tiempos = CARPETA_DATOS / "tiempos.dat"
tiempos = []

with open(ruta_tiempos, "w", encoding="utf-8") as archivo:
    archivo.write("# n t_sustitucion t_mat_mat\n")

    for n in [25, 50, 100, 200]:
        T = matriz_triangular(n)
        b = [1.0] * n

        tiempo_sustitucion = medir(
            lambda: SistemaTriangular(T, b).resolver()
        )

        A = Matrix(matriz_normal(n))
        B = Matrix(matriz_normal(n))

        tiempo_mat_mat = medir(lambda: A * B)

        tiempos.append((n, tiempo_sustitucion, tiempo_mat_mat))

        print(
            f"{n:>5} {tiempo_sustitucion:>18.6f} "
            f"{tiempo_mat_mat:>15.6f}"
        )

        archivo.write(f"{n} {tiempo_sustitucion} {tiempo_mat_mat}\n")

print("\n--- Exponentes estimados ---")
for anterior, siguiente in zip(tiempos, tiempos[1:]):
    n_anterior, t_sust_anterior, t_mat_anterior = anterior
    n_siguiente, t_sust_siguiente, t_mat_siguiente = siguiente

    p_sustitucion = math.log(t_sust_siguiente / t_sust_anterior, 2)
    p_mat_mat = math.log(t_mat_siguiente / t_mat_anterior, 2)

    print(
        f"{n_anterior} -> {n_siguiente}: "
        f"p sustitución = {p_sustitucion:.2f}, "
        f"p mat_mat = {p_mat_mat:.2f}"
    )

# Respuestas:
# 1. Para n grande, los exponentes se acercan más a 2 y 3 porque el
#    costo principal domina sobre el tiempo de crear listas y llamar funciones.
# 2. La sustitución cuesta n^2 y mat_vec cuesta 2n^2 - n, así que la
#    sustitución debería ser aproximadamente dos veces más rápida.
# 3. Si n pasa de 1000 a 10000, la sustitución tarda aproximadamente
#    100 t. El producto de matrices tarda aproximadamente 1000 t'.
#    Por eso pasar de O(n^2) a O(n^3) importa mucho para n grande.