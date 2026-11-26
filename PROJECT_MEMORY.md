# RNG Intelligence Lab — Memoria persistente del proyecto

- Versión de memoria: 0.5.2 (revisión estática y reproducción independiente de E02; propuesta pendiente de sincronización en Git)
- Fecha de inicialización: 2026-11-25 (Perú)
- Estado: Sprint 00 validado; E01 publicado y revisado; E02 publicado en review/e02, con revisión estática favorable y resultados reproducidos independientemente; integración en main pendiente; sin datos reales
- Responsable de decisiones: responsable técnico del proyecto
- Repositorio confirmado por el usuario: `https://github.com/CuevaBenjamin-dev/rng-intelligence-lab` (rama `main`, commit inicial `a0b32a9`; visibilidad pública ratificada por el responsable en S003; E01 `1fb9477`; último commit revisado en main `ec0d381`; rama de revisión `review/e02`, commit `ffca9ddb7e7d2a44d0781994f1f73a9c94237751`)
- Fuente de verdad: versión confirmada de este archivo en Git, junto con el código, pruebas y evidencias referenciadas.

## 1. Resumen para retomar el proyecto

Se investiga si un sistema de un cliente que genera enteros entre 1 y 36 puede presentar sesgos o dependencias observables que permitan anticipar sus resultados por encima de referencias estadísticas. El cliente desea evaluar la predictibilidad para reforzar el sistema. El trabajo se plantea como auditoría de seguridad e imparcialidad autorizada, no como herramienta de apuestas ni de intervención sobre usuarios reales.

El responsable técnico ha indicado que podría haber reglas adaptativas vinculadas a la cantidad de espectadores y a los números que los participantes indican antes del resultado. No se ha demostrado que estas variables influyan realmente ni que exista un mecanismo adaptativo. No se han proporcionado datos históricos, código, URL, acceso al sistema, especificación del RNG ni autorización escrita con alcance verificable. No hay resultados experimentales reales. El control estadístico sintético E00 ya fue reproducido en el entorno local. E01 ya está implementado y publicado; su resultado sintético fue reproducido independientemente. E02 ya evalúa localmente dependencia temporal sintética con marginal uniforme. E02 fue revisado estáticamente y sus resultados sintéticos reproducidos independientemente. El siguiente hito es sincronizar la memoria 0.5.2 en review/e02, verificar la versión remota, integrar la rama en main tras revisión humana y formalizar T004/T005 antes de usar datos reales. El objetivo final permanece: evaluar con evidencia si el sistema del cliente es predecible, determinar condiciones y límites, recomendar refuerzos y revalidar; no se presume vulnerabilidad.

## 2. Hechos, afirmaciones e incertidumbres

| ID | Tipo | Contenido | Estado |
|---|---|---|---|
| F01 | Información aportada | Rango declarado: enteros del 1 al 36. | Reportado; no verificado externamente |
| F02 | Información aportada | Hay personas que observan la interfaz y algunas indican qué número creen que saldrá. | Reportado |
| F03 | Información aportada | Se podrían observar resultados históricos en el momento; no hay dataset entregado. | Reportado; acceso pendiente |
| F04 | Objetivo aportado | Evaluar la predictibilidad y reforzar posteriormente el sistema. | Reportado |
| H01 | Hipótesis | Salidas uniformes e independientes de las observaciones previas. | Sin probar |
| H02 | Hipótesis | Sesgo marginal o dependencia temporal en el RNG. | Sin probar |
| H03 | Hipótesis | Dependencia respecto al número de espectadores. | Sin probar |
| H04 | Hipótesis | Dependencia respecto a las selecciones agregadas de participantes. | Sin probar |
| H05 | Hipótesis | Cambios de régimen, reglas o distribución con el tiempo. | Sin probar |
| H06 | Hipótesis | Los datos recientes podrían ser más informativos que los antiguos. | Sin probar |

No confundir una hipótesis con un hallazgo. Una asociación estadística no demuestra causalidad ni manipulación deliberada. Un algoritmo determinista puede seguir siendo impredecible desde su interfaz. No se conocen las reglas de negocio ni si hay premios, dinero o apuestas involucrados.

## 3. Objetivos y criterios de éxito

1. Establecer un protocolo reproducible, con alcance aprobado, para evaluar distribución, independencia y predictibilidad.
2. Medir si un predictor supera al azar uniforme (1/36 = 2.777... % para un único acierto exacto) y a una referencia de frecuencia histórica, fuera de muestra y sin información futura.
3. Evaluar si existe evidencia de cambios de comportamiento y dependencias contextuales cuando se disponga de datos apropiados.
4. Separar capacidad predictiva externa de hallazgos internos de diseño; reportar incertidumbre y limitaciones.
5. Recomendar mitigaciones y repetir las pruebas después de implementarlas, si se confirma una debilidad.

Un resultado negativo es válido. No se exige demostrar que el sistema sea vulnerable. No superar el azar tampoco prueba seguridad criptográfica. El éxito es una conclusión sustentada en evidencia, no un porcentaje predeterminado.

