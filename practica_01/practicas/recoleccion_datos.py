"""Lanzador del Ejercicio 1 para las pruebas de la práctica.

La implementación vive en la raíz del proyecto. Este archivo permite que
las pruebas, que buscan el script dentro de ``practicas/``, lo ejecuten.
"""

import runpy
import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROYECTO))
runpy.run_path(str(RAIZ_PROYECTO / "recoleccion_datos.py"), run_name="__main__")
