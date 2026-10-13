"""Álgebra lineal numérica, escrita desde cero con listas de listas.



- Una matriz es una lista de listas rectangular, un renglón por
  sublista: A[i][j] es el elemento del renglón i, columna j (índices
  desde 0, como en el libro y en Python). Si tienen una Matrix
  (fiscomp/matrices.py), pasen su atributo .data.
- Un vector es una lista simple de números: x[i].


"""

from math import sqrt as raiz_cuadrada
from fiscomp.matrices import (
    Matrix,
    Identity,
    LowerTriangularMatrix,
    UpperTriangularMatrix,
)

###############################################
# Producto matriz-vector y residuo
###############################################


def mat_vec(A, x):
    """Producto matriz-vector y = A x, con y[i] = sum_j A[i][j] x[j].

    A: matriz n x m (lista de listas).
    x: vector de m componentes (lista).
    Regresa una lista de n componentes. Cuesta 2n^2 - n operaciones
    de punto flotante cuando A es cuadrada (ver notas.md).
    """
    if len(A[0]) != len(x):
        raise ValueError(
            f"dimensiones incompatibles: A tiene {len(A[0])} columnas "
            f"y x tiene {len(x)} componentes"
        )
    y = []
    for renglon in A:
        suma = 0.0
        for a_ij, x_j in zip(renglon, x):
            suma += a_ij * x_j
        y.append(suma)
    return y


def residuo(A, x, b):
    """Vector residuo r = b - A x (ec. 4.17 del libro).

    Si x es la solución exacta de A x = b, r es el vector cero. Un
    residuo chico NO garantiza que x esté cerca de la solución
    exacta (ver el ejemplo de Kahan en notas.md).
    """
    Ax = mat_vec(A, x)
    return [b_i - Ax_i for b_i, Ax_i in zip(b, Ax)]


###############################################
# Normas de vectores y de matrices
###############################################


def norma_euclidea(x):
    """Norma euclídea de un vector: sqrt(sum_i |x_i|^2)."""
    return sum(abs(x_i) ** 2 for x_i in x) ** 0.5


def norma_infinito_vec(x):
    """Norma infinito (de máxima magnitud) de un vector: max_i |x_i|."""
    return max(abs(x_i) for x_i in x)


def norma_frobenius(A):
    """Norma de Frobenius de una matriz: sqrt(sum_i sum_j |A_ij|^2)."""
    return sum(abs(a_ij) ** 2 for renglon in A for a_ij in renglon) ** 0.5


def norma_infinito(A):
    """Norma infinito de una matriz (máxima suma de renglón):

        max_i sum_j |A_ij|
    """
    return max(sum(abs(a_ij) for a_ij in renglon) for renglon in A)


###############################################
# Matrices triangulares
###############################################


def triangular_inferior(A):
    """Copia de A con ceros arriba de la diagonal (como numpy.tril)."""
    n = len(A)
    return [[A[i][j] if j <= i else 0.0 for j in range(n)] for i in range(n)]


def triangular_superior(A):
    """Copia de A con ceros abajo de la diagonal (como numpy.triu)."""
    n = len(A)
    return [[A[i][j] if j >= i else 0.0 for j in range(n)] for i in range(n)]


def sustitucion_adelante(L, b):
    """Resuelve L x = b con L triangular inferior (forsub en el libro):

        x_i = (b_i - sum_{j=0}^{i-1} L_ij x_j) / L_ii,  i = 0, 1, ..., n-1

    L: matriz n x n triangular inferior (solo se leen los elementos
       de la diagonal y de abajo de ella).
    b: vector de n componentes.
    Regresa la solución x como lista. Cuesta n^2 operaciones.
    """
    n = len(b)
    x = [0.0] * n
    for i in range(n):
        suma = 0.0
        for j in range(i):  # para i = 0 este ciclo no hace nada
            suma += L[i][j] * x[j]
        x[i] = (b[i] - suma) / L[i][i]
    return x


def sustitucion_atras(U, b):
    """Resuelve U x = b con U triangular superior (backsub en el libro):

        x_i = (b_i - sum_{j=i+1}^{n-1} U_ij x_j) / U_ii,  i = n-1, ..., 1, 0

    U: matriz n x n triangular superior (solo se leen los elementos
       de la diagonal y de arriba de ella).
    b: vector de n componentes.
    Regresa la solución x como lista. Cuesta n^2 operaciones.
    """
    n = len(b)
    x = [0.0] * n
    for i in reversed(range(n)):
        suma = 0.0
        for j in range(i + 1, n):  # para i = n-1 este ciclo no hace nada
            suma += U[i][j] * x[j]
        x[i] = (b[i] - suma) / U[i][i]
    return x


###############################################
# Eliminación gaussiana y descomposición LU
###############################################


