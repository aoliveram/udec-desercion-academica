---
title: "Reporte general del proyecto"
subtitle: "Abandono académico en la Facultad de Ciencias Físicas y Matemáticas (UdeC): qué medimos, por qué y con qué"
author: "Aníbal Olivera Morales y Yannely V. Salas Gutiérrez"
date: "13 de noviembre de 2026"
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
  - \definecolor{verde}{HTML}{3B7A2A}
  - \definecolor{gris}{HTML}{8A8F98}
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
  - \newunicodechar{≠}{\ensuremath{\neq}}
  - \usepackage{enumitem}
  - \setlist{itemsep=2pt,topsep=4pt}
  - \setlength{\parskip}{5pt}
  - \setlength{\parindent}{0pt}
  - \usepackage{pdflscape}
  - \usepackage{tikz}
  - \usetikzlibrary{positioning,fit,backgrounds,arrows.meta,calc}
---

# El proyecto en una página

**Pregunta.** ¿La forma en que los estudiantes se relacionan entre sí (con quiénes pasan tiempo, a quiénes piden ayuda y con quiénes estudian), junto con cómo viven sus estudios, ayuda a anticipar quiénes dejan su carrera?

**Marco teórico.** El modelo de integración de Tinto (1975): un estudiante persiste cuando está integrado en el sistema **académico** y en el **social** de la universidad. La novedad del proyecto es medir la integración social también desde afuera, con redes de estudiantes, y no solo con lo que cada persona declara.

**Hipótesis** (informe de agosto de 2026). «Entre las dos cohortes estudiadas, aquella cuya red de afinidad y colaboración presente una mayor fragmentación estructural —caracterizada por un mayor número de componentes desconectados, menor densidad global y una mayor proporción de nodos con baja centralidad— exhibirán una menor cohesión e integración social, lo que se asocia con una mayor tasa de deserción a nivel de cohorte.»

Al ampliar el estudio a toda la facultad y a tres olas, también se puede estudiar a nivel individual: si la posición en la red y la integración declarada predicen la intención de abandono, y esta, la deserción observada.

**Diseño.**

- **Población:** estudiantes de todas las carreras de la Facultad de Ciencias Físicas y Matemáticas (CFM) matriculados en 2026. Esperamos unos 350 respondientes.
- **Tres olas**, una por semestre: 2026-II, 2027-I y 2027-II. Cada encuesta toma entre 10 y 15 minutos y se envía por el correo UdeC.
- **Deserción observada** en el registro académico (matrícula en 2027 y 2028), con autorización explícita de cada participante. No se infiere de quién deja de responder.
- **Aplicación propia** en lugar de Google Forms. Los análisis usan códigos, nunca nombres.

**Equipo.** Dr. Hernán Astudillo (investigador responsable), Claudio Faúndez, Yannely Salas y Aníbal Olivera.

**Estado (13 de noviembre).** Al instrumento le faltan dos datos de contacto. El consentimiento 2.0 se envía al Comité de Ética (CEBB) la semana del 16 de noviembre; la encuesta, el 1 de diciembre.

