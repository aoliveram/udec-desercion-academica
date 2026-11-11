---
title: "Instrumento: decisiones tomadas"
subtitle: "Qué escalas entran a la encuesta, por qué, y qué queda pendiente"
author: "Aníbal Olivera Morales y Yannely V. Salas Gutiérrez"
date: "Actualizado el 9 de noviembre de 2026"
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
  - \usepackage{titlesec}
  - \titleformat{\section}{\sffamily\Large\bfseries\color{acento}}{\thesection}{0.8em}{}
  - \titleformat{\subsection}{\sffamily\large\bfseries\color{acento}}{\thesubsection}{0.8em}{}
  - \usepackage{etoolbox}
  - \AtBeginEnvironment{longtable}{\small}
  - \renewcommand{\arraystretch}{1.25}
  - \usepackage[most]{tcolorbox}
  - \newtcolorbox{nota}{colback=fondo,colframe=acento,boxrule=0pt,leftrule=3pt,arc=0pt,left=8pt,right=8pt,top=6pt,bottom=6pt}
  - \usepackage{newunicodechar}
  - \newunicodechar{→}{\ensuremath{\rightarrow}}
  - \newunicodechar{≈}{\ensuremath{\approx}}
  - \usepackage{enumitem}
  - \setlist{itemsep=2pt,topsep=4pt}
  - \setlength{\parskip}{5pt}
  - \setlength{\parindent}{0pt}
---

Este documento registra las decisiones sobre el instrumento a medida que las tomamos. Cada decisión dice si es **firme** o **provisoria** (se puede revisar). Los ítems textuales están en `encuesta/instrumento.py`, y cómo se ven en pantalla, en [`preguntas-encuesta.pdf`](preguntas-encuesta.pdf).

# Resumen

**Qué entra hoy** (34 ítems de escalas, más la intención de abandono cuando la tengamos):

| Constructo | Escala | Ítems | Formato | Texto tomado de |
|:--|:--|:-:|:--|:--|
| Intención de abandono | López-Angulo et al. (2025) | por definir | Acuerdo, 1 a 7 | Apéndices 2 y 3 del artículo (figshare) |
| Compromiso académico | UWES-9S, completa | 9 | Frecuencia, 0 a 6 | Manual en español (Schaufeli y Bakker, 2003), p. 49 |
| Autoeficacia académica | ASES, completa | 8 | Acuerdo, 1 a 7 | Calderón Carvajal et al. (2019) |
| Sentido de pertenencia | ESPU, completa | 10 | Acuerdo, 1 a 7 | Alonso García y González Ortiz de Zárate (2024), Tabla 2 |
| Soledad | UCLA-3, completa | 3 | Frecuencia, 3 puntos | Trucharte et al. (2023) |
| Apoyo social de la familia | MSPSS, solo subescala Familia | 4 | Acuerdo, 1 a 7 | López-Angulo et al. (2021), Tabla 5 |

**Qué queda fuera:** satisfacción académica (ESA), apoyo a la autonomía docente (LCQ-5), incivilidad docente y las subescalas Amigos y Otros significativos de la MSPSS.

**Tiempo estimado:** las escalas toman unos 4 minutos (a ~7 segundos por ítem). Con las redes, el contexto y la intención, la encuesta toma entre 10 y 15 minutos, y así lo dice la bienvenida.

# Decisiones

## Diseño general

**D1. Encuesta por correo a toda la Facultad de Ciencias Físicas y Matemáticas (CFM), buscando la menor atrición posible** (firme). La encuesta se llama «Encuesta CFM» y ya no menciona solo a Ciencias Físicas. Por eso el criterio para cada escala es que aporte algo que ninguna otra pregunta capta, y que no se pise con otra.

**D2. Tres olas, una por semestre: 2026-II, 2027-I y 2027-II** (firme). La deserción observada sale del registro académico (por eso la encuesta pide autorización para consultarlo), no de quién deja de responder: alguien que no contesta la ola 2 puede haber desertado o solo no haber respondido.

**D3. Medir igual la intención de abandono** (firme). Aunque observemos la deserción, la intención aporta:

- **Potencia estadística.** Con unos 350 respondientes habría quizá 35–70 deserciones en tres semestres; la intención es continua y se mide en cada ola.
- **Mecanismo.** Permite probar si las escalas actúan sobre la intención y esta sobre la deserción.
- **Tipo de salida.** Distingue cambiarse de carrera dentro de la UdeC de irse de la universidad.

