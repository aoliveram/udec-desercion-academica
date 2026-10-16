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


def info(id, texto):
    return {"id": id, "type": "info", "label": texto}


def consentimiento(id, texto, *, acepto="Acepto participar", rechazo="No acepto"):
    return {
        "id": id,
        "type": "consent",
        "label": texto,
        "options": [acepto, rechazo],
        "accept": acepto,
        "decline": rechazo,
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


def bloque(id, texto, items, opciones, *, constructo=None, fuente=None, invertidos=()):
    """`items`: lista de pares (id_del_item, texto). `invertidos`: ids de los
    ítems que se puntúan al revés (solo documentación)."""
    invertidos = set(invertidos)
    return {
        "id": id,
        "type": "likert_block",
        "label": texto,
        "options": list(opciones),
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

    for i, p in enumerate(preguntas, start=1):
        donde = f"página {i} ({p.get('id')})"
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
