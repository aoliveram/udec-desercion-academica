"""Instrumento: encuesta para estudiantes de la Facultad de Ciencias Físicas y Matemáticas (CFM, UdeC).

ESTE ES EL ÚNICO ARCHIVO QUE HAY QUE EDITAR PARA CAMBIAR LA ENCUESTA.
Cada elemento de PREGUNTAS es una página. Los tipos de página y sus
opciones están explicados en motor/preguntas.py.

Estado: BORRADOR. Sigue la estructura del reporte del semestre 2026
(sección 2): módulos de consentimiento, redes, intención de abandono,
escalas validadas, ficha de contexto y cierre. Lo que falta está marcado
con "[POR COMPLETAR: ...]" (en el texto que ve quien responde) o con
"POR COMPLETAR" (en los comentarios).

Reglas para editar:

1. Escalas validadas (UWES-9S, ASES, ESPU, UCLA-3, MSPSS-Familia):
   copiar el texto de cada ítem y su formato de respuesta TAL CUAL aparecen
   en el artículo de validación citado. No reescribirlos. Las decisiones
   sobre qué escalas entran están en instrumento/decisiones.md.
2. Ítems nuevos (sin escala validada): marcarlos con `fuente=NUEVO`. Pasan
   por jueces expertos y entrevistas cognitivas antes de aplicarse.
3. Cada `id` es el nombre de la columna en la exportación: corto, en
   minúsculas, sin tildes ni espacios, y que no cambie una vez aplicada la
   encuesta.
4. Subir VERSION cada vez que cambie algo que ve quien responde. Queda
   registrada junto a cada respuesta.

Para revisar el instrumento completo como documento (jueces, CEBB):
    python scripts/instrumento_a_md.py > instrumento.md
"""

from motor.preguntas import (
    abierta,
    arbol,
    bloque,
    grupo,
    consentimiento,
    identificacion,
    info,
    nominacion,
    numero,
    opcion_unica,
)

TITULO = "Encuesta CFM"
VERSION = "0.3-borrador"

NUEVO = "Ítem nuevo (reporte semestre 2026, §2.4)"

# --- Escalas de respuesta -----------------------------------------------------
# Cada escala validada usa el formato de su validación (no se cambia). Si el
# artículo solo da las etiquetas de los extremos, los puntos del medio van
# con su número.

SI_NO = ["Sí", "No"]

# ESPU (Alonso García y González Ortiz de Zárate, 2024). También para la ASES:
# su validación no publica las etiquetas (decisión en instrumento/decisiones.md).
ACUERDO_7_NADA_TOTAL = ["1 · Nada de acuerdo", "2", "3", "4", "5", "6", "7 · Totalmente de acuerdo"]

# MSPSS (López-Angulo et al., 2021).
ACUERDO_7_MUY = ["1 · Muy en desacuerdo", "2", "3", "4", "5", "6", "7 · Muy de acuerdo"]

# UWES-9S: frecuencia de 0 a 6, del manual (Schaufeli y Bakker, 2003, p. 49).
# En pantalla van solo los números (con «Nunca» y «Siempre» en los extremos);
# la etiqueta completa de cada punto aparece en una burbuja al pasar el cursor.
FRECUENCIA_UWES = ["0 · Nunca", "1", "2", "3", "4", "5", "6 · Siempre"]
FRECUENCIA_UWES_AYUDAS = [
    "Nunca (ninguna vez)",
    "Casi nunca (pocas veces al año)",
    "Algunas veces (una vez al mes o menos)",
    "Regularmente (pocas veces al mes)",
    "Bastantes veces (una vez por semana)",
    "Casi siempre (pocas veces por semana)",
    "Siempre (todos los días)",
]

# UCLA-3 (Hughes et al., 2004): hardly ever / some of the time / often.
FRECUENCIA_UCLA = ["Casi nunca", "Algunas veces", "A menudo"]


# --- Módulo 0: bienvenida, consentimiento e identificación --------------------

BIENVENIDA = info(
    "bienvenida",
    "Esta encuesta es parte de un estudio sobre la experiencia de estudiar en la Facultad de "
    "Ciencias Físicas y Matemáticas (CFM) de la Universidad de Concepción. No es una prueba: no "
    "hay respuestas buenas ni malas.\n\n"
    "Toma entre 10 y 15 minutos. Tus respuestas se guardan a medida que avanzas, y si se "
    "corta la conexión puedes retomar desde el mismo enlace.",
)

