#!/usr/bin/env python3
"""Reimplementación propia de funciones matemáticas elementales.

- factorial(n)
- seno(x)
- coseno(x)
- exponencial(x)
- ln(x)

Las funciones basadas en series (seno, coseno, exponencial, ln) usan
EPS (fiscomp.precision_numerica) como criterio de convergencia: se
suman términos mientras el siguiente término siga siendo mayor o
igual que el épsilon de la máquina.
"""

from fiscomp.precision_numerica import EPS


def factorial(n):
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


def seno(x, precision=EPS):
    suma = 0.0
    k = 0
    while True:
        termino = (-1) ** k * x ** (2 * k + 1) / factorial(2 * k + 1)
        if abs(termino) < precision:
            break
        suma += termino
        k += 1
    return suma


def coseno(x, precision=EPS):
    """Aproxima cos(x) con su serie de Taylor hasta alcanzar EPS."""
    suma = 0.0
    k = 0
    while True:
        termino = (-1) ** k * x ** (2 * k) / factorial(2 * k)
        if abs(termino) < precision:
            break
        suma += termino
        k += 1
    return suma


def exponencial(x, precision=EPS):
    """Aproxima exp(x) con su serie de Taylor hasta alcanzar EPS."""
    suma = 0.0
    k = 0
    while True:
        termino = x ** k / factorial(k)
        if abs(termino) < precision:
            break
        suma += termino
        k += 1
    return suma


def ln(x, precision=EPS):
    """ln(x) para cualquier x > 0, con reduccion de rango.

    Primero se lleva x a un numero a en [0.5, 1.0), dividiendo o
    multiplicando por 2 las veces que haga falta (guardando cuantas
    veces en m). Como x = a * 2^m, entonces ln(x) = ln(a) + m*ln(2).
    ln(a) si converge rapido con la serie de y=(a-1)/(a+1) porque a ya
    quedo cerca de 1. Esta parte ya la tenias bien pensada.
    """
    if x <= 0:
        raise ValueError("ln(x) solo esta definido para x > 0")

    m = 0
    a = x
    while a >= 1.0:
        a /= 2.0
        m += 1
    while a < 0.5:
        a *= 2.0
        m -= 1

    y = (a - 1) / (a + 1)
    suma = 0.0
    k = 0
    while True:
        termino = y ** (2 * k + 1) / (2 * k + 1)
        if abs(termino) < precision:
            break
        suma += termino
        k += 1

    LN2 = 0.6931471805599453
    return 2 * suma + m * LN2


if __name__ == "__main__":
    import math

    from fiscomp.precision_numerica import error_relativo

    print(f"factorial(5) = {factorial(5)}  (math: {math.factorial(5)})")

    for x in (0.0, 0.5, 1.0, math.pi / 2, math.pi, 3 * math.pi):
        print(f"seno({x:.4f})   = {seno(x):.10f}   math.sin = {math.sin(x):.10f}")
        print(f"coseno({x:.4f}) = {coseno(x):.10f}   math.cos = {math.cos(x):.10f}")

    for x in (0.0, 1.0, -1.0, 5.0, -5.0):
        print(f"exponencial({x:.2f}) = {exponencial(x):.10f}   math.exp = {math.exp(x):.10f}")

    for x in (0.1, 0.5, 1.0, 2.0, 10.0, 1000.0):
        print(f"ln({x:.2f}) = {ln(x):.10f}   math.log = {math.log(x):.10f}   "
              f"error_relativo = {error_relativo(ln(x), math.log(x)):.2e}")
