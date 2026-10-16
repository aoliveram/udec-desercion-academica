from motor import flow
from motor.preguntas import OMIT, bloque, nominacion, opcion_unica
from motor.rosters import Person

ROSTER = [Person("1", "Ana", "2025"), Person("2", "Beto", "2025"), Person("3", "Caro", "2026")]


def test_build_context_excludes_self_from_roster():
    ctx = flow.build_context(ROSTER, self_code="2")
    assert ctx["roster"] == ROSTER
    assert [p.code for p in ctx["roster_excl_self"]] == ["1", "3"]
    assert ctx["self_code"] == "2"


def test_build_context_no_self_code_keeps_full_roster():
    ctx = flow.build_context(ROSTER, self_code=None)
    assert ctx["roster_excl_self"] == ROSTER


def test_compute_resume_index_first_unanswered():
    questions = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    assert flow.compute_resume_index(questions, answered_ids={"a"}) == 1


def test_compute_resume_index_all_answered_lands_on_last_page():
    questions = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    assert flow.compute_resume_index(questions, answered_ids={"a", "b", "c"}) == 2


def test_compute_resume_index_nothing_answered_starts_at_zero():
    questions = [{"id": "a"}, {"id": "b"}]
    assert flow.compute_resume_index(questions, answered_ids=set()) == 0


# --- what counts as answered ---------------------------------------------------

RADIO = opcion_unica("q", "¿?", ["A", "B"])
ROSTER_Q = nominacion("g1", "¿Con quiénes?", maximo=2)
BLOCK = bloque("blk", "Acuerdo", [("i1", "uno"), ("i2", "dos")], ["Sí", "No"])


def test_a_page_shown_but_not_answered_is_not_answered():
    # The app saves None for a page that was shown with nothing chosen; resume
    # must land back on it, not skip past it.
    assert not flow.is_question_answered(RADIO, {"q": {"value": None}})
    assert flow.compute_resume_index([RADIO], answered_ids=set()) == 0


def test_omitted_counts_as_answered():
    assert flow.is_answered(RADIO, OMIT)


def test_nobody_is_an_answer_but_none_is_not():
    assert flow.is_answered(ROSTER_Q, [])
    assert not flow.is_answered(ROSTER_Q, None)


def test_block_needs_every_item():
    assert not flow.is_answered(BLOCK, {"i1": "Sí"})
    assert flow.is_answered(BLOCK, {"i1": "Sí", "i2": OMIT})


def test_omit_value_fills_only_missing_block_items():
    assert flow.omit_value(BLOCK, {"i1": "Sí"}) == {"i1": "Sí", "i2": OMIT}
    assert flow.omit_value(RADIO, None) == OMIT


def test_clean_block_answers_drops_unknown_items_and_options():
    assert flow.clean_block_answers(BLOCK, {"i1": "Sí", "i2": "Quizás", "zz": "No"}) == {"i1": "Sí"}


def test_clean_nominations_revalidates_against_roster_and_cap():
    assert flow.clean_nominations(["1", "9", "2", "3"], {"1", "2", "3"}, 2) == ["1", "2"]
    assert flow.clean_nominations([], {"1"}, 2) == []
    assert flow.clean_nominations(OMIT, {"1"}, 2) == OMIT
    assert flow.clean_nominations("garbage", {"1"}, 2) is None


# --- branching_tree ---------------------------------------------------------------

TREE = {
    "root": {"label": "Root?", "options": ["A", "B"], "branches": {"A": "leaf_a", "B": "mid"}},
    "leaf_a": {"label": "Leaf A?", "options": ["X", "Y"], "branches": {}},
    "mid": {"label": "Mid?", "options": ["1", "2", "3"], "branches": {"1": "leaf_mid"}},
    "leaf_mid": {"label": "Leaf mid?", "options": ["yes", "no"], "branches": {}},
}
TREE_QUESTION = {"id": "q_tree", "type": "branching_tree", "root": "root", "tree": TREE}


def test_next_tree_node_starts_at_root_when_nothing_answered():
    assert flow.next_tree_node(TREE, "root", {}) == "root"


def test_next_tree_node_follows_the_matching_branch():
    assert flow.next_tree_node(TREE, "root", {"root": "B"}) == "mid"


def test_next_tree_node_stops_at_a_leaf_with_empty_branches():
    assert flow.next_tree_node(TREE, "root", {"root": "A", "leaf_a": "X"}) is None


def test_next_tree_node_stops_when_the_answer_has_no_branch_entry():
    assert flow.next_tree_node(TREE, "root", {"root": "B", "mid": "2"}) is None


def test_next_tree_node_descends_multiple_levels():
    assert flow.next_tree_node(TREE, "root", {"root": "B", "mid": "1"}) == "leaf_mid"


def test_clean_tree_answers_keeps_a_fully_valid_path():
    answers = {"root": "B", "mid": "1", "leaf_mid": "yes"}
    assert flow.clean_tree_answers(TREE, "root", answers) == answers


def test_clean_tree_answers_drops_everything_from_first_invalid_answer():
    answers = {"root": "B", "mid": "9", "leaf_mid": "yes"}
    assert flow.clean_tree_answers(TREE, "root", answers) == {"root": "B"}


def test_clean_tree_answers_drops_answer_for_unreachable_node():
    answers = {"root": "B", "leaf_a": "X"}
    assert flow.clean_tree_answers(TREE, "root", answers) == {"root": "B"}


def test_tree_in_progress_is_not_answered_but_finished_is():
    assert not flow.is_question_answered(TREE_QUESTION, {"q_tree": {"value": {"root": "B", "mid": "1"}}})
    assert flow.is_question_answered(TREE_QUESTION, {"q_tree": {"value": {"root": "A", "leaf_a": "X"}}})
    assert not flow.is_question_answered(TREE_QUESTION, {"q_tree": {"value": None}})


def test_omitting_a_tree_node_is_valid_and_ends_the_tree():
    answers = flow.omit_value(TREE_QUESTION, {"root": "B"})
    assert answers == {"root": "B", "mid": OMIT}
    assert flow.clean_tree_answers(TREE, "root", answers) == answers
    assert flow.next_tree_node(TREE, "root", answers) is None
