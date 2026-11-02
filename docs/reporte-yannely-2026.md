---
title: "Encuesta FCFM 2026: constructos y calendario"
subtitle: "Lo esencial del reporte del semestre para las próximas semanas"
author: "Aníbal Olivera Morales, para Yannely V. Salas Gutiérrez"
date: "16 de octubre de 2026"
lang: es
documentclass: article
papersize: letter
fontsize: 11pt
geometry: "margin=2.3cm"
mainfont: Charter
sansfont: "Helvetica Neue"
monofont: Menlo
numbersections: true
colorlinks: true
linkcolor: "acento"
urlcolor: "acento"
header-includes:
  - \usepackage{xcolor}
  - \definecolor{acento}{HTML}{1F4E79}
  - \definecolor{fondo}{HTML}{EEF3F8}
  - \definecolor{alerta}{HTML}{8C2D19}
  - \definecolor{fondoalerta}{HTML}{FBEFEA}
  - \usepackage{titlesec}
  - \titleformat{\section}{\sffamily\Large\bfseries\color{acento}}{\thesection}{0.8em}{}
  - \titleformat{\subsection}{\sffamily\large\bfseries\color{acento}}{\thesubsection}{0.8em}{}
  - \usepackage{etoolbox}
  - \AtBeginEnvironment{longtable}{\small}
  - \renewcommand{\arraystretch}{1.25}
  - \usepackage[most]{tcolorbox}
  - \newtcolorbox{nota}{colback=fondo,colframe=acento,boxrule=0pt,leftrule=3pt,arc=0pt,left=8pt,right=8pt,top=6pt,bottom=6pt}
  - \newtcolorbox{alerta}{colback=fondoalerta,colframe=alerta,boxrule=0pt,leftrule=3pt,arc=0pt,left=8pt,right=8pt,top=6pt,bottom=6pt}
  - \usepackage{newunicodechar}
  - \newunicodechar{→}{\ensuremath{\rightarrow}}
  - \newunicodechar{≈}{\ensuremath{\approx}}
  - \usepackage{enumitem}
  - \setlist{itemsep=2pt,topsep=4pt}
  - \setlength{\parskip}{5pt}
  - \setlength{\parindent}{0pt}
---

Este documento resume, del reporte del semestre, solo lo que necesitas para las próximas semanas: **qué medir** (sección 1, con un ejemplo completo en la sección 2) y **cuándo** (sección 3).

La encuesta llegará a toda la Facultad de Ciencias Físicas y Matemáticas, no solo a Ciencias Físicas. Con más estudiantes, el tamaño de la muestra deja de ser la limitación principal y podemos usar escalas validadas completas.

# Constructos psicológicos candidatos

Lo que queremos predecir es la **intención de abandono**: si la persona piensa dejar la carrera, la universidad o los estudios. Esa parte ya está en la encuesta. Los siete constructos de abajo son los candidatos a predictores, todos con respaldo en la literatura sobre abandono (el modelo de integración de Tinto y sus sucesores).

Para cada constructo, tu tarea es:

1. Leer qué es y por qué se relaciona con el abandono.
2. Encontrar una **escala ya validada en español**, idealmente con universitarios chilenos.
3. Conseguir el **texto exacto** de sus preguntas (ítems) y su formato de respuesta.

| Constructo | Qué capta | Por dónde empezar a buscar |
|:-----------------|:----------------------------------|:----------------------------------|
| Autoeficacia académica | Confianza en la propia capacidad para cumplir con las exigencias de la carrera. Es uno de los mejores predictores de la permanencia. | ASES (Chemers et al., 2001), validada en Chile por Calderón Carvajal et al. (2019) |
| Sentido de pertenencia | Sentirse aceptado/a, valorado/a e incluido/a en la universidad. | ESPU (Alonso García y González Ortiz de Zárate, 2024); para la física, Good et al. (2012) |
| Satisfacción académica | Agrado y bienestar con la experiencia de estudiar la carrera. | ESA (Lent et al., 2007), validada en Chile por Vergara-Morales et al. (2018) |
| Compromiso académico (*engagement*) | Energía, dedicación y concentración en los estudios. | UWES-9S, validada en Chile por Carmona-Halty et al. (2019) |
| Apoyo social percibido | Sentir que se cuenta con familia, amistades y otras personas importantes. | MSPSS (Zimet et al., 1988), validada en universitarios chilenos por López-Angulo et al. (2021) |
| Relación con docentes (incivilidad) | Trato descortés o descalificador de parte de docentes. Su contraparte positiva es el apoyo a la autonomía. | No hay escala validada en español para universitarios: partir de Cortina et al. (2001) y Di Marco et al. (2018). Polo positivo: LCQ (Núñez et al., 2012) |
| Soledad o aislamiento | Sentirse solo/a o dejado/a de lado. Es la versión *sentida* del aislamiento que mide la red. | UCLA-3 (Hughes et al., 2004). **Ejemplo desarrollado en la sección 2** |

