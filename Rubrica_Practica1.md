# Rúbrica — Práctica 1 (Tipos de datos, control de flujo y funciones)

- **Alumno:** María Fernanda Falcón Hérnandez
- **Repositorio:** fiscomp_practicas
- **Fecha de revisión:** 21 de septiembre de 2026

Revisión de la Práctica 1

## Resultado de las pruebas automáticas

Resultado: `OK`, `FALLÓ`, `OMITIDA` (la prueba no encontró el archivo o la función con el nombre que espera) o `TIEMPO` (no terminó dentro del límite de tiempo).

| Prueba | Ejercicio | Resultado | Detalle |
| --- | --- | --- | --- |
| `test_factorial` | Base (no se califica) | OK |  |
| `test_seno` | Base (no se califica) | OK |  |
| `test_coseno` | 3 | OK |  |
| `test_exponencial` | 3 | OK |  |
| `test_ln` | 3 | OK |  |
| `test_pi_guardado` | 2 | OK |  |
| `test_corre_sin_errores_y_genera_el_reporte` | 1 | OK |  |
| `test_reporte_existe` | 4 | OK |  |

## Ejercicio 1 — Carga del electrón (experimento de Millikan) — 35 pts

### Parte A — Recolección de datos — 12 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| El script de recolección corre de principio a fin y captura los datos con `input()`, convirtiendo a `int`/`float` lo que regresa como `str` | 3 | 3 |
| `str`: nombre del experimento y del responsable | 1 | 1 |
| `float`/`int`: condiciones del experimento y mediciones | 1 | 1 |
| `bool`: alguna condición con criterio razonable (p. ej., si la gota es válida) | 1 | 1 |
| `tuple`: condiciones que no cambian entre gotas (voltaje, distancia entre placas, viscosidad) | 1 | 1 |
| `list`: carga medida de cada gota, en Coulombs (al menos 3 o 4 gotas) | 1 | 1 |
| `set`: valores únicos medidos | 1 | 1 |
| `dict`: resumen final del experimento, completado en la Parte B | 1 | 1 |
| Datos coherentes: unidades en Coulombs, orden de magnitud cercano a 1e-19, experimento (real o inventado) con sentido | 2 | 1 |
| **Subtotal Parte A** | **12** | **11** |

**Observaciones**
- Tu script corre completo (ahora también pasa la prueba automática: separaste el nombre del experimento y el del responsable en dos `input()`, en vez de pedirlos juntos separados por coma). Usas `str`, `float`/`int`, `bool` (`es_valida`), `tuple` (`condiciones`), `list`, `set` (`cargas_unicas`) y `dict` (`resumen`).
- Corregiste el orden de las etiquetas de las condiciones en el reporte (viscosidad, densidad, voltaje y distancia, en el mismo orden en que las capturas). Bien.
- El `reporte_recoleccion.txt` que subiste todavía tiene los datos de una corrida de prueba (todo en 1, error relativo de 6e18); vuelve a correr tu script con datos que se parezcan a un experimento real y sube ese reporte.

### Parte B — Estimación de la carga del electrón — 15 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Función que estima la carga del electrón (`estimar_carga_electron` u otro nombre claro) en el mismo script; regresa la estimación de `e` y su desviación estándar | 3 | 3 |
| Primera aproximación con el mínimo de las cargas medidas | 2 | 2 |
| `n = round(carga / e_aproximada)` para cada gota | 2 | 2 |
| Estimación por gota `carga / n`; el promedio de esas estimaciones es la estimación final | 2 | 2 |
| Desviación estándar calculada correctamente sobre las estimaciones por gota (fórmula explícita; población o muestra, pero consistente) | 3 | 3 |
| Error relativo contra `e = 1.602176634e-19 C` (con `error_relativo()` del curso o una versión propia), agregado al `dict` del resumen | 3 | 3 |
| **Subtotal Parte B** | **15** | **15** |

**Observaciones**
- Ajustaste `estimar_carga_electron` para que reciba `cargas_medidas` y regrese `(e_estimada, desviación)`; ya no recibe pares `[carga, válida]` ni regresa la suma de las estimaciones. Corregido.
- `min`, `round` (con protección para `n = 0`) y la estimación por gota siguen igual de bien.
- Cambiaste la desviación estándar a la suma de los cuadrados de las diferencias respecto al promedio, en vez de `sqrt(E[x^2] - media^2)`; con eso evitas la pérdida de precisión que te señalé. Corregido.
- Sigues calculando el error relativo con `error_relativo` y 1.602176634e-19, y agregándolo al dict.

