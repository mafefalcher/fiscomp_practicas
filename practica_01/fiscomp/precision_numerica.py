#! /usr/bin/env python3
"""Herramientas sobre la representación de punto flotante.

Ilustra dos de las fuentes de error numérico más comunes:

- Error de redondeo: epsilon_maquina() lo estima directamente, y
  son_iguales() ofrece una forma de comparar flotantes que lo tolera.
- Error de truncamiento: error_relativo() sirve para medir qué tan
  buena es una aproximación numérica (como una serie truncada) frente
  al valor exacto.

(La incertidumbre experimental, la tercera fuente de error, no es un
tema de aritmética de punto flotante y no se trata en este módulo.)
"""


def epsilon_maquina():
    epsilon = 1.0
    while 1.0 + epsilon / 2.0 > 1.0:
        epsilon /= 2.0
    return epsilon


EPS = epsilon_maquina()


def son_iguales(a, b, tolerancia=EPS):
    return abs(a - b) < tolerancia


def error_relativo(aproximado, exacto):
    if exacto == 0.0:
        return abs(aproximado - exacto)
    return abs(aproximado - exacto) / abs(exacto)


if __name__ == "__main__":
    import math
    import sys

    print(f"epsilon_maquina() = {EPS}")
    print(f"sys.float_info.epsilon = {sys.float_info.epsilon}")
    print(f"¿Coinciden? {EPS == sys.float_info.epsilon}")