\begin{nota}
\textbf{Cómo buscar.} En Google Scholar, SciELO o Redalyc, combina el nombre de la escala con \emph{validación}, \emph{Chile} y \emph{universitarios}; si no conoces el nombre, busca \emph{escala de [constructo] estudiantes universitarios propiedades psicométricas}.

\textbf{Qué anotar de cada escala:} número de ítems, formato de respuesta, población y N de la validación, confiabilidad (α u ω), ítems invertidos y si es de uso libre.

\textbf{Regla de oro:} los ítems de una escala validada se deben copiar textuales del artículo. No se deberían reescribir porque si se cambia la redacción, deja de ser exactamente la escala validada.
\end{nota}

**Presupuesto de tiempo.** Las siete escalas completas suman unos 55 ítems, cerca de 10 minutos. Junto con las preguntas de redes y de contexto, la encuesta queda en unos 20–25 minutos, que mucho para lo que queremos. Por eso, luego tendremos que seleccionar. 

# Ejemplo completo: soledad (UCLA-3)

**Definición.** La soledad es la experiencia desagradable de tener menos relaciones, o relaciones menos cercanas, de las que uno quisiera (Peplau y Perlman, 1982). No es lo mismo que estar solo/a: se puede tener muchos contactos y sentirse solo/a.

**Por qué nos interesa.** La red mide el aislamiento desde afuera: a quién nadie nombra. Esta escala lo mide desde adentro. Comparar ambas es un resultado en sí mismo: alguien que la red muestra aislado pero que no se siente solo/a (quizás sus amistades están en otra carrera), o alguien muy nombrado que se siente solo/a.

**Escala.** UCLA-3 (Hughes et al., 2004): la versión de tres ítems de la escala de soledad de UCLA, pensada para encuestas largas. Toma unos 30 segundos.

| | Ítem original | Traducción de trabajo |
|:--|:------------------------------------|:------------------------------------|
| 1 | How often do you feel that you lack companionship? | ¿Con qué frecuencia sientes que te falta compañía? |
| 2 | How often do you feel left out? | ¿Con qué frecuencia te sientes excluido/a o dejado/a de lado? |
| 3 | How often do you feel isolated from others? | ¿Con qué frecuencia te sientes aislado/a de los demás? |

**Respuesta:** *Hardly ever* (1) · *Some of the time* (2) · *Often* (3).

**Puntaje:** la suma de los tres ítems, de 3 a 9 (más alto = más soledad). No tiene ítems invertidos (un ítem invertido sería por ejemplo "con qué frecuencia te sientes incluido o considerado").

\begin{alerta}
La traducción de arriba es \textbf{de trabajo}, no validada. Lo que falta es justamente el paso 2: buscar una versión en español ya validada (por ejemplo, \emph{UCLA-3 validación español} o \emph{escala de soledad de tres ítems}) y usar su redacción exacta. Si no hay una para Chile, hay que tener más cuidado.
\end{alerta}

**Cómo queda en la encuesta.** En `encuesta/instrumento.py` se agrega como un bloque (las tres preguntas en una página, con la misma escala de respuesta):

```python
FRECUENCIA_3 = ["Casi nunca", "A veces", "A menudo"]

SOLEDAD = bloque(
    "ucla3",
    "Las siguientes preguntas son sobre cómo te has sentido. ¿Con qué frecuencia…",
    items=[
        ("ucla3_1", "…sientes que te falta compañía?"),
        ("ucla3_2", "…te sientes excluido/a o dejado/a de lado?"),
        ("ucla3_3", "…te sientes aislado/a de los demás?"),
    ],
    opciones=FRECUENCIA_3,
    constructo="Soledad (UCLA-3)",
    fuente="Hughes et al. (2004); traducción de trabajo",
)
```

y se suma `SOLEDAD` a la lista `PREGUNTAS`. Con la demo abierta, el cambio aparece al guardar el archivo. Para los otros seis constructos el procedimiento es el mismo; la IA de VS Code puede ayudarte a escribir el bloque si le pasas los ítems.

\newpage

# Calendario

**Fecha límite:** el enlace se envía por el correo UdeC **a más tardar la semana del 7 al 11 de diciembre**, y solo después de que el comité de ética (CEBB) apruebe el proyecto. Por eso el calendario se arma hacia atrás desde la aprobación.

Supuestos con el comité (por confirmar): responde en **4 días hábiles**, habrá **una ronda de correcciones** (2 días hábiles para hacerlas) y el servidor y el enlace estarán listos apenas llegue el OK. Con eso, el comité toma unos 10 días hábiles. Si enviamos el **16 de noviembre**, la aprobación llega el 30 de noviembre y el envío puede ser el 1 de diciembre, con más de una semana de margen. El último día posible para el primer envío al comité es el 26 de noviembre, sin margen alguno.