def eliminacion_gaussiana(A, b):
    """Resuelve A x = b con eliminación gaussiana (gauelim en el libro).

    Fase de eliminación: para cada renglón pivote j = 0, ..., n-2 y
    cada renglón i = j+1, ..., n-1 de abajo,

        coeficiente = A_ij / A_jj
        renglón i  <-  renglón i - coeficiente * renglón j

    (en A y en b), hasta que A queda triangular superior. Luego,
    sustitución hacia atrás.

    A: matriz n x n (lista de listas). b: vector de n componentes.
    No modifica A ni b: trabaja sobre copias. Sin pivoteo: si algún
    pivote A_jj vale cero, levanta ZeroDivisionError (ver notas.md).
    Cuesta 2n^3/3 + 3n^2/2 - 13n/6 operaciones la eliminación, más n^2
    la sustitución hacia atrás.
    """
    A = [renglon[:] for renglon in A]
    b = b[:]
    n = len(b)
    for j in range(n - 1):
        for i in range(j + 1, n):
            coeficiente = A[i][j] / A[j][j]
            # En el libro, con NumPy: A[i,j:] -= coeficiente*A[j,j:]
            for k in range(j, n):
                A[i][k] -= coeficiente * A[j][k]
            b[i] -= coeficiente * b[j]
    return sustitucion_atras(A, b)


def descomposicion_lu(A):
    """Descomposición LU de Doolittle: A = L U (ludec en el libro).

    Es la misma eliminación gaussiana, pero sin b: lo que queda de A
    al final es U (triangular superior), y los coeficientes que se
    usaron para eliminar se guardan en L (triangular inferior, con
    unos en la diagonal): L_ij = coeficiente que anuló a A_ij.

    A: matriz n x n (lista de listas); no se modifica.
    Regresa (L, U), dos listas de listas. Sin pivoteo, como
    eliminacion_gaussiana. Cuesta 2n^3/3 + n^2/2 - 7n/6 operaciones.
    """
    n = len(A)
    U = [renglon[:] for renglon in A]
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for j in range(n - 1):
        for i in range(j + 1, n):
            coeficiente = U[i][j] / U[j][j]
            for k in range(j, n):
                U[i][k] -= coeficiente * U[j][k]
            L[i][j] = coeficiente
    return L, U


def resolver_lu(L, U, b):
    """Resuelve A x = b a partir de la descomposición A = L U:

        L y = b   (sustitución hacia adelante)
        U x = y   (sustitución hacia atrás)

    L, U: lo que regresa descomposicion_lu(A). b: vector de n
    componentes. Cuesta 2n^2 operaciones: con la misma L y U se pueden
    resolver muchos sistemas con distinto b sin repetir la
    descomposición, que es la parte cara.
    """
    y = sustitucion_adelante(L, b)
    return sustitucion_atras(U, y)



def inversa(A):
    """Matriz inversa con LU: la columna k de A^-1 es la solución de

        A x_k = e_k,

    con e_k la columna k de la identidad (porque A A^-1 = I). Son n
    sistemas con la misma A: una sola descomposición LU y n pares de
    sustituciones. Cuesta ~2n^3/3 + 2n^3 = 8n^3/3 operaciones.

    A: matriz n x n (lista de listas); no se modifica.
    Regresa A^-1 como lista de listas. Sin pivoteo (ver
    descomposicion_lu).
    """
    n = len(A)
    L, U = descomposicion_lu(A)
    columnas = []
    for k in range(n):
        e_k = [1.0 if i == k else 0.0 for i in range(n)]
        columnas.append(resolver_lu(L, U, e_k))
    # columnas[k][i] es el elemento (i, k) de la inversa: transponemos.
    return [[columnas[k][i] for k in range(n)] for i in range(n)]


def determinante(A):
    """Determinante con LU: det(A) = det(L) det(U), y como L tiene unos
    en la diagonal,

        det(A) = U_00 U_11 ... U_(n-1)(n-1).

    Cuesta ~2n^3/3 operaciones (contra ~n! con cofactores). Sin
    pivoteo: si aparece un pivote cero levanta ZeroDivisionError,
    aunque A no sea singular.
    """
    _, U = descomposicion_lu(A)
    producto = 1.0
    for i in range(len(U)):
        producto *= U[i][i]
    return producto


###############################################
# Pivoteo parcial
###############################################