# POR COMPLETAR: reemplazar por el texto aprobado por el CEBB. Este borrador
# solo recoge los puntos que el reporte (sección 4) recomienda incluir.
CONSENTIMIENTO = consentimiento(
    "consentimiento",
    "**Consentimiento informado (BORRADOR — reemplazar por el texto aprobado por el CEBB)**\n\n"
    "- **Objetivo.** Conocer cómo se relacionan las redes de compañerismo, la experiencia "
    "académica y la intención de continuar en la carrera.\n"
    "- **Voluntariedad.** Participar es voluntario. Puedes no contestar cualquier pregunta y "
    "dejar la encuesta cuando quieras, sin ninguna consecuencia.\n"
    "- **Compañeros y compañeras.** Algunas preguntas te piden marcar nombres de la lista del "
    "curso. Esas personas aparecerán en los datos aunque no participen, siempre con un código "
    "en lugar de su nombre.\n"
    "- **Confidencialidad.** Nadie del curso, ningún docente ni la jefatura de carrera verá tus "
    "respuestas. Los resultados se publican solo de forma agregada.\n"
    "- **Sin consecuencias académicas.** Nadie recibirá un puntaje de riesgo individual.\n"
    "- **Contacto.** [POR COMPLETAR: nombre y correo del profesor/a responsable y del CEBB-UdeC].",
)

AUTORIZA_REGISTROS = opcion_unica(
    "autoriza_registros",
    "¿Autorizas al equipo a consultar tu registro académico (estado de matrícula en 2027, "
    "puntajes de admisión y créditos aprobados), solo para este estudio?",
    SI_NO,
    constructo="Consentimiento",
    fuente="Reporte semestre 2026, §2.5",
)

IDENTIFICACION = identificacion("identificacion")


# --- Módulo 1: redes (generadores de nombres) --------------------------------

INSTRUCCIONES_REDES = info(
    "instrucciones_redes",
    "En las próximas preguntas verás una lista de estudiantes de la CFM, agrupada por año de "
    "ingreso. Puedes buscar por nombre.\n\n"
    "Marca a quienes correspondan. **No hay un número correcto**: puedes marcar a varias "
    "personas, a una o a nadie (en ese caso, marca «No hay nadie»).",
)

G1_AFINIDAD = nominacion(
    "g1_afinidad",
    "¿Con quiénes de la lista pasas tiempo o conversas de temas que no son de la universidad, "
    "dentro o fuera del campus (también en línea)?",
    maximo=15,
    constructo="Integración social (red de afinidad)",
    fuente="Reporte semestre 2026, §2.6 (G1)",
)

G2_AYUDA = nominacion(
    "g2_ayuda",
    "Cuando no entiendes una materia o un ejercicio, ¿a quiénes de la lista sueles pedirle "
    "ayuda o con quiénes comparas resultados?",
    maximo=15,
    constructo="Integración académica (red de ayuda)",
    fuente="Reporte semestre 2026, §2.6 (G2)",
)

G3_ESTUDIO = nominacion(
    "g3_estudio",
    "¿Con quiénes de la lista estudias o resuelves guías y tareas habitualmente?",
    maximo=15,
    constructo="Integración académica (red de estudio)",
    fuente="Reporte semestre 2026, §2.6 (G3)",
)

METAPERCEPCION = numero(
    "meta_afinidad",
    "¿Cuántas personas de la lista crees que te marcaron a ti en la primera pregunta "
    "(con quiénes pasan tiempo o conversan)?",
    maximo="nomina",
    constructo="Metapercepción",
    fuente="Reporte semestre 2026, §2.6",
)

LAZOS_FUERA = numero(
    "lazos_otras_carreras",
    "¿Cuántas personas cercanas tienes en otras carreras de la UdeC?",
    maximo=100,
    constructo="Integración social (fuera de la nómina)",
    fuente="Reporte semestre 2026, §2.6",
)


# --- Módulo 2: intención de abandono (POR COMPLETAR) ----------------------------
# Placeholder hasta tener los ítems de López-Angulo, Muñoz-Inostroza,
# Sáez-Delgado, Chandia, Mella-Norambuena y Brito-Álvarez (2025), Journal of
# College Student Retention (escalas de intención de abandono y de cambio de
# carrera, validadas en Chile).

INTENCION = info(
    "intencion_pendiente",
    "**[POR COMPLETAR: preguntas de intención de abandono]**\n\n"
    "Aquí irán los ítems de las escalas de intención de abandono y de cambio de carrera de "
    "López-Angulo et al. (2025), cuando tengamos el artículo.",
)


# --- Módulos 3 y 4: escalas validadas ---------------------------------------
# Elegidas en noviembre de 2026; el porqué de cada una (y de las que quedaron
# fuera: ESA, LCQ-5, incivilidad, MSPSS completa) está en
# instrumento/decisiones.md. Ítems copiados textuales del artículo citado.

# Módulo 3: integración académica

