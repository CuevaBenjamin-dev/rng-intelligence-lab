# RNG Intelligence Lab

Laboratorio de auditoría estadística y evaluación de predictibilidad de generadores de enteros del 1 al 36. Investigación defensiva; no hay datos del cliente en este repositorio.

## Inicio local (Windows / PowerShell)

Entorno verificado: Python 3.14.2. Los controles E00, E01 y E02 usan únicamente la biblioteca estándar.

```powershell
python --version
python -m src.baseline
python -m src.experiment_e01
python -m src.experiment_e02
python -m unittest discover -s tests -v
```

Si `python` no se reconoce y tienes el lanzador de Windows, usa `py -3` en su lugar. Ejecuta desde la raíz del proyecto.

Los scripts muestran controles **sintéticos** con semillas fijas. Usan un PRNG de simulación y no certifican seguridad criptográfica ni describen el sistema del cliente.

## E01 — detección de sesgo marginal

`src.statistical_audit` genera enteros del 1 al 36 en dos escenarios: uniforme, con probabilidad `1/36` por categoría, y sesgado, con `P(1)=0.08` y `P(2)=...=P(36)=0.92/35`. Calcula frecuencias absolutas y relativas para las 36 categorías, incluidas las no observadas. Rechaza conteos inválidos y muestras con frecuencia esperada menor que 5 por categoría.

Para cada escenario, `src.experiment_e01` ejecuta 100 corridas de 3600 observaciones. Usa una semilla maestra fija (`20261125` para uniforme y `20261126` para sesgado) y deriva una subsemilla distinta por corrida. La prueba de bondad de ajuste de Pearson compara los conteos de cada corrida con `E=3600/36=100` bajo la hipótesis nula de uniformidad: `χ² = Σ(O−E)²/E`. Son 35 grados de libertad, α = 0.05 y se rechaza cuando `χ² ≥ 49.802`. El [NIST/SEMATECH e-Handbook](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3674.htm) publica `49.802` en la tabla de valores críticos de cola superior para 35 grados de libertad y 0.05, redondeado a tres decimales.

Resultado reproducido en Python 3.14.2 el 2026-11-25 (100 corridas × 3600 observaciones por escenario):

| Escenario | Rechazos | Tasa observada | Frecuencia agregada de 1 |
|---|---:|---:|---:|
| Uniforme | 4/100 | 4 % | 9764/360000 = 2.71 % |
| Sesgado | 100/100 | 100 % | 29001/360000 = 8.06 % |

El comando imprime además las frecuencias absolutas y relativas agregadas de las 36 categorías. El 4 % del control uniforme es compatible con falsos positivos muestrales; no se exige cero. El 100 % de detección se refiere solo al sesgo sintético fijado aquí, con este tamaño muestral y estas semillas; no garantiza detectar sesgos más pequeños. El test examina la distribución marginal, no la independencia temporal, la predictibilidad ni la seguridad criptográfica. Las subsemillas producen corridas seudoaleatorias reproducibles. No se usaron datos reales.

## E02 — independencia temporal sintética

**Protocolo fijado antes de ejecutar E02.** Hipótesis nula operativa H0: los valores son independientes e idénticamente distribuidos en el tiempo; el control negativo usa la distribución uniforme. Esta hipótesis implica que, condicionando en los conteos de las 36 categorías, cualquier orden de la secuencia es igualmente probable. Alternativa dirigida H1: hay exceso de repeticiones consecutivas. El estadístico predefinido es `T = Σ 1[x_t = x_(t−1)]`, para `t=2..n`; valores mayores apoyan H1.

El control positivo comienza con un valor uniforme y, para cada paso, repite el anterior con probabilidad `q=0.02`; en otro caso extrae un valor uniforme nuevo. La distribución marginal permanece uniforme: si el valor anterior es uniforme, `P(X_t=j)=q/36+(1−q)/36=1/36`. Sin embargo, `P(X_t=X_(t−1))=q+(1−q)/36`, mayor que `1/36`. Así, una marginal uniforme no implica independencia. No se interpreta el chi-cuadrado de E01 sobre esta secuencia dependiente, porque su referencia supone observaciones independientes.

En cada corrida se barajan los `n` valores observados `B=199` veces, conservando exactamente sus frecuencias y destruyendo el orden. El valor `p=(1+# {T_permutado ≥ T_observado})/(B+1)` incluye empates y nunca es cero; se rechaza si `p≤0.05`. Es una prueba condicional de exceso de repeticiones válida bajo intercambiabilidad. El procedimiento usa permutaciones aleatorias independientes con reposición, no enumera todos los órdenes. La corrección de Monte Carlo sigue a [Phipson y Smyth](https://gksmyth.github.io/pubs/PermPValuesPreprint.pdf). La intercambiabilidad es el supuesto clave; variaciones temporales de la marginal también pueden romperlo.

Parámetros fijados: `100` corridas por escenario, `n=3600`, `B=199`, `α=0.05`, semillas maestras `20261127` (negativo) y `20261128` (positivo); cada corrida usa subsemillas separadas para generación y permutación. Se reportan rechazos, tasas e intervalos descriptivos de Wilson al 95 % para las tasas sobre las 100 corridas, más frecuencias marginales descriptivas. La resolución mínima del valor `p` es `1/200=0.005`. La prueba solo tiene potencia frente al patrón de repeticiones elegido; un no rechazo no demuestra independencia general ni seguridad criptográfica. Todos los datos son sintéticos.

Resultado observado en Python 3.14.2 el 2026-11-26:

| Escenario | Rechazos | Tasa (IC Wilson 95 %) | Repeticiones consecutivas medias | Frecuencia agregada de 1 |
|---|---:|---:|---:|---:|
| Independiente | 3/100 | 3 % (1.0 %–8.5 %) | 99.8 | 10006/360000 (2.78 %) |
| Dependiente, `q=0.02` | 100/100 | 100 % (96.3 %–100 %) | 167.1 | 9904/360000 (2.75 %) |

Los intervalos cuantifican la incertidumbre de las tasas de rechazo para estas corridas seudoaleatorias. El 3 % del control es una tasa observada, no una calibración exacta del nivel nominal. La frecuencia agregada de la categoría 1 es descriptiva; la uniformidad marginal del control positivo se deduce de su mecanismo estacionario, no de una prueba sobre esos conteos. Estos resultados no se extrapolan al cliente.

## Archivos centrales

- `PROJECT_MEMORY.md`: memoria técnica, hipótesis, alcance, decisiones, evidencias y roadmap.
- `AGENTS.md`: instrucciones para agentes de desarrollo como Codex.
- `src/baseline.py`: primer control sintético E00.
- `src/statistical_audit.py`: generadores, frecuencias y prueba chi-cuadrado E01.
- `src/experiment_e01.py`: corridas y reporte sintético E01.
- `src/temporal_audit.py` y `src/experiment_e02.py`: prueba y calibración temporal E02.
- `tests/`: pruebas automatizadas de E00, E01 y E02.

## Flujo de trabajo

Leer memoria → seleccionar tarea → implementar → probar → actualizar memoria → revisar diff → commit.

El repositorio actual en GitHub es público por decisión expresa del responsable técnico. Solo se publica el laboratorio sintético: no subir datos reales del cliente, secretos ni resultados sensibles sin autorización específica. Antes de trabajar sobre un sistema real, confirmar alcance y permiso escrito.
