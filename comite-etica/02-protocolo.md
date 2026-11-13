---
title: "Protocolo de investigación"
subtitle: "Topología de redes de afinidad como predictor de abandono académico"
author: "Investigador responsable: Dr. Hernán Astudillo · Departamento de Física · Facultad de Ciencias Físicas y Matemáticas, Universidad de Concepción"
date: "Versión 1.0 (borrador), noviembre de 2026"
lang: es
documentclass: article
papersize: letter
fontsize: 11pt
geometry: "margin=2.3cm"
mainfont: Charter
sansfont: "Helvetica Neue"
numbersections: true
colorlinks: true
linkcolor: "acento"
urlcolor: "acento"
header-includes:
  - \usepackage{xcolor}
  - \definecolor{acento}{HTML}{1F4E79}
  - \usepackage{titlesec}
  - \titleformat{\section}{\sffamily\Large\bfseries\color{acento}}{\thesection}{0.8em}{}
  - \titleformat{\subsection}{\sffamily\large\bfseries\color{acento}}{\thesubsection}{0.8em}{}
  - \usepackage{etoolbox}
  - \AtBeginEnvironment{longtable}{\small}
  - \renewcommand{\arraystretch}{1.25}
  - \usepackage{enumitem}
  - \setlist{itemsep=2pt,topsep=4pt}
  - \setlength{\parskip}{5pt}
  - \setlength{\parindent}{0pt}
---

# Antecedentes generales

| | |
|:--|:--|
| **Título** | Topología de redes de afinidad como predictor de abandono académico |
| **Investigador responsable** | Dr. Hernán Astudillo, Departamento de Física, FCFM (hastudil@udec.cl) |
| **Equipo de investigación** | Dr. Hernán Astudillo, Claudio Faúndez, Yannely Salas y Aníbal Olivera |
| **Unidad académica** | Departamento de Física, Facultad de Ciencias Físicas y Matemáticas (CFM), Universidad de Concepción |
| **Tipo de proyecto y financiamiento** | [POR COMPLETAR: tesis / proyecto interno; fuente de financiamiento, si la hay] |
| **Duración** | Noviembre de 2026 a junio de 2029: tres encuestas (2026-II, 2027-I y 2027-II), consulta al registro académico (2027 y 2028) y eliminación de los datos identificables (ver §7.4) |
| **Población** | Estudiantes de pregrado de todas las carreras de la CFM matriculados en 2026, de 18 años o más |
| **Documentos adjuntos** | Consentimiento informado v2.0 (`consentimiento-informado.pdf`); instrumento completo con todas sus pantallas (`preguntas-encuesta.pdf`); decisiones sobre el instrumento (`decisiones.pdf`); reporte general del proyecto (`reporte-general.pdf`) |

# Fundamentación

La deserción en educación superior es un problema persistente en Chile. En las carreras profesionales del área de Ciencias Básicas, la retención de primer año fue de 76 % para la cohorte 2025, una de las más bajas entre las áreas de conocimiento (SIES, 2025). Los indicadores institucionales habituales (notas, asistencia) detectan el riesgo tarde y miran a cada estudiante por separado, sin considerar con quiénes se relaciona.

El modelo de integración de Tinto (1975) sostiene que un estudiante persiste cuando está integrado en el sistema académico y en el social de la universidad: con sus pares, con sus docentes y con sus estudios. Este proyecto mide esa integración de dos maneras: desde adentro, con escalas validadas que cada estudiante responde sobre sí, y desde afuera, con las redes que forman los estudiantes al nombrar a con quiénes pasan tiempo, a quiénes piden ayuda y con quiénes estudian. Existen antecedentes en la propia Universidad de que la estructura relacional de un curso es un factor activo en la integración (Astudillo et al., citado en el informe del proyecto de agosto de 2026).

