#!/usr/bin/env python3
"""Escribe el instrumento como documento Markdown, página por página.

Sale directo de instrumento.py, así que refleja exactamente lo que ve
quien responde. Sirve para la revisión de jueces expertos, las entrevistas
cognitivas y el envío al CEBB.

Uso (desde la carpeta encuesta/):
    python scripts/instrumento_a_md.py > instrumento.md
    pandoc instrumento.md -o instrumento.pdf      # si se quiere en PDF
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import instrumento  # noqa: E402
from motor.preguntas import OMIT, validar  # noqa: E402

TIPOS = {
    "info": "texto",
    "consent": "consentimiento",
    "self_id": "identificación (lista con la nómina)",
    "roster_checklist": "nominación (casillas con la nómina)",
    "radio": "opción única",
    "likert_block": "bloque de ítems con la misma escala",
    "number": "número",
    "text": "texto libre",
    "branching_tree": "preguntas encadenadas",
}


def quote(text):
    return "\n".join(f"> {line}" if line else ">" for line in text.split("\n"))


def metadata(q):
    parts = []
    if q.get("construct"):
        parts.append(f"constructo: {q['construct']}")
    if q.get("source"):
        parts.append(f"fuente: {q['source']}")
    return f"*{' · '.join(parts)}*\n\n" if parts else ""


def page(n, q):
    out = [f"### Página {n}: `{q['id']}` ({TIPOS[q['type']]})\n", metadata(q)]
    t = q["type"]
    if t == "info":
        out.append(quote(q["label"]))
    elif t == "consent":
        out.append(quote(q["label"]))
        out.append("\n\n" + " · ".join(f"( ) {o}" for o in q["options"]))
    elif t == "self_id":
        out.append(quote(f"**{q['label']}**"))
        out.append("\n\n*(lista desplegable con buscador: todas las personas de la nómina)*")
    elif t == "roster_checklist":
        out.append(quote(f"**{q['label']}**"))
        out.append(
            f"\n\n*(casillas con la nómina, sin la propia persona, agrupadas por cohorte y con buscador; "
            f"máximo {q['max_selections']}; opción «{q['nobody_label']}»)*"
        )
    elif t == "radio":
        out.append(quote(f"**{q['label']}**"))
        out.append("\n\n" + "\n".join(f"- ( ) {o}" for o in q["options"]))
        if q["reverse_scored"]:
            out.append("\n\n*Ítem invertido.*")
    elif t == "likert_block":
        out.append(quote(f"**{q['label']}**"))
        out.append("\n\nEscala: " + " · ".join(q["options"]) + "\n")
        for i, item in enumerate(q["items"], start=1):
            inv = " *(invertido)*" if item["reverse_scored"] else ""
            out.append(f"\n{i}. {item['label']} `{item['id']}`{inv}")
    elif t == "number":
        maximo = "tamaño de la nómina − 1" if q["max_value"] == "nomina" else q["max_value"]
        rango = f"entero desde {q['min_value']}" + (f" hasta {maximo}" if maximo is not None else "")
        out.append(quote(f"**{q['label']}**"))
        out.append(f"\n\n*({rango})*")
    elif t == "text":
        out.append(quote(f"**{q['label']}**"))
        out.append("\n\n*(texto libre)*")
    elif t == "branching_tree":
        for node_id, node in q["tree"].items():
            out.append(f"\n**{node['label']}** `{node_id}`\n")
            for option in node["options"]:
                siguiente = node["branches"].get(option)
                destino = f" → `{siguiente}`" if siguiente else ""
                out.append(f"\n- ( ) {option}{destino}")
            out.append("\n")
    return "".join(out) + "\n"


def main():
    problemas = validar(instrumento.PREGUNTAS)
    if problemas:
        sys.exit("El instrumento tiene problemas:\n" + "\n".join(f"- {p}" for p in problemas))

    preguntas = instrumento.PREGUNTAS
    n_items = sum(len(q["items"]) if q["type"] == "likert_block" else 1 for q in preguntas if q["type"] != "info")
    print(f"# {instrumento.TITULO}\n")
    print(f"Versión **{instrumento.VERSION}** · {len(preguntas)} páginas · {n_items} preguntas o ítems.\n")
    print(
        f"Una página por pantalla. En toda pregunta, salvo el consentimiento y la identificación, "
        f"quien responde puede elegir «{OMIT}» al intentar avanzar sin responder.\n"
    )
    for n, q in enumerate(preguntas, start=1):
        print("---\n")
        print(page(n, q))


if __name__ == "__main__":
    main()