Usaremos las escalas de intención de abandono y de cambio de carrera de López-Angulo, Muñoz-Inostroza, Sáez-Delgado, Chandia, Mella-Norambuena y Brito-Álvarez (2025), *Journal of College Student Retention*, validadas con 641 estudiantes chilenos de primer año, con cinco fases cada una (percepción de no encajar, pensamientos de dejar o cambiarse, deliberación, búsqueda de información, decisión final). Ya tenemos el artículo y los ítems en español (apéndices 2 y 3, en figshare). **Falta decidir qué fases usar; mientras tanto, la encuesta tiene una pantalla de reemplazo.** Si las escalas resultan largas, se pueden usar solo algunas fases como subescalas.

**D4. No se cambia el formato de respuesta de una escala validada** (firme). Se usa el número de puntos y las etiquetas de su validación, aunque eso signifique varios formatos en la encuesta (frecuencia 0–6, acuerdo 1–7, frecuencia de 3 puntos). Cada escala va en su propia pantalla, con su instrucción. Cuando el artículo solo da las etiquetas de los extremos, los puntos del medio van con su número.

**D5. Una subescala se puede usar sola si cumple cuatro condiciones** (firme): la validación la muestra como un factor propio con su confiabilidad; se usan todos sus ítems, sin cambios; se interpreta solo como esa dimensión; y se reporta así.

## Escalas que entran

**D6. Compromiso académico con el UWES-9S, por sobre la ESA** (provisoria). Las dos se pisan: varios ítems casi se repiten («Disfruto de mis clases» y «Soy feliz cuando estoy haciendo tareas…»; «Me entusiasman los contenidos» y «Estoy entusiasmado con mi carrera»). Con unos 350 casos no podríamos separar sus efectos, así que elegimos una. El UWES gana hoy por razones prácticas:

| Criterio | UWES-9S | ESA |
|:--|:--|:--|
| Texto en español referido a la carrera | Sí, del manual de los autores | No: la versión chilena pregunta por «esta asignatura» |
| Validación en Chile | N = 1.502, análisis confirmatorio, invarianza por sexo | N = 608 |
| Dimensiones | Tres (vigor, dedicación, absorción), usables por separado | Una |

Revisamos las dos fuentes posibles de una ESA referida a la carrera, y ninguna sirve:

- **Medrano y Pérez (2010)** adapta otra escala (Sisto et al., 2008, de Brasil): 8 ítems sobre el ambiente pedagógico, frecuencia de 0 a 3, solo análisis exploratorio, N = 251.
- **Medrano, Fernández Liporace y Pérez (2014)**, la versión que cita el paper chileno, no publica los ítems en español (ni en su versión en español ni en la inglesa): solo da un ejemplo («Disfruto de mis clases la mayor parte del tiempo»). Además usa una escala de acuerdo de 10 puntos.

*Cuándo reabrir:* si Medrano (`leomedpsico@gmail.com`) nos envía la versión referida a la carrera. Entonces la elección sería teórica: el UWES calza con Tinto (la dedicación se parece al compromiso con la meta de titularse) y la ESA con el modelo de Lent (la autoeficacia aumenta la satisfacción, y esta la persistencia).

**D7. Los ítems del UWES son los del cuestionario del manual, no los de su texto** (firme). El manual en español trae dos listas distintas: la de la página 49 (el cuestionario, con asterisco en los 9 de la versión corta) y la de la sección 4.9 (pp. 21–22), que es una traducción del texto del manual y nombra ítems que no existen en el cuestionario. Usamos la de la página 49, que coincide con los ítems en inglés de la validación chilena (Carmona-Halty et al., 2019).

Adaptaciones al UWES, todas menores:

- La instrucción del manual dice «en el trabajo» (error de copia de la versión para empleados): la cambiamos a «en sus estudios».
- La instrucción explicaba cómo escribir un número en papel; la cambiamos a «marque «Nunca»; en caso contrario, indique cuántas veces…».
- «Bastante veces» (errata del manual) pasa a «Bastantes veces».
- **En pantalla, las opciones van como números** (0 · Nunca, 1, 2, 3, 4, 5, 6 · Siempre), igual que las escalas de acuerdo. La etiqueta completa de cada punto («Regularmente (pocas veces al mes)», etc.) aparece en una burbuja al pasar el cursor; en el celular, al tocar la opción, si el navegador lo permite. Las etiquetas completas con su frecuencia se veían demasiado cargadas. La escala y su significado no cambian.

**D8. Autoeficacia académica con la ASES completa, 8 ítems** (firme). Es de los mejores predictores individuales de permanencia, y su validación chilena tiene N = 4.950. El ítem 7 («Encuentro que mis actividades académicas son interesantes y apasionantes») se parece más a compromiso que a autoeficacia: lo dejamos, para no romper la validación, y lo revisaremos en el piloto.

