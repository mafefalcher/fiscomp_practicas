# Prácticas de Física Computacional

Este repositorio contiene las Prácticas 1 y 2 del curso.

## Estructura

```text
fiscomp/
  constantes.py             # Constantes, incluido PI
  precision_numerica.py     # Épsilon de máquina y error relativo
  funciones_especiales.py   # factorial, seno, coseno, exponencial y ln
  vectores.py               # VectorND (Práctica 1)
  matrices.py               # Matrix (Práctica 2)

practicas/
  pruebas_practica_01.py    # Pruebas automáticas de la Práctica 1
  pruebas_practica_02.py    # Pruebas automáticas de la Práctica 2
  recoleccion_datos.py      # Lanzador para probar el Ejercicio 1
  reporte_recoleccion.txt
  reporte_ejercicio4.txt

recoleccion_datos.py        # Ejercicio 1: experimento de Millikan
pi_leibniz.py               # Ejercicio 2: aproximación de pi
ejercicio4_errores.py       # Ejercicio 4: comparación con math
```

## Ejecutar las pruebas

Desde la raíz del repositorio:

```powershell
py -m practicas.pruebas_practica_01
py -m practicas.pruebas_practica_02
```

Ambos comandos deben terminar con `OK`.
