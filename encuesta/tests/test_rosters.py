import pytest

from motor import rosters


def write(tmp_path, name, text, encoding="utf-8"):
    (tmp_path / f"{name}.csv").write_text(text, encoding=encoding)


def test_load_roster_reads_codes_names_and_cohorts(tmp_path):
    write(tmp_path, "curso", "N,NOMBRE,COHORTE\n1,Ana,2025\n2,Beto,2026\n")
    assert rosters.load_roster("curso", tmp_path) == [
        rosters.Person("1", "Ana", "2025"),
        rosters.Person("2", "Beto", "2026"),
    ]


def test_cohort_column_is_optional(tmp_path):
    write(tmp_path, "curso", "N,NOMBRE\n1,Ana\n")
    assert rosters.load_roster("curso", tmp_path) == [rosters.Person("1", "Ana", "")]


def test_accepts_excel_bom_and_semicolons(tmp_path):
    write(tmp_path, "excel", "N;NOMBRE;COHORTE\n1;Ana Pérez;2025\n", encoding="utf-8-sig")
    assert rosters.load_roster("excel", tmp_path) == [rosters.Person("1", "Ana Pérez", "2025")]


def test_skips_blank_lines(tmp_path):
    write(tmp_path, "curso", "N,NOMBRE\n1,Ana\n,\n2,Beto\n")
    assert [p.code for p in rosters.load_roster("curso", tmp_path)] == ["1", "2"]


def test_missing_roster_returns_none(tmp_path):
    assert rosters.load_roster("no-existe", tmp_path) is None


@pytest.mark.parametrize("nomina", ["../etc/passwd", "/etc/passwd", "a/b", ".oculta", "", None])
def test_rejects_anything_but_a_plain_name(tmp_path, nomina):
    assert rosters.roster_path(nomina, tmp_path) is None


@pytest.mark.parametrize(
    "text, message",
    [
        ("NOMBRE\nAna\n", "falta la columna N"),
        ("N,NOMBRE\n1,Ana\n1,Beto\n", "repetido"),
        ("N,NOMBRE\n1,\n", "no pueden quedar vacíos"),
        ("N,NOMBRE\n", "vacía"),
    ],
)
def test_malformed_rosters_raise_a_clear_error(tmp_path, text, message):
    write(tmp_path, "mala", text)
    with pytest.raises(rosters.RosterError, match=message):
        rosters.load_roster("mala", tmp_path)


def test_display_order_is_by_cohort_then_accent_insensitive_name():
    people = [
        rosters.Person("1", "Óscar", "2026"),
        rosters.Person("2", "Beto", "2025"),
        rosters.Person("3", "Ana", "2026"),
        rosters.Person("4", "Pía", "2026"),
    ]
    assert [p.name for p in rosters.display_order(people)] == ["Beto", "Ana", "Óscar", "Pía"]


def test_normalize_ignores_accents_and_case():
    assert rosters.normalize("José MUÑOZ") == rosters.normalize("jose munoz")


def test_example_roster_is_valid():
    from motor import settings

    people = rosters.load_roster("ejemplo", settings.EXAMPLES_DIR)
    assert len(people) == 76
    assert rosters.has_cohorts(people)
