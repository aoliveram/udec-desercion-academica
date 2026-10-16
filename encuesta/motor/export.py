"""Turn a roster's responses into pseudonymized tables for analysis.

Plain Python (no Streamlit), used by scripts/exportar.py. Output, one row per
roster member in `nodes`, and one edge list per nomination question:

- Every person on the roster is a node, whether or not they answered: a
  classmate who didn't take part can still have been nominated.
- Ids are HMAC pseudonyms of the roster code `N` (see `pseudonym`), so the
  same person keeps the same id across exports and waves as long as their
  `N` and the key stay the same.
- Missing data is never a blank cell. Three sentinels keep apart the cases
  the analysis has to tell apart:
    SIN_RESPUESTA  didn't reach the question (or never answered at all)
    OMITIDA        chose «Prefiero no contestar»
    NO_APLICA      a branching_tree node off the path the person took
  and, for nominations, `<id>_n = 0` means "No hay nadie" (an answer),
  never a missing one.
"""

import hashlib
import hmac
import json

from motor.preguntas import OMIT

NO_ANSWER = "SIN_RESPUESTA"
OMITTED = "OMITIDA"
NOT_APPLICABLE = "NO_APLICA"

# Pages that carry no analyzable answer of their own.
SKIPPED_TYPES = {"info", "consent", "self_id"}

STATUS_LABELS = {"completed": "completa", "in_progress": "incompleta"}


def pseudonym(key: bytes, code) -> str:
    digest = hmac.new(key, f"persona|{code}".encode("utf-8"), hashlib.sha256).hexdigest()
    return f"E_{digest[:10]}"


def key_fingerprint(key: bytes) -> str:
    """Public, non-reversible fingerprint to check two machines use the same key."""
    return hashlib.sha256(b"huella|" + key).hexdigest()[:8]


def _options_text(options):
    return "; ".join(f"{i}={opt}" for i, opt in enumerate(options, start=1))


def codebook(questions):
    """One dict per exported column (node table, edge lists and open texts)."""
    rows = []
    for page, q in enumerate(questions, start=1):
        base = {
            "pagina": page,
            "pregunta": q["id"],
            "tipo": q["type"],
            "constructo": q.get("construct") or "",
            "fuente": q.get("source") or "",
        }
        if q["type"] in SKIPPED_TYPES:
            continue
        if q["type"] == "radio":
            rows.append({**base, "columna": q["id"], "archivo": "nodos.csv", "texto": q["label"],
                         "opciones": _options_text(q["options"]), "invertido": int(q["reverse_scored"])})
        elif q["type"] == "likert_block":
            for item in q["items"]:
                rows.append({**base, "columna": item["id"], "archivo": "nodos.csv",
                             "texto": f"{q['label']} {item['label']}",
                             "opciones": _options_text(q["options"]), "invertido": int(item["reverse_scored"])})
        elif q["type"] == "branching_tree":
            for node_id, node in q["tree"].items():
                rows.append({**base, "columna": f"{q['id']}__{node_id}", "archivo": "nodos.csv",
                             "texto": node["label"], "opciones": _options_text(node["options"]), "invertido": 0})
        elif q["type"] == "number":
            rows.append({**base, "columna": q["id"], "archivo": "nodos.csv", "texto": q["label"],
                         "opciones": "número entero", "invertido": 0})
        elif q["type"] == "roster_checklist":
            rows.append({**base, "columna": f"{q['id']}_n", "archivo": "nodos.csv", "texto": q["label"],
                         "opciones": f"número de personas nominadas (grado de salida); 0 = «{q['nobody_label']}»",
                         "invertido": 0})
            rows.append({**base, "columna": "desde, hacia", "archivo": f"aristas_{q['id']}.csv",
                         "texto": q["label"], "opciones": "una fila por nominación (quién nomina -> a quién)",
                         "invertido": 0})
        elif q["type"] == "text":
            rows.append({**base, "columna": q["id"], "archivo": "textos_abiertos.csv", "texto": q["label"],
                         "opciones": "texto libre", "invertido": 0})
    return rows