| Semana | Qué hacemos | Hito |
|:------------|:--------------------------------------------------------|:------------------|
| 19–23 oct | Crear la cuenta de GitHub, instalar VS Code, clonar el proyecto y probar la demo (pasos en el correo). Leer Lietz (2009). Empezar a buscar escalas | Demo funcionando |
| 26–30 oct | Una ficha por constructo: escala, ítems, formato, validación y referencia. Decidir cuáles entran | Escalas elegidas |
| 2–6 nov | Cargar los ítems exactos en `instrumento.py` y redactar los de incivilidad. Aníbal prepara el protocolo y el consentimiento | Versión 0 en la app |
| 9–13 nov | Pruebas con voz alta entre colegas, revisión de jueces, ajustes y medición del tiempo | **Instrumento congelado (13 nov)** |
| 16–20 nov | **Envío al CEBB el lunes 16.** Mientras se espera: servidor, enlace, nómina y prueba de punta a punta | Primera respuesta (20 nov) |
| 23–27 nov | Correcciones (23–24) y reenvío el martes 24 | Reenvío (24 nov) |
| 30 nov – 4 dic | Aprobación esperada el lunes 30. **Envío del enlace el 1 de diciembre** | **Encuesta enviada** |
| 7–11 dic | Recordatorios y seguimiento. Es el margen: si el comité se atrasa, aquí cae el envío | Fecha límite |
| 14–18 dic | Cierre de la toma de datos y limpieza. Cierre del curso el 18 | — |

Tres cosas a tener presentes: (1) el instrumento que se envía al comité es el que se aplica, porque cambiarlo después exige una enmienda; (2) no se toman datos de estudiantes antes de la aprobación, así que las pruebas con voz alta las hacen colegas; (3) el 1 de diciembre entra en vigencia la Ley 21.719 de protección de datos: consentimiento explícito y no pedir datos que no se analizarán. Quedan por confirmar con el comité los plazos reales y si corresponde el de la FCFM o el central.

# Referencias

Alonso García, S., y González Ortiz de Zárate, A. (2024). Validación de la Escala de Sentido de Pertenencia a la Universidad en España. *Revista Iberoamericana de Diagnóstico y Evaluación Psicológica*, 73(3), 5–17.

Calderón Carvajal, C., Carreño Mendoza, B., Micin Carvallo, S., y Urzúa Martínez, S. (2019). Estructura interna e invarianza métrica de la escala de autoeficacia académica ASES. *Salud & Sociedad*, 10(2), 164–172.

Carmona-Halty, M. A., Schaufeli, W. B., y Salanova, M. (2019). The Utrecht Work Engagement Scale for Students (UWES-9S): Factorial validity, reliability, and measurement invariance in a Chilean sample of undergraduate university students. *Frontiers in Psychology*, 10, 1017.

Chemers, M. M., Hu, L., y Garcia, B. F. (2001). Academic self-efficacy and first-year college student performance and adjustment. *Journal of Educational Psychology*, 93(1), 55–64.

Cortina, L. M., Magley, V. J., Williams, J. H., y Langhout, R. D. (2001). Incivility in the workplace: Incidence and impact. *Journal of Occupational Health Psychology*, 6(1), 64–80.

Di Marco, D., Martínez-Corts, I., Arenas, A., y Gamero, N. (2018). Spanish validation of the shortened Workplace Incivility Scale: An alternative to the original version. *Frontiers in Psychology*, 9, 959.

Good, C., Rattan, A., y Dweck, C. S. (2012). Why do women opt out? Sense of belonging and women's representation in mathematics. *Journal of Personality and Social Psychology*, 102(4), 700–717.

Hughes, M. E., Waite, L. J., Hawkley, L. C., y Cacioppo, J. T. (2004). A short scale for measuring loneliness in large surveys. *Research on Aging*, 26(6), 655–672.

International Test Commission (2018). ITC guidelines for translating and adapting tests (2.ª ed.). *International Journal of Testing*, 18(2), 101–134.

Lent, R. W., Singley, D., Sheu, H.-B., Schmidt, J. A., y Schmidt, L. C. (2007). Relation of social-cognitive factors to academic satisfaction in engineering students. *Journal of Career Assessment*, 15(1), 87–97.

López-Angulo, Y., et al. (2021). Propiedades psicométricas de la Escala Multidimensional de Apoyo Social Percibido en estudiantes universitarios chilenos. *Revista Iberoamericana de Diagnóstico y Evaluación Psicológica*, 58(1).

Núñez, J. L., León, J., Grijalvo, F., y Martín-Albo, J. (2012). Measuring autonomy support in university students: The Spanish version of the Learning Climate Questionnaire. *The Spanish Journal of Psychology*, 15(3), 1466–1472.

Peplau, L. A., y Perlman, D. (1982). Perspectives on loneliness. En L. A. Peplau y D. Perlman (Eds.), *Loneliness: A sourcebook of current theory, research and therapy* (pp. 1–18). Wiley.

Vergara-Morales, J., Del Valle, M., Díaz, A., y Pérez, M. V. (2018). Adaptación de la Escala de Satisfacción Académica en estudiantes universitarios chilenos. *Psicología Educativa*, 24(2), 99–106.

Zimet, G. D., Dahlem, N. W., Zimet, S. G., y Farley, G. K. (1988). The Multidimensional Scale of Perceived Social Support. *Journal of Personality Assessment*, 52(1), 30–41.
