"""End-to-end tests: drive the real app.py with Streamlit's AppTest (no
browser), against the real instrument and the fictitious example roster."""

import csv
import importlib.util
import json
import sys

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

import instrumento
from motor import audit, db, export, rosters, settings
from motor.preguntas import OMIT

from conftest import ENCUESTA_DIR

QUESTIONS = instrumento.PREGUNTAS
INDEX = {q["id"]: i for i, q in enumerate(QUESTIONS)}
SELF = "5"
NOMINATED = ["2", "40"]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("DIRECTORIO_NOMINAS", str(settings.EXAMPLES_DIR))
    monkeypatch.setenv("IP_HASH_PEPPER", "pepper-de-prueba")
    monkeypatch.setattr(settings, "DB_PATH", tmp_path / "encuesta.db")
    st.cache_resource.clear()
    st.cache_data.clear()
    yield tmp_path
    st.cache_resource.clear()
    st.cache_data.clear()


def start(query=None):
    at = AppTest.from_file(str(ENCUESTA_DIR / "app.py"), default_timeout=30)
    for k, v in (query or {"nomina": "ejemplo"}).items():
        at.query_params[k] = v
    return at.run()


def page(at):
    return QUESTIONS[at.session_state["_page"]]


def key(question, *parts):
    return "__".join(["w", question["id"], *parts])


def click_next(at):
    return at.button(key=f"_next_{at.session_state['_page']}").click().run()


def answer_current_page(at, self_code=SELF):
    fill(at, page(at), self_code)
    at.run()
    assert not at.exception, at.exception
    return click_next(at)


def fill(at, q, self_code=SELF):
    t = q["type"]
    if t == "group":
        for member in q["members"]:
            fill(at, member, self_code)
    elif t == "consent":
        at.radio(key=key(q)).set_value(q["accept"])
        for member in q.get("members", []):
            fill(at, member, self_code)
    elif t == "self_id":
        at.selectbox(key=key(q)).set_value(self_code)
    elif t == "roster_checklist":
        for code in NOMINATED:
            at.checkbox(key=key(q, code)).check()
    elif t == "radio":
        at.radio(key=key(q)).set_value(q["options"][0])
    elif t == "likert_block":
        for item in q["items"]:
            at.radio(key=key(q, item["id"])).set_value(q["options"][-1])
    elif t == "number":
        at.number_input(key=key(q)).set_value(3)
    elif t == "text":
        at.text_area(key=key(q)).input("Todo bien")
    elif t == "branching_tree":
        node_id = q["root"]
        while node_id is not None:
            option = q["tree"][node_id]["options"][0]
            at.radio(key=key(q, node_id)).set_value(option).run()
            node_id = q["tree"][node_id]["branches"].get(option)


def respondent(env_path):
    conn = db.connect(env_path / "encuesta.db")
    rows = conn.execute("SELECT * FROM respondents").fetchall()
    assert len(rows) == 1
    return conn, rows[0], json.loads(rows[0]["survey_data_json"])


def test_full_run_completes_with_timing_and_intact_audit_chain(env):
    at = start()
    for _ in QUESTIONS:
        at = answer_current_page(at)
    assert at.success[0].value.startswith("¡Gracias!")

    conn, row, data = respondent(env)
    assert row["status"] == "completed"
    assert row["instrument_version"] == instrumento.VERSION
    assert data["identificacion"]["value"] == SELF
    assert data["g1_afinidad"]["value"] == NOMINATED  # stored in display order: cohort, then name
    # ctx_trabajo is a tree inside a group: its answers live under the group's page.
    assert data["ctx_familia_trabajo"]["value"]["ctx_trabajo"] == {"trabaja": "Sí", "horas": "Menos de 10"}
    assert data["cierre"]["value"] == {"comentarios": "Todo bien"}
    times = db.get_answer_times(conn, row["id"])
    assert set(times) == {q["id"] for q in QUESTIONS}
    assert all(t is not None for t in times.values())
    assert audit.verify_chain(conn) == (True, None)


