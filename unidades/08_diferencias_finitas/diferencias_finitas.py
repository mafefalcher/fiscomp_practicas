#!/usr/bin/env python3
"""Práctica 3: diferenciación numérica con diferencias finitas."""

from pathlib import Path
import sys

# Las funciones seno, coseno, EPS y error_relativo se hicieron en la Práctica 1.
RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ_PROYECTO / "practica_01"))

from fiscomp.funciones_especiales import coseno, seno
from fiscomp.precision_numerica import EPS, error_relativo


def diff_forward(f, x0, h):
    """Diferencia hacia adelante; tiene error de truncamiento O(h)."""
    return (f(x0 + h) - f(x0)) / h


def diff_backward(f, x0, h):
    """Diferencia hacia atrás; tiene error de truncamiento O(h)."""
    return (f(x0) - f(x0 - h)) / h


def diff_central(f, x0, h):
    """Diferencia central; tiene error de truncamiento O(h**2)."""
    return (f(x0 + h / 2) - f(x0 - h / 2)) / h


# Funciones de prueba.
def const_5(x):
    return 5.0


def ident(x):
    return x


def sqr(x):
    return x ** 2


def sin_x2(x):
    return seno(x ** 2)


# Derivadas exactas de las funciones de prueba.
def d_const_5(x):
    return 0.0


def d_ident(x):
    return 1.0


def d_sqr(x):
    return 2 * x


def d_sin_x2(x):
    return 2 * x * coseno(x ** 2)


def imprimir_tabla():
    """Compara los tres métodos con la derivada exacta."""
    x0 = 6.0
    h = 0.1
    funciones = [
        ("f(x) = 5", const_5, d_const_5),
        ("f(x) = x", ident, d_ident),
        ("f(x) = x^2", sqr, d_sqr),
        ("f(x) = sin(x^2)", sin_x2, d_sin_x2),
    ]

    print("Comparación de derivadas en x0 = 6.0, h = 0.1")
    print("-" * 88)
    print(f"{'función':18} {'exacta':>14} {'adelante':>14} {'atrás':>14} {'central':>14}")
    for nombre, funcion, derivada in funciones:
        exacta = derivada(x0)
        adelante = diff_forward(funcion, x0, h)
        atras = diff_backward(funcion, x0, h)
        central = diff_central(funcion, x0, h)
        print(f"{nombre:18} {exacta:14.8f} {adelante:14.8f} {atras:14.8f} {central:14.8f}")


def generar_datos():
    """Genera el barrido de h solicitado en datos/derivada_sin_x2.dat."""
    x0 = 1.0
    h = 1.0
    exacta = d_sin_x2(x0)
    ruta_datos = Path(__file__).resolve().parent / "datos"
    ruta_datos.mkdir(exist_ok=True)
    ruta_archivo = ruta_datos / "derivada_sin_x2.dat"
    filas = []

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("# h diff_forward error_forward diff_central error_central\n")
        for _ in range(50):
            adelante = diff_forward(sin_x2, x0, h)
            central = diff_central(sin_x2, x0, h)
            error_adelante = error_relativo(adelante, exacta)
            error_central = error_relativo(central, exacta)
            archivo.write(
                f"{h:.16e} {adelante:.16e} {error_adelante:.16e} "
                f"{central:.16e} {error_central:.16e}\n"
            )
            filas.append((h, adelante, error_adelante, central, error_central))
            h /= 2

    print(f"\nSe generó: {ruta_archivo}")
    return filas


def imprimir_h_optima(filas):
    """Encuentra el menor error medido y lo compara con h óptima teórica."""
    mejor_adelante = min(filas, key=lambda fila: fila[2])
    mejor_central = min(filas, key=lambda fila: fila[4])
    h_adelante_teorica = (4 * EPS) ** 0.5
    h_central_teorica = (24 * EPS) ** (1 / 3)

    print("\nh óptima")
    print("-" * 50)
    print(f"Adelante: h medida = {mejor_adelante[0]:.6e}")
    print(f"           h teórica = {h_adelante_teorica:.6e}")
    print(f"Central:  h medida = {mejor_central[0]:.6e}")
    print(f"           h teórica = {h_central_teorica:.6e}")
    print("Las h no coinciden exactamente porque las fórmulas teóricas son aproximaciones")
    print("y el redondeo depende de las operaciones reales de la computadora.")


if __name__ == "__main__":
    imprimir_tabla()
    filas = generar_datos()
    imprimir_h_optima(filas)