## 4. Límites de seguridad, privacidad e imparcialidad

- Antes de conectar o probar el sistema real: documentar autorización, titular, activos, entorno, técnicas permitidas, volumen, periodo, tratamiento de datos y contacto responsable.
- Trabajar inicialmente con datos sintéticos, después con exportaciones aprobadas y preferentemente en una réplica aislada. No automatizar interacciones reales ni emitir predicciones operativas para apuestas o decisiones contra participantes.
- No recopilar identificadores personales, credenciales, cookies o tokens. Priorizar conteos agregados y datos anonimizados. No publicar secretos ni datasets del cliente en GitHub, aunque sea privado.
- No alterar las probabilidades para perjudicar a los participantes. Si hay dinero o premios, confirmar obligaciones de imparcialidad y revisión normativa con el cliente.
- No usar información posterior al sorteo como entrada del modelo. Mantener separadas fuentes externas e internas.
- Reportar debilidades de forma privada al responsable autorizado, con evidencia, impacto, limitaciones y mitigación.

El repositorio es público por decisión del responsable (D006). Solo publicar código, datos sintéticos y documentación genérica no confidencial. Los datos reales, identificadores, detalles de acceso, evidencias y hallazgos específicos del cliente deben permanecer en almacenamiento separado y autorizado; en la memoria pública, conservar únicamente referencias no identificativas y estados que sea legítimo publicar.

## 5. Protocolo científico propuesto (por aprobar)

- Definir antes de cada experimento las hipótesis, métricas primarias, tamaño de muestra, periodo, criterios de inclusión y método de comparación. Estimar tamaño de muestra por potencia estadística; no asumir que una cantidad fija basta para todos los efectos.
- Capturar eventos en orden y con marca temporal UTC; conservar metadatos, procedencia y versión del sistema cuando esté disponible.
- Explorar calidad de datos, faltantes, duplicados y distribución. Probar uniformidad (chi-cuadrado con supuestos apropiados), independencia temporal y asociaciones contextuales. Considerar pruebas de permutación válidas para la estructura temporal.
- Comparar predictor uniforme, referencia de frecuencia histórica y, únicamente si los datos lo justifican, modelos estadísticos o ML. Separar cronológicamente entrenamiento, validación y prueba final. No ajustar hiperparámetros usando la prueba final.
- Medir exactitud top-1, log loss, calibración y métricas secundarias como top-k si se definen previamente. Reportar intervalos, tamaño del efecto, comparación contra referencias y ajuste por pruebas múltiples. Si hay dependencia temporal, emplear inferencia apropiada (por ejemplo, remuestreo por bloques cuando corresponda).
- Registrar predicciones y su hora antes del resultado durante evaluaciones prospectivas autorizadas y aisladas; no modificar el conjunto de prueba tras observar sus resultados.
- Investigar concept drift con ventanas de entrenamiento de tamaños comparados en validación; no eliminar datos antiguos sin justificación. Distinguir deriva de distribución de cambio en la relación entradas-resultado.
- Separar correlación y causalidad: probar condiciones controladas, aleatorizar el orden de condiciones cuando sea viable y repetir corridas independientes.

### Experimentos candidatos (no ejecutados sobre el cliente)

| ID | Pregunta | Condición |
|---|---|---|
| E00 | ¿El laboratorio funciona con una fuente uniforme? | Control sintético local |
| E01 | ¿Detecta desviaciones conocidas? | Control sintético con sesgo predefinido |
| E02 | ¿Detecta dependencia temporal? | Secuencia sintética dependiente |
| E03 | ¿Cambia la distribución según espectadores? | Réplica autorizada, condiciones controladas |
| E04 | ¿Cambia según selecciones agregadas? | Réplica autorizada, sin usuarios reales |
| E05 | ¿Hay deriva o cambios de versión? | Corridas y ventanas comparables |
| E06 | ¿Se replica un hallazgo fuera de muestra? | Evaluación independiente |
| E07 | ¿La mitigación reduce el hallazgo? | Comparación antes/después autorizada |

## 6. Contrato preliminar de datos (no implementado)

| Campo | Tipo | Disponibilidad / observaciones |
|---|---|---|
| event_id | string | Identificador único, sin datos personales |
| observed_at_utc | timestamp | Momento de observación previa |
| result_at_utc | timestamp | Momento en que se revela el resultado |
| result | int 1..36 | Etiqueta; conocida después del evento |
| viewer_count | int nullable | Conteo previo al resultado, si autorizado |
| participant_count | int nullable | Conteo agregado previo |
| selections_1_to_36 | array[36] nullable | Conteos agregados previos, si permitidos |
| previous_result | int nullable | Solo último resultado ya revelado |
| elapsed_seconds | number nullable | Tiempo transcurrido medido antes de predecir |
| source_version | string nullable | Versión aprobada; campo de auditoría |
| source | enum | synthetic / authorized_export / authorized_test |
| experiment_id | string nullable | Referencia de corrida |