```{=latex}
\begin{landscape}
\section{Mapa de constructos}
{\small Todo lo que estudiamos, ordenado según el modelo de Tinto: entrada, integración académica y social, intención y deserción. Entre paréntesis, el número de ítems; con $\triangleright$, la pantalla de \texttt{preguntas-encuesta.pdf} donde están. Todo se mide en cada ola (2026-II, 2027-I y 2027-II).}\par
\begin{center}
\vspace{10pt}
\resizebox{\linewidth}{!}{%
\begin{tikzpicture}[node distance=2.4mm,
mbase/.style={rectangle, rounded corners=2pt, font=\scriptsize\sffamily, align=left, inner sep=3pt,
               line width=0.6pt, text width=#1,
               execute at begin node={\hyphenpenalty=10000\exhyphenpenalty=10000}},
  mentra/.style={mbase=#1, draw=acento, fill=acento!10},
  mcond/.style={mbase=#1, draw=acento, fill=white, dash pattern=on 2.5pt off 1.5pt},
  mreg/.style={mbase=#1, draw=verde, fill=verde!12},
  mfuera/.style={mbase=#1, draw=gris, fill=white, dashed, text=gris},
  mcol/.style={font=\footnotesize\sffamily\bfseries, text=acento, text width=#1, inner sep=0pt, anchor=north west},
  mpanel/.style={draw=acento!35, rounded corners=4pt, inner sep=6pt, fill=white},
  mmarco/.style={draw=acento!55, rounded corners=6pt, inner sep=8pt, fill=fondo},
  mflecha/.style={-{Latex[length=2.6mm]}, line width=1.1pt, draw=acento!75},
  mnota/.style={font=\scriptsize\sffamily, text=gris}
]
% --- Entrada ---------------------------------------------------------------
\node[mcol=3.8cm] (tA) at (0,0) {Entrada};
\node[mentra=3.8cm, below=of tA] (ctx)
  {\textbf{Contexto} (6, ítems nuevos)\\primera generación, trabajo remunerado y horas, vivienda, traslado, primera opción, otra carrera previa\\{\color{acento}$\triangleright$ pantallas 19, 20 y 21}};
\node[mreg=3.8cm, below=of ctx] (reg)
  {\textbf{Registro académico}\\puntajes de admisión, créditos aprobados (con autorización)\\{\color{acento}$\triangleright$ autorización en la pantalla 2}};
\node[mentra=3.8cm, below=of reg] (fam)
  {\textbf{Apoyo de la familia}\\MSPSS, subescala Familia (4)\\{\color{acento}$\triangleright$ pantalla 17}};
\node[mfuera=3.8cm, below=of fam] (amig)
  {\textbf{MSPSS Amigos y Otros significativos} (8)\\se pisan con la red y la ESPU\\{$\triangleright$ no está en la encuesta}};

% --- Integración académica ---------------------------------------------------
\node[mcol=4cm] (tB1) at (5.2,0) {Integración académica};
\node[mentra=4cm, below=of tB1] (uwes)
  {\textbf{Compromiso académico}\\UWES-9S (9): vigor, dedicación, absorción\\{\color{acento}$\triangleright$ pantalla 13}};
\node[mentra=4cm, below=of uwes] (ases)
  {\textbf{Autoeficacia académica}\\ASES (8)\\{\color{acento}$\triangleright$ pantalla 14}};
\node[mentra=4cm, below=of ases] (redac)
  {\textbf{Redes de ayuda (G2) y de estudio (G3)}\\nombres de una lista (2)\\{\color{acento}$\triangleright$ pantallas 6 y 7}};
\node[mentra=4cm, below=of redac] (metaac)
  {\textbf{Metapercepción}\\cuántos creo que me nombraron en G2 y G3 (2)\\{\color{acento}$\triangleright$ pantalla 8}};
\node[mfuera=4cm, below=of metaac] (esa)
  {\textbf{Satisfacción académica}, ESA (7)\\se pisa con el UWES\\{$\triangleright$ no está en la encuesta}};
\node[mentra=4cm, below=of esa] (inciv)
  {\textbf{Incivilidad docente}\\WIS corta, adaptada (4) + 1 ítem nuevo\\{\color{acento}$\triangleright$ pantalla 18}};
\node[mfuera=4cm, below=of inciv] (doc)
  {\textbf{Apoyo docente a la autonomía}\\LCQ-5 (5)\\{$\triangleright$ no está en la encuesta}};

% --- Integración social ------------------------------------------------------
\node[mcol=4cm] (tB2) at (10.3,0) {Integración social};
\node[mentra=4cm, below=of tB2] (espu)
  {\textbf{Sentido de pertenencia}\\ESPU (10): integración social, orgullo\\{\color{acento}$\triangleright$ pantalla 15}};
\node[mentra=4cm, below=of espu] (ucla)
  {\textbf{Soledad}\\UCLA-3 (3)\\{\color{acento}$\triangleright$ pantalla 16}};
\node[mentra=4cm, below=of ucla] (redaf)
  {\textbf{Red de afinidad (G1)}\\nombres de una lista (1)\\{\color{acento}$\triangleright$ pantalla 5}};
\node[mentra=4cm, below=of redaf] (metaaf)
  {\textbf{Metapercepción}\\cuántos creo que me nombraron en G1 (1)\\{\color{acento}$\triangleright$ pantalla 8}};
\node[mentra=4cm, below=of metaaf] (lazos)
  {\textbf{Lazos fuera de la nómina}\\amistades en otras facultades (1)\\{\color{acento}$\triangleright$ pantalla 9}};

% --- Intención -----------------------------------------------------------------
\node[mcol=3.8cm] (tC) at (16.0,0) {Intención (abandono y cambio de carrera)};
\node[mentra=3.8cm, below=6mm of tC] (f2)
  {\textbf{Fase 2: pensamientos} (6)\\la ven todos\\{\color{acento}$\triangleright$ pantalla 10}};
\node[mcond=3.8cm, below=of f2] (f3)
  {\textbf{Fase 3: deliberación} (6)\\solo si en la fase 2 hubo algo distinto de «1»\\{\color{acento}$\triangleright$ pantalla 11}};
\node[mcond=3.8cm, below=of f3] (f4)
  {\textbf{Fase 4: búsqueda de información} (6)\\solo si en la fase 3 hubo algo distinto de «1»\\{\color{acento}$\triangleright$ pantalla 12}};
\node[mfuera=3.8cm, below=of f4] (f15)
  {\textbf{Fases 1 (no encajar) y 5 (decisión final)} (12)\\la 1 se pisa con UWES y ESPU; la 5 casi no varía\\{$\triangleright$ no está en la encuesta}};

% --- Paneles (fondo) -----------------------------------------------------------
\begin{scope}[on background layer]
  \node[mmarco, fit=(tB1)(doc)(tB2)(lazos), inner ysep=10pt] (pB) {};
  \node[mpanel, fit=(tA)(amig)] (pA) {};
  \node[mpanel, fit=(tB1)(doc)] (pB1) {};
  \node[mpanel, fit=(tB2)(lazos)] (pB2) {};
  \node[mpanel, fit=(tC)(f15)] (pC) {};
\end{scope}
\node[mnota, anchor=south] at (pB.north) {Integración en la universidad (modelo de Tinto)};

% --- Resultado -------------------------------------------------------------------
\node[mcol=3.2cm, anchor=west] (tD) at ($(pC.east)+(0.9,1.2)$) {Resultado};
\node[mreg=3.2cm, below=of tD] (des)
  {\textbf{Deserción observada}\\registro 2027 y 2028: sigue en su carrera, se cambia de carrera o deja la UdeC\\{\color{acento}$\triangleright$ autorización en la pantalla 2}};
\begin{scope}[on background layer]
  \node[mpanel, fit=(tD)(des)] (pD) {};
\end{scope}

% --- Flechas ---------------------------------------------------------------------
\draw[mflecha] (pA.east |- pA.center) -- (pB.west |- pA.center);
\draw[mflecha] (pB.east |- pC.center) -- (pC.west |- pC.center);
\draw[mflecha] (pC.east |- pD.center) -- (pD.west |- pD.center);
\draw[mflecha, dash pattern=on 4pt off 2pt]
  ($(pB.north east)+(-1.2,0)$) .. controls ($(pB.north east)+(-0.6,1.5)$) and ($(pD.north |- pB.north)+(0,1.5)$) .. (pD.north)
  node[mnota, pos=0.5, above] {también directo, no solo a través de la intención};

% --- Leyenda --------------------------------------------------------------------
\node[mentra=2.6cm, anchor=north west] (l1) at ($(pA.south west |- pB.south)+(0,-0.6)$) {Entra a la encuesta};
\node[mcond=2.9cm, right=4mm of l1] (l2) {Entra, solo para algunos};
\node[mreg=3.1cm, right=4mm of l2] (l3) {Del registro académico};
\node[mfuera=2.6cm, right=4mm of l3] (l4) {Queda fuera};
\end{tikzpicture}}
\end{center}
\end{landscape}
```

