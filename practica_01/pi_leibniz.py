#!/usr/bin/env python3
# Ejercicio 2 - pi con el metodo de Leibniz

import math

m = 1000000
pi = 0

for n in range(m):
    pi = pi + (4 * (-1) ** n) / (2 * n + 1)  # Serie de Leibniz

print(pi)
print(math.pi)
print(f"error absoluto: {abs(pi - math.pi):.3e}")

# Este es el valor que quedo guardado como PI en fiscomp/constantes.py,
# para no tener que volver a sumar el millon de terminos cada vez que
# algun otro script necesite pi.
# Con 1,000,000 de términos queda un error absoluto cercano a 1e-6.
# La serie converge muy lentamente: su error es del orden de 1/N. Para
# acercarse al epsilon de máquina (~1e-16) se requerirían alrededor de
# 10^15 o más términos, una cantidad impráctica de calcular.
