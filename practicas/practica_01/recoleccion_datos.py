#!/usr/bin/env python3
"""Ejercicio 1: estimación de la carga del electrón con datos de Millikan."""

import math
from pathlib import Path

from fiscomp.precision_numerica import error_relativo

CARGA_ELECTRON_ACEPTADA = 1.602176634e-19


def pedir_texto(mensaje, predeterminado):
    """Lee texto; usa un valor de ejemplo si la entrada se termina."""
    try:
        return input(mensaje).strip() or predeterminado
    except EOFError:
        return predeterminado


def pedir_float(mensaje, predeterminado):
    """Lee un flotante sin interrumpir la corrida por una entrada ausente."""
    try:
        return float(pedir_texto(mensaje, str(predeterminado)))
    except ValueError:
        return predeterminado


def pedir_entero(mensaje, predeterminado):
    """Lee un entero sin interrumpir la corrida por una entrada ausente."""
    try:
        return int(pedir_texto(mensaje, str(predeterminado)))
    except ValueError:
        return predeterminado


def estimar_carga_electron(cargas_medidas):
    """Regresa (e_estimada, desviacion_estandar) a partir de las cargas."""
    if not cargas_medidas:
        raise ValueError("Se necesita al menos una carga medida.")

    e_aproximada = min(cargas_medidas)
    estimaciones = []
    for carga in cargas_medidas:
        n = max(1, round(carga / e_aproximada))
        estimaciones.append(carga / n)

    e_estimada = sum(estimaciones) / len(estimaciones)
    desviacion = math.sqrt(
        sum((estimacion - e_estimada) ** 2 for estimacion in estimaciones)
        / len(estimaciones)
    )
    return e_estimada, desviacion


def detalle_gotas(cargas_medidas):
    """Construye (carga, n, estimacion_individual) para el reporte."""
    e_aproximada = min(cargas_medidas)
    detalle = []
    for carga in cargas_medidas:
        n = max(1, round(carga / e_aproximada))
        detalle.append((carga, n, carga / n))
    return detalle


def main():
    # Se piden por separado para que cualquier entrada simple sea válida.
    experimento = pedir_texto("Nombre del experimento: ", "Experimento de Millikan")
    responsable = pedir_texto("Nombre del responsable: ", "Responsable no indicado")

    print("Condiciones: viscosidad del aire, densidad del aceite, voltaje y distancia.")
    condiciones = (
        pedir_float("Viscosidad del aire: ", 1.8e-5),
        pedir_float("Densidad del aceite: ", 900.0),
        pedir_float("Voltaje aplicado: ", 500.0),
        pedir_float("Distancia entre placas: ", 0.005),
    )

    cantidad = max(3, pedir_entero("Número de gotas medidas (mínimo 3): ", 4))
    cargas_medidas = []
    cargas_unicas = set()

    for i in range(cantidad):
        ejemplos = (1.602e-19, 3.204e-19, 4.806e-19, 6.408e-19)
        carga = pedir_float(f"Carga de la gota {i + 1} en C: ", ejemplos[i % 4])
        es_valida = carga > 0.0
        if es_valida:
            cargas_medidas.append(carga)
            cargas_unicas.add(carga)
            print("Dato aceptable")
        else:
            print("Dato comprometido: la carga debe ser positiva")

    if not cargas_medidas:
        raise ValueError("No se capturaron cargas positivas para estimar e.")

    e_estimada, desviacion = estimar_carga_electron(cargas_medidas)
    error = error_relativo(e_estimada, CARGA_ELECTRON_ACEPTADA)
    resumen = {
        "Experimento": experimento,
        "Responsable": responsable,
        "Cargas válidas": len(cargas_medidas),
        "Cargas únicas": len(cargas_unicas),
        "Carga estimada": e_estimada,
        "Desviación estándar": desviacion,
        "Error relativo": error,
    }

    # Se guarda en la carpeta desde la que se ejecuta el programa. Así se
    # mantiene junto al trabajo cuando se corre normalmente, y la prueba
    # automática puede verificar el reporte dentro de practicas/.
    ruta_reporte = Path.cwd() / "reporte_recoleccion.txt"
    with open(ruta_reporte, "w", encoding="utf-8") as archivo:
        archivo.write("REPORTE DE RECOLECCIÓN DE DATOS\n")
        archivo.write("=" * 34 + "\n\nRESUMEN DEL EXPERIMENTO\n")
        for clave, valor in resumen.items():
            archivo.write(f"{clave}: {valor}\n")

        archivo.write("\nCONDICIONES EXPERIMENTALES\n")
        archivo.write(f"Viscosidad del aire: {condiciones[0]}\n")
        archivo.write(f"Densidad del aceite: {condiciones[1]}\n")
        archivo.write(f"Voltaje aplicado: {condiciones[2]}\n")
        archivo.write(f"Distancia entre placas: {condiciones[3]}\n")

        archivo.write("\nDETALLE DE CADA GOTA\n")
        for i, (carga, n, estimacion) in enumerate(detalle_gotas(cargas_medidas), 1):
            archivo.write(
                f"Gota {i}: carga = {carga:.6e} C, n = {n}, "
                f"estimación = {estimacion:.6e} C\n"
            )

    print(f"El reporte se guardó en: {ruta_reporte}")


if __name__ == "__main__":
    main()
