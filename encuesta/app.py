"""Streamlit entry point: one page per question, every answer persisted as
soon as it's given, resumable via a per-respondent link.

The instrument itself lives in instrumento.py; this file only knows how to
render each page type (see motor/preguntas.py) and move between pages.

Run from this folder:  streamlit run app.py   (or scripts/demo.py)
A respondent link is the app's URL plus ?nomina=<roster name>.
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone

import streamlit as st

import instrumento
from motor import audit, db, flow, preguntas, rosters, security, settings
from motor.preguntas import OMIT

QUESTIONS = instrumento.PREGUNTAS

st.set_page_config(page_title=instrumento.TITULO, page_icon=":material/edit_note:")

_problems = preguntas.validar(QUESTIONS)
if _problems:
    st.error("El instrumento tiene problemas:\n\n" + "\n".join(f"- {p}" for p in _problems))
    st.stop()

SELF_ID_Q = next(q for q in QUESTIONS if q["type"] == "self_id")
CONSENT_Q = next((q for q in QUESTIONS if q["type"] == "consent"), None)


@st.cache_resource
def get_db():
    return db.connect()


@st.cache_data(ttl="5m")
def load_roster(nomina):
    return rosters.load_roster(nomina)


def get_client_ip() -> str:
    # Behind the documented reverse proxy (Cloudflare Tunnel, with the server
    # itself bound to 127.0.0.1) the real client address arrives in
    # X-Forwarded-For; st.context.ip_address would otherwise just be the
    # proxy's own loopback address. The header is client-controlled, so only
    # honor it while that assumption holds (settings.TRUST_PROXY_HEADERS).
    if settings.TRUST_PROXY_HEADERS:
        forwarded = (st.context.headers or {}).get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
    return st.context.ip_address or "unknown"


def widget_key(question, *parts):
    return "__".join(["w", question["id"], *map(str, parts)])


def scroll_to_top_script():
    """Script that brings a newly opened page back to the top.

    No native Streamlit API resets the scroll position on navigation. Three
    details, each checked in a browser:
    - What scrolls is Streamlit's main container (data-testid="stMain"),
      not the window, so window.scrollTo alone does nothing.
    - Streamlit doesn't re-run a script whose HTML is identical to the one
      already on the page, so each visit gets its own number.
    - Wrapped in a function so re-running it doesn't redeclare a variable.
    Two nested requestAnimationFrame calls wait for the new page's layout to
    settle before scrolling."""
    visit = st.session_state["_scroll_visit"] = st.session_state.get("_scroll_visit", 0) + 1
    return (
        f'<script data-visita="{visit}">(() => {{'
        "const top = () => {"
        "document.querySelectorAll('[data-testid=\"stMain\"]').forEach((e) => e.scrollTo(0, 0));"
        "window.scrollTo(0, 0);"
        "};"
        "requestAnimationFrame(() => requestAnimationFrame(top));"
        "})();</script>"
    )


def show_omitted_note():
    st.caption(f"Marcaste «{OMIT}» en esta pregunta.")


# --- one renderer per page type ---------------------------------------------
# Each takes (question, saved value, context) and returns the page's current
# value with the meaning documented in motor/flow.py. Widgets get their
# default from the saved value, so the database (not session_state) is what
# survives a reload, a resume link, or leaving the page and coming back.


def render_info(question, saved, context):
    st.markdown(question["label"])
    return True


def render_consent(question, saved, context):
    st.markdown(question["label"])
    if question.get("document"):
        with st.expander("Leer el documento completo"):
            st.markdown(question["document"])
    if question.get("document_pdf"):
        pdf = settings.BASE_DIR / question["document_pdf"]
        if pdf.exists():
            st.download_button(
                "Descargar el documento (PDF)", pdf.read_bytes(), file_name=pdf.name,
                mime="application/pdf", icon=":material/download:", key=f"{widget_key(question)}__pdf",
            )
    options = question["options"]
    prior = flow.consent_decision(question, saved)
    choice = st.radio(
        "**¿Aceptas participar?**" if question.get("members") else "Tu decisión",
        options,
        index=options.index(prior) if prior in options else None,
        key=widget_key(question),
    )
    decision = choice if choice in options else None
    if not question.get("members"):
        return decision
    # Extra questions on the same page (e.g. the academic-record
    # authorization), each stored under its own id.
    saved_members = saved if isinstance(saved, dict) else {}
    answers = {"decision": decision} if decision is not None else {}
    for member in question["members"]:
        value = render_radio(member, saved_members.get(member["id"]), context)
        if value is not None:
            answers[member["id"]] = value
    return answers or None


def render_self_id(question, saved, context):
    people = rosters.display_order(context["roster"])
    show_cohort = rosters.has_cohorts(people)
    labels = {p.code: f"{p.name} · {p.cohort}" if show_cohort else p.name for p in people}
    options = [p.code for p in people]
    choice = st.selectbox(
        question["label"],
        options,
        index=options.index(saved) if saved in options else None,
        format_func=labels.get,
        placeholder="Busca tu nombre...",
        key=widget_key(question),
    )
    if choice not in labels:
        return None

    # Two people can pick the same name at the same moment; the first to
    # reach the database keeps it. A rejected pick is treated as "no
    # answer": it isn't saved as this respondent's identity and Siguiente
    # stays disabled.
    claim = db.claim_name(conn, respondent_row["nomina"], choice, respondent_id)
    if claim == "claimed":
        audit.append_event(conn, respondent_id, "self_id_claimed", {"code": choice})
        if saved is not None and saved != choice:
            audit.append_event(conn, respondent_id, "self_id_changed", {"from": saved, "to": choice})
    elif claim == "taken":
        # Every rerun while the taken name is still selected lands here;
        # only log the first.
        if st.session_state.get("_last_rejected_name") != choice:
            audit.append_event(conn, respondent_id, "self_id_claim_rejected", {"code": choice})
            st.session_state["_last_rejected_name"] = choice
        st.error("Este nombre ya fue seleccionado. Revisa que sea el tuyo o avisa a quien aplica la encuesta.")
        return None
    return choice


def render_roster_checklist(question, saved, context):
    # Plain checkboxes rather than st.multiselect: its built-in "Select all"
    # bulk action ignores max_selections. The cap is enforced here instead
    # by disabling unchecked boxes once it's reached.
    people = rosters.display_order(context["roster_excl_self"])
    max_sel = question["max_selections"]
    saved = flow.clean_nominations(saved, {p.code for p in people}, max_sel)
    saved_codes = saved if isinstance(saved, list) else []
    nobody_key = f"_nobody_{question['id']}"

    # A box hidden by the name filter isn't rendered, so Streamlit drops its
    # widget state; its default then comes back from the saved value, which
    # still includes it because `selected` starts from checked_before.
    checked_before = {
        p.code: st.session_state.get(widget_key(question, p.code), p.code in saved_codes) for p in people
    }
    nobody_before = st.session_state.get(nobody_key, saved == [])
    n_before = sum(checked_before.values())

    st.markdown(f"**{question['label']}**")
    st.caption(f"No hay un número correcto. Puedes marcar hasta {max_sel}; llevas {n_before}.")
    query = st.text_input(
        "Buscar por nombre",
        key=f"_filter_{question['id']}",
        placeholder="Buscar por nombre",
        label_visibility="collapsed",
    )
    summary = st.empty()

    needle = rosters.normalize(query.strip())
    visible = [p for p in people if needle in rosters.normalize(p.name)] if needle else people
    grouped = rosters.has_cohorts(people)
    selected = {code for code, checked in checked_before.items() if checked}

    for cohort in dict.fromkeys(p.cohort for p in visible):
        members = [p for p in visible if p.cohort == cohort]
        if grouped:
            st.markdown(f"**{cohort or 'Sin cohorte'}**")
        cols = st.columns(3)
        for i, p in enumerate(members):
            disabled = nobody_before or (not checked_before[p.code] and n_before >= max_sel)
            with cols[i % 3]:
                checked = st.checkbox(
                    p.name, value=checked_before[p.code], key=widget_key(question, p.code), disabled=disabled
                )
            if checked:
                selected.add(p.code)
            else:
                selected.discard(p.code)
    if needle and not visible:
        st.caption("Ningún nombre coincide con la búsqueda.")

    st.divider()
    nobody = st.checkbox(question["nobody_label"], value=nobody_before, key=nobody_key, disabled=n_before > 0)

    ordered = [p.code for p in people if p.code in selected]
    if len(ordered) > max_sel:
        # Only reachable via tampered session_state, not normal clicks.
        audit.append_event(
            conn, respondent_id, "selection_cap_exceeded", {"question_id": question["id"], "count": len(ordered)}
        )
        ordered = ordered[:max_sel]
    if ordered:
        names = {p.code: p.name for p in people}
        summary.caption("Marcaste: " + ", ".join(names[c] for c in ordered))
        return ordered
    if nobody:
        return []
    if saved == OMIT:
        show_omitted_note()
        return OMIT
    return None


def render_radio(question, saved, context):
    st.markdown(f"**{question['label']}**")
    options = question["options"]
    choice = st.radio(
        question["label"],
        options,
        index=options.index(saved) if saved in options else None,
        key=widget_key(question),
        label_visibility="collapsed",
    )
    if choice in options:
        return choice
    if saved == OMIT:
        show_omitted_note()
        return OMIT
    return None


def option_tooltips_css(question):
    """CSS that shows each option's `ayudas` text in a bubble on hover.

    Streamlit radios have no per-option tooltip, so this styles the option
    labels of every item in the block (their widget keys share a prefix and
    Streamlit puts `st-key-<key>` on each widget's container). On a phone
    the bubble shows on tap, where the browser supports sticky hover."""
    scope = f'[class*="st-key-{widget_key(question)}__"] div[role="radiogroup"] > label'
    rules = [f"{scope} {{ position: relative; }}"]
    for n, text in enumerate(question["option_help"], start=1):
        if not text:
            continue
        content = json.dumps(text)  # a valid CSS string literal, quotes escaped
        rules.append(
            f"{scope}:nth-of-type({n}):hover::after {{ content: {content}; position: absolute; "
            "bottom: calc(100% + 6px); left: 50%; transform: translateX(-50%); white-space: nowrap; "
            "background: #31333F; color: #FFFFFF; font-size: 0.8rem; line-height: 1.3; "
            "padding: 4px 8px; border-radius: 6px; z-index: 1000; pointer-events: none; }"
        )
    return "<style>\n" + "\n".join(rules) + "\n</style>"


def italic(text):
    """Markdown italics for each paragraph (a single *...* can't span a blank line)."""
    return "\n\n".join(f"*{para.strip()}*" for para in text.split("\n\n") if para.strip())


def render_likert_block(question, saved, context):
    # The block's instruction in italics and each statement in bold, so the
    # eye lands on what has to be answered.
    st.markdown(italic(question["label"]))
    if question.get("option_help"):
        st.html(option_tooltips_css(question))
    options = question["options"]
    saved = flow.clean_block_answers(question, saved if isinstance(saved, dict) else {})
    answers = {}
    for item in question["items"]:
        prior = saved.get(item["id"])
        choice = st.radio(
            f"**{item['label']}**",
            options,
            index=options.index(prior) if prior in options else None,
            key=widget_key(question, item["id"]),
            horizontal=True,
        )
        if choice in options:
            answers[item["id"]] = choice
        elif prior == OMIT:
            answers[item["id"]] = OMIT
            show_omitted_note()
    return answers or None


def step_number(key, delta, minimum, maximum):
    """«−»/«+» callback. From an empty field «+» gives minimum + 1 and «−»
    gives the minimum, so the whole question can be answered without typing
    (no phone keyboard)."""
    current = st.session_state.get(key)
    new = (minimum + 1 if delta > 0 else minimum) if current is None else current + delta
    new = max(minimum, new)
    if maximum is not None:
        new = min(maximum, new)
    st.session_state[key] = new


def render_number(question, saved, context):
    max_value = question["max_value"]
    if max_value == "nomina":
        max_value = len(context["roster_excl_self"])
    min_value = question["min_value"]
    prior = saved if isinstance(saved, int) and not isinstance(saved, bool) else None
    if prior is not None and (prior < min_value or (max_value is not None and prior > max_value)):
        prior = None
    key = widget_key(question)
    # The value lives in session_state (not value=) so the buttons below can
    # change it; restore it from the database when the widget is new.
    if key not in st.session_state:
        st.session_state[key] = prior
    st.markdown(f"**{question['label']}**")
    # Streamlit disables its own +/- while the field is empty, so they're
    # hidden and replaced by buttons that also work from empty.
    st.html(
        f"<style>.st-key-{key} [data-testid='stNumberInputStepUp'], "
        f".st-key-{key} [data-testid='stNumberInputStepDown'] {{ display: none; }}</style>"
    )
    with st.container(horizontal=True, vertical_alignment="center", gap="small"):
        number = st.number_input(
            question["label"],
            min_value=min_value,
            max_value=max_value,
            value=None,
            step=1,
            placeholder="Escribe un número",
            key=key,
            label_visibility="collapsed",
        )
        st.button(
            "", icon=":material/remove:", key=f"{key}__menos", help="Restar uno",
            on_click=step_number, args=(key, -1, min_value, max_value),
        )
        st.button(
            "", icon=":material/add:", key=f"{key}__mas", help="Sumar uno",
            on_click=step_number, args=(key, 1, min_value, max_value),
        )
    if number is not None:
        return int(number)
    if saved == OMIT:
        show_omitted_note()
        return OMIT
    return None


def render_text(question, saved, context):
    st.markdown(f"**{question['label']}**")
    text = st.text_area(
        question["label"],
        value=saved if isinstance(saved, str) and saved != OMIT else "",
        max_chars=settings.MAX_TEXT_LENGTH,
        key=widget_key(question),
        label_visibility="collapsed",
    )
    return security.sanitize_text(text)


def render_branching_tree(question, saved, context):
    # A handful of radios asked in sequence, which one comes next depending
    # on the previous answer -- still one page and one id. Every node on the
    # current path is rendered on every rerun: a keyed widget that isn't
    # called in a run is dropped, so skipping answered nodes would make them
    # vanish the moment a later one gets answered.
    tree, root = question["tree"], question["root"]
    existing = flow.clean_tree_answers(tree, root, saved if isinstance(saved, dict) else {})
    answers = {}
    node_id = root
    while node_id is not None:
        node = tree[node_id]
        prior = existing.get(node_id)
        answer = st.radio(
            f"**{node['label']}**",  # bold like every other question
            node["options"],
            index=node["options"].index(prior) if prior in node["options"] else None,
            key=widget_key(question, node_id),
        )
        if answer not in node["options"]:
            if prior == OMIT:
                answers[node_id] = OMIT
                show_omitted_note()
            break
        answers[node_id] = answer
        node_id = node["branches"].get(answer)
    return answers or None


def render_group(question, saved, context):
    # Each member is drawn by its own renderer, with its own widget keys
    # (member ids are unique across the instrument), so it behaves exactly
    # as it would on a page of its own.
    saved = saved if isinstance(saved, dict) else {}
    answers = {}
    for n, member in enumerate(question["members"]):
        if n:
            st.divider()
        value = RENDERERS[member["type"]](member, saved.get(member["id"]), context)
        if member["type"] != "info" and value is not None:
            answers[member["id"]] = value
    return answers or None


RENDERERS = {
    "info": render_info,
    "consent": render_consent,
    "self_id": render_self_id,
    "roster_checklist": render_roster_checklist,
    "radio": render_radio,
    "likert_block": render_likert_block,
    "number": render_number,
    "text": render_text,
    "branching_tree": render_branching_tree,
    "group": render_group,
}


def omit_prompt_message(question, value):
    if question["type"] == "roster_checklist":
        return f"No has marcado a nadie. Si no hay nadie, marca «{question['nobody_label']}»."
    if question["type"] == "likert_block":
        missing = sum(1 for item in question["items"] if (value or {}).get(item["id"]) is None)
        return f"Te falta responder {missing} de {len(question['items'])} afirmaciones."
    if question["type"] == "group":
        members = flow.answerable_members(question)
        missing = sum(1 for m in members if not flow.is_answered(m, (value or {}).get(m["id"])))
        return f"Te falta responder {missing} de {len(members)} preguntas."
    return "No has seleccionado una respuesta."


# --- page transitions and timing ----------------------------------------------


def close_current_visit():
    """Close the open page visit (final, precise dwell time) and copy that
    time onto the page's answer."""
    if st.session_state.get("_visit_row_id") is None:
        return None
    left = QUESTIONS[st.session_state["_visit_page_index"]]
    entered_at = datetime.fromisoformat(st.session_state["_visit_entered_at"])
    duration = (datetime.now(timezone.utc) - entered_at).total_seconds()
    db.close_page_visit(conn, st.session_state["_visit_row_id"], duration)
    db.set_answer_time_spent(conn, respondent_id, left["id"], duration)
    st.session_state["_visit_row_id"] = None
    return left, duration


def go_to(index):
    st.session_state["_page"] = index
    st.rerun()


def finalize():
    close_current_visit()
    db.mark_completed(conn, respondent_id)
    audit.append_event(conn, respondent_id, "survey_completed", {})
    st.rerun()


def decline(consent_value):
    close_current_visit()
    db.mark_declined(conn, respondent_id, CONSENT_Q["id"], consent_value)
    audit.append_event(conn, respondent_id, "consent_declined", {})
    st.rerun()


# --- resolve the respondent: resume via token, or start a new one -------------

conn = get_db()

# Text a bit larger than Streamlit's 16 px so questions and options read
# easily, also on a phone. Done in CSS rather than with the theme's
# baseFontSize: setting any [theme] option swaps Streamlit's default colors.
# Widget labels and options (radios, checkboxes) are a size smaller than body
# text by default; they're brought up to it.
st.html(
    "<style>"
    f"html {{ font-size: {settings.BASE_FONT_SIZE_PX}px; }}"
    '[data-testid="stWidgetLabel"] p, div[role="radiogroup"] label p, '
    '[data-testid="stCheckbox"] label p { font-size: 1rem; }'
    "</style>"
)

st.title(instrumento.TITULO)

token = st.query_params.get("token") or st.session_state.get("_token")
respondent_row = db.get_respondent_by_token_hash(conn, security.hash_token(token)) if token else None

if respondent_row is None:
    nomina = st.query_params.get("nomina")
    try:
        new_roster = load_roster(nomina) if nomina else None
    except rosters.RosterError as e:
        st.error(f"La nómina de esta encuesta tiene un problema: {e}")
        st.stop()
    if new_roster is None:
        st.error("Este enlace no corresponde a ninguna encuesta. Pide el enlace correcto a quien aplica la encuesta.")
        st.stop()

    ip_hash = security.hash_ip(get_client_ip())
    allowed = db.check_and_record_rate_limit(
        conn, ip_hash, settings.RATE_LIMIT_WINDOW_SECONDS, settings.RATE_LIMIT_MAX_NEW_RESPONDENTS
    )
    if not allowed:
        st.error("Se han registrado demasiadas personas desde tu red en la última hora. Intenta más tarde.")
        st.stop()

    token = security.generate_token()
    respondent_id = str(uuid.uuid4())
    db.create_respondent(conn, respondent_id, security.hash_token(token), nomina, instrumento.VERSION, ip_hash)
    audit.append_event(
        conn,
        respondent_id,
        "respondent_created",
        {"nomina": nomina, "ip_hash": ip_hash, "instrument_version": instrumento.VERSION},
    )
    st.query_params["token"] = token
    respondent_row = db.get_respondent_by_token_hash(conn, security.hash_token(token))
else:
    db.touch_respondent(conn, respondent_row["id"])

st.session_state["_token"] = token
respondent_id = respondent_row["id"]

if respondent_row["status"] == "completed":
    st.success("¡Gracias! Tus respuestas ya quedaron guardadas.")
    st.stop()
if respondent_row["status"] == "declined":
    st.info("Gracias por tu tiempo. No se guardó ninguna respuesta tuya.")
    st.stop()

try:
    roster = load_roster(respondent_row["nomina"])
except rosters.RosterError:
    roster = None
if roster is None:
    st.error("No se encontró la nómina de esta encuesta. Avisa a quien aplica la encuesta.")
    st.stop()

saved_data = json.loads(respondent_row["survey_data_json"] or "{}")
self_code = saved_data.get(SELF_ID_Q["id"], {}).get("value")
if self_code not in {p.code for p in roster}:
    self_code = None
context = flow.build_context(roster, self_code)

answered_ids = {q["id"] for q in QUESTIONS if flow.is_question_answered(q, saved_data)}
if "_page" not in st.session_state:
    st.session_state["_page"] = flow.compute_resume_index(QUESTIONS, answered_ids)

idx = min(max(st.session_state["_page"], 0), len(QUESTIONS) - 1)
question = QUESTIONS[idx]
is_last = idx == len(QUESTIONS) - 1

# --- landed on a new page: close the one we left, open a new visit window ------

if st.session_state.get("_visit_page_index") != idx:
    closed = close_current_visit()
    if closed is not None:
        left, duration = closed
        audit.append_event(conn, respondent_id, "page_left", {"question_id": left["id"], "duration_seconds": duration})
        if duration < settings.FAST_ANSWER_THRESHOLD_SECONDS:
            audit.append_event(
                conn, respondent_id, "fast_answer_flag", {"question_id": left["id"], "duration_seconds": duration}
            )
    st.session_state["_visit_row_id"] = db.open_page_visit(conn, respondent_id, idx)
    st.session_state["_visit_page_index"] = idx
    st.session_state["_visit_entered_at"] = datetime.now(timezone.utc).isoformat()
    st.session_state.pop("_omit_prompt", None)
    audit.append_event(conn, respondent_id, "page_entered", {"question_id": question["id"]})

    st.html(scroll_to_top_script(), unsafe_allow_javascript=True)

# --- the page itself -------------------------------------------------------------

st.progress((idx + 1) / len(QUESTIONS))
st.caption(f"Página {idx + 1} de {len(QUESTIONS)}")

saved_value = saved_data.get(question["id"], {}).get("value")
value = RENDERERS[question["type"]](question, saved_value, context)


def persist(page_value):
    elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(st.session_state["_visit_entered_at"])).total_seconds()
    db.upsert_answer(conn, respondent_id, question["id"], idx, page_value, elapsed)
    saved_data[question["id"]] = {"value": page_value}
    blob = json.dumps(saved_data, ensure_ascii=False)
    db.save_survey_blob(conn, respondent_id, blob, hashlib.sha256(blob.encode("utf-8")).hexdigest())


persist(value)
answered = flow.is_answered(question, value)

# Pressing Siguiente on an unanswered page doesn't advance: it shows this
# prompt instead, so skipping is a deliberate act and is recorded as such.
if not answered and st.session_state.get("_omit_prompt") == question["id"]:
    with st.container(border=True):
        st.markdown(omit_prompt_message(question, value))
        omit_label = "Prefiero no contestar las que faltan" if question["type"] in ("likert_block", "group") else OMIT
        if st.button(omit_label, type="primary", key=f"_omit_btn_{idx}"):
            persist(flow.omit_value(question, value))
            if is_last:
                finalize()
            go_to(idx + 1)

declining = question["type"] == "consent" and flow.consent_decision(question, value) == question["decline"]
if declining:
    next_label = "Terminar"
elif is_last:
    next_label = "Enviar"
elif idx == 0 and question["type"] == "info":
    next_label = "Comenzar"
else:
    next_label = "Siguiente"

blocked_help = None
if not answered and question["type"] == "consent":
    if flow.consent_decision(question, value) is None:
        blocked_help = "Debes indicar si aceptas participar para continuar."
    else:
        blocked_help = "Responde también las preguntas de esta página para continuar."
elif not answered and question["type"] == "self_id":
    blocked_help = "Debes seleccionar tu nombre para continuar."

col_prev, col_next = st.columns(2)
with col_prev:
    prev_clicked = st.button(
        "Anterior", icon=":material/arrow_back:", width="stretch", disabled=idx == 0, key=f"_prev_{idx}"
    )
with col_next:
    next_clicked = st.button(
        next_label,
        icon=":material/arrow_forward:",
        icon_position="right",
        width="stretch",
        disabled=blocked_help is not None,
        help=blocked_help,
        key=f"_next_{idx}",
    )

if prev_clicked:
    go_to(idx - 1)
if next_clicked:
    if declining:
        decline(flow.consent_decision(question, value))
    elif answered:
        if is_last:
            finalize()
        go_to(idx + 1)
    else:
        st.session_state["_omit_prompt"] = question["id"]
        st.rerun()