def test_completed_link_is_read_only(env):
    at = start()
    for _ in QUESTIONS:
        at = answer_current_page(at)
    token = at.session_state["_token"]

    again = start({"token": token})
    assert again.success[0].value.startswith("¡Gracias!")
    assert not again.button


def test_declining_ends_the_survey_without_saving_anything_else(env):
    at = click_next(start())
    q = page(at)
    at.radio(key=key(q)).set_value(q["decline"]).run()
    assert at.button(key="_next_1").label == "Terminar"
    at = click_next(at)

    assert at.info[0].value.startswith("Gracias por tu tiempo")
    _, row, data = respondent(env)
    assert row["status"] == "declined"
    assert data == {"consentimiento": {"value": q["decline"]}}


def test_withdrawing_consent_later_deletes_answers_and_frees_the_name(env):
    at = start()
    while page(at)["type"] != "roster_checklist":
        at = answer_current_page(at)
    at = answer_current_page(at)  # one nomination page answered

    at.session_state["_page"] = INDEX["consentimiento"]
    at.run()
    at.radio(key="w__consentimiento").set_value(QUESTIONS[INDEX["consentimiento"]]["decline"]).run()
    at = click_next(at)

    conn, row, data = respondent(env)
    assert row["status"] == "declined"
    assert list(data) == ["consentimiento"]
    assert conn.execute("SELECT COUNT(*) AS n FROM answers").fetchone()["n"] == 0
    assert conn.execute("SELECT COUNT(*) AS n FROM name_claims").fetchone()["n"] == 0


def test_identity_and_consent_cannot_be_skipped(env):
    at = click_next(start())
    assert at.button(key="_next_1").disabled
    at.radio(key="w__consentimiento").set_value("Acepto participar").run()
    # The academic-record authorization is on the same page and also required.
    assert at.button(key="_next_1").disabled
    at.radio(key="w__autoriza_registros").set_value("No").run()
    at = click_next(at)
    assert page(at)["type"] == "self_id"
    assert at.button(key=f"_next_{INDEX['identificacion']}").disabled


def test_unanswered_page_offers_to_omit_and_records_it(env):
    q = next(q for q in QUESTIONS if q["type"] == "number")
    at = start()
    while page(at)["id"] != q["id"]:
        at = answer_current_page(at)
    at = click_next(at)
    assert page(at)["id"] == q["id"]  # didn't advance
    at = at.button(key=f"_omit_btn_{INDEX[q['id']]}").click().run()
    assert page(at)["id"] == QUESTIONS[INDEX[q["id"]] + 1]["id"]

    _, _, data = respondent(env)
    assert data[q["id"]]["value"] == OMIT


def test_consent_page_stores_the_authorization_under_its_own_column(env):
    from motor import export

    at = start()
    while page(at)["type"] != "self_id":
        at = answer_current_page(at)
    _, _, data = respondent(env)
    consent = QUESTIONS[INDEX["consentimiento"]]
    assert data["consentimiento"]["value"]["decision"] == consent["accept"]
    cells = export.encode_answers(QUESTIONS, data)
    assert cells["autoriza_registros"] == 1  # «Sí», first option


def test_nobody_is_recorded_as_an_empty_list_not_as_missing(env):
    at = start()
    while page(at)["id"] != "g2_ayuda":
        at = answer_current_page(at)
    at.checkbox(key="_nobody_g2_ayuda").check().run()
    at = click_next(at)
    assert page(at)["id"] == "g3_estudio"

    # g3: nothing marked -> prompt -> «Prefiero no contestar»
    at = click_next(at)
    assert any("No has marcado a nadie" in m.value for m in at.markdown)
    at = at.button(key=f"_omit_btn_{INDEX['g3_estudio']}").click().run()

    _, _, data = respondent(env)
    assert data["g2_ayuda"]["value"] == []
    assert data["g3_estudio"]["value"] == OMIT