**Hipótesis.** «Entre las dos cohortes estudiadas, aquella cuya red de afinidad y colaboración presente una mayor fragmentación estructural —caracterizada por un mayor número de componentes desconectados, menor densidad global y una mayor proporción de nodos con baja centralidad— exhibirán una menor cohesión e integración social, lo que se asocia con una mayor tasa de deserción a nivel de cohorte.» Con la ampliación a toda la facultad y a tres mediciones, se estudia además si la posición en la red y la integración declarada predicen la intención de abandono y la deserción observada.

**Valor social.** Entender por qué algunos estudiantes dejan sus carreras, para que la Universidad pueda diseñar apoyos preventivos. El proyecto no entrega puntajes de riesgo individuales a nadie (ver §8).

# Objetivos

**Objetivo general.** Analizar si la estructura de las redes de relaciones entre estudiantes de la CFM y su integración académica y social se asocian con la intención de abandono y con la deserción observada.

**Objetivos específicos.**

1. Caracterizar las redes de afinidad, ayuda académica y estudio conjunto de los estudiantes de la CFM en tres momentos (2026-II, 2027-I y 2027-II).
2. Medir con escalas validadas la integración académica y social, la intención de abandono y de cambio de carrera, y el trato percibido de los docentes.
3. Evaluar si la fragmentación de la red de cada cohorte se asocia con su tasa de deserción.
4. Evaluar si la posición de cada estudiante en la red y su integración declarada predicen su intención de abandono y su deserción observada en el registro académico.

# Metodología

## Diseño

Estudio cuantitativo, longitudinal, de tres mediciones, con un censo de la población (no una muestra). La deserción se observa en el registro académico, con autorización explícita de cada participante.

## Población, criterios de inclusión y exclusión

- **Inclusión:** estar matriculado/a en una carrera de pregrado de la CFM en 2026 y tener 18 años o más.
- **Exclusión:** menores de 18 años. La opción para aceptar participar dice «Acepto participar y tengo 18 años o más»; quien no cumple ese requisito no puede aceptar. Al no aceptar, la encuesta termina y solo se guarda esa decisión, para contar los rechazos.
- Los criterios no excluyen a ningún grupo por otra razón: toda la facultad recibe la misma invitación.

## Reclutamiento

Cada estudiante recibe la invitación por su correo institucional UdeC, con un enlace a la encuesta. La nómina de estudiantes (nombre, año de ingreso y número de matrícula) la proporciona la Facultad, con la autorización correspondiente (ver la carta adjunta). Se envían hasta dos recordatorios por ola. No hay incentivos ni compensaciones, y ningún docente participa en la invitación: así se evita cualquier presión sobre la decisión de participar.

## Procedimiento

La encuesta se responde en línea, en una aplicación propia del equipo, y toma entre 10 y 15 minutos. Su orden es:

1. Bienvenida y **consentimiento informado** en una pantalla. Incluye un resumen, el documento completo en un desplegable y en PDF para descargar, y una autorización aparte para consultar el registro académico. Se puede participar sin dar esa autorización.
2. **Identificación:** cada estudiante elige su nombre de la nómina. Cada nombre se puede elegir una sola vez, y desde ahí la persona queda fuera de las listas de las preguntas siguientes.
3. **Redes:** tres preguntas en las que se marcan compañeros de la nómina (afinidad, ayuda y estudio), una pregunta sobre cuántas personas cree cada quien que lo marcaron, y otra sobre sus amistades en otras facultades.
4. **Escalas:** intención de abandono y de cambio de carrera, compromiso académico, autoeficacia, sentido de pertenencia, soledad, apoyo de la familia e incivilidad docente.
5. **Contexto:** seis preguntas (primera generación, trabajo, vivienda, traslado, primera opción, otra carrera previa) y un comentario abierto opcional.

Todas las preguntas, salvo el consentimiento y la identificación, se pueden omitir con «Prefiero no contestar». La encuesta se puede dejar y retomar con el enlace personal. En la segunda y la tercera ola se recuerdan las condiciones del estudio, con la opción de retirarse, antes de responder.

## Instrumentos