Los campos nulos son desconocidos, no cero. Determinar latencia, reloj, frecuencia de eventos, momento de cierre de selecciones, disponibilidad de variables y mecanismo de exportación antes de fijar el esquema definitivo. Una variable visible solo a un administrador no debe presentarse como accesible a un usuario externo.

## 7. Arquitectura y tecnologías

### MVP local

Python 3.11+ (propuesta compatible; no fijar una versión exacta hasta comprobar el entorno), biblioteca estándar, CSV o archivos locales cuando se necesiten, Git, VS Code. Primer control sin dependencias externas. Incorporar NumPy, pandas/Polars, SciPy y scikit-learn cuando los experimentos lo requieran. Pruebas automatizadas y reproducibilidad desde el inicio.

### Evolución candidata, no aprobada ni instalada

Captura autorizada -> validación -> almacenamiento -> análisis estadístico -> evaluación de modelos -> reporte de auditoría.

- Captura: exportación primero; API o WebSocket únicamente si se autoriza y es necesario.
- Almacenamiento: PostgreSQL cuando existan volúmenes y consultas que lo justifiquen.
- Modelos: frecuencia, regresión multinomial, Markov, árboles/XGBoost; River y detección de cambios si se confirma deriva. LSTM/GRU/Transformers solo si hay evidencia y datos suficientes.
- Operación: FastAPI, dashboard Angular/Next.js, Docker Compose, GitHub Actions, MLflow, Prometheus/Grafana según necesidad; Redis solo si se justifica.
- Infraestructura futura: VPS Hostinger KVM 4 para cargas CPU razonables. Capacidad, disponibilidad, aislamiento y costos deben verificarse antes del despliegue. No se necesita GPU para iniciar.

No adoptar todas las tecnologías a la vez. No desplegar, conectar al cliente ni entrenar modelos complejos antes de validar las fases previas.

## 8. Roadmap y backlog

| ID | Tarea | Estado | Criterio de aceptación |
|---|---|---|---|
| T001 | Inicializar memoria, instrucciones y README | Completada (commit inicial) | Revisión humana y commit inicial |
| T002 | Crear repositorio y entorno local | Completada según evidencia S002/S003 | Repo local y remoto sincronizados; visibilidad pública ratificada |
| T003 | Ejecutar control sintético E00 | Completada (reproducido en Windows) | Script reproducible y pruebas pasan en entorno local |
| T004 | Confirmar alcance y requisitos del cliente | Pendiente | Autorización, reglas, fuentes, entorno y disponibilidad documentados |
| T005 | Formalizar protocolo y tamaño muestral | Pendiente | Métricas, hipótesis y partición definidos antes de probar |
| T006 | Implementar controles sintéticos E01/E02 | E01 publicado y revisado; E02 publicado en review/e02, revisión estática favorable y reproducción independiente coincidente; integración en main pendiente | Señales conocidas detectadas y control uniforme interpretado correctamente |
| T007 | Diseñar captura y validar dataset aprobado | Bloqueado por T004 | Esquema, calidad, procedencia y tiempos comprobados |
| T008 | Ejecutar auditoría estadística | Bloqueado por T005/T007 | Informe reproducible con incertidumbre |
| T009 | Comparar modelos, si se justifica | Bloqueado por T008 | Evaluación fuera de muestra y comparación con referencias |
| T010 | Recomendar mitigaciones y revalidar | Pendiente | Informe privado y comparación antes/después si corresponde |
| T011 | API, dashboard y despliegue | Diferido | Solo si existe valor comprobado y aprobación |

## 9. Registro de decisiones (ADR resumido)

| ID / fecha | Decisión | Motivo | Estado |
|---|---|---|---|
| D001 / 2026-11-25 | Memoria Markdown versionada | Continuidad entre humanos, ChatGPT y agentes | Solicitado por el usuario |
| D002 / 2026-11-25 | Nombre RNG Intelligence Lab y propuesta de repo privado | Identificación y confidencialidad | Nombre confirmado; visibilidad reemplazada por D006 |
| D003 / 2026-11-25 | Python local y control sintético antes de ML | Reducir complejidad y establecer referencia | Implementado y reproducido (E00) |
| D004 / 2026-11-25 | Mantener alcance defensivo y no buscar confirmar una vulnerabilidad | Validez científica e imparcialidad | Propuesto como requisito de trabajo |
| D005 / 2026-11-25 | Separar PROJECT_MEMORY.md de AGENTS.md | Memoria de hechos frente a reglas de trabajo | Implementado en el commit inicial |
| D006 / 2026-11-25 | Mantener el repositorio público | Decisión explícita del responsable; publicar solo material genérico y sintético | Aprobado; reemplaza la visibilidad de D002 |
| D007 / 2026-11-25 | E01 con biblioteca estándar, P(1)=0.08, 100×3600 por escenario, Pearson a α=0.05 | Control sintético reproducible | Implementado y publicado; corresponde a D006 en la memoria remota anterior a la reconciliación |
| D008 / 2026-11-25 | Publicación de E01 sintético en main | Decisión de mantener el repositorio público; solo simulación | Publicado; corresponde a D007 en la memoria remota anterior a la reconciliación |
| D009 / 2026-11-26 | E02: contar repeticiones adyacentes y calibrar con 199 permutaciones condicionales por corrida; 100 corridas de 3600 por escenario, α=0.05, cadena con repetición adicional 0.02 | Aislar orden temporal de frecuencias marginales sin dependencias externas | Implementado y verificado localmente; validez condicionada a intercambiabilidad bajo H0 |