def test_nomination_list_excludes_self_and_respects_the_cap(env):
    at = start()
    while page(at)["id"] != "g1_afinidad":
        at = answer_current_page(at)
    q = page(at)
    codes = [c.key.rsplit("__", 1)[1] for c in at.checkbox if c.key.startswith("w__g1_afinidad__")]
    assert SELF not in codes and len(codes) == 75

    for code in codes[: q["max_selections"]]:
        at.checkbox(key=key(q, code)).check()
    at.run()
    unchecked = [c for c in at.checkbox if c.key.startswith("w__g1_afinidad__") and not c.value]
    assert unchecked and all(c.disabled for c in unchecked)
    assert at.checkbox(key="_nobody_g1_afinidad").disabled


def test_name_filter_keeps_hidden_selections(env):
    at = start()
    while page(at)["id"] != "g1_afinidad":
        at = answer_current_page(at)
    at.checkbox(key="w__g1_afinidad__2").check().run()
    at.text_input(key="_filter_g1_afinidad").input("zzz").run()
    assert not [c for c in at.checkbox if c.key.startswith("w__g1_afinidad__")]
    at = click_next(at)

    _, _, data = respondent(env)
    assert data["g1_afinidad"]["value"] == ["2"]


def test_partially_answered_block_omits_only_the_missing_items(env):
    block_id = next(q["id"] for q in QUESTIONS if q["type"] == "likert_block")
    at = start()
    while page(at)["id"] != block_id:
        at = answer_current_page(at)
    q = page(at)
    n = len(q["items"])
    first = q["items"][0]["id"]
    at.radio(key=key(q, first)).set_value(q["options"][0]).run()
    at = click_next(at)
    assert any(f"Te falta responder {n - 1} de {n}" in m.value for m in at.markdown)
    at = at.button(key=f"_omit_btn_{INDEX[block_id]}").click().run()

    _, _, data = respondent(env)
    value = data[block_id]["value"]
    assert value[first] == q["options"][0]
    assert [value[item["id"]] for item in q["items"][1:]] == [OMIT] * (n - 1)


def test_resume_link_lands_on_the_first_unanswered_page(env):
    at = start()
    while page(at)["id"] != "g2_ayuda":
        at = answer_current_page(at)
    token = at.session_state["_token"]

    resumed = start({"token": token})
    assert page(resumed)["id"] == "g2_ayuda"
    g1 = QUESTIONS[INDEX["g1_afinidad"]]
    resumed.session_state["_page"] = INDEX["g1_afinidad"]
    resumed.run()
    assert all(resumed.checkbox(key=key(g1, code)).value for code in NOMINATED)


def test_a_name_can_only_be_claimed_once(env):
    first = start()
    while page(first)["id"] != "instrucciones_redes":
        first = answer_current_page(first)

    second = start()
    while page(second)["type"] != "self_id":
        second = answer_current_page(second)
    second.selectbox(key="w__identificacion").set_value(SELF).run()
    assert second.error and "ya fue seleccionado" in second.error[0].value
    assert second.button(key=f"_next_{INDEX['identificacion']}").disabled


def test_unknown_roster_link_is_rejected(env):
    at = start({"nomina": "no-existe"})
    assert "no corresponde a ninguna encuesta" in at.error[0].value


