#!/usr/bin/env python3
"""Vector de N dimensiones."""


class VectorND:
    """Vector de N dimensiones, representado por una lista de coordenadas."""

    def __init__(self, coords):
        try:
            self.coords = list(coords)
        except TypeError as error:
            raise TypeError(
                "coords debe ser algo iterable (lista, tupla, ...), no "
                f"{type(coords).__name__}"
            ) from error

        if not self.coords:
            raise ValueError("un VectorND necesita al menos una coordenada")

        for c in self.coords:
            if not isinstance(c, (int, float)):
                raise TypeError(
                    f"coordenada no numérica: {c!r} ({type(c).__name__})"
                )

    def __repr__(self):
        return f"VectorND({self.coords!r})"

    def __len__(self):
        return len(self.coords)

    def __eq__(self, otro):
        if not isinstance(otro, VectorND):
            return NotImplemented
        return self.coords == otro.coords

    def __getitem__(self, indice):
        return self.coords[indice]

    def _checar_dimensiones(self, otro):
        if len(self) != len(otro):
            raise ValueError(
                f"las dimensiones no coinciden: {len(self)} != {len(otro)}"
            )

    def __add__(self, otro):
        self._checar_dimensiones(otro)
        return VectorND([a + b for a, b in zip(self.coords, otro.coords)])

    def __neg__(self):
        return VectorND([-a for a in self.coords])

    def __sub__(self, otro):
        self._checar_dimensiones(otro)
        return VectorND([a - b for a, b in zip(self.coords, otro.coords)])

    def __mul__(self, escalar):
        return VectorND([a * escalar for a in self.coords])

    __rmul__ = __mul__

    def __truediv__(self, escalar):
        return VectorND([a / escalar for a in self.coords])

    def dot(self, otro):
        self._checar_dimensiones(otro)
        return sum(a * b for a, b in zip(self.coords, otro.coords))

    def norm(self):
        return self.dot(self) ** 0.5

    def normalizado(self):
        try:
            return self / self.norm()
        except ZeroDivisionError as error:
            raise ZeroDivisionError(
                "no se puede normalizar el vector cero "
                "(no tiene dirección definida)"
            ) from error

    def distancia_a(self, otro):
        return (self - otro).norm()


if __name__ == "__main__":
    v1 = VectorND([1, 2, 3])
    v2 = VectorND([4, 5, 6])

    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"-v1 = {-v1}")
    print(f"2 * v1 = {2 * v1}")
    print(f"v1 * 2 = {v1 * 2}")
    print(f"v1 / 2 = {v1 / 2}")
    print(f"v1[0] = {v1[0]}")
    print(f"v1 . v2 = {v1.dot(v2)}")
    print(f"norm(v1) = {v1.norm()}")
    print(f"normalizado(v1) = {v1.normalizado()}")
    print(f"distancia_a(v1, v2) = {v1.distancia_a(v2)}")
    print(f"norm(normalizado(v1)) = {v1.normalizado().norm()}")
    print(f"v1 == VectorND([1, 2, 3]) -> {v1 == VectorND([1, 2, 3])}")

    print(30 * "=")

    entradas_invalidas = [5, [], [1, "dos", 3]]
    for entrada in entradas_invalidas:
        try:
            VectorND(entrada)
        except (TypeError, ValueError) as error:
            print(
                f"VectorND({entrada!r}) rechazado: "
                f"{type(error).__name__}: {error}"
            )

    cero = VectorND([0, 0, 0])
    try:
        cero.normalizado()
    except ZeroDivisionError as error:
        print(f"normalizado() del vector cero: {error}")
        print(f"causa original: {error.__cause__!r}")