Para cambios importantes registrar contexto, alternativas, decisión, consecuencias, evidencia y estado (propuesta/aprobada/reemplazada).

## 10. Evidencia y resultados

No hay resultados del cliente. Las gráficas y porcentajes mostrados anteriormente en la conversación fueron ejemplos hipotéticos, no mediciones. La referencia teórica de 1/36 sí es una propiedad matemática bajo uniformidad.

### E00 — control local

Artefactos preparados: `src/baseline.py`, `tests/test_baseline.py`. Genera una secuencia uniforme sintética reproducible con un PRNG de simulación (no criptográfico), entrena una referencia de frecuencia en el segmento inicial y la compara con una selección uniforme independiente en el segmento final. No es una auditoría criptográfica. Ejecución verificada en el entorno de preparación (Python 3.13.5): `python -m src.baseline` produjo 8 000 eventos de entrenamiento y 2 000 de prueba; referencia uniforme teórica 2.78 %, selector uniforme independiente 2.75 %, referencia de frecuencia histórica 2.80 %. `python -m unittest discover -s tests -v`: 4 pruebas superadas. No se realizó inferencia estadística formal ni se probó el sistema del cliente.

**Reproducción local S002 (2026-11-25, según salida aportada por el responsable):** Python 3.14.2; Git 2.50.0.windows.1. `python -m src.baseline`: 8 000 eventos de entrenamiento, 2 000 de prueba, referencia teórica 2.78 %, selector uniforme 2.75 %, frecuencia histórica 2.80 %. `python -m unittest discover -s tests -v`: 4/4 pruebas aprobadas en 0.019 s (`test_accuracy`, `test_evaluation`, `test_invalid_count`, `test_range_and_reproducibility`). Commit inicial `a0b32a9`, mensaje `chore: initialize RNG Intelligence Lab`, seis archivos, push a `origin/main` exitoso. Las diferencias observadas no prueban predictibilidad ni seguridad. No se dispone de evidencia del cliente.

### E01 — control sintético de sesgo marginal