def eliminacion_gaussiana_pivoteo(A, b):
    """Eliminación gaussiana con pivoteo parcial (gauelim_pivot en el
    libro).

    Igual que eliminacion_gaussiana, pero antes de usar el renglón j
    como pivote se busca, en la columna j y del renglón j para abajo,
    el elemento de mayor valor absoluto (renglón k), y se intercambian
    los renglones j y k de A y de b. Así el pivote nunca es cero (si A
    no es singular) y los coeficientes nunca pasan de 1 en valor
    absoluto.

    A: matriz n x n (lista de listas). b: vector de n componentes.
    No modifica A ni b. Regresa la solución x.
    """
    A = [renglon[:] for renglon in A]
    b = b[:]
    n = len(b)
    for j in range(n - 1):
        # k: el renglón (de j para abajo) con el |A[k][j]| más grande.
        # Con ">" estricto, si hay empate se queda el primero.
        k = j
        for m in range(j + 1, n):
            if abs(A[m][j]) > abs(A[k][j]):
                k = m
        if k != j:
            A[j], A[k] = A[k], A[j]
            b[j], b[k] = b[k], b[j]
        for i in range(j + 1, n):
            coeficiente = A[i][j] / A[j][j]
            for k_col in range(j, n):
                A[i][k_col] -= coeficiente * A[j][k_col]
            b[i] -= coeficiente * b[j]
    return sustitucion_atras(A, b)


###############################################
# Método iterativo de Jacobi
###############################################


def paso_jacobi(A, b, x):
    """Una iteración del método de Jacobi:

        x_nuevo_i = (b_i - sum_{j != i} A_ij x_j) / A_ii

    Todas las componentes nuevas se calculan con el x *anterior*.
    Regresa una lista nueva (no modifica x).
    """
    n = len(b)
    x_nuevo = []
    for i in range(n):
        suma = 0.0
        for j in range(n):
            if j != i:
                suma += A[i][j] * x[j]
        x_nuevo.append((b[i] - suma) / A[i][i])
    return x_nuevo


def cambio_relativo(x_viejo, x_nuevo):
    """Criterio de paro del libro (termcrit):

        sum_i |(x_nuevo_i - x_viejo_i) / x_nuevo_i|
    """
    return sum(abs((xn - xv) / xn) for xv, xn in zip(x_viejo, x_nuevo))


def jacobi(A, b, kmax=50, tol=1e-6):
    """Resuelve A x = b con el método iterativo de Jacobi, empezando en
    x = 0, hasta que cambio_relativo sea menor que tol.

    A: matriz n x n (lista de listas), con diagonal sin ceros. Converge
       seguro si A es diagonalmente dominante.
    kmax: número máximo de iteraciones (entero); tol: tolerancia.
    Regresa (x, k): la solución y el número de iteraciones que tomó,
    o (None, kmax) si no convergió.
    """
    x = [0.0] * len(b)
    for k in range(1, kmax):
        x_nuevo = paso_jacobi(A, b, x)
        error = cambio_relativo(x, x_nuevo)
        x = x_nuevo
        if error < tol:
            break
    else:
        # Solo llega aquí si el for terminó sin break: no convergió.
        return None, kmax
    return x, k


###############################################
# Matriz de prueba
###############################################


def crear_prueba(n, val):
    """Matriz de prueba del libro (testcreate): A_ij = sqrt(val + n i + j),
    y b_j = (A_0j)^2.1. No es simétrica. Regresa (A, b).
    """
    A = [[raiz_cuadrada(val + n * i + j) for j in range(n)] for i in range(n)]
    b = [a_0j**2.1 for a_0j in A[0]]
    return A, b

###############################################
# Práctica 4: sistemas lineales con objetos
###############################################


class MatrizSingularError(ValueError):
    """Error para una matriz triangular con un cero en la diagonal."""


class PivoteCeroError(ZeroDivisionError):
    """Error cuando la eliminación encuentra un pivote cero."""


def _validar_matriz_y_vector(A, b=None):
    """Valida una matriz cuadrada y, opcionalmente, un vector compatible."""
    if not isinstance(A, Matrix):
        raise TypeError("A debe ser un objeto Matrix.")

    if A.rows != A.cols:
        raise ValueError("A debe ser una matriz cuadrada.")

    if b is not None and len(b) != A.rows:
        raise ValueError("b debe tener el mismo número de componentes que A tiene renglones.")


