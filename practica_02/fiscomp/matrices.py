#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
matrices.py
-----------

Este módulo define la clase Matrix para representar matrices y
realizar operaciones básicas.
"""


class Matrix:
    """
    Clase para representar matrices y sus operaciones básicas.
    """

    def __init__(self, data):
        """
        Inicializa una matriz a partir de una lista de listas.
        """
        if not data:
            raise ValueError("una Matrix necesita al menos un renglón.")
        if not all(len(data[0]) == len(row) for row in data):
            raise ValueError("Todas las filas deben tener la misma longitud.")

        self.data = [list(row) for row in data]
        self.rows = len(self.data)
        self.cols = len(self.data[0])

    def __str__(self):
        """Representación bonita para impresión."""
        return "\n".join(["\t".join(map(str, row)) for row in self.data])

    def shape(self):
        """Devuelve la dimensión de la matriz como (filas, columnas)."""
        return (self.rows, self.cols)

    def get_row(self, i):
        """Devuelve la fila i."""
        if not -self.rows <= i < self.rows:
            raise ValueError("Índice de fila fuera de rango.")
        return self.data[i]

    def get_col(self, j):
        """Devuelve la columna j."""
        if not -self.cols <= j < self.cols:
            raise ValueError("Índice de columna fuera de rango.")
        return [row[j] for row in self.data]

    def copy(self):
        """Devuelve una copia independiente de la matriz."""
        return Matrix([row[:] for row in self.data])

    def transpose(self):
        """Devuelve la transpuesta de la matriz."""
        result = [
            [self.data[j][i] for j in range(self.rows)]
            for i in range(self.cols)
        ]
        return Matrix(result)

    def __add__(self, other):
        """Suma dos matrices del mismo tamaño."""
        if self.shape() != other.shape():
            raise ValueError("Las matrices deben tener las mismas dimensiones.")

        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __sub__(self, other):
        """Resta dos matrices del mismo tamaño."""
        if self.shape() != other.shape():
            raise ValueError("Las matrices deben tener las mismas dimensiones.")

        return self + (other * -1)

    def __mul__(self, other):
        """Multiplica por un escalar o por otra matriz."""
        if isinstance(other, (int, float)):
            result = [
                [value * other for value in row]
                for row in self.data
            ]
            return Matrix(result)

        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError(
                    "Las dimensiones no son compatibles para multiplicar."
                )

            result = [
                [
                    sum(
                        self.data[i][k] * other.data[k][j]
                        for k in range(self.cols)
                    )
                    for j in range(other.cols)
                ]
                for i in range(self.rows)
            ]
            return Matrix(result)

        raise TypeError(
            "Solo se puede multiplicar una Matrix por un número o Matrix."
        )

    __rmul__ = __mul__


if __name__ == "__main__":
    A = Matrix([[1, 2, 3], [4, 5, 6]])
    B = Matrix([[7, 8, 9], [10, 11, 12]])
    C = Matrix([[1, 2], [3, 4], [5, 6]])

    print("Matriz A:")
    print(A)

    print("\nMatriz B:")
    print(B)

    print("\nA + B:")
    print(A + B)

    print("\nA - B:")
    print(A - B)

    print("\nA * 2:")
    print(A * 2)

    print("\n2 * A:")
    print(2 * A)

    print("\nA * C:")
    print(A * C)

    print("\nTranspuesta de A:")
    print(A.transpose())