Código: `src/statistical_audit.py`, `src/experiment_e01.py`; pruebas: `tests/test_statistical_audit.py`. Escenarios uniforme y sesgado, P(1)=0.08, P(2..36)=0.92/35. 100 corridas por escenario, 3600 observaciones por corrida; frecuencia esperada 100 por categoría. Semillas maestras 20261125 y 20261126, subsemillas de 64 bits. Pearson con 35 grados de libertad, α=0.05, umbral 49.802 (NIST/SEMATECH: https://www.itl.nist.gov/div898/handbook/eda/section3/eda3674.htm). El código usa la biblioteca estándar.

| Escenario | Rechazos | Tasa | Conteo agregado categoría 1 |
|---|---:|---:|---:|
| Uniforme | 4/100 | 4 % | 9764/360000 (2.71 %) |
| Sesgado | 100/100 | 100 % | 29001/360000 (8.06 %) |

Codex reportó ejecución local en Python 3.14.2 de E00 y E01 y 13/13 pruebas aprobadas. La revisión posterior de ChatGPT leyó los nueve archivos del commit `ec0d381f98fe96348e10ec70404bcebf052d7391` mediante GitHub y reprodujo independientemente los conteos y tasas usando Python 3.13.5 y la misma lógica y semillas. Verificó el cuantil con SciPy (49.80184956820181). No se pudo clonar el repositorio en el entorno de ejecución por falta de resolución DNS; no se ejecutó allí la suite original de 13 pruebas. La reproducción independiente no equivale a ejecutar los archivos originales. No hay defecto bloqueante identificado en E01 mediante revisión estática; el 4 % es compatible con α=0.05 y el 100 % no garantiza sensibilidad ante sesgos menores. La prueba marginal no evalúa independencia temporal ni certifica seguridad criptográfica. Sin datos del cliente.

### E02 — control sintético de orden temporal

**Protocolo fijado en README antes de ejecutar el experimento:** H0 operativa: secuencia iid en el tiempo; el control negativo es uniforme. Condicionando en los conteos, H0 implica intercambiabilidad de todos los órdenes. H1 dirigida: exceso de repeticiones consecutivas. Estadístico `T=Σ 1[X_t=X_(t−1)]`. Cada corrida se compara con 199 permutaciones completas de sus propios valores; `p=(1+#{T_perm≥T_obs})/200`, con empates incluidos, y se rechaza si `p≤0.05`. La prueba condicional mantiene los conteos fijos. El control positivo inicia uniforme y en cada paso repite el valor anterior con probabilidad 0.02 o extrae uno uniforme nuevo; su marginal estacionaria es uniforme, mientras `P(X_t=X_(t−1))=0.02+0.98/36`, superior a `1/36`. La prueba de uniformidad marginal de E01 no sustituye este contraste de orden; su referencia chi-cuadrado tampoco debe aplicarse sin más a observaciones dependientes.

Parámetros: 100 corridas por escenario, 3600 observaciones y 199 permutaciones por corrida, α=0.05; semillas maestras 20261127 (independiente) y 20261128 (dependiente), con subsemillas de 64 bits separadas para datos y permutaciones. Implementación en `src/temporal_audit.py`, `src/experiment_e02.py` y `tests/test_temporal_audit.py`, solo biblioteca estándar.

Ejecución local en Python 3.14.2 el 2026-11-26: control independiente 3/100 rechazos, tasa 3 % e intervalo descriptivo de Wilson al 95 % de 1.0 %–8.5 %; control dependiente 100/100, tasa 100 % e intervalo 96.3 %–100 %. Media de repeticiones adyacentes: 99.8 y 167.1. La categoría 1 apareció 10006/360000 (2.78 %) y 9904/360000 (2.75 %) respectivamente. Las 20 pruebas unitarias pasaron en una ejecución preliminar; la validación final se registra en S005. La tasa 3 % no exige cero falsos positivos; el 100 % describe solo este mecanismo y parámetros. Las subsemillas del PRNG hacen el resultado reproducible, no prueban independencia matemática entre corridas. La prueba detecta el patrón dirigido, no toda dependencia; la intercambiabilidad puede fallar también por deriva de la marginal. La resolución mínima de `p` es 0.005. No hay datos del cliente ni inferencia sobre su sistema.

**Revisión metodológica preliminar S006 (2026-11-26):** se leyó la memoria local v0.5.0 y el informe de Codex. Se recalcularon las expectativas teóricas de repeticiones para 3599 pares adyacentes: 3599/36 = 99.972222 y 3599 × (0.02 + 0.98/36) = 169.952778; son coherentes con las medias reportadas de 99.8 y 167.1. Se recalcularon los IC Wilson del 95 % para 3/100 (1.02545 %–8.45194 %) y 100/100 (96.30065 %–100 %). El mínimo p es 1/200 = 0.005. Se verificó que la corrección de Monte Carlo y la alternativa unilateral descritas son coherentes con el diseño condicionado a los conteos bajo intercambiabilidad. Esta revisión no reproduce las corridas, no inspecciona los tres archivos de E02 ni ejecuta las 21 pruebas; los resultados de ejecución siguen siendo evidencia reportada por Codex. No hay evidencia del sistema real.

**Revisión de código y reproducción independiente S007 (2026-11-26):** se inspeccionaron los tres archivos Python nuevos y el README de review/e02. Se comprobó el generador estacionario, el estadístico de repeticiones, las permutaciones sobre copias, la conservación de conteos, los empates, la corrección Monte Carlo, la regla de rechazo y el cálculo de Wilson; no se identificaron defectos bloqueantes dentro del alcance sintético. Se reprodujo la lógica de E02 por separado en Python 3.13.5 con las semillas y parámetros publicados: independiente 3/100 rechazos, media 99.77, categoría 1: 10006; dependiente 100/100 rechazos, media 167.13, categoría 1: 9904. Coincide con las cifras redondeadas de Codex. No se ejecutó la suite original de 21 pruebas desde ChatGPT: la conexión GitHub permitió leer los archivos, pero el entorno local no pudo resolver github.com. La ejecución independiente no sustituye la ejecución de la suite original. Mejoras no bloqueantes: prueba explícita de no mutación de entrada, prueba de borde p=0.05 y, cuando se justifique, centralización de validadores. No hay datos ni evidencia del cliente.

## 11. Flujo de trabajo y actualización de la memoria

1. Antes de trabajar: leer `PROJECT_MEMORY.md`, `AGENTS.md`, código y pruebas relevantes; verificar rama y estado del repositorio.
2. Seleccionar una tarea pequeña del backlog y definir aceptación. No asumir decisiones que no han sido aprobadas.
3. Implementar, ejecutar pruebas, revisar diff y registrar comandos, resultados reales y limitaciones.
4. Actualizar el resumen, backlog, decisiones, evidencias y siguiente paso en esta memoria. No borrar decisiones históricas; marcar reemplazos. No copiar conversaciones completas ni secretos.
5. Hacer commit descriptivo y sincronizar tras revisión humana. La historia Git conserva versiones previas; las conversaciones no son la única fuente de continuidad.
6. En una conversación nueva, aportar este archivo o solicitar su lectura desde un repositorio accesible. ChatGPT no sincroniza automáticamente el archivo local; Codex debe abrir el repo correcto. No afirmar que el archivo se actualizó sin una escritura verificada.

Formato mínimo por sesión: fecha, tarea, cambios, pruebas ejecutadas y resultado, decisiones nuevas, pendientes, próximo paso y referencia al commit si existe (no inventar hashes).

Cuando la memoria crezca, trasladar detalles extensos a archivos `docs/experiments/`, `docs/adr/` o reportes y enlazarlos aquí, conservando el resumen operativo y la trazabilidad. El usuario pidió guardar todo lo relevante, no duplicar datos brutos o contenido sensible.

## 12. Historial de sesiones

### 2026-11-25 — S001: diseño e inicialización

- Definidos el problema, hipótesis, límites de alcance, referencia teórica, roadmap y arquitectura candidata.
- Preparados memoria, instrucciones para agentes, README, exclusiones de Git y control sintético local.
- Control sintético E00 ejecutado en el entorno de preparación: cuatro pruebas superadas; resultados en sección 10.
- Sin conexión al cliente; no se afirma acceso ni predictibilidad. Sin repositorio remoto confirmado.
- Próximo paso: descargar, revisar, ejecutar control y pruebas en Windows/VS Code; crear repo privado y confirmar alcance del cliente.

### 2026-11-25 — S002: reproducción local y publicación inicial

- El responsable compartió salida de PowerShell y captura de GitHub; se confirma la inicialización, reproducción de E00 y sincronización inicial según esa evidencia.
- Entorno local: Windows / PowerShell, Python 3.14.2, Git 2.50.0.windows.1. No se instalaron dependencias adicionales para E00. Los avisos LF/CRLF no bloquearon el commit.
- Rama `main` enlazada a `origin/main`; commit inicial `a0b32a9`.
- Incidencia I001: el repositorio figura como **Public** en la captura. Cambiar a **Private** y comprobar el historial de exposición; si hubiera información confidencial o secretos, evaluar exposición y rotar credenciales. No añadir datos del cliente al repositorio.
- Se mantiene la separación entre hechos, hipótesis y evidencia. No se ha conectado al sistema del cliente ni se ha confirmado el alcance de autorización.
- Próximo paso: confirmar privacidad, sincronizar esta memoria, luego diseñar e implementar T006/E01 (control sintético con sesgo conocido), seguido de E02 (dependencia temporal sintética). En paralelo, preparar T004/T005 antes de usar datos reales.
- Criterio propuesto para E01: predefinir un generador uniforme de control, otro con distribución sintética sesgada, tamaño de muestra, prueba de uniformidad, nivel de significación y semillas; medir falsos positivos y detección en múltiples corridas. No afirmar hallazgos del cliente.
- Esta actualización de memoria se entregó como archivo local descargable; todavía no se ha confirmado su commit ni cambio de visibilidad en GitHub.

### 2026-11-25 — S003: decisión de publicación e inicio de Sprint 01

- El responsable ratificó que el repositorio permanecerá público. D006 sustituye la propuesta anterior de visibilidad privada; I001 queda cerrada como decisión de visibilidad, no como evaluación de exposición.
- Salida aportada: `git status` indica rama `main` sincronizada con `origin/main` y árbol limpio; `git diff -- PROJECT_MEMORY.md` no muestra cambios; el intento de commit no creó un commit y `git push` indica `Everything up-to-date`. No se conoce la versión efectiva de la memoria en el repositorio. El archivo adjunto a S003 sí es v0.2.0. Verificar el archivo versionado con `git show HEAD:PROJECT_MEMORY.md` y sustituir el archivo de la raíz por v0.3.0 antes de confirmar sincronización.
- E01: plan propuesto, no ejecutado. Implementar un control uniforme y otro sintético sesgado, conteos de las 36 categorías, estadístico chi-cuadrado de Pearson y decisión con alfa 0.05 y 35 grados de libertad; 3 600 observaciones por corrida, 100 corridas independientes por escenario, semillas reproducibles y probabilidad 0.08 para una categoría sintética con las 35 restantes equiprobables. Parámetros ilustrativos de validación del laboratorio, no tamaño muestral definitivo para el cliente. Reportar tasas observadas de rechazo y sus denominadores, sin exigir falsos positivos nulos ni prometer detección perfecta. Verificar que las frecuencias esperadas sean suficientes y que el umbral provenga de la distribución chi-cuadrado.
- Propuesta de implementación: `src/statistical_audit.py`, `src/experiment_e01.py`, `tests/test_statistical_audit.py` y documentación de ejecución; conservar E00 y sus pruebas. Puede usarse la biblioteca estándar con umbral fijo documentado para esta prueba; no incorporar dependencias si no hacen falta. Codex es opcional y debe leer esta memoria y AGENTS.md antes de trabajar.
- Próximo paso: sincronizar la memoria, implementar y ejecutar E01 y sus pruebas en local, registrar resultados reales y limitaciones; después E02. T004/T005 siguen pendientes y el uso de datos reales está bloqueado. No se ha modificado directamente el repositorio ni se ha ejecutado E01.

### 2026-11-25 — S004: implementación y publicación de E01

- Codex implementó los tres archivos de E01 y actualizó README y memoria; reportó 13 pruebas aprobadas y `git diff --check` sin errores. Se conservó E00. La memoria remota reporta otra ejecución de 13 pruebas y `git diff --cached --check` sin errores antes de publicar.
- Commit funcional [`1fb94778c988053a600538065cc6611f1ddb9106`](https://github.com/CuevaBenjamin-dev/rng-intelligence-lab/commit/1fb94778c988053a600538065cc6611f1ddb9106), `feat: add synthetic E01 bias detection`; commit documental [`ec0d381f98fe96348e10ec70404bcebf052d7391`](https://github.com/CuevaBenjamin-dev/rng-intelligence-lab/commit/ec0d381f98fe96348e10ec70404bcebf052d7391), `docs: record E01 GitHub publication`. Ambos fueron comprobados por el conector GitHub. No se cambió visibilidad ni se conectó al cliente.
- Incidencia I002: la memoria de GitHub en `ec0d381` indica versión 0.1.0 y renumera S002/S003 y D006/D007 respecto de la versión 0.3.0 adjunta, perdiendo parte de la continuidad. Esta propuesta conserva la historia anterior y añade los hechos posteriores, con correspondencia explícita de ADR. I001 se mantiene cerrada por decisión de visibilidad pública. I002 se cerrará tras revisar, guardar y confirmar esta versión en Git.
- Revisión independiente: resultados de E01 reproducidos en Python 3.13.5 y cuantil verificado; suite original no ejecutada por ChatGPT (ver sección 10). No se hizo commit ni push desde ChatGPT.
- Próximo paso propuesto: E02, control sintético de independencia temporal, manteniendo E00/E01. Definir antes de implementar una hipótesis nula de independencia y una alternativa sintética con marginal uniforme; calibrar el método mediante permutación y corridas reproducibles, distinguir dependencia de sesgo marginal y reportar incertidumbre. No aplicar a sistemas reales hasta aprobar T004/T005 y T007. No se ha implementado E02.

### 2026-11-26 — S005: E02 sintético y memoria reconciliada

- Se leyó íntegramente la reconciliación 0.4.0 recibida como `PROJECT_MEMORY (6).md` y se trasladó al nombre canónico `PROJECT_MEMORY.md`; la versión local pasa a 0.5.0 sin eliminar S001–S004 ni reutilizar D001–D008. I002 queda resuelta en el árbol local, pendiente de revisión y commit; no se afirma sincronización con GitHub.
- Antes de ejecutar E02 se fijaron en README H0, H1 dirigida, estadístico, permutaciones, regla de rechazo, semillas, tamaño y limitaciones. Se implementaron `src/temporal_audit.py`, `src/experiment_e02.py` y `tests/test_temporal_audit.py`; se actualizó README y esta memoria. D009 registra la decisión metodológica. E00 y E01 no se modificaron.
- Validación final en Python 3.14.2: `python -m src.baseline` terminó correctamente (2.75 % selector uniforme; 2.80 % frecuencia histórica); `python -m src.experiment_e01` reprodujo 4/100 y 100/100 rechazos; `python -m src.experiment_e02` obtuvo 3/100 y 100/100 rechazos, con intervalos y frecuencias detallados en sección 10; `python -m unittest discover -s tests -v` aprobó 21/21 pruebas; `git diff --check` salió con código 0 y solo advirtió la futura conversión LF/CRLF de dos documentos.
- Limitaciones: el control positivo representa un solo tipo de dependencia con marginal uniforme; el contraste es unilateral de repeticiones y depende de intercambiabilidad bajo H0. Los intervalos de Wilson describen incertidumbre de la tasa sobre 100 corridas seudoaleatorias. No se usaron datos del cliente ni se extrajeron conclusiones sobre él.
- Pendiente: revisión humana de E02 y de la memoria 0.5.0; después, formalizar T005 y el alcance T004 antes de cualquier dato real. No se ejecutó commit ni push en esta sesión.

### 2026-11-26 — S006: revisión metodológica preliminar de E02

- El responsable compartió la respuesta de Codex y la memoria local 0.5.0. Se comprobó que conserva S001–S005, D001–D009, las hipótesis y el objetivo final. No se renumeraron sesiones ni decisiones.
- Se verificó matemáticamente la coherencia de las expectativas, los intervalos de Wilson y la resolución mínima del valor p; detalles en sección 10. No se reprodujeron las simulaciones ni se ejecutaron los archivos originales de E02 desde ChatGPT. Las 21 pruebas aprobadas y las tasas de rechazo corresponden a la ejecución local reportada.
- Revisión de código pendiente: comprobar generación y validación de entradas, estadístico de repeticiones (incluidos casos límite), permutaciones que preserven conteos sin modificar la entrada, empates y corrección Monte Carlo, separación de subsemillas, intervalos y reproducibilidad; confirmar ausencia de regresiones con la suite. La revisión de la implementación debe distinguirse de la revisión metodológica.
- Propuesta de flujo: publicar los cambios sintéticos en una rama de revisión `review/e02` o aportar los archivos/diff para inspección, revisar y luego integrar en `main` por decisión del responsable. No se ha creado ninguna rama ni se ha hecho commit o push desde ChatGPT. I002 queda pendiente de verificar en GitHub. El repositorio sigue público por decisión D006; no publicar material confidencial.
- Próximo hito: tras la revisión de E02, formalizar T004 (alcance y autorización) y T005 (protocolo científico y tamaño muestral); mantener E03/E04 sobre el cliente bloqueados hasta contar con autorización y datos adecuados. No se ha comenzado la fase de datos reales ni se ha demostrado predictibilidad del sistema.
- Esta revisión se entrega como propuesta de memoria v0.5.1 para integrar localmente sin sobrescribir cambios posteriores.

### 2026-11-26 — S007: publicación en rama y revisión de E02

- Según la terminal aportada, se creó `review/e02`, se agregaron únicamente los cinco archivos previstos, `git diff --cached --check` no mostró errores, se creó el commit `ffca9dd` y se publicó la rama. Los avisos LF/CRLF no bloquearon el flujo.
- GitHub confirmó el [commit `ffca9ddb7e7d2a44d0781994f1f73a9c94237751`](https://github.com/CuevaBenjamin-dev/rng-intelligence-lab/commit/ffca9ddb7e7d2a44d0781994f1f73a9c94237751). La comparación con `main` (`ec0d381`) indica un commit por delante, ninguno por detrás, cinco archivos afectados, 420 inserciones y 29 eliminaciones; no se modificaron los archivos de E00/E01.
- Se completó la revisión estática de E02 y la reproducción independiente de sus dos escenarios; resultados y límites en sección 10. Las 21 pruebas originales siguen siendo evidencia de la ejecución local de Codex, no de una ejecución de ChatGPT. Se recomienda integrar tras sincronizar la memoria y revisar los cambios.
- Continuidad: el archivo remoto en `review/e02` es v0.5.0, con S001–S005 y D001–D009; su blob Git `618da8672d1271ca1551328b8e0c063278acd6b8` coincide con la memoria v0.5.0 aportada previamente. El adjunto actual v0.5.1 tiene blob normalizado `049be49600323584c30a1647ecbf965de3c7671e`, conserva S006 y no coincide con el remoto. I002: historial S001–S005 recuperado en rama de revisión, pero falta confirmar S006/S007 y la integración en main. No se presume la causa de la discrepancia.
- Se prepara esta memoria v0.5.2 partiendo del adjunto v0.5.1, conservando S001–S006 y D001–D009. Próximo paso: reemplazar el archivo canónico local, verificar versión, revisar diff, commit documental y push a review/e02; comprobar el contenido remoto y abrir/integrar pull request a main tras aprobación humana. No se hizo commit, push ni merge desde ChatGPT.
- Tras integración, priorizar T004/T005: definir alcance autorizado, requisitos de imparcialidad, disponibilidad de datos y protocolo científico. E03/E04 sobre datos del cliente siguen bloqueados; se pueden diseñar controles genéricos sintéticos si se justifica. El objetivo final sigue siendo evaluar predictibilidad con evidencia y recomendar mitigaciones/revalidación, no afirmar una vulnerabilidad.

## 13. Preguntas pendientes al cliente

- ¿Qué función cumple el sistema? ¿Hay premios, dinero o apuestas? ¿Qué propiedad de aleatoriedad exige el producto?
- ¿El cliente autoriza explícitamente esta auditoría y qué activos, condiciones y técnicas permite?
- ¿Existe ambiente de pruebas o exportación de eventos? ¿Cuántos eventos se generan y con qué frecuencia?
- ¿Qué variables se conocen antes del resultado? ¿Los conteos son fiables y se puede obtener su marca temporal?
- ¿Hay versiones, reglas documentadas o código que se pueda revisar? ¿Se generan resultados en servidor o cliente?
- ¿Qué periodo, métricas, nivel de confianza y criterio de remediación se acordarán?

## 14. Referencias técnicas iniciales

- NIST SP 800-22 Rev. 1a: https://csrc.nist.gov/pubs/sp/800/22/r1/upd1/final (pruebas sobre secuencias binarias; no aplicar directamente a 1..36 sin un mapeo y justificación apropiados; no certifica seguridad).
- NIST SP 800-90A Rev. 1: https://csrc.nist.gov/pubs/sp/800/90/a/r1/final (DRBG; referencia de diseño para revisar cuando proceda).
- scikit-learn TimeSeriesSplit: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html (validación temporal).
- GitHub: https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository
- OpenAI Codex: https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex (instrucciones persistentes AGENTS.md).

Estas referencias son puntos de partida; verificar versiones aplicables y adecuación metodológica antes de adoptar estándares o pruebas específicas.
