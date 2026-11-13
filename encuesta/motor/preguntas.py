"""Constructores para escribir el instrumento en `instrumento.py`.

Cada función devuelve una **página** de la encuesta. La app mide el tiempo
por página, guarda cada respuesta apenas se marca y permite retomar la
encuesta con el enlace personal.

Tipos de página:

- `info`            texto sin pregunta (bienvenida, instrucciones, cierre).
- `consentimiento`  acepto / no acepto. "No acepto" termina la encuesta y
                    borra lo que se haya respondido.
- `identificacion`  "¿Quién eres tú?": la persona elige su nombre de la
                    nómina. Cada nombre se puede elegir una sola vez y desde
                    ahí queda fuera de las listas de nominación.
- `nominacion`      casillas con la nómina (sin la propia persona), agrupada
                    por cohorte y con buscador, más la opción "No hay nadie".
- `opcion_unica`    una pregunta con alternativas (una sola respuesta).
- `bloque`          varias afirmaciones con la misma escala en una página
                    (lo normal para una escala validada).
- `numero`          un número entero.
- `abierta`         texto libre (opcional por diseño).
- `arbol`           preguntas encadenadas: cuál viene después depende de la
                    respuesta anterior (p. ej. "¿Trabajas?" -> "¿Cuántas horas?").
- `grupo`           dos o más preguntas en una misma página (`opcion_unica`,
                    `numero`, `abierta`, `arbol`, `bloque` o un texto `info`).
                    Cada una conserva su id y su columna.

Páginas condicionales: `mostrar_si(pagina, anterior=..., distinta_de=...)`
hace que una página aparezca solo según lo respondido en una página
anterior (p. ej. la fase 3 de intención de abandono, solo para quien no
marcó «1» en toda la fase 2). Quien no la ve queda como NO_APLICA.

Omitir: si alguien aprieta "Siguiente" sin responder, la app le ofrece
«Prefiero no contestar» y lo registra como tal (no como una respuesta).
No se puede omitir el consentimiento ni la identificación.

Metadatos opcionales (`constructo`, `fuente`, `invertido`/`invertidos`):
no cambian lo que ve quien responde, pero van al codebook de la
exportación y a la ficha del instrumento (`scripts/instrumento_a_md.py`).
"""

import re

# Lo que se guarda cuando alguien elige «Prefiero no contestar». Al analizar
# es un dato faltante, pero distinto de "no llegó a esa pregunta".
OMIT = "Prefiero no contestar"

_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")

NOT_CONDITIONAL = {"consent", "self_id"}


def info(id, texto):
    return {"id": id, "type": "info", "label": texto}


def consentimiento(
    id, texto, *, acepto="Acepto participar", rechazo="No acepto", documento=None, documento_pdf=None,
    adicionales=(),
):
    """`documento`: texto completo del consentimiento (Markdown), que se
    muestra en un desplegable «Leer el documento completo»; `documento_pdf`:
    ruta (relativa a la carpeta encuesta/) de un PDF que se ofrece para
    descargar. `adicionales`: preguntas de opción única que van en la misma
    página, debajo de la decisión (p. ej. autorizar el registro académico);
    cada una conserva su id y su columna, y hay que responderlas para seguir
    (salvo si la persona no acepta participar)."""
    return {
        "id": id,
        "type": "consent",
        "label": texto,
        "options": [acepto, rechazo],
        "accept": acepto,
        "decline": rechazo,
        "document": documento,
        "document_pdf": documento_pdf,
        "members": list(adicionales),
    }


def identificacion(id, texto="¿Quién eres tú? Busca y selecciona tu nombre en la lista."):
    return {"id": id, "type": "self_id", "label": texto}


def nominacion(id, texto, *, maximo=15, nadie="No hay nadie", constructo=None, fuente=None):
    return {
        "id": id,
        "type": "roster_checklist",
        "label": texto,
        "max_selections": maximo,
        "nobody_label": nadie,
        "construct": constructo,
        "source": fuente,
    }


def opcion_unica(id, texto, opciones, *, constructo=None, fuente=None, invertido=False):
    return {
        "id": id,
        "type": "radio",
        "label": texto,
        "options": list(opciones),
        "construct": constructo,
        "source": fuente,
        "reverse_scored": invertido,
    }


