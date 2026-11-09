# Construcción del instrumento: fichas por constructo

Aquí se decide qué entra a la encuesta. Hay una ficha por constructo; cuando
una escala queda elegida y sus ítems están copiados textuales del artículo de
validación, se carga en [`encuesta/instrumento.py`](../encuesta/instrumento.py).

| Archivo | Qué es |
|:--|:--|
| [`decisiones.pdf`](decisiones.pdf) (fuente: `decisiones.md`) | **Las decisiones tomadas**: qué escalas entran, por qué, y qué queda pendiente |
| [`preguntas-encuesta.pdf`](preguntas-encuesta.pdf) | La encuesta pantalla por pantalla, tal como la ve un estudiante. Se genera desde `instrumento.py` con `python scripts/instrumento_a_pdf.py` (en `encuesta/`) |
| [`items-Informe.docx`](items-Informe.docx) | El Word con las escalas, revisado y comentado por Aníbal y Yannely |
| [`items-extraidos.pdf`](items-extraidos.pdf) (fuente: `items-extraidos.md`) | Los ítems copiados de cada paper, incluidas las escalas que quedaron fuera |
| [`escalas-items.docx`](escalas-items.docx) | La versión anterior del Word, sin comentarios |

Regla de oro: los ítems de una escala validada se copian **textuales** del
artículo. Si se cambia la redacción, deja de ser la escala validada.

## Estado

| Constructo | Escala | Ítems | Decisión |
|:--|:--|:-:|:--|
| Intención de abandono | López-Angulo et al. (2025) | por definir | Entra; falta conseguir el artículo (placeholder en la encuesta) |
| Compromiso académico | UWES-9S | 9 | Entra (provisoria, por sobre la ESA) |
| Autoeficacia académica | ASES | 8 | Entra |
| Sentido de pertenencia | ESPU | 10 | Entra |
| Soledad | UCLA-3 | 3 | Entra |
| Apoyo social percibido | MSPSS, solo subescala Familia | 4 | Entra |
| Satisfacción académica | ESA | — | Fuera (se pisa con el UWES) |
| Relación con docentes | LCQ-5 + incivilidad | — | Fuera |

Presupuesto: 34 ítems de escalas (~4 min). Con redes, contexto e intención,
la encuesta debería quedar en 10–13 minutos. El detalle está en
[`decisiones.pdf`](decisiones.pdf).

Las fichas de abajo son de la etapa de búsqueda de escalas (octubre de 2026).

## Qué anotar en cada ficha

Número de ítems · formato de respuesta (puntos y etiquetas) · población y N de
la validación · estructura factorial · confiabilidad (α u ω) · ítems
invertidos · si es de uso libre · referencia completa.

---

## Autoeficacia académica: ASES

- **Original:** Chemers, Hu y Garcia (2001). 8 ítems.
- **Validación chilena:** Calderón Carvajal et al. (2019), *Salud & Sociedad*
  10(2), 164–172. N = 4.950 universitarios chilenos; Likert de 7 puntos.
  Acceso abierto: [revista](https://revistas.ucn.cl/index.php/saludysociedad/article/view/3746).
- **Pendiente:** texto exacto de los 8 ítems, etiquetas de la escala, invertidos.
- **Decisión:**

## Satisfacción académica: ESA

- **Original:** Lent et al. (2007). 7 ítems, un factor.
- **Validación chilena:** Vergara-Morales et al. (2018), *Psicología
  Educativa* 24(2), 99–106. N = 608, siete universidades.
- **Pendiente:** ítems, formato de respuesta.
- **Decisión:**

## Sentido de pertenencia: ESPU

- **Validación:** Alonso García y González Ortiz de Zárate (2024), *RIDEP*
  73(3), 5–17 (España, N = 812). Versión final de 10 ítems; el resumen habla
  de tres factores pero la Tabla 2 muestra dos (integración social y orgullo).
- **Ojo:** Correa-Rojas et al. (2024), *Ciencias Psicológicas* 18(1) (Perú),
  usa la misma sigla pero es **otra escala**: adapta una escala escolar
  (Akar-Vural et al., 2013) e incluye un factor de respeto a las normas. No
  sirve como versión latinoamericana de la ESPU española.
- **Pendiente:** ítems, formato, decidir qué versión se usa.
- **Decisión:**

## Compromiso académico: UWES-9S

- **Original:** Schaufeli et al. (2002).
- **Validación chilena:** Carmona-Halty, Schaufeli y Salanova (2019),
  *Frontiers in Psychology* 10, 1017 (acceso abierto). También Guerra Díaz y
  Jorquera Gutiérrez (2021). Uso libre con fines académicos.
- **Pendiente:** ítems en español, formato (frecuencia de 7 puntos en el original).
- **Decisión:**

## Apoyo social percibido: MSPSS

- **Original:** Zimet et al. (1988). 12 ítems, tres fuentes: familia, amigos,
  otros significativos.
- **Validación chilena:** López-Angulo, Pérez-Villalobos, Bernardo, Cobo
  Rendón, Sáez Delgado y Díaz-Mujica (2021), *RIDEP* 58(1), 127–140.
  N = 1.975 de 1.º y 2.º año en universidades del sur de Chile; α entre 0,86 y
  0,93; invariante por sexo. Acceso abierto en
  [Redalyc](https://www.redalyc.org/journal/4596/459669141011/459669141011.pdf).
- **Pendiente:** ítems, formato.
- **Decisión:**

## Soledad: UCLA-3

- **Original:** Hughes et al. (2004). 3 ítems, respuesta de 3 puntos.
- **Versión española:** Trucharte et al. (2023), *Current Psychology* 42(9)
  (España, N = 1.951, unifactorial, α = 0,82). Usar su redacción en vez de la
  traducción de trabajo del reporte.
- **Pendiente:** ítems en español y etiquetas de respuesta.
- **Decisión:**

## Relación con docentes

**Polo positivo: apoyo a la autonomía (LCQ-5).** Núñez et al. (2012), *The
Spanish Journal of Psychology* 15(3), versión española con forma corta de 5
ítems (N = 422). Acceso abierto en el
[repositorio de la ULPGC](https://accedacris.ulpgc.es/handle/10553/42816).

**Polo negativo: incivilidad docente (ítems nuevos).** No hay escala validada
en español para universitarios. Base: Cortina et al. (2001) y la versión
española corta de Di Marco et al. (2018). Un ítem por conducta, escala de
frecuencia; el impacto se pregunta aparte. Nunca nombrar docentes ni
asignaturas. Requiere jueces y entrevistas cognitivas.

- **Decisión:**

---

## Fuera del núcleo por ahora

- **Identidad física** (Hazari et al., 2010). Hay una adaptación al español
  con estudiantes STEM mexicanos (González Peña, Morán-Soto y
  Rodriguez-Lara, 2024, *Humanities & Social Sciences Communications*).
- **Costo percibido** (Flake et al., 2015). Sin versión en español.
- **DASS-21** (Antúnez y Vinet, 2012). Solo con protocolo de derivación.