*Etiquetas:* la validación no las publica. Usamos las de la ESPU (1 = nada de acuerdo, 7 = totalmente de acuerdo), que calzan con ítems que son descripciones de uno mismo y evitan un formato más. Es un supuesto: conviene confirmarlo con Calderón (`ccalderon@ucn.cl`).

**D9. Sentido de pertenencia con la ESPU completa, 10 ítems** (firme). Es el núcleo de la integración social en Tinto. La dimensión de integración social (ítems 1–5) es la versión *sentida* de lo que mide la red; la de orgullo (6–10) se acerca al compromiso con la institución.

*Universidad o facultad* (provisoria): dejamos el texto original («universidad»). Cambiarlo sería una adaptación, y la red ya mide la integración en la carrera; la ESPU aporta el nivel de la institución.

**D10. Soledad con la UCLA-3** (firme). Tres ítems, la versión sentida del aislamiento que mide la red. Etiquetas: «Casi nunca», «Algunas veces», «A menudo» (*hardly ever*, *some of the time*, *often*). La instrucción es nuestra traducción de la de Hughes et al. (2004).

**D11. Apoyo social: solo la subescala Familia de la MSPSS, 4 ítems** (firme). Capta el apoyo que viene de fuera de la universidad, que la red no ve. La subescala Amigos no distingue si los amigos son de la universidad, y se pisa con la red y con la ESPU. La subescala Familia es un factor propio en la validación chilena (α = .90), así que cumple D5. El texto es el de López-Angulo et al. (2021), Tabla 5 (códigos A3, A4, A8, A11), no el de Arechabala y Miranda (2002).

**D12. Instrucciones de las escalas de acuerdo** (provisoria). Las validaciones de la ASES, la ESPU y la MSPSS no publican su instrucción. Usamos una genérica: «Indica qué tan de acuerdo estás con cada afirmación».

## Escalas que quedan fuera

**D13. Fuera: ESA, LCQ-5 e incivilidad** (provisoria para la ESA, ver D6).

- **ESA:** se pisa con el UWES (D6).
- **LCQ-5:** pertinencia baja, y en la versión española pregunta por un profesor en particular. El ítem 9 de la ESPU («Los profesores muestran interés y compromiso…») ya da una mirada a los docentes.
- **Incivilidad:** no hay escala validada para universitarios en español; habría que redactar ítems nuevos y validarlos, y además obligaría a incluir la LCQ (9 ítems en total).

## Presentación

**D14. Las preguntas de contexto van de a dos por pantalla** (firme). Primera generación con trabajo remunerado, vivienda con traslado, y primera opción con otra carrera. La pregunta abierta de comentarios va en la misma pantalla que el cierre. Así la encuesta pasa de 24 a 20 pantallas (19 desde D15). Cada pregunta conserva su propia columna en la exportación.

**D15. Consentimiento informado en una sola pantalla, versión 2.0** (provisoria hasta que la apruebe el CEBB). La pantalla trae un resumen, el documento completo en un desplegable (y en PDF para descargar), «¿Aceptas participar?» y la autorización del registro académico. La autorización sigue siendo una pregunta aparte (la ley pide autorizar cada fin por separado), con su propia columna, y se puede responder que no y participar igual. El documento completo (`encuesta/documentos/consentimiento-informado.md`) actualiza la versión 1.0, que ya no describía el estudio: toda la CFM, la app propia en vez de Google Forms, 10–15 minutos en tres olas, el registro académico, los compañeros nombrados que no participan, la seudonimización en vez de «anonimización», y la descarga en vez de una «copia firmada». En la segunda y la tercera ola se recordarán las condiciones, con la opción de retirarse, en vez de repetir el consentimiento completo.

**D16. Metapercepción para las tres redes, en una pantalla** (firme). Después de las tres preguntas de nombres, una pantalla pregunta cuántas personas cree cada quien que lo marcaron en cada red (afinidad, ayuda y estudio). Cada versión mide algo distinto: sentirse integrado, sentirse visto como competente y como compañero de estudio. No hay un problema ético nuevo: es una percepción sobre uno mismo, y nadie recibe nunca cuántas personas lo marcaron de verdad.

**D17. «Padres», no «padres o tutores»** (firme). En la pregunta de primera generación: en la universidad no hay apoderados ni tutores.

# Pendientes

1. Elegir qué fases de López-Angulo et al. (2025) usar y cargarlas en la encuesta (D3).
2. Confirmar las etiquetas de la ASES con Calderón (D8).
3. Pedir a Medrano la ESA referida a la carrera, si queremos reabrir D6.
4. Completar el consentimiento 2.0 (contacto de la DISE, dónde se guardan los datos y por cuánto tiempo) y enviarlo al CEBB.
5. Piloto: revisar el ítem 7 de la ASES, la estructura de cada escala y las correlaciones entre constructos (AFC con todos, HTMT, EGA).