def bloque(id, texto, items, opciones, *, ayudas=None, constructo=None, fuente=None, invertidos=()):
    """`items`: lista de pares (id_del_item, texto). `invertidos`: ids de los
    ítems que se puntúan al revés (solo documentación).

    `ayudas`: opcional, una lista del mismo largo que `opciones` con el texto
    que aparece en una burbuja al pasar el cursor sobre cada opción (None en
    una posición = sin burbuja). Sirve para mostrar opciones cortas ("0" a
    "6") sin perder el significado de cada una."""
    invertidos = set(invertidos)
    return {
        "id": id,
        "type": "likert_block",
        "label": texto,
        "options": list(opciones),
        "option_help": list(ayudas) if ayudas is not None else None,
        "items": [
            {"id": item_id, "label": item_texto, "reverse_scored": item_id in invertidos}
            for item_id, item_texto in items
        ],
        "construct": constructo,
        "source": fuente,
        "_reverse_ids": invertidos,
    }


def numero(id, texto, *, minimo=0, maximo=None, constructo=None, fuente=None):
    """`maximo="nomina"` usa el tamaño de la nómina menos la propia persona
    (útil para "¿cuántas personas crees que te nombraron?")."""
    return {
        "id": id,
        "type": "number",
        "label": texto,
        "min_value": minimo,
        "max_value": maximo,
        "construct": constructo,
        "source": fuente,
    }


def abierta(id, texto, *, constructo=None, fuente=None):
    return {"id": id, "type": "text", "label": texto, "construct": constructo, "source": fuente}


def arbol(id, raiz, nodos, *, constructo=None, fuente=None):
    """`nodos`: {id_nodo: {"texto": ..., "opciones": [...], "siguiente": {opcion: id_nodo}}}.
    Una opción sin entrada en "siguiente" termina el árbol ahí."""
    return {
        "id": id,
        "type": "branching_tree",
        "root": raiz,
        "tree": {
            node_id: {
                "label": nodo["texto"],
                "options": list(nodo["opciones"]),
                "branches": dict(nodo.get("siguiente", {})),
            }
            for node_id, nodo in nodos.items()
        },
        "construct": constructo,
        "source": fuente,
    }


GROUP_MEMBER_TYPES = {"radio", "number", "text", "branching_tree", "likert_block", "info"}


def grupo(id, preguntas):
    """Varias preguntas en una misma página, una debajo de otra. `preguntas`:
    páginas hechas con opcion_unica, numero, abierta, arbol, bloque o info
    (un texto sin respuesta). La página se da por respondida cuando todas sus
    preguntas lo están; «Prefiero no contestar» omite solo las que faltan."""
    return {"id": id, "type": "group", "members": list(preguntas)}


def mostrar_si(pagina, *, anterior, distinta_de):
    """La `pagina` aparece solo si en la página `anterior` (que va antes)
    hay al menos una respuesta distinta de `distinta_de`. «Prefiero no
    contestar» no cuenta como distinta. Si la página `anterior` tampoco
    apareció, esta tampoco. Quien no la ve queda como NO_APLICA en la
    exportación."""
    return {**pagina, "show_if": {"page": anterior, "other_than": distinta_de}}


def opciones_de(pagina):
    """Todas las opciones de respuesta de una página (y de lo que tenga dentro)."""
    out = list(pagina.get("options", []))
    for m in pagina.get("members", []):
        out += opciones_de(m)
    for node in pagina.get("tree", {}).values():
        out += node["options"]
    return out