UWES = bloque(
    "uwes",
    "Las siguientes preguntas se refieren a los sentimientos de las personas en sus estudios. "
    "Por favor, lea cuidadosamente cada pregunta y decida si se ha sentido de esta forma. "
    "Si nunca se ha sentido así, marque «Nunca»; en caso contrario, indique cuántas veces se ha "
    "sentido así.",
    items=[
        ("uwes_vi1", "Mis tareas como estudiante me hacen sentir lleno de energía"),
        ("uwes_vi2", "Me siento fuerte y vigoroso cuando estoy estudiando o voy a las clases"),
        ("uwes_de2", "Estoy entusiasmado con mi carrera"),
        ("uwes_de3", "Mis estudios me inspiran cosas nuevas"),
        ("uwes_vi3", "Cuando me levanto por la mañana me apetece ir a clase o estudiar"),
        ("uwes_ab3", "Soy feliz cuando estoy haciendo tareas relacionadas con mis estudios"),
        ("uwes_de4", "Estoy orgulloso de hacer esta carrera"),
        ("uwes_ab4", "Estoy inmerso en mis estudios"),
        ("uwes_ab5", "Me “dejo llevar” cuando realizo mis tareas como estudiante"),
    ],
    opciones=FRECUENCIA_UWES,
    ayudas=FRECUENCIA_UWES_AYUDAS,
    constructo="Compromiso académico (UWES-9S): vigor (vi), dedicación (de), absorción (ab)",
    fuente="Schaufeli y Bakker (2003), manual en español, p. 49; validación chilena: Carmona-Halty et al. (2019)",
)

ASES = bloque(
    "ases",
    "Indica qué tan de acuerdo estás con cada afirmación.",
    items=[
        ("ases_01", "Sé cómo organizar mi tiempo para cumplir con una tarea académica."),
        ("ases_02", "Sé cómo tomar apuntes."),
        ("ases_03", "Sé cómo estudiar para que me vaya bien en una prueba."),
        ("ases_04", "Soy bueno haciendo trabajos escritos y de investigación"),
        ("ases_05", "Soy un muy buen estudiante."),
        ("ases_06", "Normalmente obtengo muy buenas notas de mis trabajos académicos."),
        ("ases_07", "Encuentro que mis actividades académicas son interesantes y apasionantes."),
        (
            "ases_08",
            "Me siento seguro(a) de que podré enfrentar con éxito todas las exigencias que se me "
            "presenten en la universidad.",
        ),
    ],
    opciones=ACUERDO_7_NADA_TOTAL,
    constructo="Autoeficacia académica (ASES): factor 1 = ítems 1-4, factor 2 = ítems 5-8",
    fuente="Chemers et al. (2001); validación chilena: Calderón Carvajal et al. (2019)",
)

# Módulo 4: integración social

ESPU = bloque(
    "espu",
    "Indica qué tan de acuerdo estás con cada afirmación.",
    items=[
        ("espu_int_01", "Interactúo socialmente con compañeros de clase dentro y fuera de la Universidad"),
        ("espu_int_02", "Me siento integrado dentro de clase"),
        ("espu_int_03", "Tengo afecto por mis compañeros"),
        ("espu_int_04", "Tengo muchos amigos estudiando en esta Universidad"),
        ("espu_int_05", "En la universidad me siento aceptado por los demás"),
        ("espu_org_06", "Estaría orgulloso de apoyar a mi universidad en lo que pueda en el futuro"),
        ("espu_org_07", "Creo que hay suficientes recursos para los estudiantes en el campus"),
        ("espu_org_08", "Me gusta que otros sepan que estudio en esta universidad"),
        ("espu_org_09", "Los profesores muestran interés y compromiso en el aprendizaje de los estudiantes"),
        ("espu_org_10", "Me siento a gusto en las instalaciones de la universidad: aulas, biblioteca, cafetería"),
    ],
    opciones=ACUERDO_7_NADA_TOTAL,
    constructo="Sentido de pertenencia (ESPU): integración social (int) y orgullo (org)",
    fuente="Alonso García y González Ortiz de Zárate (2024), Tabla 2",
)

UCLA3 = bloque(
    "ucla3",
    "Las siguientes preguntas son sobre cómo te sientes respecto de distintos aspectos de tu vida. "
    "Para cada una, indica con qué frecuencia te sientes así.",
    items=[
        ("ucla_01", "¿Con qué frecuencia sientes que te falta compañía?"),
        ("ucla_02", "¿Con qué frecuencia te sientes excluido?"),
        ("ucla_03", "¿Con qué frecuencia te sientes aislado de los demás?"),
    ],
    opciones=FRECUENCIA_UCLA,
    constructo="Soledad (UCLA-3)",
    fuente="Hughes et al. (2004); versión española: Trucharte et al. (2023)",
)

