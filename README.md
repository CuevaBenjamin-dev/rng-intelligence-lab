# RNG Intelligence Lab

Laboratorio de auditoría estadística y evaluación de predictibilidad de generadores de enteros del 1 al 36. Investigación defensiva; no hay datos del cliente en este repositorio.

## Inicio local (Windows / PowerShell)

Entorno verificado: Python 3.14.2. Los controles E00 y E01 usan únicamente la biblioteca estándar.

```powershell
python --version
python -m src.baseline
python -m src.experiment_e01
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

## Archivos centrales

- `PROJECT_MEMORY.md`: memoria técnica, hipótesis, alcance, decisiones, evidencias y roadmap.
- `AGENTS.md`: instrucciones para agentes de desarrollo como Codex.
- `src/baseline.py`: primer control sintético E00.
- `src/statistical_audit.py`: generadores, frecuencias y prueba chi-cuadrado E01.
- `src/experiment_e01.py`: corridas y reporte sintético E01.
- `tests/`: pruebas automatizadas de E00 y E01.

## Flujo de trabajo

Leer memoria → seleccionar tarea → implementar → probar → actualizar memoria → revisar diff → commit.

El repositorio actual en GitHub es público por decisión expresa del responsable técnico. Solo se publica el laboratorio sintético: no subir datos reales del cliente, secretos ni resultados sensibles sin autorización específica. Antes de trabajar sobre un sistema real, confirmar alcance y permiso escrito.
