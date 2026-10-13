#!/usr/bin/env python3
"""Práctica 3: diferencias finitas."""

from pathlib import Path
import sys

# Busca la carpeta practica_01, que contiene fiscomp.
archivo_actual = Path(__file__).resolve()
ruta_practica_01 = None

for carpeta in [archivo_actual.parent, *archivo_actual.parents]:
    if (carpeta / "practica_01" / "fiscomp").is_dir():
        ruta_practica_01 = carpeta / "practica_01"
        break

if ruta_practica_01 is None:
    raise FileNotFoundError("No encontré la carpeta practica_01/fiscomp.")

sys.path.insert(0, str(ruta_practica_01))

from fiscomp.funciones_especiales import seno, coseno
from fiscomp.precision_numerica import EPS, error_relativo


# Diferencias finitas

def diff_forward(f, x0, h):
    return (f(x0 + h) - f(x0)) / h


def diff_backward(f, x0, h):
    return (f(x0) - f(x0 - h)) / h


def diff_central(f, x0, h):
    return (f(x0 + h / 2) - f(x0 - h / 2)) / h


# Funciones de prueba

def const_5(x):
    return 5.0


def ident(x):
    return x


def sqr(x):
    return x ** 2


def sin_x2(x):
    return seno(x ** 2)


# Derivadas exactas

def const_5_prima(x):
    return 0.0


def ident_prima(x):
    return 1.0


def sqr_prima(x):
    return 2 * x


def sin_x2_prima(x):
    return 2 * x * coseno(x ** 2)


# Ejercicio 2: comparación de errores

x0 = 6.0
h = 0.1

funciones = [
    ["f(x)=5", const_5, const_5_prima],
    ["f(x)=x", ident, ident_prima],
    ["f(x)=x^2", sqr, sqr_prima],
    ["f(x)=sin(x^2)", sin_x2, sin_x2_prima],
]

print("COMPARACION DE DIFERENCIAS FINITAS")
print(f"x0 = {x0}, h = {h}")

for nombre, funcion, derivada in funciones:
    exacta = derivada(x0)

    adelante = diff_forward(funcion, x0, h)
    atras = diff_backward(funcion, x0, h)
    central = diff_central(funcion, x0, h)

    print("\n" + nombre)
    print("Derivada exacta:", exacta)
    print("Adelante:", adelante,
          "Error:", error_relativo(adelante, exacta))
    print("Atras:", atras,
          "Error:", error_relativo(atras, exacta))
    print("Central:", central,
          "Error:", error_relativo(central, exacta))


# Ejercicio 3: barrido de h

x0 = 1.0
h = 1.0
exacta = sin_x2_prima(x0)

carpeta_datos = Path(__file__).resolve().parent / "datos"
carpeta_datos.mkdir(exist_ok=True)

ruta_datos = carpeta_datos / "derivada_sin_x2.dat"

filas = []

with open(ruta_datos, "w", encoding="utf-8") as archivo:
    archivo.write(
        "# h diff_forward error_forward diff_central error_central\n"
    )

    for i in range(50):
        adelante = diff_forward(sin_x2, x0, h)
        central = diff_central(sin_x2, x0, h)

        error_adelante = error_relativo(adelante, exacta)
        error_central = error_relativo(central, exacta)

        archivo.write(
            f"{h} {adelante} {error_adelante} "
            f"{central} {error_central}\n"
        )

        filas.append(
            [h, adelante, error_adelante, central, error_central]
        )

        h = h / 2


# Ejercicio 4: h óptima medida

mejor_adelante = filas[0]
mejor_central = filas[0]

for fila in filas:
    if fila[2] < mejor_adelante[2]:
        mejor_adelante = fila

    if fila[4] < mejor_central[4]:
        mejor_central = fila


h_teorica_adelante = (4 * EPS) ** 0.5
h_teorica_central = (24 * EPS) ** (1 / 3)

print("\nH OPTIMA")
print("h medida adelante:", mejor_adelante[0])
print("h teorica adelante:", h_teorica_adelante)
print("h medida central:", mejor_central[0])
print("h teorica central:", h_teorica_central)

# No coinciden exactamente porque la fórmula supone funciones y
# derivadas de orden 1. Además, el barrido solo prueba h = 1 / 2**n.


# Ejercicio 5: gráfica opcional

try:
    import matplotlib.pyplot as plt

    valores_h = []
    errores_adelante = []
    errores_central = []

    for fila in filas:
        valores_h.append(fila[0])
        errores_adelante.append(fila[2])
        errores_central.append(fila[4])

    plt.plot(
        valores_h, errores_adelante,
        "o-", color="red", markersize=3,
        label="Adelante O(h)"
    )

    plt.plot(
        valores_h, errores_central,
        "o-", color="blue", markersize=3,
        label="Central O(h^2)"
    )

    plt.axvline(
        h_teorica_adelante,
        color="red",
        linestyle="--",
        label="h opt adelante"
    )

    plt.axvline(
        h_teorica_central,
        color="blue",
        linestyle="--",
        label="h opt central"
    )

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("h")
    plt.ylabel("Error relativo")
    plt.title("Error de diferencias finitas")
    plt.grid(True)
    plt.legend()

    ruta_grafica = Path(__file__).resolve().parent / "grafica_derivada.png"
    plt.savefig(ruta_grafica)
    plt.show()

    print("\nGráfica guardada en:", ruta_grafica)

except ImportError:
    print(
        "\nNo se generó la gráfica porque falta matplotlib.\n"
        "Puedes instalarlo con: py -m pip install matplotlib"
    )

print("\nDatos guardados en:", ruta_datos)