El instrumento completo, con todas sus pantallas, instrucciones y procedimientos de nominación, está en `preguntas-encuesta.pdf`. El fundamento de cada escala, en `decisiones.pdf`.

| Constructo | Instrumento | Ítems | Evidencia de validez |
|:--|:--|:-:|:--|
| Intención de abandono y de cambio de carrera | Bäulke et al. (2022), fases 2 a 4 | 6 a 18 | Chile: López-Angulo et al. (2025), N = 641, ω entre .83 y .97 |
| Compromiso académico | UWES-9S | 9 | Chile: Carmona-Halty et al. (2019), N = 1.502, α = .90 |
| Autoeficacia académica | ASES | 8 | Chile: Calderón Carvajal et al. (2019), N = 4.950, α = .82 |
| Sentido de pertenencia | ESPU | 10 | España: Alonso García y González Ortiz de Zárate (2024), N = 812 |
| Soledad | UCLA-3 | 3 | España: Trucharte et al. (2023), N = 1.951, α = .82 |
| Apoyo de la familia | MSPSS, subescala Familia | 4 | Chile: López-Angulo et al. (2021), N = 1.975, α = .90 |
| Incivilidad docente | WIS corta, adaptada a docentes, más 1 ítem nuevo | 4 + 1 | España: Di Marco et al. (2018), N = 407 trabajadores. Sin validación en estudiantes |
| Redes y contexto | Preguntas nuevas, en el formato usual de los generadores de nombres | 13 | Descriptivas; no forman escalas |

Las escalas se aplican con el texto y el formato de respuesta de su validación. Las adaptaciones (instrucciones, referente de la incivilidad) están documentadas en `decisiones.pdf`. Ninguna pregunta pide relatar hechos traumáticos, y ninguna pregunta por el nombre de un docente.

# Consentimiento informado en línea

El consentimiento sigue el guion del CEBB VRID-UdeC: título, investigadores, objetivos, procedimientos, riesgos y beneficios, confidencialidad y protección de datos, derechos del participante, costos y compensación, contactos del investigador responsable y del Comité, y la declaración de consentimiento.

**Se solicita aceptar el consentimiento electrónico en lugar de la firma.** La encuesta es en línea y llega por correo a toda la facultad. Pedir una firma manuscrita y un ministro de fe obligaría a identificar a cada participante con un documento aparte, en contra de la minimización de datos, y reduciría mucho la participación. En su lugar:

- El consentimiento es **expreso**: la encuesta no avanza sin marcar «Acepto participar y tengo 18 años o más».
- La autorización para consultar el registro académico es **una decisión aparte**, con su propia respuesta (sí o no), como exige que cada fin se autorice por separado.
- Cada participante puede **descargar el documento completo en PDF**.
- La aplicación registra la aceptación, con su fecha y hora y la respuesta a la autorización del registro académico, en un registro de auditoría que no se puede alterar sin que se note (ver §7.1).
- Quien marca «No acepto» termina la encuesta. Solo se guarda esa decisión, para contar los rechazos.
- Quien acepta y luego cambia de opinión puede volver a esa pantalla y retirarse: se borran sus respuestas y su nombre queda libre.

# Estudiantes no participantes

**Qué información existe sobre ellos.** Un estudiante que no participa no responde nada. La única información que puede existir sobre él es que un compañero que sí participa lo haya marcado en una pregunta de nombres. La nómina incluye a toda la facultad porque la red se define sobre la población completa, no solo sobre quienes responden.

**Por qué se conserva esa marca.** La marca es un dato de quien responde: describe con quién dice relacionarse el estudiante que sí consintió. Eliminarla alteraría su respuesta y la estructura de toda la red; la literatura sobre datos faltantes en redes muestra que suprimir nodos distorsiona las medidas de los demás (Kossinets, 2006; Smith y Moody, 2013).

**Cómo se trata.**

