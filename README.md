# RNG Intelligence Lab

Laboratorio de auditoría estadística y evaluación de predictibilidad de generadores de enteros del 1 al 36. Investigación defensiva; no hay datos del cliente en este repositorio.

## Inicio local (Windows / PowerShell)

Requisitos: Git, VS Code y Python 3.11 o superior. El control inicial no requiere paquetes externos.

```powershell
python --version
python -m src.baseline
python -m unittest discover -s tests -v
```

Si `python` no se reconoce y tienes el lanzador de Windows, usa `py -3` en su lugar. Ejecuta desde la raíz del proyecto.

El script muestra resultados de un control **sintético**, con semilla fija para reproducibilidad; usa un PRNG de simulación y no certifica seguridad criptográfica. Las tasas observadas fluctúan por azar. No implica que el sistema del cliente pueda predecirse.

## Archivos centrales

- `PROJECT_MEMORY.md`: memoria técnica, hipótesis, alcance, decisiones, evidencias y roadmap.
- `AGENTS.md`: instrucciones para agentes de desarrollo como Codex.
- `src/baseline.py`: primer control sintético E00.
- `tests/test_baseline.py`: pruebas automatizadas.

## Flujo de trabajo

Leer memoria → seleccionar tarea → implementar → probar → actualizar memoria → revisar diff → commit.

El repositorio debe ser privado; no subir datos reales del cliente, secretos ni resultados sensibles sin autorización específica. Antes de trabajar sobre un sistema real, confirmar alcance y permiso escrito.
