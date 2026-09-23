#!/usr/bin/env python3
"""Pruebas automáticas de la Práctica 3."""

import subprocess
import sys
import unittest
from pathlib import Path

CARPETA_UNIDAD = Path(__file__).resolve().parent.parent / "unidades" / "08_diferencias_finitas"
RUTA_SCRIPT = CARPETA_UNIDAD / "diferencias_finitas.py"
RUTA_DATOS = CARPETA_UNIDAD / "datos" / "derivada_sin_x2.dat"


class TestBarridoDeH(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        RUTA_DATOS.unlink(missing_ok=True)
        cls.resultado = subprocess.run(
            [sys.executable, str(RUTA_SCRIPT)],
            cwd=CARPETA_UNIDAD,
            capture_output=True,
            text=True,
            timeout=60,
        )

    def leer_filas(self):
        filas = []
        with open(RUTA_DATOS, encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.startswith("#") or not linea.strip():
                    continue
                filas.append([float(valor) for valor in linea.split()])
        return filas

    def test_corre_sin_errores(self):
        self.assertEqual(self.resultado.returncode, 0, self.resultado.stderr)

    def test_genera_archivo_de_datos(self):
        self.assertTrue(RUTA_DATOS.exists())

    def test_formato_de_columnas(self):
        filas = self.leer_filas()
        self.assertGreaterEqual(len(filas), 10)
        for fila in filas[:5]:
            self.assertEqual(len(fila), 5)

    def test_central_es_mas_precisa_para_h_grande(self):
        for fila in self.leer_filas()[:3]:
            self.assertLess(fila[4], fila[2])

    def test_error_central_baja_al_principio(self):
        errores = [fila[4] for fila in self.leer_filas()[:5]]
        self.assertEqual(errores, sorted(errores, reverse=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