def _code(options, value):
    if value is None:
        return NO_ANSWER
    if value == OMIT:
        return OMITTED
    return options.index(value) + 1 if value in options else NO_ANSWER


def encode_answers(questions, data):
    """{column: cell} for one respondent's saved data (`{qid: {"value": v}}`)."""
    cells = {}
    for q in questions:
        value = data.get(q["id"], {}).get("value")
        if q["type"] in SKIPPED_TYPES or q["type"] == "text":
            continue
        if q["type"] == "radio":
            cells[q["id"]] = _code(q["options"], value)
        elif q["type"] == "likert_block":
            answers = value if isinstance(value, dict) else {}
            for item in q["items"]:
                cells[item["id"]] = _code(q["options"], answers.get(item["id"]))
        elif q["type"] == "branching_tree":
            answers = value if isinstance(value, dict) else {}
            on_path = _tree_path(q, answers)
            finished = bool(answers) and on_path[-1] is None
            for node_id, node in q["tree"].items():
                if node_id in answers and node_id in on_path:
                    cells[f"{q['id']}__{node_id}"] = _code(node["options"], answers[node_id])
                else:
                    cells[f"{q['id']}__{node_id}"] = NOT_APPLICABLE if finished else NO_ANSWER
        elif q["type"] == "number":
            if value is None:
                cells[q["id"]] = NO_ANSWER
            elif value == OMIT:
                cells[q["id"]] = OMITTED
            else:
                cells[q["id"]] = value
        elif q["type"] == "roster_checklist":
            if value is None:
                cells[f"{q['id']}_n"] = NO_ANSWER
            elif value == OMIT:
                cells[f"{q['id']}_n"] = OMITTED
            else:
                cells[f"{q['id']}_n"] = len(value)
    return cells


def _tree_path(question, answers):
    """Node ids visited along the answers, ending in None if a leaf (or an
    omission) was reached, or in the pending node id otherwise."""
    path = []
    node_id = question["root"]
    while node_id is not None and node_id in answers:
        path.append(node_id)
        answer = answers[node_id]
        node_id = None if answer == OMIT else question["tree"][node_id]["branches"].get(answer)
    path.append(node_id)
    return path


def empty_answers(questions):
    """Cells for a roster member with no response at all."""
    return {column: NO_ANSWER for column in encode_answers(questions, {})}


def pick_respondents(respondents, roster_codes, self_id_question_id):
    """Map roster code -> the respondent row to export for that person.

    Returns (by_code, report). Declined respondents and those who never
    picked a name can't be tied to a node; they're only counted. The app
    lets only one respondent hold a name at a time, so duplicates shouldn't
    happen; if they do (e.g. a name freed by hand), a completed response
    wins over an incomplete one, then the most recent.
    """
    report = {"rechazos": 0, "sin_identificacion": 0, "fuera_de_nomina": 0, "duplicados": 0}
    by_code = {}
    for r in respondents:
        if r["status"] == "declined":
            report["rechazos"] += 1
            continue
        data = json.loads(r["survey_data_json"] or "{}")
        code = data.get(self_id_question_id, {}).get("value")
        if code is None:
            report["sin_identificacion"] += 1
            continue
        if code not in roster_codes:
            report["fuera_de_nomina"] += 1
            continue
        if code in by_code:
            report["duplicados"] += 1
            current = by_code[code]
            if (current["status"] == "completed") and r["status"] != "completed":
                continue
        by_code[code] = r
    return by_code, report


def edges(questions, data, self_code, roster_codes, key):
    """{question_id: [(from, to), ...]} for one respondent, plus how many
    nominated codes no longer resolve against the roster."""
    out, unresolved = {}, 0
    source = pseudonym(key, self_code)
    for q in questions:
        if q["type"] != "roster_checklist":
            continue
        value = data.get(q["id"], {}).get("value")
        pairs = []
        if isinstance(value, list):
            for code in value:
                if code not in roster_codes or code == self_code:
                    unresolved += 1
                    continue
                pairs.append((source, pseudonym(key, code)))
        out[q["id"]] = pairs
    return out, unresolved
