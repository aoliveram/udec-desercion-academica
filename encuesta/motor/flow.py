"""Pure survey-flow logic, kept out of app.py so it's testable without a
Streamlit runtime.

Every page stores one value under its question id. What the value means:

- None            not answered yet (the page was shown, nothing chosen)
- OMIT            the respondent chose «Prefiero no contestar»
- anything else   the answer: an option label, a number, a text, a list
                  of roster codes ([] = "No hay nadie"), {item_id: option}
                  for a likert_block, {node_id: option} for a branching_tree,
                  {member_id: member value} for a group, and
                  {"decision": option, member_id: option} for a consent page
                  with extra questions
"""

from motor.preguntas import OMIT

# Pages whose answer can't be skipped with «Prefiero no contestar».
NOT_OMITTABLE = {"info", "consent", "self_id"}


def build_context(roster, self_code):
    """roster: [Person, ...] (see rosters.py). Returns what the page
    renderers need to know about the roster and the respondent."""
    return {
        "roster": roster,
        "roster_excl_self": [p for p in roster if p.code != self_code] if self_code else list(roster),
        "self_code": self_code,
    }


def is_answered(question, value):
    """Whether a page's value lets the respondent move on (OMIT counts)."""
    if value is None:
        return False
    if value == OMIT:
        return True
    if question["type"] == "branching_tree":
        return next_tree_node(question["tree"], question["root"], value) is None
    if question["type"] == "likert_block":
        return all(value.get(item["id"]) is not None for item in question["items"])
    if question["type"] == "group":
        return all(is_answered(m, value.get(m["id"])) for m in answerable_members(question))
    if question["type"] == "consent" and question.get("members"):
        decision = consent_decision(question, value)
        if decision is None:
            return False
        if decision == question["decline"]:
            return True  # declining needs nothing else
        return all(isinstance(value, dict) and value.get(m["id"]) is not None for m in question["members"])
    return True


def consent_decision(question, value):
    """The accept/decline choice in a consent page's value: the value itself
    for a plain consent page, value["decision"] for one with extra questions."""
    if isinstance(value, dict):
        return value.get("decision")
    return value


def answerable_members(group):
    """A group's members that take an answer (its info texts don't)."""
    return [m for m in group["members"] if m["type"] != "info"]


def is_question_answered(question, saved_data):
    return is_answered(question, saved_data.get(question["id"], {}).get("value"))


def _choices(value):
    """Every option label in a page value (nested dicts included)."""
    if isinstance(value, dict):
        for v in value.values():
            yield from _choices(v)
    elif isinstance(value, str):
        yield value


def _page_by_id(questions, page_id):
    return next(q for q in questions if q["id"] == page_id)


def is_shown(question, saved_data, questions):
    """Whether a page is part of this respondent's path. A page with a
    `show_if` condition (mostrar_si) is, when the page it points to is
    itself shown and holds at least one answer other than the excluded
    one («Prefiero no contestar» doesn't count)."""
    condition = question.get("show_if")
    if not condition:
        return True
    ref = _page_by_id(questions, condition["page"])
    if not is_shown(ref, saved_data, questions):
        return False
    value = saved_data.get(ref["id"], {}).get("value")
    return any(c != condition["other_than"] and c != OMIT for c in _choices(value))


def skipped_by_path(question, saved_data, questions):
    """True when the respondent's answers ruled the page out (export:
    NO_APLICA), as opposed to not having got that far yet (SIN_RESPUESTA)."""
    condition = question.get("show_if")
    if not condition:
        return False
    ref = _page_by_id(questions, condition["page"])
    if skipped_by_path(ref, saved_data, questions):
        return True
    if not is_shown(ref, saved_data, questions) or not is_question_answered(ref, saved_data):
        return False
    return not is_shown(question, saved_data, questions)


def neighbor_index(questions, saved_data, index, step):
    """The next (step=1) or previous (step=-1) page on the respondent's
    path, or None if there isn't one."""
    i = index + step
    while 0 <= i < len(questions):
        if is_shown(questions[i], saved_data, questions):
            return i
        i += step
    return None


def compute_resume_index(questions, answered_ids):
    """Index of the first not-yet-answered question, or the last question
    if everything's already answered (so a respondent who answered
    everything but never hit submit lands back on the last page, not page
    0)."""
    return next(
        (i for i, q in enumerate(questions) if q["id"] not in answered_ids),
        len(questions) - 1,
    )


def omit_value(question, value):
    """The value to record when the respondent presses «Prefiero no
    contestar» on a page that isn't fully answered."""
    if question["type"] == "likert_block":
        filled = dict(value or {})
        for item in question["items"]:
            if filled.get(item["id"]) is None:
                filled[item["id"]] = OMIT
        return filled
    if question["type"] == "branching_tree":
        answers = dict(value or {})
        pending = next_tree_node(question["tree"], question["root"], answers)
        if pending is not None:
            answers[pending] = OMIT
        return answers
    if question["type"] == "group":
        answers = dict(value or {})
        for m in answerable_members(question):
            if not is_answered(m, answers.get(m["id"])):
                answers[m["id"]] = omit_value(m, answers.get(m["id"]))
        return answers
    return OMIT


def next_tree_node(tree, root_id, answers):
    """Walk a branching_tree question's spec given the node ids already
    answered. Returns the id of the next node that still needs a widget
    rendered, or None once a leaf has been reached (the tree is fully
    answered along the path these answers describe).

    `tree`: {node_id: {"options": [...], "branches": {answer: next_node_id}}}.
    A node with no entry for a given answer in "branches" (including a
    node with an empty "branches" dict) is a leaf for that answer. OMIT at
    any node ends the tree there.
    """
    node_id = root_id
    while node_id in answers:
        if answers[node_id] == OMIT:
            return None
        next_id = tree[node_id]["branches"].get(answers[node_id])
        if next_id is None:
            return None
        node_id = next_id
    return node_id


def clean_tree_answers(tree, root_id, answers):
    """Drop any answer that doesn't match its node's declared options, and
    anything hanging off a since-invalidated branch ("re-validate, don't
    trust stored/session state"). Walks from the root along valid answers
    only, so a corrupted answer partway down also drops everything below it.
    """
    cleaned = {}
    node_id = root_id
    while node_id in answers:
        answer = answers[node_id]
        node = tree.get(node_id)
        if node is None:
            break
        if answer == OMIT:
            cleaned[node_id] = answer
            break
        if answer not in node["options"]:
            break
        cleaned[node_id] = answer
        next_id = node["branches"].get(answer)
        if next_id is None:
            break
        node_id = next_id
    return cleaned


def clean_block_answers(question, answers):
    """Keep only {item_id: option-or-OMIT} pairs that belong to the block."""
    allowed = set(question["options"]) | {OMIT}
    item_ids = {item["id"] for item in question["items"]}
    return {
        item_id: answer
        for item_id, answer in (answers or {}).items()
        if item_id in item_ids and answer in allowed
    }


def clean_nominations(value, valid_codes, max_selections):
    """Re-validate a stored nomination value against the current roster."""
    if value is None or value == OMIT:
        return value
    if not isinstance(value, list):
        return None
    return [code for code in value if code in valid_codes][:max_selections]