class SistemaTriangular:
    """Representa y resuelve un sistema triangular T x = b."""

    def __init__(self, T, b):
        if not isinstance(T, (LowerTriangularMatrix, UpperTriangularMatrix)):
            raise TypeError(
                "T debe ser LowerTriangularMatrix o UpperTriangularMatrix."
            )

        if len(b) != T.rows:
            raise ValueError(
                "b debe tener el mismo número de componentes que T tiene renglones."
            )

        self.T = T
        self.b = list(b)
        self.n = T.rows
        self.flops = 0

    def _dividir(self, numerador, i):
        """Divide entre el elemento diagonal y convierte el error."""
        try:
            resultado = numerador / self.T.data[i][i]
        except ZeroDivisionError as error:
            raise MatrizSingularError(
                f"T[{i}][{i}] = 0: la matriz triangular es singular."
            ) from error

        self.flops += 1
        return resultado

    def sustitucion_adelante(self):
        """Resuelve un sistema con matriz triangular inferior."""
        if not isinstance(self.T, LowerTriangularMatrix):
            raise TypeError(
                "La sustitución hacia adelante requiere una matriz triangular inferior."
            )

        self.flops = 0
        x = [0.0] * self.n

        for i in range(self.n):
            suma = 0.0
            for j in range(i):
                suma += self.T.data[i][j] * x[j]
                self.flops += 2
            x[i] = self._dividir(self.b[i] - suma, i)

        return x

    def sustitucion_atras(self):
        """Resuelve un sistema con matriz triangular superior."""
        if not isinstance(self.T, UpperTriangularMatrix):
            raise TypeError(
                "La sustitución hacia atrás requiere una matriz triangular superior."
            )

        self.flops = 0
        x = [0.0] * self.n

        for i in reversed(range(self.n)):
            suma = 0.0
            for j in range(i + 1, self.n):
                suma += self.T.data[i][j] * x[j]
                self.flops += 2
            x[i] = self._dividir(self.b[i] - suma, i)

        return x

    def resolver(self):
        """Resuelve el sistema usando la sustitución adecuada."""
        if isinstance(self.T, LowerTriangularMatrix):
            return self.sustitucion_adelante()
        return self.sustitucion_atras()

    def residuo(self, x):
        """Regresa el vector b - T x."""
        return residuo(self.T.data, x, self.b)


class EliminacionGaussiana:
    """Hace la fase de eliminación gaussiana sobre una Matrix."""

    def __init__(self, A, b=None, coeficientes=False):
        _validar_matriz_y_vector(A, b)

        self.n = A.rows
        U_datos = [renglon[:] for renglon in A.data]
        b_nuevo = list(b) if b is not None else None

        if coeficientes:
            L_datos = [
                [1.0 if i == j else 0.0 for j in range(self.n)]
                for i in range(self.n)
            ]
        else:
            L_datos = None

        for j in range(self.n - 1):
            for i in range(j + 1, self.n):
                try:
                    coeficiente = U_datos[i][j] / U_datos[j][j]
                except ZeroDivisionError as error:
                    raise PivoteCeroError(
                        f"El pivote en el renglón {j} es cero. "
                        "Intenta usar pivoteo."
                    ) from error

                # Se asigna directamente para evitar ceros de redondeo.
                U_datos[i][j] = 0.0

                for k in range(j + 1, self.n):
                    U_datos[i][k] -= coeficiente * U_datos[j][k]

                if b_nuevo is not None:
                    b_nuevo[i] -= coeficiente * b_nuevo[j]

                if L_datos is not None:
                    L_datos[i][j] = coeficiente

        self.U = UpperTriangularMatrix(U_datos)
        self.b_nuevo = b_nuevo
        self.L = LowerTriangularMatrix(L_datos) if coeficientes else None


class SistemaLineal:
    """Representa un sistema lineal A x = b."""

    def __init__(self, A, b):
        _validar_matriz_y_vector(A, b)

        self.A = A
        self.b = list(b)
        self.n = A.rows

    def resolver_gauss(self):
        """Resuelve el sistema mediante eliminación gaussiana."""
        eliminacion = EliminacionGaussiana(self.A, self.b)
        sistema_triangular = SistemaTriangular(
            eliminacion.U,
            eliminacion.b_nuevo,
        )
        return sistema_triangular.resolver()

    def resolver_lu(self):
        """Resuelve el sistema mediante factorización LU."""
        return FactorizacionLU(self.A).resolver(self.b)

    def residuo(self, x):
        """Regresa b - A x."""
        return residuo(self.A.data, x, self.b)


class FactorizacionLU:
    """Representa la factorización A = L U."""

    def __init__(self, A):
        eliminacion = EliminacionGaussiana(A, coeficientes=True)

        self.A = A
        self.n = A.rows
        self.L = eliminacion.L
        self.U = eliminacion.U

    def resolver(self, b):
        """Resuelve A x = b reutilizando la factorización LU."""
        y = SistemaTriangular(self.L, b).resolver()
        return SistemaTriangular(self.U, y).resolver()

    def determinante(self):
        """Regresa el determinante de A."""
        return self.U.determinant()

    def inversa(self):
        """Regresa la inversa de A usando la factorización LU."""
        columnas = []

        identidad = Identity(self.n)

        for k in range(self.n):
            e_k = identidad.get_col(k)
            columnas.append(self.resolver(e_k))

        datos = [
            [columnas[k][i] for k in range(self.n)]
            for i in range(self.n)
        ]

        return Matrix(datos)