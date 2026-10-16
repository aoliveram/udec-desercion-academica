"""Pure survey-flow logic, kept out of app.py so it's testable without a
Streamlit runtime.

Every page stores one value under its question id. What the value means:

- None            not answered yet (the page was shown, nothing chosen)
- OMIT            the respondent chose «Prefiero no contestar»
- anything else   the answer: an option label, a number, a text, a list
                  of roster codes ([] = "No hay nadie"), {item_id: option}
                  for a likert_block, {node_id: option} for a branching_tree
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
    return True


def is_question_answered(question, saved_data):
    return is_answered(question, saved_data.get(question["id"], {}).get("value"))


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