# Constructos que medimos

## Resultado: deserción e intención

| Constructo | Qué capta y por qué | Instrumento | Ítems y formato | Validación |
|:-----------|:-------------------------------|:---------------|:--------------|:---------------|
| **Deserción observada** | Si la persona sigue en su carrera, se cambió a otra o dejó la UdeC. Es lo que queremos predecir. | Registro académico, matrícula en 2027 y 2028 (con autorización) | No se pregunta | — |
| **Intención de abandono y de cambio de carrera** | El paso previo a la deserción. Es continua y se mide en cada ola, lo que da potencia estadística (con 350 respondientes habría quizás 35 a 70 deserciones en tres semestres) y permite ver el mecanismo. Distingue dejar los estudios universitarios de cambiarse de carrera. | Bäulke et al. (2022), validación chilena de López-Angulo et al. (2025) | Fases 2 a 4: entre 6 y 18 ítems, según las respuestas. Acuerdo de 1 a 7 | N = 641 estudiantes chilenos de primer año; ω entre .83 y .97 por fase |

La escala original describe la decisión de abandonar como un proceso de cinco fases: percibir que uno no encaja, pensar en dejar o cambiarse, deliberar, buscar información y decidir. Usamos las fases 2, 3 y 4, cada una en su pantalla, con abandono arriba y cambio de carrera debajo. La fase 2 la ve todo el mundo; las otras dos se abren solo para quien marcó algo distinto de «1» en la fase anterior. Así, quien no piensa en irse responde 6 ítems, y quien sí, hasta 18.