### Reporte — 8 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Genera un archivo de reporte (por ejemplo `reporte_recoleccion.txt`) con `open()` y `write()` (o `print(file=...)`), en la carpeta del script o en una ruta que funcione en cualquier computadora | 3 | 3 |
| Incluye el resumen del `dict`: carga estimada, desviación estándar y error relativo | 3 | 3 |
| Incluye el detalle de cada gota: carga medida, `n` y estimación individual | 2 | 2 |
| **Subtotal Reporte** | **8** | **8** |

**Observaciones**
- Tu reporte incluye el resumen, las condiciones y el detalle por gota (carga, `n`, estimación individual), y ahora sí está el archivo `reporte_recoleccion.txt` en tu repositorio.

## Ejercicio 2 — π con el método de Leibniz — 15 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Suma correctamente la serie de Leibniz (`1 − 1/3 + 1/5 − …`, multiplicada por 4) con muchos términos; no vale copiar `math.pi` ni escribir el valor a mano | 5 | 5 |
| `PI` queda guardado como constante en un archivo que otros programas puedan importar (por ejemplo `fiscomp/constantes.py`), con un valor cercano al real (error relativo menor que 1e-4) y sin volver a correr la suma en cada import | 4 | 4 |
| Comentario que indica qué tan cerca quedaste, comparando contra `math.pi` | 3 | 3 |
| Explicación de por qué no se puede llegar más lejos en un tiempo razonable (convergencia lenta, error del orden de 1/N) | 3 | 3 |
| **Subtotal Ejercicio 2** | **15** | **15** |

**Observaciones**
- Tu `pi_leibniz.py` suma 1,000,000 de términos, imprime el error absoluto contra `math.pi` y `fiscomp/constantes.py` guarda `PI = 3.1415916535897743` (`test_pi_guardado` OK).
- Agregaste el comentario que faltaba: cuantificas qué tan cerca quedaste (error absoluto ≈ 1e-6) y explicas por qué no se puede llegar más lejos en un tiempo razonable (convergencia como 1/N, se necesitarían del orden de 10^15 términos para llegar a EPS). Completo.

## Ejercicio 3 — El resto de las funciones especiales — 35 pts

### `coseno(x)` — 10 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Da resultados correctos en los valores de prueba (`test_coseno`; crédito parcial por valor de `x`) | 6 | 6 |
| Serie de Taylor con `EPS` como criterio de corte, siguiendo el patrón de `seno()` | 2 | 2 |
| Reutiliza `factorial()`, no usa `math`, código claro y con docstring o comentarios | 2 | 2 |
| **Subtotal `coseno`** | **10** | **10** |

### `exponencial(x)` — 10 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Da resultados correctos en los valores de prueba (`test_exponencial`; crédito parcial por valor de `x`, incluidos los negativos) | 6 | 6 |
| Serie de Taylor con `EPS` como criterio de corte, siguiendo el patrón de `seno()` | 2 | 2 |
| Reutiliza `factorial()`, no usa `math`, código claro y con docstring o comentarios | 2 | 2 |
| **Subtotal `exponencial`** | **10** | **10** |

### `ln(x)` — 15 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Da resultados correctos en los valores de prueba (`test_ln`; crédito parcial por valor de `x`; 2.0, 5.0 y 10.0 requieren una serie que converja rápido fuera del entorno de `x = 1`) | 8 | 8 |
| Serie con `EPS` como criterio de corte (no un número fijo de términos) y sin `math` | 4 | 4 |
| Funciona para cualquier `x > 0` (serie de `ln((1+y)/(1-y))`, reducción de rango u otra) y lo documentas: qué serie usaste, para qué rango es válida y por qué | 3 | 3 |
| **Subtotal `ln`** | **15** | **15** |

**Observaciones del Ejercicio 3**
- `coseno`, `exponencial` y `ln` pasan todas las pruebas (8/8, 7/7, 6/6), usan `EPS` y `factorial()`, y ninguna usa `math`.
- Agregaste docstrings a `coseno` y `exponencial`, y quitaste el comentario sobre el bug que ya habías corregido. Con eso las tres funciones quedan completas.
- Tu `ln` sigue muy bien documentada: reduces `x` a `[0.5, 1)` con potencias de 2 y usas la serie de `y = (a-1)/(a+1)` más `m*ln(2)`.