- El no participante figura en la red solo con un código, su año de ingreso (dato institucional, necesario para la hipótesis por cohorte) y las marcas que recibió. No se registra ninguna otra característica suya.
- **Nunca se consulta su registro académico:** no autorizó esa consulta.
- No es objeto de análisis individual, no aparece en ningún informe y no se calcula ningún indicador sobre su persona. En los análisis, sus vínculos salientes se tratan como datos faltantes.

**Información.** El consentimiento informa que las personas nombradas aparecen en los datos con un código aunque no participen, y que a nadie se le informa quién lo marcó.

**Fundamento.** El tratamiento se ampara en los fines científicos que reconoce la Ley 21.719, con minimización (solo la existencia del vínculo y el año de ingreso), seudonimización, acceso restringido y publicación solo de resultados agregados.

# Gestión y protección de datos

## Almacenamiento

- Las respuestas se guardan a medida que se contestan, en una base de datos local en un computador del equipo con disco cifrado y acceso físico restringido ([POR CONFIRMAR: equipo y ubicación]). No se usan servicios de almacenamiento en la nube de terceros.
- El computador no expone puertos a internet: los estudiantes acceden por un túnel cifrado (HTTPS) que solo transporta la conexión y no guarda respuestas.
- La base guarda el número de cada estudiante en la nómina, no su nombre. La nómina con los nombres se guarda en el mismo equipo, fuera del repositorio de código.
- Se hacen copias de respaldo cada hora durante la aplicación, en un medio cifrado.
- Cada evento de la encuesta queda en un registro de auditoría encadenado por hashes, que permite verificar que los datos no se alteraron.
- La dirección IP no se guarda: solo un hash con una clave secreta, para limitar respuestas automatizadas.

## Seudonimización

Para analizar, los datos se exportan y cada estudiante pasa a ser un código generado con HMAC-SHA256 y una clave secreta del proyecto. El mismo estudiante recibe el mismo código en las tres olas, lo que permite unir sus respuestas sin usar su nombre. Todo el análisis se hace sobre los datos seudonimizados.

**Los datos no son anónimos, sino seudonimizados,** por dos razones propias del diseño:

- Las preguntas de redes describen vínculos entre personas concretas de la nómina.
- Unir las tres olas y el registro académico requiere saber, mientras dura el estudio, qué código corresponde a qué estudiante.

Por eso se reconoce que seudonimizar a las personas no anonimiza una red: la estructura de vínculos podría permitir reidentificar a alguien con conocimiento del contexto. **Los datos de quién nombró a quién no se publican en ningún caso.**

## Control de acceso

- Solo [POR CONFIRMAR: integrantes] administran el equipo donde se guardan los datos.
- La clave de seudonimización la custodia el investigador responsable. Se guarda separada de los datos y nunca entra al repositorio de código.
- Quienes analizan trabajan solo con los datos seudonimizados.
- Ningún docente, jefatura de carrera ni autoridad de la Universidad accede a respuestas individuales.

## Conservación y eliminación

| Fase | Qué se conserva | Plazo | Para qué |
|:--|:--|:--|:--|
| A. Identificable | Base de la aplicación, nóminas con nombres y número de matrícula, clave de seudonimización | Hasta 12 meses después de la última consulta al registro académico (matrícula 2028), es decir, hasta junio de 2029 | Unir las tres olas y el registro académico |
| B. Investigación | Datos seudonimizados, sin nombres ni clave | Con acceso restringido, para investigación | Análisis y publicaciones con resultados agregados |

Al cerrar la fase A se eliminan de forma segura la base, sus respaldos, las nóminas y la clave. Desde ese momento los códigos ya no se pueden vincular con ninguna persona. Mientras dure la fase A, cualquier participante puede pedir que se eliminen sus datos; después ya no es posible identificar cuáles son, lo que también informa el consentimiento.

En la fase B no se publican datos de red individuales ni tablas con celdas de menos de 5 casos, y no se presentan resultados por carrera cuando eso permitiría reconocer a alguien.

# Prevención de estigmatización y procedimiento ante malestar