## Redes de estudiantes

Son el aporte distintivo del proyecto. Siguen el formato usual de los *generadores de nombres* del análisis de redes sociales en cursos y escuelas:

- **Una relación por pregunta**, con un período de referencia: las instrucciones dicen que todo es sobre este semestre.
- **Se reconoce en una lista, no se recuerda de memoria.** Cada pregunta muestra la nómina completa de la CFM, agrupada por año de ingreso, con un buscador por nombre. Quien responde no aparece en la lista: su nombre queda fuera desde la pantalla de identificación.
- **Casillas, con un máximo amplio de 15** para no truncar las redes de quien tiene muchos vínculos. Solo al llegar a 15 aparece un aviso y las demás casillas se desactivan. Si no hay nadie, se marca «No hay nadie», que se guarda como una respuesta (cero vínculos) y no como un dato faltante.
- **Cada marca es un vínculo con dirección**, de quien marca a quien es marcado. Se exporta como una lista de vínculos con códigos, nunca con nombres. Quien no responde igual es parte de la red: otros pueden haberlo marcado.

Las preguntas son nuevas (reporte del semestre 2026, §2.6).

| Constructo | Pregunta (resumida) | Qué capta |
|:-----------|:-------------------------------|:-------------------------------|
| **Red de afinidad (G1)** | Con quiénes pasas tiempo o conversas de temas que no son de la universidad | Integración social, vista desde afuera |
| **Red de ayuda (G2)** | A quiénes sueles pedirles ayuda cuando no entiendes una materia o un ejercicio | Integración académica: quién es recurso para quién |
| **Red de estudio (G3)** | Con quiénes estudias o resuelves guías y tareas | Integración académica: colaboración |
| **Metapercepción** (una por red) | Cuántas personas crees que te marcaron a ti | Sentirse integrado, visto como competente y como compañero de estudio. Se compara con lo que dice la red; nadie recibe nunca cuántas personas lo marcaron de verdad |
| **Lazos fuera de la nómina** | Cuántas amistades cercanas tienes en la UdeC fuera de la CFM (0, 1 a 2, 3 a 5, 6 o más) | La integración social que la red de la CFM no ve: es común tener amistades en otras facultades |

Con estas redes se calculan, por cohorte, la fragmentación de la hipótesis original (componentes, densidad, centralidad) y, por persona, su posición: cuántos la nombran, si queda aislada, si sus vínculos están dentro o fuera de su cohorte.

## Escalas validadas

Todas se aplican completas (o como una subescala que es un factor propio en su validación) y con el formato de respuesta original. Los ítems se copian textuales del artículo.