def validar(preguntas):
    """Revisa el instrumento antes de mostrarlo. Devuelve una lista de
    problemas en castellano (vacía si todo está bien)."""
    problemas = []
    vistos = set()

    def registrar_id(id_, donde):
        if not isinstance(id_, str) or not _ID_RE.match(id_):
            problemas.append(
                f"{donde}: el id {id_!r} debe empezar con letra minúscula y usar solo a-z, 0-9 y _"
            )
        elif id_ in vistos:
            problemas.append(f"{donde}: el id {id_!r} está repetido")
        vistos.add(id_)

    def revisar_opciones(opciones, donde):
        if len(opciones) < 2:
            problemas.append(f"{donde}: necesita al menos dos opciones")
        if len(set(opciones)) != len(opciones):
            problemas.append(f"{donde}: hay opciones repetidas")
        if OMIT in opciones:
            problemas.append(
                f"{donde}: «{OMIT}» no va entre las opciones; la app lo ofrece sola al intentar avanzar sin responder"
            )

    tipos = [p["type"] for p in preguntas]
    if not preguntas:
        return ["el instrumento no tiene preguntas"]

    def revisar_pagina(p, donde):
        registrar_id(p.get("id"), donde)
        if p["type"] in ("radio", "consent", "likert_block"):
            revisar_opciones(p["options"], donde)
        if p["type"] == "likert_block":
            if not p["items"]:
                problemas.append(f"{donde}: el bloque no tiene ítems")
            for item in p["items"]:
                registrar_id(item["id"], f"{donde}, ítem")
            sobrantes = p["_reverse_ids"] - {item["id"] for item in p["items"]}
            if sobrantes:
                problemas.append(f"{donde}: invertidos que no son ítems del bloque: {sorted(sobrantes)}")
            if p.get("option_help") is not None and len(p["option_help"]) != len(p["options"]):
                problemas.append(f"{donde}: `ayudas` debe tener una entrada por opción")
        if p["type"] == "consent":
            for m in p.get("members", []):
                if m["type"] != "radio":
                    problemas.append(f"{donde}: el consentimiento solo admite preguntas de opción única adicionales")
                    continue
                revisar_pagina(m, f"{donde}, pregunta {m.get('id')}")
        if p["type"] == "group":
            miembros = p["members"]
            if len([m for m in miembros if m["type"] != "info"]) < 1:
                problemas.append(f"{donde}: el grupo no tiene preguntas")
            for m in miembros:
                if m["type"] not in GROUP_MEMBER_TYPES:
                    problemas.append(
                        f"{donde}: un grupo solo admite {sorted(GROUP_MEMBER_TYPES)}, no {m['type']!r} ({m.get('id')})"
                    )
                    continue
                revisar_pagina(m, f"{donde}, pregunta {m.get('id')}")
        if p["type"] == "branching_tree":
            if p["root"] not in p["tree"]:
                problemas.append(f"{donde}: la raíz {p['root']!r} no es un nodo del árbol")
            for node_id, node in p["tree"].items():
                revisar_opciones(node["options"], f"{donde}, nodo {node_id}")
                for opcion, siguiente in node["branches"].items():
                    if opcion not in node["options"]:
                        problemas.append(f"{donde}, nodo {node_id}: {opcion!r} no es una de sus opciones")
                    if siguiente not in p["tree"]:
                        problemas.append(f"{donde}, nodo {node_id}: {siguiente!r} no es un nodo del árbol")
        if p["type"] == "roster_checklist" and p["max_selections"] < 1:
            problemas.append(f"{donde}: el máximo de nominaciones debe ser al menos 1")

    for i, p in enumerate(preguntas, start=1):
        revisar_pagina(p, f"página {i} ({p.get('id')})")
        condicion = p.get("show_if")
        if condicion:
            donde = f"página {i} ({p.get('id')})"
            previas = {q["id"]: q for q in preguntas[: i - 1]}
            if p["type"] in NOT_CONDITIONAL:
                problemas.append(f"{donde}: el consentimiento y la identificación no pueden ser condicionales")
            if condicion["page"] not in previas:
                problemas.append(f"{donde}: mostrar_si apunta a {condicion['page']!r}, que no es una página anterior")
            elif condicion["other_than"] not in opciones_de(previas[condicion["page"]]):
                problemas.append(
                    f"{donde}: {condicion['other_than']!r} no es una opción de la página {condicion['page']!r}"
                )

    if tipos.count("self_id") != 1:
        problemas.append("debe haber exactamente una página de identificacion()")
    if tipos.count("consent") > 1:
        problemas.append("hay más de una página de consentimiento()")
    if "self_id" in tipos:
        posicion_id = tipos.index("self_id")
        if "consent" in tipos and tipos.index("consent") > posicion_id:
            problemas.append("el consentimiento debe ir antes de la identificación")
        for i, tipo in enumerate(tipos):
            if tipo == "roster_checklist" and i < posicion_id:
                problemas.append(f"página {i + 1}: las nominaciones deben ir después de la identificación")
            if preguntas[i]["type"] == "number" and preguntas[i]["max_value"] == "nomina" and i < posicion_id:
                problemas.append(f"página {i + 1}: maximo='nomina' requiere ir después de la identificación")
    return problemas