def test_export_produces_pseudonymized_tables(env, monkeypatch):
    at = start()
    for _ in QUESTIONS:
        at = answer_current_page(at)

    key_text = "clave-de-prueba"
    monkeypatch.setenv("CLAVE_SEUDONIMOS", key_text)
    out = env / "export"
    spec = importlib.util.spec_from_file_location("exportar", ENCUESTA_DIR / "scripts" / "exportar.py")
    exportar = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exportar)
    monkeypatch.setattr(sys, "argv", ["exportar.py", "--nomina", "ejemplo", "--salida", str(out)])
    exportar.main()

    with open(out / "nodos.csv", encoding="utf-8") as f:
        nodes = {row["id"]: row for row in csv.DictReader(f)}
    assert len(nodes) == 76
    me = nodes[export.pseudonym(key_text.encode(), SELF)]
    assert me["estado"] == "completa"
    assert me["g1_afinidad_n"] == "2"
    assert me["ctx_trabajo__horas"] == "1"
    others = [row for pid, row in nodes.items() if row is not me]
    assert all(row["estado"] == "sin_respuesta" and row["g1_afinidad_n"] == "SIN_RESPUESTA" for row in others)

    with open(out / "aristas_g1_afinidad.csv", encoding="utf-8") as f:
        edges = list(csv.DictReader(f))
    assert {e["hacia"] for e in edges} == {export.pseudonym(key_text.encode(), c) for c in NOMINATED}

    everything = "".join(p.read_text(encoding="utf-8") for p in out.iterdir())
    for person in rosters.load_roster("ejemplo"):
        assert person.name not in everything
    assert "Todo bien" in (out / "textos_abiertos.csv").read_text(encoding="utf-8")
    assert "Completas:     1" in (out / "resumen.txt").read_text(encoding="utf-8")


def test_partially_answered_group_omits_only_the_missing_questions(env):
    group = next(q for q in QUESTIONS if q["type"] == "group")
    first, *rest = [m for m in group["members"] if m["type"] != "info"]
    at = start()
    while page(at)["id"] != group["id"]:
        at = answer_current_page(at)
    fill(at, first)
    at = click_next(at.run())
    assert any(f"Te falta responder {len(rest)} de {len(rest) + 1} preguntas" in m.value for m in at.markdown)
    at = at.button(key=f"_omit_btn_{INDEX[group['id']]}").click().run()
    assert page(at)["id"] != group["id"]

    _, _, data = respondent(env)
    value = data[group["id"]]["value"]
    assert value[first["id"]] is not None and value[first["id"]] != OMIT
    assert all(value[m["id"]] not in (None, {}) for m in rest)


def test_block_with_option_help_injects_hover_css(env):
    block = next(q for q in QUESTIONS if q["type"] == "likert_block" and q.get("option_help"))
    at = start()
    while page(at)["id"] != block["id"]:
        at = answer_current_page(at)
    css = " ".join(h.proto.body for h in at.get("html"))
    assert f'st-key-w__{block["id"]}__' in css
    assert block["option_help"][3] in css


def _go_to_first_number_page(at):
    q = next(q for q in QUESTIONS if q["type"] == "number")
    while page(at)["id"] != q["id"]:
        at = answer_current_page(at)
    return at, q


def test_plus_on_an_empty_number_gives_one_and_keeps_counting(env):
    at, q = _go_to_first_number_page(start())
    assert at.number_input(key=key(q)).value is None  # no default
    at = at.button(key=key(q) + "__mas").click().run()
    assert at.number_input(key=key(q)).value == 1
    at = at.button(key=key(q) + "__mas").click().run()
    assert at.number_input(key=key(q)).value == 2
    at = click_next(at)
    _, _, data = respondent(env)
    assert data[q["id"]]["value"] == 2


def test_minus_on_an_empty_number_stays_at_zero(env):
    at, q = _go_to_first_number_page(start())
    at = at.button(key=key(q) + "__menos").click().run()
    assert at.number_input(key=key(q)).value == 0
    at = at.button(key=key(q) + "__menos").click().run()
    assert at.number_input(key=key(q)).value == 0


def test_each_page_gets_a_fresh_scroll_to_top_script(env):
    at = start()
    first = [h.proto.body for h in at.get("html") if "stMain" in h.proto.body]
    at = answer_current_page(at)
    second = [h.proto.body for h in at.get("html") if "stMain" in h.proto.body]
    assert first and second and first != second  # identical HTML wouldn't run again