**Riesgo de etiquetamiento.** El riesgo principal no es la revictimización (la encuesta no pide relatar experiencias traumáticas), sino que un estudiante quede etiquetado por su posición en la red o por sus respuestas. Para prevenirlo:

- Nadie recibe un puntaje de riesgo individual, ni listas de estudiantes «en riesgo», «aislados» o «centrales».
- Los resultados que se entregan a la Facultad o a las carreras son agregados, sin sociogramas con nombres y con supresión de celdas pequeñas.
- Las respuestas no tienen ninguna consecuencia académica, y así lo dice el consentimiento.
- Las preguntas sobre incivilidad no piden nombres de docentes, y los resultados sobre docentes se informan solo agregados para toda la facultad.

**Procedimiento ante malestar.** La encuesta es en línea y no hay un integrante del equipo presente al responder. Por eso:

- Cualquier pregunta se puede omitir y la encuesta se puede dejar en cualquier momento.
- El consentimiento y la pantalla final indican a quién acudir: la Dirección de Servicios Estudiantiles (DISE) [POR COMPLETAR: contacto] y el investigador responsable.
- Para situaciones de maltrato o acoso, la pantalla final indica además el canal institucional de denuncia de la Universidad (Ley 21.369) [POR CONFIRMAR: unidad y contacto].
- Antes de cada ola se informa a la DISE que podrían llegar estudiantes derivados del estudio.

**Alcance.** El análisis se hace sobre datos seudonimizados y no contempla revisar respuestas individuales para detectar riesgos. La encuesta no es un instrumento de detección, y el consentimiento lo dice explícitamente: no reemplaza los canales de apoyo y de denuncia de la Universidad. Si el equipo se comprometiera a actuar ante lo que revelen las respuestas, tendría que reidentificar a estudiantes, en contra de la confidencialidad prometida.

# Población esperada y justificación del tamaño

**No hay muestreo:** se invita a toda la población, porque una red solo se puede describir con la población completa. La matrícula de pregrado de la CFM en 2026 es de [POR COMPLETAR: número] estudiantes. Esperamos unos 350 respondientes por ola.

**Suficiencia para los objetivos individuales.**

- Con 350 respondientes, una correlación de r = .15 entre un predictor y la intención de abandono se detecta con una potencia de .80 (α = .05, bilateral).
- La deserción observada es un evento poco frecuente: se esperan entre 35 y 70 casos en tres semestres. Con la regla de 10 eventos por variable, eso permite modelos con 3 a 7 predictores. Por eso la intención de abandono, que es continua y se mide en cada ola, es el resultado principal del análisis individual, y la deserción, el resultado final.

**Dependencia entre observaciones.** Los estudiantes de una misma red no son observaciones independientes. Por eso:

- los análisis de red usan modelos que tratan la red completa como la unidad (ver §10);
- los análisis individuales incluyen la carrera y la cohorte como niveles de agrupación.

**Alcance de las inferencias:** las conclusiones se refieren a la CFM de la Universidad de Concepción. Son un estudio de caso, no una estimación para todas las universidades.

# Plan de análisis

1. **Calidad de la medición:** análisis factorial confirmatorio de cada escala con datos ordinales, confiabilidad (ω) y validez discriminante entre constructos (HTMT).
2. **Descripción de las redes** por cohorte y por carrera: densidad, componentes, reciprocidad, transitividad y distribución de la centralidad.
3. **Hipótesis por cohorte:** comparación de la fragmentación de las redes con la tasa de deserción de cada cohorte.
4. **Nivel individual:** modelos multinivel de la intención de abandono en función de la posición en la red y de las escalas, y de la deserción observada en función de la intención, con mediación.
5. **Evolución en tres olas:** modelos de coevolución de red y conducta (SAOM, RSiena) para distinguir **selección** (quien piensa irse se aísla) de **influencia** (la intención se transmite entre amigos).

**Datos faltantes.**

