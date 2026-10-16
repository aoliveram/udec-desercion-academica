"""Instrumento: encuesta para estudiantes de 1.º y 2.º año de Ciencias Físicas (FCFM, UdeC).

ESTE ES EL ÚNICO ARCHIVO QUE HAY QUE EDITAR PARA CAMBIAR LA ENCUESTA.
Cada elemento de PREGUNTAS es una página. Los tipos de página y sus
opciones están explicados en motor/preguntas.py.

Estado: BORRADOR. Sigue la estructura del reporte del semestre 2026
(sección 2): módulos de consentimiento, redes, intención de abandono,
escalas validadas, ficha de contexto y cierre. Lo que falta está marcado
con "[POR COMPLETAR: ...]" (en el texto que ve quien responde) o con
"POR COMPLETAR" (en los comentarios).

Reglas para editar:

1. Escalas validadas (ASES, ESA, UWES-9S, ESPU, MSPSS, UCLA-3, LCQ-5):
   copiar el texto de cada ítem y su formato de respuesta TAL CUAL aparecen
   en el artículo de validación citado. No reescribirlos.
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
    consentimiento,
    identificacion,
    info,
    nominacion,
    numero,
    opcion_unica,
)

TITULO = "Encuesta de Ciencias Físicas"
VERSION = "0.1-borrador"

NUEVO = "Ítem nuevo (reporte semestre 2026, §2.4)"

# --- Escalas de respuesta -----------------------------------------------------

ACUERDO_5 = ["Muy en desacuerdo", "En desacuerdo", "Ni de acuerdo ni en desacuerdo", "De acuerdo", "Muy de acuerdo"]
SI_NO = ["Sí", "No"]


# --- Módulo 0: bienvenida, consentimiento e identificación --------------------

BIENVENIDA = info(
    "bienvenida",
    "Esta encuesta es parte de un estudio sobre la experiencia de estudiar Ciencias Físicas "
    "en la Universidad de Concepción. No es una prueba: no hay respuestas buenas ni malas.\n\n"
    "Toma alrededor de 25 minutos. Tus respuestas se guardan a medida que avanzas, y si se "
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
    "En las próximas preguntas verás la lista de estudiantes de 1.º y 2.º año de Ciencias "
    "Físicas, agrupada por año de ingreso. Puedes buscar por nombre.\n\n"
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


# --- Módulo 2: intención de abandono (resultado proximal, ítems nuevos) ------

INTENCION = bloque(
    "intencion",
    "¿Qué tan de acuerdo estás con cada afirmación?",
    items=[
        ("int_dejar_carrera", "Durante este semestre he pensado seriamente en dejar la carrera de Ciencias Físicas."),
        ("int_cambiar_carrera", "Si pudiera, el próximo año me cambiaría a otra carrera."),
        ("int_terminar", "Estoy decidido/a a terminar esta carrera."),
        ("int_seguir_udec", "El próximo año pienso seguir estudiando en la Universidad de Concepción."),
    ],
    opciones=ACUERDO_5,
    constructo="Intención de abandono",
    fuente=NUEVO,
    invertidos=["int_terminar"],
)

INTENCION_DESTINO = opcion_unica(
    "int_destino",
    "Si dejaras Ciencias Físicas, ¿qué harías con mayor probabilidad?",
    [
        "Me cambiaría a otra carrera en la UdeC",
        "Me iría a otra universidad o instituto",
        "Dejaría de estudiar por un tiempo",
        "No lo he pensado",
    ],
    constructo="Intención de abandono",
    fuente=NUEVO,
)

INTENCION_CONDUCTA = opcion_unica(
    "int_averiguo_cambio",
    "En los últimos tres meses, ¿has averiguado formalmente sobre un cambio de carrera o un traslado?",
    SI_NO,
    constructo="Intención de abandono",
    fuente=NUEVO,
)


# --- Módulos 3 a 6: escalas validadas (POR COMPLETAR) ------------------------
#
# Cada escala es un bloque(). Plantilla (descomentar, pegar el texto textual
# de cada ítem y agregar la variable a PREGUNTAS más abajo):
#
# ESA = bloque(
#     "esa",
#     "<enunciado de la escala, tal como en la validación>",
#     items=[
#         ("esa_01", "<ítem 1, textual>"),
#         ("esa_02", "<ítem 2, textual>"),
#         # ... hasta esa_07
#     ],
#     opciones=ACUERDO_5,  # verificar el formato de respuesta en la validación
#     constructo="Satisfacción académica (ESA)",
#     fuente="Lent et al. (2007); validación chilena: Vergara-Morales et al. (2018)",
#     invertidos=[],  # ids de los ítems que se puntúan al revés, si los hay
# )
#
# Escalas previstas (reporte, secciones 2.4 y 2.7):
#
#   Módulo 3, integración académica
#     ASES     8 ítems   Chemers et al. (2001); Calderón Carvajal et al. (2019)
#     ESA      7 ítems   Lent et al. (2007); Vergara-Morales et al. (2018)
#     UWES-9S  9 ítems   Schaufeli et al. (2002); Carmona-Halty et al. (2019)
#   Módulo 4, integración social
#     ESPU    10 ítems   Alonso García y González Ortiz de Zárate (2024)
#     UCLA-3   3 ítems   Hughes et al. (2004)
#     MSPSS   12 ítems   Zimet et al. (1988); López-Angulo et al. (2021)
#   Módulo 5, docentes
#     LCQ-5    5 ítems   Núñez et al. (2012)
#     Incivilidad docente, 5-7 ítems nuevos (adaptar Cortina et al., 2001).
#       Frecuencia en un ítem, impacto en la motivación en otro; nunca
#       nombrar docentes ni asignaturas.
#   Módulo 6, disciplina
#     Identidad física 5-6 ítems (Hazari et al., 2010; traducir con TRAPD)
#     Costo percibido 4 ítems, uno por factor (Flake et al., 2015)
#
# Núcleo que no se recorta: redes, intención, ASES, ESA y ESPU. Si el piloto
# pasa de 25 minutos, recortar primero MSPSS y después UWES-9S.


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
    "¿Ciencias Físicas fue tu primera opción al postular?",
    SI_NO,
    constructo="Contexto: preferencia",
    fuente=NUEVO,
)

CTX_OTRA_CARRERA = opcion_unica(
    "ctx_otra_carrera",
    "¿Estudiaste otra carrera antes de entrar a Ciencias Físicas?",
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
    "cierre",
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
    # Módulo 2: intención de abandono
    INTENCION,
    INTENCION_DESTINO,
    INTENCION_CONDUCTA,
    # Módulos 3 a 6: escalas validadas (agregar aquí, p. ej. ESA, ASES, ESPU...)
    # Módulo 7: contexto
    CTX_PRIMERA_GENERACION,
    CTX_TRABAJO,
    CTX_VIVIENDA,
    CTX_TRASLADO,
    CTX_PRIMERA_OPCION,
    CTX_OTRA_CARRERA,
    # Cierre
    COMENTARIOS,
    CIERRE,
]