| Constructo | Qué capta y por qué | Escala | Ítems y formato | Validación |
|:-----------|:-------------------------------|:---------------|:--------------|:---------------|
| **Compromiso académico** | Energía, dedicación y concentración en los estudios. Calza con el compromiso con la meta de titularse de Tinto. | UWES-9S (Schaufeli y Bakker, 2003; texto del manual en español) | 9 (vigor, dedicación, absorción). Frecuencia de 0 a 6 | Chile: Carmona-Halty et al. (2019), N = 1.502, α = .90, invarianza por sexo |
| **Autoeficacia académica** | Confianza en poder cumplir con las exigencias de la carrera. De los mejores predictores de permanencia. | ASES (Chemers et al., 2001) | 8. Acuerdo de 1 a 7 (etiquetas por confirmar) | Chile: Calderón Carvajal et al. (2019), N = 4.950, α = .82 |
| **Sentido de pertenencia** | Sentirse aceptado e incluido en la universidad: la versión *sentida* de la integración social. | ESPU (Alonso García y González Ortiz de Zárate, 2024) | 10 (integración social, orgullo). Acuerdo de 1 a 7 | España: N = 812, α = .83 y .78 |
| **Incivilidad docente** | Trato descortés de profesores (no escuchar, interrumpir, ignorar, burlarse, descalificar). Tinto incluye la calidad de las interacciones con docentes; en Sharif-Nia et al. (2023) el acoso de docentes aumenta la intención de abandono a través de la pertenencia y la satisfacción. | WIS corta (Cortina et al., 2001), adaptada a docentes y a «este semestre», más 1 ítem nuevo | 4 + 1. Frecuencia de 1 a 5 | España: Di Marco et al. (2018), N = 407 trabajadores, α = .75. Sin validación en estudiantes |
| **Soledad** | Tener menos relaciones, o menos cercanas, de las que uno quisiera. Comparada con la red, separa a quien está aislado de quien se siente aislado. | UCLA-3 (Hughes et al., 2004) | 3. Frecuencia de 3 puntos | España: Trucharte et al. (2023), N = 1.951, α = .82 |
| **Apoyo de la familia** | El apoyo que viene de fuera de la universidad, que la red no ve. | MSPSS, subescala Familia (Zimet et al., 1988) | 4. Acuerdo de 1 a 7 | Chile: López-Angulo et al. (2021), N = 1.975 universitarios, α = .90 |

## Contexto y registro académico

| Constructo | Cómo se obtiene | Por qué |
|:-----------|:-------------------------------|:-------------------------------|
| **Primera generación** | Pregunta: si alguno de los padres estudió en la educación superior | Recursos y orientación familiar sobre la universidad |
| **Trabajo remunerado** | Pregunta, y si trabaja, cuántas horas a la semana | Compite con el tiempo de estudio y de integración |
| **Vivienda y traslado** | Dos preguntas: con quién vive y cuánto demora en llegar | Condicionan cuánto tiempo pasa en el campus |
| **Preferencia y trayectoria** | Dos preguntas: si la carrera fue su primera opción y si estudió otra antes | Compromiso inicial con la carrera |
| **Admisión y rendimiento** | Registro académico: puntajes de admisión y créditos aprobados | Características de entrada y el predictor más fuerte de retención en un estudio previo en la Facultad de Ingeniería de la UdeC. No se preguntan, para no alargar la encuesta |

# Constructos que quedan fuera

| Constructo | Escala revisada | Por qué queda fuera | Cuándo reabrir |
|:-----------|:---------------|:-------------------------------|:-----------------|
| **Satisfacción académica** | ESA (Lent et al., 2007); Chile: Vergara-Morales et al. (2018), N = 608, 7 ítems | Se pisa con el UWES: varios ítems casi se repiten, y con 350 casos no podríamos separar sus efectos. Además, la versión chilena pregunta por «esta asignatura», no por la carrera | Si Medrano nos envía la versión referida a la carrera. Entonces la elección entre UWES y ESA sería teórica |
| **Apoyo docente a la autonomía** | LCQ-5 (Núñez et al., 2012), N = 422, 5 ítems | Pertinencia baja; pregunta por un profesor en particular. El ítem 9 de la ESPU ya mira a los docentes | Si la primera ola muestra que la relación con docentes pesa |
| **Apoyo de amigos y de otros significativos** | MSPSS, subescalas Amigos y Otros significativos (8 ítems) | No distinguen si los amigos son de la universidad y se pisan con la red y con la ESPU | — |
| **No encajar en la carrera** | Fase 1 de las escalas de intención (6 ítems) | Su contenido se pisa con el UWES y la ESPU: inflaría la relación entre predictores e intención | — |
| **Decisión final de abandonar** | Fase 5 de las escalas de intención (6 ítems) | Casi todos marcan «1» (en la validación, curtosis cercana a 20), y quien ya decidió probablemente no responda las olas siguientes. La deserción se ve en el registro | — |