## Ejercicio 4 — Error de sus funciones especiales — 15 pts

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Comparas `seno`, `coseno`, `exponencial` y `ln` contra `math.sin`, `math.cos`, `math.exp` y `math.log` con `error_relativo()`, para varios valores de `x` que permitan ver dónde crece el error | 5 | 5 |
| Reporte con los resultados escrito con `open()` en modo escritura (`w`) y `write()` (unidad 04), legible: `x`, valor aproximado, valor real y error | 3 | 3 |
| Identificas al menos un valor de `x` donde el error es sorprendentemente alto | 3 | 3 |
| Explicas por qué: el valor "real" queda muy cerca de cero y el error *relativo* se dispara aunque el error absoluto sea chico | 4 | 4 |
| **Subtotal Ejercicio 4** | **15** | **15** |

**Observaciones**
- Tu `ejercicio4_errores.py` compara las cuatro funciones en 6-8 valores de x (incluye múltiplos de `pi` y valores grandes) y escribe una tabla con aproximado, real y error relativo; ahora sí subiste `reporte_ejercicio4.txt` al repositorio.
- Tu análisis identifica correctamente los casos donde el error se dispara (seno cerca de múltiplos de pi, coseno cerca de pi/2) y lo explicas porque el valor real es cercano a 0. Muy bien.

## Reto opcional — crédito adicional (hasta 5 pts)

| Criterio | Máx | Obt. |
| --- | ---: | ---: |
| Reducción de rango en `seno`/`coseno` (llevar `x` a un intervalo chico con identidades trigonométricas) y evidencia de que mejora la precisión para `x` grande | 5 | 0 |

**Observaciones**
- Este reto era opcional y no lo entregaste.

## Penalizaciones (criterios transversales)

| Concepto | Rango | Aplicado |
| --- | --- | ---: |
| Retraso: la entrega registrada cambió de repositorio después de la fecha de entrega y de que tu Práctica 1 ya estaba calificada | −2 | −2 |
| Retrabajo: buena parte del código se corrigió después de haber recibido la calificación, incorporando las observaciones de esa revisión | −4 | −4 |
| Entrega difícil de seguir: hay versiones distintas del mismo archivo y no se distingue cuál es la final | −1 a −2 | 0 |

No descuento por los nombres de tus archivos, de tus funciones ni por las carpetas que elegiste, mientras se entienda dónde está cada cosa y funcione.

**Observaciones**
- Después de haberte entregado la calificación de la Práctica 1 (con la que ya tenías un resultado bastante bueno, 91.5/100), cambiaste de repositorio y corregiste varias de las observaciones que te hice: los docstrings de `coseno` y `exponencial`, la firma y la desviación estándar de `estimar_carga_electron`, el orden de las etiquetas del reporte, la explicación del Ejercicio 2 y subir el reporte del Ejercicio 4.
- Esas correcciones sí mejoran tu entrega, pero te aplico una penalización de 6 puntos en total: 2 por el retraso (el cambio de repositorio ocurrió después de la fecha de entrega y de que tu trabajo ya estaba calificado) y 4 por el retrabajo hecho después de recibir tu calificación. No puedo subir mucho tu nota sobre el resultado que ya tenías.

## Calificación final

| Concepto | Máx | Obtenido |
| --- | ---: | ---: |
| Ejercicio 1 — Carga del electrón | 35 | 34 |
| Ejercicio 2 — π con Leibniz | 15 | 15 |
| Ejercicio 3 — Funciones especiales | 35 | 35 |
| Ejercicio 4 — Error de las funciones | 15 | 15 |
| Penalizaciones | | −6 |
| Crédito adicional | (+5) | 0 |
| **Total** | **100** | **93** |

## Comentarios generales y sugerencias

- Ya tenías un buen trabajo antes de estos cambios, y las correcciones que hiciste están bien hechas: la firma de `estimar_carga_electron`, la desviación estándar, el orden de las condiciones en el reporte y la explicación del Ejercicio 2 quedaron resueltas.
- Como te expliqué en las Penalizaciones, esta corrección llegó después de que ya tenías una calificación, así que tu nota no sube mucho respecto a la anterior.
- Todavía te falta correr tu script de recolección con datos que se parezcan a un experimento real (no los de la prueba automática) y subir ese reporte.

## Nota

La suma base es 100 pts. El reto opcional suma crédito adicional hasta 5 pts y no sustituye ningún criterio obligatorio de los ejercicios 1–4. Cuando tu trabajo muestra verificación numérica sólida aunque falte algún detalle menor, te doy crédito parcial proporcional. Si algo de esta revisión no te queda claro, coméntamelo y lo revisamos.
