import instrumento
from motor.preguntas import (
    OMIT,
    arbol,
    bloque,
    consentimiento,
    identificacion,
    info,
    nominacion,
    numero,
    opcion_unica,
    validar,
)

MINIMO = [consentimiento("consentimiento", "texto"), identificacion("yo")]


def test_the_real_instrument_is_valid():
    assert validar(instrumento.PREGUNTAS) == []


def test_minimal_instrument_is_valid():
    assert validar(MINIMO) == []


def test_duplicate_ids_are_reported_including_block_items():
    preguntas = MINIMO + [
        opcion_unica("p1", "¿?", ["A", "B"]),
        bloque("b", "¿?", [("p1", "repetido"), ("i2", "ok")], ["A", "B"]),
    ]
    assert any("repetido" in p for p in validar(preguntas))


def test_ids_must_be_safe_column_names():
    assert any("debe empezar" in p for p in validar(MINIMO + [info("Mal Id", "x")]))


def test_omit_is_never_one_of_the_options():
    problemas = validar(MINIMO + [opcion_unica("p", "¿?", ["A", OMIT])])
    assert any(OMIT in p for p in problemas)


def test_exactly_one_identification_page():
    assert validar([consentimiento("c", "t")])
    assert validar(MINIMO + [identificacion("otra")])


def test_nominations_must_come_after_identification():
    preguntas = [consentimiento("c", "t"), nominacion("g1", "¿?"), identificacion("yo")]
    assert any("después de la identificación" in p for p in validar(preguntas))


def test_consent_must_come_before_identification():
    preguntas = [identificacion("yo"), consentimiento("c", "t")]
    assert any("antes de la identificación" in p for p in validar(preguntas))


def test_roster_sized_maximum_needs_identification_first():
    preguntas = [numero("meta", "¿?", maximo="nomina")] + MINIMO
    assert any("maximo='nomina'" in p for p in validar(preguntas))


def test_reverse_ids_must_belong_to_the_block():
    preguntas = MINIMO + [bloque("b", "¿?", [("i1", "x")], ["A", "B"], invertidos=["i9"])]
    assert any("invertidos" in p for p in validar(preguntas))


def test_tree_branches_must_point_to_existing_nodes():
    malo = arbol("t", "a", {"a": {"texto": "¿?", "opciones": ["Sí", "No"], "siguiente": {"Sí": "zz"}}})
    assert any("no es un nodo" in p for p in validar(MINIMO + [malo]))


def test_block_items_carry_reverse_flag():
    b = bloque("b", "¿?", [("i1", "x"), ("i2", "y")], ["A", "B"], invertidos=["i2"])
    assert [item["reverse_scored"] for item in b["items"]] == [False, True]
