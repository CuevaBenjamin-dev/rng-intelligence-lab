# RNG Intelligence Lab — Memoria persistente del proyecto

- Versión de memoria: 0.1.0
- Fecha de inicialización: 2026-11-25 (Perú)
- Estado: inicialización / investigación previa a datos reales
- Responsable de decisiones: responsable técnico del proyecto
- Repositorio propuesto: `rng-intelligence-lab` (privado; URL aún no confirmada)
- Fuente de verdad: versión confirmada de este archivo en Git, junto con el código, pruebas y evidencias referenciadas.

## 1. Resumen para retomar el proyecto

Se investiga si un sistema de un cliente que genera enteros entre 1 y 36 puede presentar sesgos o dependencias observables que permitan anticipar sus resultados por encima de referencias estadísticas. El cliente desea evaluar la predictibilidad para reforzar el sistema. El trabajo se plantea como auditoría de seguridad e imparcialidad autorizada, no como herramienta de apuestas ni de intervención sobre usuarios reales.

El responsable técnico ha indicado que podría haber reglas adaptativas vinculadas a la cantidad de espectadores y a los números que los participantes indican antes del resultado. No se ha demostrado que estas variables influyan realmente ni que exista un mecanismo adaptativo. No se han proporcionado datos históricos, código, URL, acceso al sistema, especificación del RNG ni autorización escrita con alcance verificable. No hay resultados experimentales reales. El primer hito es construir un control estadístico reproducible con datos sintéticos y definir el protocolo de captura autorizado.

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
| T001 | Inicializar memoria, instrucciones y README | Archivos preparados | Revisión humana y commit inicial |
| T002 | Crear repositorio privado y entorno local | Pendiente | Repo clonado y primer commit sincronizado |
| T003 | Ejecutar control sintético E00 | Verificado en preparación; pendiente en PC del usuario | Script reproducible y pruebas pasan en entorno local |
| T004 | Confirmar alcance y requisitos del cliente | Pendiente | Autorización, reglas, fuentes, entorno y disponibilidad documentados |
| T005 | Formalizar protocolo y tamaño muestral | Pendiente | Métricas, hipótesis y partición definidos antes de probar |
| T006 | Implementar controles sintéticos E01/E02 | Pendiente | Señales conocidas detectadas y control uniforme interpretado correctamente |
| T007 | Diseñar captura y validar dataset aprobado | Bloqueado por T004 | Esquema, calidad, procedencia y tiempos comprobados |
| T008 | Ejecutar auditoría estadística | Bloqueado por T005/T007 | Informe reproducible con incertidumbre |
| T009 | Comparar modelos, si se justifica | Bloqueado por T008 | Evaluación fuera de muestra y comparación con referencias |
| T010 | Recomendar mitigaciones y revalidar | Pendiente | Informe privado y comparación antes/después si corresponde |
| T011 | API, dashboard y despliegue | Diferido | Solo si existe valor comprobado y aprobación |

## 9. Registro de decisiones (ADR resumido)

| ID / fecha | Decisión | Motivo | Estado |
|---|---|---|---|
| D001 / 2026-11-25 | Memoria Markdown versionada | Continuidad entre humanos, ChatGPT y agentes | Solicitado por el usuario |
| D002 / 2026-11-25 | Nombre RNG Intelligence Lab y repo privado | Identificación y confidencialidad | Propuesto; pendiente de revisión |
| D003 / 2026-11-25 | Python local y control sintético antes de ML | Reducir complejidad y establecer referencia | Propuesto / scaffold preparado |
| D004 / 2026-11-25 | Mantener alcance defensivo y no buscar confirmar una vulnerabilidad | Validez científica e imparcialidad | Propuesto como requisito de trabajo |
| D005 / 2026-11-25 | Separar PROJECT_MEMORY.md de AGENTS.md | Memoria de hechos frente a reglas de trabajo | Propuesto |

Para cambios importantes registrar contexto, alternativas, decisión, consecuencias, evidencia y estado (propuesta/aprobada/reemplazada).

## 10. Evidencia y resultados

No hay resultados del cliente. Las gráficas y porcentajes mostrados anteriormente en la conversación fueron ejemplos hipotéticos, no mediciones. La referencia teórica de 1/36 sí es una propiedad matemática bajo uniformidad.

### E00 — control local

Artefactos preparados: `src/baseline.py`, `tests/test_baseline.py`. Genera una secuencia uniforme sintética reproducible con un PRNG de simulación (no criptográfico), entrena una referencia de frecuencia en el segmento inicial y la compara con una selección uniforme independiente en el segmento final. No es una auditoría criptográfica. Ejecución verificada en el entorno de preparación (Python 3.13.5): `python -m src.baseline` produjo 8 000 eventos de entrenamiento y 2 000 de prueba; referencia uniforme teórica 2.78 %, selector uniforme independiente 2.75 %, referencia de frecuencia histórica 2.80 %. `python -m unittest discover -s tests -v`: 4 pruebas superadas. No se realizó inferencia estadística formal ni se probó el sistema del cliente. Repetir en el entorno local del responsable.

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