También revisamos y descartamos: la «ESPU» peruana de Correa-Rojas et al. (2024), que con la misma sigla es otra escala (escolar, con un factor de respeto a las normas); la traducción de la MSPSS de Arechabala y Miranda (2002), hecha con adultos mayores (usamos el texto de López-Angulo et al., 2021); y las dos versiones de la ESA de Medrano, que no publican sus ítems o miden otra cosa.

# Largo de la encuesta

\begin{nota}
\textbf{22 pantallas, entre 10 y 15 minutos.} Las escalas suman entre 45 y 57 ítems (unos 5 a 6,5 minutos a 7 segundos por ítem), según cuántas fases de intención vea cada persona. El resto es el consentimiento, la identificación, las tres preguntas de redes con su metapercepción y seis preguntas de contexto, de a dos por pantalla.
\end{nota}

| Bloque | Ítems | Pantallas |
|:-------|:-----:|:---------:|
| Bienvenida, consentimiento (con autorización del registro) e identificación | 2 | 3 |
| Redes: instrucciones, G1, G2, G3, metapercepción y lazos fuera | 7 | 6 |
| Intención de abandono y de cambio de carrera | 6 a 18 | 1 a 3 |
| UWES-9S, ASES, ESPU, UCLA-3, MSPSS Familia e incivilidad | 39 | 6 |
| Contexto y cierre con comentario abierto | 7 a 8 | 4 |

# Qué podremos responder

Lo que sigue es el plan de análisis en grandes líneas; se afinará con los datos de la primera ola.

- **A nivel de cohorte (hipótesis original):** si las cohortes con redes más fragmentadas tienen más deserción.
- **A nivel individual:** si la posición en la red y las escalas predicen la intención y la deserción observada, y si el efecto pasa por la intención (mediación) o es también directo.
- **Aislamiento visto desde afuera y sentido desde adentro:** comparar la red con la UCLA-3 y la ESPU, y la metapercepción con cuántas personas nombraron de verdad a cada quien.
- **Con tres olas:** separar **selección** (quien piensa irse se va aislando) de **influencia** (la intención se contagia entre amigos), con modelos de coevolución de red y conducta (RSiena).
- **Abandono frente a cambio de carrera:** si las redes y las escalas predicen distinto cada salida. Para esto el registro debe traer la carrera de matrícula, no solo si sigue matriculado.

# Pendientes

1. **Consentimiento 2.0:** contacto de la Dirección de Servicios Estudiantiles (DISE), dónde se guardan los datos y por cuánto tiempo. Envío al CEBB la semana del 16 de noviembre.
2. **Contacto de apoyo estudiantil** en la pantalla final de la encuesta.
3. **Registro académico:** pedirlo con la carrera de matrícula. Si además queremos vía de admisión o beneficios, el consentimiento tiene que nombrarlos (hoy autoriza matrícula, puntajes de admisión y créditos aprobados).
4. **Etiquetas de la ASES:** confirmarlas con Calderón, o cerrar el pendiente.
5. **Con los datos de la primera ola:** revisar el ítem 7 de la ASES, el ítem 4 de las escalas de intención, la estructura de cada escala y las correlaciones entre constructos.

# Referencias

Alonso García, S., y González Ortiz de Zárate, A. (2024). Validación de la Escala de Sentido de Pertenencia a la Universidad en España. *Revista Iberoamericana de Diagnóstico y Evaluación Psicológica*, 73(3), 5–17.

