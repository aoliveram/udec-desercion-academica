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

1. Escalas validadas (intención de abandono y de cambio de carrera, UWES-9S,
   ASES, ESPU, UCLA-3, MSPSS-Familia):
   copiar el texto de cada ítem y su formato de respuesta TAL CUAL aparecen
   en el artículo de validación citado. No reescribirlos. Las decisiones
   sobre qué escalas entran están en instrumento/decisiones.md.
2. Ítems nuevos (sin escala validada): marcarlos con `fuente=NUEVO`.
3. Cada `id` es el nombre de la columna en la exportación: corto, en
   minúsculas, sin tildes ni espacios, y que no cambie una vez aplicada la
   encuesta.
4. Subir VERSION cada vez que cambie algo que ve quien responde. Queda
   registrada junto a cada respuesta.

Para revisar el instrumento completo como documento (jueces, CEBB):
    python scripts/instrumento_a_md.py > instrumento.md
"""

from pathlib import Path

from motor.preguntas import (
    abierta,
    arbol,
    bloque,
    grupo,
    consentimiento,
    identificacion,
    info,
    mostrar_si,
    nominacion,
    numero,
    opcion_unica,
)

TITULO = "Encuesta CFM"
VERSION = "0.6-borrador"

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

# Consentimiento en una sola pantalla: un resumen, el documento completo en un
# desplegable (y en PDF para descargar), la decisión y la autorización del
# registro académico. POR COMPLETAR: es la versión 2.0 en borrador; reemplazar
# por la versión que apruebe el CEBB (documentos/consentimiento-informado.md).

AUTORIZA_REGISTROS = opcion_unica(
    "autoriza_registros",
    "¿Autorizas que el equipo consulte tu registro académico (matrícula en 2027 y 2028, puntajes "
    "de admisión y créditos aprobados), solo para este estudio? Puedes participar aunque "
    "respondas que no.",
    SI_NO,
    constructo="Consentimiento: registro académico",
    fuente="Consentimiento informado v2.0",
)

CONSENTIMIENTO = consentimiento(
    "consentimiento",
    "**Consentimiento informado**\n\n"
    "Te invitamos a participar en el estudio *Topología de redes de afinidad como predictor de "
    "abandono académico* (Departamento de Física, UdeC), para estudiantes de la Facultad de "
    "Ciencias Físicas y Matemáticas.\n\n"
    "- **Qué harás:** responder esta encuesta (10 a 15 minutos) en tres momentos: este "
    "semestre, el primero y el segundo de 2027. Preguntamos por tus compañeros y compañeras, tu "
    "experiencia de estudiar, el trato de tus profesores y algunos datos de contexto.\n"
    "- **Es voluntario:** puedes omitir cualquier pregunta, dejar la encuesta o retirarte del "
    "estudio cuando quieras, sin consecuencias. Si te retiras, borramos tus datos.\n"
    "- **Tus compañeros:** algunas preguntas piden marcar nombres de una lista. Esas personas "
    "aparecen en los datos con un código, nunca con su nombre, aunque no participen.\n"
    "- **Confidencialidad:** solo el equipo investigador ve los datos. Tu nombre se reemplaza por "
    "un código para unir tus respuestas de las tres encuestas. Ningún docente ni la jefatura verá "
    "respuestas individuales, y nadie recibirá un puntaje de riesgo. Los resultados se publican "
    "solo agregados.\n"
    "- **Riesgos:** algunas preguntas tocan temas como la soledad. Si algo te incomoda, puedes "
    "escribir a la DISE [POR COMPLETAR: contacto] o al investigador responsable.\n"
    "- **Contacto:** Dr. Hernán Astudillo (hastudil@udec.cl). Por tus derechos como participante: "
    "CEBB-UdeC (cebb@udec.cl).",
    documento=(Path(__file__).parent / "documentos" / "consentimiento-informado.md").read_text(encoding="utf-8"),
    documento_pdf="documentos/consentimiento-informado.pdf",
    acepto="Acepto participar y tengo 18 años o más",
    adicionales=[AUTORIZA_REGISTROS],
)

IDENTIFICACION = identificacion("identificacion")


# --- Módulo 1: redes (generadores de nombres) --------------------------------

INSTRUCCIONES_REDES = info(
    "instrucciones_redes",
    "Las próximas preguntas son sobre **este semestre**. En cada una verás una lista de "
    "estudiantes de la CFM, agrupada por año de ingreso. Puedes buscar por nombre.\n\n"
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
    "Cuando no entiendes una materia o un ejercicio, ¿a quiénes de la lista sueles pedirles ayuda?",
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

# Metapercepción: cuántas personas cree cada quien que lo marcaron, una por
# red, en una sola pantalla. Se compara con lo que dice la red (nadie recibe
# nunca cuántas personas lo marcaron de verdad).
METAPERCEPCION = grupo(
    "metapercepcion",
    [
        info(
            "metapercepcion_intro",
            "Ahora al revés: piensa en cuántas personas de la lista te marcaron **a ti** en cada "
            "una de las preguntas anteriores. No tienes que estar seguro/a; responde lo que creas.",
        ),
        numero(
            "meta_afinidad",
            "¿Cuántas personas crees que te marcaron como alguien con quien pasan tiempo o conversan?",
            maximo="nomina",
            constructo="Metapercepción (red de afinidad)",
            fuente="Reporte semestre 2026, §2.6",
        ),
        numero(
            "meta_ayuda",
            "¿Cuántas personas crees que te marcaron como alguien a quien le piden ayuda?",
            maximo="nomina",
            constructo="Metapercepción (red de ayuda)",
            fuente="Reporte semestre 2026, §2.6",
        ),
        numero(
            "meta_estudio",
            "¿Cuántas personas crees que te marcaron como alguien con quien estudian o resuelven "
            "guías y tareas?",
            maximo="nomina",
            constructo="Metapercepción (red de estudio)",
            fuente="Reporte semestre 2026, §2.6",
        ),
    ],
)

# Lazos fuera del límite de la red: la nómina es la CFM, así que las
# amistades de otras facultades no aparecen en G1-G3. En rangos, porque un
# número exacto es difícil de recordar.
LAZOS_FUERA = opcion_unica(
    "lazos_otras_carreras",
    "¿Cuántas amistades cercanas tienes en la UdeC fuera de la CFM, en otras facultades?",
    ["0", "1 a 2", "3 a 5", "6 o más"],
    constructo="Integración social (fuera de la nómina)",
    fuente="Reporte semestre 2026, §2.6",
)


# --- Módulo 2: intención de abandono y de cambio de carrera -------------------
# Escalas de Bäulke, Grunschel y Dresel (2022), validación chilena de
# López-Angulo, Muñoz-Inostroza, Sáez-Delgado, Chandia, Mella-Norambuena y
# Brito-Álvarez (2025), Journal of College Student Retention. Ítems en español
# de sus apéndices 2 (abandono) y 3 (cambio de carrera), en figshare
# (doi 10.6084/m9.figshare.28926803), con el número de ítem del apéndice.
#
# Se usan las fases 2 (pensamientos), 3 (deliberación) y 4 (búsqueda de
# información), una pantalla por fase, con abandono arriba y cambio de carrera
# debajo. La fase 2 la ven todos; la 3, solo quien marcó algo distinto de «1»
# en la fase 2; la 4, solo quien marcó algo distinto de «1» en la fase 3
# (decisión en instrumento/decisiones.md, D3). Las fases 1 (no encajar) y 5
# (decisión final) quedan fuera.
#
# Los subtítulos que separan abandono de cambio de carrera son nuestros; los
# ítems y la escala, del artículo. En pantalla van solo los números (con
# las etiquetas, el 1 y el 7 no caben en una línea); la etiqueta de cada
# punto aparece en una burbuja.

ACUERDO_7_TOTAL = ["1", "2", "3", "4", "5", "6", "7"]
ACUERDO_7_TOTAL_AYUDAS = [
    "Totalmente en desacuerdo",
    "En desacuerdo",
    "Ligeramente en desacuerdo",
    "Ni de acuerdo ni en desacuerdo",
    "Ligeramente de acuerdo",
    "De acuerdo",
    "Totalmente de acuerdo",
]

INTENCION_INSTRUCCION = "Indica tu grado de acuerdo con cada una de las afirmaciones."
SOBRE_ABANDONO = "**Sobre dejar los estudios universitarios por completo** (no seguir en ninguna carrera universitaria)"
SOBRE_CAMBIO = "**Sobre cambiarte de carrera** (seguir en la universidad, pero en otra carrera)"

FASES_INTENCION = {
    2: ("pensamientos de dejar los estudios / de cambiarse", {
        "ab": [
            (4, "Tengo varias ideas sobre lo que podría hacer en lugar de estudiar en la universidad."),
            (5, "Estoy pensando dejar mis estudios por completo."),
            (6, "No puedo evitar la sensación de que debería dejar mis estudios."),
        ],
        "cc": [
            (4, "Tengo varias ideas sobre lo que podría estudiar en lugar de mi carrera."),
            (5, "Estoy pensando en cambiar de carrera."),
            (6, "No puedo evitar la sensación de que debería cambiar de carrera."),
        ],
    }),
    3: ("deliberación", {
        "ab": [
            (7, "Evalúo con detalle lo que significaría para mí abandonar mis estudios."),
            (8, "Evalúo las ventajas y desventajas de abandonar mis estudios."),
            (9, "Pienso sistemáticamente lo que significaría para mí abandonar mis estudios en comparación con "
                "continuarlos."),
        ],
        "cc": [
            (7, "Evalúo con detalle lo que supondría para mí un cambio de carrera."),
            (8, "Evalúo las ventajas y desventajas de un cambio de carrera."),
            (9, "Pienso sistemáticamente lo que significaría para mí cambiar de carrera en comparación con "
                "seguir estudiando mi carrera actual."),
        ],
    }),
    4: ("búsqueda de información", {
        "ab": [
            (10, "Me informo específicamente sobre las alternativas al estudio universitario."),
            (11, "Busco específicamente información sobre alternativas a los estudios universitarios (ej. "
                 "internet, personas conocidas, entre otras)."),
            (12, "Investigo a fondo cuáles son los requisitos en las distintas alternativas a los estudios "
                 "universitarios (ej. Centro de Formación Técnica, Instituto Técnico Profesional, etc.)."),
        ],
        "cc": [
            (10, "Me informo específicamente sobre otras carreras."),
            (11, "Busco en distintas fuentes/canales información sobre otras carreras (ej. internet, personas "
                 "conocidas, entre otras)."),
            (12, "Investigo a fondo cuáles son los requisitos para otras carreras."),
        ],
    }),
}


def fase_intencion(fase):
    nombre, items = FASES_INTENCION[fase]
    escalas = {
        "ab": ("Intención de abandono", "Apéndice 2", INTENCION_INSTRUCCION + "\n\n" + SOBRE_ABANDONO),
        "cc": ("Intención de cambio de carrera", "Apéndice 3", SOBRE_CAMBIO),
    }
    bloques = []
    for escala, (constructo, apendice, texto) in escalas.items():
        numeros = [n for n, _ in items[escala]]
        bloques.append(
            bloque(
                f"int_{escala}_f{fase}",
                texto,
                items=[(f"int_{escala}{n:02d}", t) for n, t in items[escala]],
                opciones=ACUERDO_7_TOTAL,
                ayudas=ACUERDO_7_TOTAL_AYUDAS,
                constructo=f"{constructo}, fase {fase}: {nombre}",
                fuente=f"López-Angulo et al. (2025), {apendice.lower()}, ítems {numeros[0]}-{numeros[-1]} "
                "(original: Bäulke et al., 2022)",
            )
        )
    return grupo(f"intencion_f{fase}", bloques)


INTENCION_F2 = fase_intencion(2)
INTENCION_F3 = mostrar_si(fase_intencion(3), anterior="intencion_f2", distinta_de=ACUERDO_7_TOTAL[0])
INTENCION_F4 = mostrar_si(fase_intencion(4), anterior="intencion_f3", distinta_de=ACUERDO_7_TOTAL[0])


# --- Módulos 3 y 4: escalas validadas ---------------------------------------
# Elegidas en noviembre de 2026; el porqué de cada una (y de las que quedaron
# fuera: ESA, LCQ-5, incivilidad, MSPSS completa) está en
# instrumento/decisiones.md. Ítems copiados textuales del artículo citado.

# Módulo 3: integración académica

UWES = bloque(
    "uwes",
    "Indica con qué frecuencia te has sentido así en tus estudios.",
    items=[
        ("uwes_vi1", "Mis tareas como estudiante me hacen sentir lleno de energía"),
        ("uwes_vi2", "Me siento fuerte y vigoroso cuando estoy estudiando o voy a las clases"),
        ("uwes_de2", "Estoy entusiasmado con mi carrera"),
        ("uwes_de3", "Mis estudios me inspiran cosas nuevas"),
        ("uwes_vi3", "Cuando me levanto por la mañana me apetece ir a clase o estudiar"),
        ("uwes_ab3", "Soy feliz cuando estoy haciendo tareas relacionadas con mis estudios"),
        ("uwes_de4", "Estoy orgulloso de hacer esta carrera"),
        ("uwes_ab4", "Estoy inmerso en mis estudios"),
        # Aclaración entre paréntesis (nuestra): en Chile «dejarse llevar» también
        # puede leerse como dejar las tareas para última hora.
        ("uwes_ab5", "Me “dejo llevar” cuando realizo mis tareas como estudiante (me concentro tanto que pierdo la noción del tiempo)"),
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


# Incivilidad docente: los 4 ítems de la Workplace Incivility Scale, versión
# corta (Cortina et al., 2001; Matthews y Ritter, 2016), en la validación
# española de Di Marco et al. (2018), adaptados: referente «algún profesor o
# profesora de tus asignaturas» (en vez de compañeros o supervisores), período
# «este semestre» (en vez del último año) y trato de tú. El artículo solo da
# los extremos en inglés (never, many times); los puntos del medio van con su
# número. El ítem 5 es nuevo: va en la misma pantalla, con su columna, y queda
# fuera del análisis factorial de los 4 ítems (decisiones.md, D19).
FRECUENCIA_5_INCIVILIDAD = ["1 · Nunca", "2", "3", "4", "5 · Muchas veces"]

INCIVILIDAD = bloque(
    "incivilidad",
    "Durante este semestre, ¿con qué frecuencia algún profesor o profesora de tus asignaturas…",
    items=[
        ("inciv_01", "…ha prestado poca atención a tus ideas o ha mostrado poco interés en tus opiniones?"),
        ("inciv_02", "…te ha interrumpido o ha comenzado a hablar mientras tú hablabas?"),
        ("inciv_03", "…te ha ignorado o ha dejado de hablarte (por ejemplo, te ha hecho el vacío)?"),
        ("inciv_04", "…ha hecho bromas a tu costa?"),
        ("inciv_05", "…te ha descalificado frente a otros?"),
    ],
    opciones=FRECUENCIA_5_INCIVILIDAD,
    constructo="Incivilidad docente (ítems 1-4: WIS corta; ítem 5: nuevo)",
    fuente="Di Marco et al. (2018), adaptado a docentes; ítem 5: NUEVO",
)

# --- Módulo 7: ficha de contexto (ítems nuevos) ------------------------------
# Lo que ya está en los registros (PAES, NEM, vía de admisión, beneficios)
# no se pregunta: se pide al registro académico con la autorización de arriba.

CTX_PRIMERA_GENERACION = opcion_unica(
    "ctx_padres_educacion_superior",
    "¿Alguno de tus padres estudió en la educación superior (universidad, instituto o CFT)?",
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
    CONSENTIMIENTO,  # incluye la autorización del registro académico
    IDENTIFICACION,
    # Módulo 1: redes
    INSTRUCCIONES_REDES,
    G1_AFINIDAD,
    G2_AYUDA,
    G3_ESTUDIO,
    METAPERCEPCION,
    LAZOS_FUERA,
    # Módulo 2: intención de abandono y de cambio de carrera
    INTENCION_F2,
    INTENCION_F3,  # solo si en la fase 2 hubo algo distinto de «1»
    INTENCION_F4,  # solo si en la fase 3 hubo algo distinto de «1»
    # Módulo 3: integración académica
    UWES,
    ASES,
    # Módulo 4: integración social
    ESPU,
    UCLA3,
    MSPSS_FAMILIA,
    INCIVILIDAD,  # al final de las escalas: es la más sensible
    # Módulo 7: contexto, de a dos preguntas por página
    grupo("ctx_familia_trabajo", [CTX_PRIMERA_GENERACION, CTX_TRABAJO]),
    grupo("ctx_vivienda_traslado", [CTX_VIVIENDA, CTX_TRASLADO]),
    grupo("ctx_trayectoria", [CTX_PRIMERA_OPCION, CTX_OTRA_CARRERA]),
    # Cierre: comentarios y despedida en la última página
    grupo("cierre", [COMENTARIOS, CIERRE]),
]