- Quien no responde es un nodo con sus vínculos salientes faltantes. Los modelos SAOM tratan los faltantes en sus estimaciones; las medidas de centralidad se calculan con y sin esos nodos, como análisis de sensibilidad.
- «Prefiero no contestar» se registra aparte de «no llegó a la pregunta».
- En las fases 3 y 4 de intención, que aparecen solo si la fase anterior tuvo una respuesta distinta de «1», la falta de respuesta es parte del diseño y se trata como tal.

# Plan de trabajo

| Período | Actividad |
|:--|:--|
| Semana del 16 de noviembre de 2026 | Envío al Comité |
| Diciembre de 2026 | Primera ola, tras la aprobación |
| Primer semestre de 2027 | Segunda ola |
| Segundo semestre de 2027 | Tercera ola |
| Abril de 2027 y abril de 2028 | Consulta al registro académico (matrícula), solo para quienes lo autorizaron |
| 2027 a 2028 | Análisis y publicaciones |
| Junio de 2029 | Eliminación de los datos identificables (fin de la fase A) |

# Devolución de resultados

Al terminar el estudio se enviará a todos los participantes, por su correo UdeC, un resumen de los resultados generales. A la Facultad se le entregará un informe agregado, sin datos individuales.

# Bioseguridad

El proyecto no usa muestras biológicas, sustancias químicas, agentes biológicos ni fuentes de radiación. No aplica.

# Referencias

Alonso García, S., y González Ortiz de Zárate, A. (2024). Validación de la Escala de Sentido de Pertenencia a la Universidad en España. *Revista Iberoamericana de Diagnóstico y Evaluación Psicológica*, 73(3), 5–17.

Bäulke, L., Grunschel, C., y Dresel, M. (2022). Student dropout at university: A phase-orientated view on quitting studies and changing majors. *European Journal of Psychology of Education*, 37(1), 853–876.

Calderón Carvajal, C., Carreño Mendoza, B., Micin Carvallo, S., y Urzúa Martínez, S. (2019). Estructura interna e invarianza métrica de la escala de autoeficacia académica ASES. *Salud & Sociedad*, 10(2), 164–172.

Carmona-Halty, M. A., Schaufeli, W. B., y Salanova, M. (2019). The Utrecht Work Engagement Scale for Students (UWES-9S). *Frontiers in Psychology*, 10, 1017.

Di Marco, D., Martínez-Corts, I., Arenas, A., y Gamero, N. (2018). Spanish validation of the shorter version of the Workplace Incivility Scale. *Frontiers in Psychology*, 9, 959.

Kossinets, G. (2006). Effects of missing data in social networks. *Social Networks*, 28(3), 247–268.

López-Angulo, Y., Muñoz-Inostroza, K., Sáez-Delgado, F., Chandia, E., Mella-Norambuena, J., y Brito-Álvarez, F. (2025). Validation of scales to measure dropout and changing majors intentions of Chilean university students. *Journal of College Student Retention*. https://doi.org/10.1177/15210251251360672

López-Angulo, Y., Pérez-Villalobos, M. V., Bernardo, A. B., Cobo Rendón, R., Sáez Delgado, F., y Díaz-Mujica, A. (2021). Propiedades psicométricas de la Escala Multidimensional de Apoyo Social Percibido en estudiantes universitarios chilenos. *RIDEP*, 58(1), 127–140.

Sharif-Nia, H., Marôco, J., Rahmatpour, P., Allen, K. A., Kaveh, O., y Hoseinzadeh, E. (2023). Bullying behaviors and intention to drop-out among nursing students. *BMC Nursing*, 22, 417.

Smith, J. A., y Moody, J. (2013). Structural effects of network sampling coverage I: Nodes missing at random. *Social Networks*, 35(4), 652–668.

Tinto, V. (1975). Dropout from higher education: A theoretical synthesis of recent research. *Review of Educational Research*, 45(1), 89–125.

Trucharte, A., Calderón, L., Cerezo, E., Contreras, A., Peinado, V., y Valiente, C. (2023). Three-item loneliness scale: Psychometric properties and normative data of the Spanish version. *Current Psychology*, 42, 7466–7474.