Bäulke, L., Grunschel, C., y Dresel, M. (2022). Student dropout at university: A phase-orientated view on quitting studies and changing majors. *European Journal of Psychology of Education*, 37(1), 853–876.

Calderón Carvajal, C., Carreño Mendoza, B., Micin Carvallo, S., y Urzúa Martínez, S. (2019). Estructura interna e invarianza métrica de la escala de autoeficacia académica ASES. *Salud & Sociedad*, 10(2), 164–172.

Carmona-Halty, M. A., Schaufeli, W. B., y Salanova, M. (2019). The Utrecht Work Engagement Scale for Students (UWES-9S): Factorial validity, reliability, and measurement invariance in a Chilean sample of undergraduate university students. *Frontiers in Psychology*, 10, 1017.

Chemers, M. M., Hu, L., y Garcia, B. F. (2001). Academic self-efficacy and first-year college student performance and adjustment. *Journal of Educational Psychology*, 93(1), 55–64.

Cortina, L. M., Magley, V. J., Williams, J. H., y Langhout, R. D. (2001). Incivility in the workplace: Incidence and impact. *Journal of Occupational Health Psychology*, 6(1), 64–80.

Di Marco, D., Martínez-Corts, I., Arenas, A., y Gamero, N. (2018). Spanish validation of the shorter version of the Workplace Incivility Scale: An employment status invariant measure. *Frontiers in Psychology*, 9, 959.

Hughes, M. E., Waite, L. J., Hawkley, L. C., y Cacioppo, J. T. (2004). A short scale for measuring loneliness in large surveys. *Research on Aging*, 26(6), 655–672.

Lent, R. W., Singley, D., Sheu, H.-B., Schmidt, J. A., y Schmidt, L. C. (2007). Relation of social-cognitive factors to academic satisfaction in engineering students. *Journal of Career Assessment*, 15(1), 87–97.

López-Angulo, Y., Muñoz-Inostroza, K., Sáez-Delgado, F., Chandia, E., Mella-Norambuena, J., y Brito-Álvarez, F. (2025). Validation of scales to measure dropout and changing majors intentions of Chilean university students. *Journal of College Student Retention: Research, Theory & Practice*. https://doi.org/10.1177/15210251251360672

López-Angulo, Y., Pérez-Villalobos, M. V., Bernardo, A. B., Cobo Rendón, R., Sáez Delgado, F., y Díaz-Mujica, A. (2021). Propiedades psicométricas de la Escala Multidimensional de Apoyo Social Percibido en estudiantes universitarios chilenos. *Revista Iberoamericana de Diagnóstico y Evaluación Psicológica*, 58(1), 127–140.

Núñez, J. L., León, J., Grijalvo, F., y Martín-Albo, J. (2012). Measuring autonomy support in university students: The Spanish version of the Learning Climate Questionnaire. *The Spanish Journal of Psychology*, 15(3), 1466–1472.

Schaufeli, W. B., y Bakker, A. B. (2003). *UWES: Utrecht Work Engagement Scale. Manual en español, versión para estudiantes*. Universidad de Utrecht.

Sharif-Nia, H., Marôco, J., Rahmatpour, P., Allen, K. A., Kaveh, O., y Hoseinzadeh, E. (2023). Bullying behaviors and intention to drop-out among nursing students: The mediation roles of sense of belonging and major satisfaction. *BMC Nursing*, 22, 417.

Tinto, V. (1975). Dropout from higher education: A theoretical synthesis of recent research. *Review of Educational Research*, 45(1), 89–125.

Trucharte, A., Calderón, L., Cerezo, E., Contreras, A., Peinado, V., y Valiente, C. (2023). Three-item loneliness scale: Psychometric properties and normative data of the Spanish version. *Current Psychology*, 42, 7466–7474.

Vergara-Morales, J., Del Valle, M., Díaz, A., y Pérez, M. V. (2018). Adaptación de la Escala de Satisfacción Académica en estudiantes universitarios chilenos. *Psicología Educativa*, 24(2), 99–106.

Zimet, G. D., Dahlem, N. W., Zimet, S. G., y Farley, G. K. (1988). The Multidimensional Scale of Perceived Social Support. *Journal of Personality Assessment*, 52(1), 30–41.
