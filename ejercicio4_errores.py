#!/usr/bin/env python3

import math
from pathlib import Path

from fiscomp.funciones_especiales import coseno, exponencial, ln, seno
from fiscomp.precision_numerica import error_relativo

VALORES_TRIG = [0.0, 0.5, 1.0, math.pi / 6, math.pi / 2, math.pi, 2 * math.pi, 10 * math.pi]
VALORES_EXP = [0.0, 1.0, -1.0, 5.0, -5.0, 20.0]
VALORES_LN = [0.01, 0.5, 1.0, 2.0, 10.0, 1000.0]


def comparar(nombre_funcion, funcion_propia, funcion_math, valores):
    filas = []
    for x in valores:
        aprox = funcion_propia(x)
        exacto = funcion_math(x)
        error = error_relativo(aprox, exacto)
        filas.append((x, aprox, exacto, error))
    return filas


if __name__ == "__main__":
    resultados = {
        "seno": comparar("seno", seno, math.sin, VALORES_TRIG),
        "coseno": comparar("coseno", coseno, math.cos, VALORES_TRIG),
        "exponencial": comparar("exponencial", exponencial, math.exp, VALORES_EXP),
        "ln": comparar("ln", ln, math.log, VALORES_LN),
    }

    ruta_reporte = Path(__file__).resolve().parent / "reporte_ejercicio4.txt"
    with open(ruta_reporte, "w", encoding="utf-8") as reporte:
        reporte.write("REPORTE - EJERCICIO 4: ERROR DE LAS FUNCIONES ESPECIALES\n")
        reporte.write("=" * 60 + "\n\n")

        for nombre, filas in resultados.items():
            reporte.write(f"--- {nombre} ---\n")
            reporte.write(f"{'x':>12}  {'aproximado':>18}  {'math':>18}  {'error_relativo':>15}\n")
            for x, aprox, exacto, error in filas:
                reporte.write(f"{x:>12.6f}  {aprox:>18.12f}  {exacto:>18.12f}  {error:>15.3e}\n")
            reporte.write("\n")

        reporte.write("Analisis\n")
        reporte.write("-" * 60 + "\n")
        reporte.write(
            "El error relativo se dispara en seno(x) cerca de multiplos de\n"
            "pi, y en coseno(x) cerca de pi/2, 3*pi/2, etc, porque ahi el\n"
            "valor 'real' esta muy cerca de 0 y error_relativo() divide\n"
            "entre ese valor: un error absoluto chico se ve enorme en\n"
            "terminos relativos. En exponencial(x) y ln(x) no aparece ese\n"
            "problema en los valores probados."
        )

    print(f"Listo. Se generó {ruta_reporte}")
    for nombre, filas in resultados.items():
        peor = max(filas, key=lambda fila: fila[3])
        print(f"{nombre}: peor error relativo = {peor[3]:.3e} en x = {peor[0]:.4f}")
