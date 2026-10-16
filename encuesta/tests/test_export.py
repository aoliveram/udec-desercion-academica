import json

import instrumento
from motor import export
from motor.preguntas import OMIT, arbol, bloque, identificacion, nominacion, numero, opcion_unica

KEY = b"clave-de-prueba"

QUESTIONS = [
    identificacion("yo"),
    nominacion("g1", "¿Con quiénes?"),
    opcion_unica("p", "¿?", ["A", "B", "C"], invertido=True),
    bloque("blk", "Acuerdo:", [("i1", "uno"), ("i2", "dos")], ["No", "Sí"], invertidos=["i2"]),
    numero("n", "¿Cuántos?"),
    arbol(
        "t",
        "trabaja",
        {
            "trabaja": {"texto": "¿Trabajas?", "opciones": ["Sí", "No"], "siguiente": {"Sí": "horas"}},
            "horas": {"texto": "¿Horas?", "opciones": ["<10", "10+"]},
        },
    ),
]


def v(value):
    return {"value": value}


def test_pseudonyms_are_stable_and_depend_on_the_key():
    assert export.pseudonym(KEY, "7") == export.pseudonym(KEY, "7")
    assert export.pseudonym(KEY, "7") != export.pseudonym(KEY, "8")
    assert export.pseudonym(KEY, "7") != export.pseudonym(b"otra", "7")
    assert export.pseudonym(KEY, "7").startswith("E_")


def test_encode_answers_codes_options_by_position():
    data = {"p": v("C"), "blk": v({"i1": "Sí", "i2": OMIT}), "n": v(4), "g1": v(["2", "3"])}
    cells = export.encode_answers(QUESTIONS, data)
    assert cells["p"] == 3
    assert cells["i1"] == 2
    assert cells["i2"] == export.OMITTED
    assert cells["n"] == 4
    assert cells["g1_n"] == 2


def test_missing_omitted_and_nobody_stay_distinct():
    no_answer = export.encode_answers(QUESTIONS, {})
    assert no_answer["p"] == export.NO_ANSWER
    assert no_answer["g1_n"] == export.NO_ANSWER
    assert export.encode_answers(QUESTIONS, {"g1": v([])})["g1_n"] == 0
    assert export.encode_answers(QUESTIONS, {"g1": v(OMIT), "n": v(OMIT)})["n"] == export.OMITTED


def test_tree_nodes_off_the_path_are_not_applicable():
    off_path = export.encode_answers(QUESTIONS, {"t": v({"trabaja": "No"})})
    assert off_path["t__trabaja"] == 2
    assert off_path["t__horas"] == export.NOT_APPLICABLE

    unfinished = export.encode_answers(QUESTIONS, {"t": v({"trabaja": "Sí"})})
    assert unfinished["t__horas"] == export.NO_ANSWER

    omitted = export.encode_answers(QUESTIONS, {"t": v({"trabaja": OMIT})})
    assert omitted["t__trabaja"] == export.OMITTED
    assert omitted["t__horas"] == export.NOT_APPLICABLE


def test_codebook_documents_every_node_table_column():
    for questions in (QUESTIONS, instrumento.PREGUNTAS):
        documented = {row["columna"] for row in export.codebook(questions) if row["archivo"] == "nodos.csv"}
        assert documented == set(export.encode_answers(questions, {}))


def test_codebook_marks_reverse_scored_items():
    rows = {row["columna"]: row for row in export.codebook(QUESTIONS)}
    assert rows["p"]["invertido"] == 1
    assert rows["i1"]["invertido"] == 0
    assert rows["i2"]["invertido"] == 1
    assert rows["p"]["opciones"] == "1=A; 2=B; 3=C"


def test_edges_skip_self_loops_and_codes_outside_the_roster():
    data = {"g1": v(["2", "1", "99"])}
    out, unresolved = export.edges(QUESTIONS, data, "1", {"1", "2"}, KEY)
    assert out == {"g1": [(export.pseudonym(KEY, "1"), export.pseudonym(KEY, "2"))]}
    assert unresolved == 2


def _row(rid, status, code, created):
    blob = {} if code is None else {"yo": {"value": code}}
    return {"id": rid, "status": status, "survey_data_json": json.dumps(blob), "created_at": created}


def test_pick_respondents_prefers_completed_and_counts_the_rest():
    rows = [
        _row("a", "completed", "1", "t1"),
        _row("b", "in_progress", "1", "t2"),
        _row("c", "declined", None, "t3"),
        _row("d", "in_progress", None, "t4"),
        _row("e", "in_progress", "99", "t5"),
    ]
    by_code, report = export.pick_respondents(rows, {"1", "2"}, "yo")
    assert by_code["1"]["id"] == "a"
    assert report == {"rechazos": 1, "sin_identificacion": 1, "fuera_de_nomina": 1, "duplicados": 1}