MSPSS_FAMILIA = bloque(
    "mspss_familia",
    "Indica qué tan de acuerdo estás con cada afirmación.",
    items=[
        ("mspss_a3", "Mi familia me da la ayuda y apoyo emocional que requiero"),
        ("mspss_a4", "Tengo la seguridad que mi familia trata de apoyarme"),
        ("mspss_a8", "Mi familia me ayuda a tomar decisiones"),
        ("mspss_a11", "Puedo conversar de mis problemas con mi familia"),
    ],
    opciones=ACUERDO_7_MUY,
    constructo="Apoyo social percibido de la familia (MSPSS, subescala Familia)",
    fuente="Zimet et al. (1988); López-Angulo et al. (2021), Tabla 5",
)


# --- Módulo 7: ficha de contexto (ítems nuevos) ------------------------------
# Lo que ya está en los registros (PAES, NEM, vía de admisión, beneficios)
# no se pregunta: se pide al registro académico con la autorización de arriba.

CTX_PRIMERA_GENERACION = opcion_unica(
    "ctx_padres_educacion_superior",
    "¿Alguno de tus padres o tutores estudió en la educación superior (universidad, instituto o CFT)?",
    ["Sí", "No", "No lo sé"],
    constructo="Contexto: primera generación",
    fuente=NUEVO,
)

CTX_TRABAJO = arbol(
    "ctx_trabajo",
    raiz="trabaja",
    nodos={
        "trabaja": {
            "texto": "¿Tienes actualmente un trabajo remunerado?",
            "opciones": SI_NO,
            "siguiente": {"Sí": "horas"},
        },
        "horas": {
            "texto": "¿Cuántas horas a la semana trabajas, aproximadamente?",
            "opciones": ["Menos de 10", "Entre 10 y 20", "Más de 20"],
        },
    },
    constructo="Contexto: trabajo remunerado",
    fuente=NUEVO,
)

CTX_VIVIENDA = opcion_unica(
    "ctx_vivienda",
    "Durante el semestre, ¿con quién vives?",
    ["Con mi familia", "En pensión o residencia", "Con amigos/as o compañeros/as", "Solo/a", "Otra situación"],
    constructo="Contexto: vivienda",
    fuente=NUEVO,
)

CTX_TRASLADO = opcion_unica(
    "ctx_traslado",
    "¿Cuánto te demoras normalmente en llegar a la universidad (solo ida)?",
    ["Menos de 30 minutos", "Entre 30 y 60 minutos", "Entre 1 y 2 horas", "Más de 2 horas"],
    constructo="Contexto: traslado",
    fuente=NUEVO,
)

CTX_PRIMERA_OPCION = opcion_unica(
    "ctx_primera_opcion",
    "¿Tu carrera actual fue tu primera opción al postular?",
    SI_NO,
    constructo="Contexto: preferencia",
    fuente=NUEVO,
)

CTX_OTRA_CARRERA = opcion_unica(
    "ctx_otra_carrera",
    "¿Estudiaste otra carrera antes de entrar a tu carrera actual?",
    SI_NO,
    constructo="Contexto: trayectoria",
    fuente=NUEVO,
)


# --- Cierre --------------------------------------------------------------------

COMENTARIOS = abierta(
    "comentarios",
    "¿Quieres agregar algo sobre tu experiencia en la carrera o sobre esta encuesta? (opcional)",
)

CIERRE = info(
    "cierre_texto",
    "Llegaste al final. Presiona **Enviar** para terminar.\n\n"
    "¡Gracias por participar! Si alguna pregunta te removió algo y quieres conversarlo, puedes "
    "escribir a [POR COMPLETAR: contacto de apoyo estudiantil de la UdeC].",
)


# --- Orden de las páginas ------------------------------------------------------

PREGUNTAS = [
    # Módulo 0
    BIENVENIDA,
    CONSENTIMIENTO,
    AUTORIZA_REGISTROS,
    IDENTIFICACION,
    # Módulo 1: redes
    INSTRUCCIONES_REDES,
    G1_AFINIDAD,
    G2_AYUDA,
    G3_ESTUDIO,
    METAPERCEPCION,
    LAZOS_FUERA,
    # Módulo 2: intención de abandono (placeholder)
    INTENCION,
    # Módulo 3: integración académica
    UWES,
    ASES,
    # Módulo 4: integración social
    ESPU,
    UCLA3,
    MSPSS_FAMILIA,
    # Módulo 7: contexto, de a dos preguntas por página
    grupo("ctx_familia_trabajo", [CTX_PRIMERA_GENERACION, CTX_TRABAJO]),
    grupo("ctx_vivienda_traslado", [CTX_VIVIENDA, CTX_TRASLADO]),
    grupo("ctx_trayectoria", [CTX_PRIMERA_OPCION, CTX_OTRA_CARRERA]),
    # Cierre: comentarios y despedida en la última página
    grupo("cierre", [COMENTARIOS, CIERRE]),
]
