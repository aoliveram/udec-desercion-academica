#!/usr/bin/env python3
"""Exporta las respuestas de una nómina a tablas seudonimizadas para R o Python.

Uso (desde la carpeta encuesta/):
    python scripts/exportar.py --nomina cfisicas-2026

Necesita la clave de seudonimización (`clave_seudonimos` en
.streamlit/secrets.toml, o la variable de entorno CLAVE_SEUDONIMOS). La
clave la custodia el profesor/a responsable: con la misma clave, la misma
persona tiene el mismo id en todas las exportaciones y olas.

Escribe en data/exportaciones/<nomina>/:
    nodos.csv              una fila por persona de la nómina (haya respondido o no)
    aristas_<pregunta>.csv una por pregunta de nominación (desde, hacia)
    textos_abiertos.csv    respuestas de texto libre (revisar antes de compartir:
                           pueden contener nombres)
    tiempos.csv            segundos por página y persona
    codebook.csv           qué es cada columna y cómo se codifica
    resumen.txt            tasas de respuesta y advertencias
Ningún nombre real llega a estos archivos.
"""

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import instrumento  # noqa: E402
from motor import db, export, rosters, settings  # noqa: E402

CLAVE_AYUDA = (
    "Falta la clave de seudonimización. Define clave_seudonimos en .streamlit/secrets.toml "
    "o la variable de entorno CLAVE_SEUDONIMOS. Para crear una nueva (solo la primera vez; "
    "después se usa siempre la misma):\n"
    '    python -c "import secrets; print(secrets.token_hex(32))"'
)


def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nomina", required=True, help="nombre de la nómina (el ?nomina= del enlace)")
    parser.add_argument("--salida", type=Path, help="carpeta de salida (por defecto data/exportaciones/<nomina>)")
    parser.add_argument("--forzar", action="store_true", help="sobrescribir una exportación anterior")
    args = parser.parse_args()

    clave = settings.get_secret("clave_seudonimos")
    if not clave:
        sys.exit(CLAVE_AYUDA)
    key = clave.encode("utf-8")
    print(f"Huella de la clave: {export.key_fingerprint(key)}")

    try:
        roster = rosters.load_roster(args.nomina)
    except rosters.RosterError as e:
        sys.exit(f"ERROR: {e}")
    if roster is None:
        sys.exit(f"ERROR: no existe la nómina {args.nomina!r} en {settings.rosters_dir()}")

    out_dir = args.salida or settings.DATA_DIR / "exportaciones" / args.nomina
    if out_dir.exists() and any(out_dir.iterdir()) and not args.forzar:
        sys.exit(f"ERROR: {out_dir} ya tiene archivos. Usa --forzar para sobrescribir.")
    out_dir.mkdir(parents=True, exist_ok=True)

    questions = instrumento.PREGUNTAS
    self_id_q = next(q for q in questions if q["type"] == "self_id")
    roster_codes = {p.code for p in roster}
    ids = {p.code: export.pseudonym(key, p.code) for p in roster}
    if len(set(ids.values())) != len(ids):
        sys.exit("ERROR: colisión de seudónimos. Abortando.")

    conn = db.connect()
    respondents = db.get_respondents(conn, args.nomina)
    by_code, report = export.pick_respondents(respondents, roster_codes, self_id_q["id"])

    answer_columns = list(export.empty_answers(questions))
    node_fields = ["id", "cohorte", "estado", "version_instrumento", "tiempo_total_s", "paginas_rapidas"]
    node_fields += answer_columns
    nodes, times, texts = [], [], []
    edge_lists = {q["id"]: [] for q in questions if q["type"] == "roster_checklist"}
    unresolved = 0
    versions = Counter()

    for person in roster:
        r = by_code.get(person.code)
        row = {"id": ids[person.code], "cohorte": person.cohort}
        if r is None:
            row.update(estado="sin_respuesta", version_instrumento="", tiempo_total_s="", paginas_rapidas="")
            row.update(export.empty_answers(questions))
            nodes.append(row)
            continue

        data = json.loads(r["survey_data_json"] or "{}")
        page_times = db.get_answer_times(conn, r["id"])
        versions[r["instrument_version"]] += 1
        row.update(
            estado=export.STATUS_LABELS[r["status"]],
            version_instrumento=r["instrument_version"],
            tiempo_total_s=round(sum(t for t in page_times.values() if t), 1),
            paginas_rapidas=db.count_events(conn, r["id"], "fast_answer_flag"),
        )
        row.update(export.encode_answers(questions, data))
        nodes.append(row)

        person_edges, n_unresolved = export.edges(questions, data, person.code, roster_codes, key)
        unresolved += n_unresolved
        for qid, pairs in person_edges.items():
            edge_lists[qid].extend({"desde": a, "hacia": b} for a, b in pairs)

        for page, q in enumerate(questions, start=1):
            if q["id"] in page_times and page_times[q["id"]] is not None:
                times.append({"id": ids[person.code], "pagina": page, "pregunta": q["id"],
                              "segundos": round(page_times[q["id"]], 2)})
            if q["type"] == "text":
                text = data.get(q["id"], {}).get("value")
                if text:
                    texts.append({"id": ids[person.code], "pregunta": q["id"], "texto": text})

    nodes.sort(key=lambda row: row["id"])  # never in the roster's (alphabetical) order
    write_csv(out_dir / "nodos.csv", node_fields, nodes)
    for qid, rows in edge_lists.items():
        write_csv(out_dir / f"aristas_{qid}.csv", ["desde", "hacia"], rows)
    write_csv(out_dir / "textos_abiertos.csv", ["id", "pregunta", "texto"], texts)
    write_csv(out_dir / "tiempos.csv", ["id", "pagina", "pregunta", "segundos"], times)
    codebook = export.codebook(questions)
    write_csv(
        out_dir / "codebook.csv",
        ["columna", "archivo", "pagina", "pregunta", "tipo", "texto", "opciones", "constructo", "fuente", "invertido"],
        codebook,
    )

    status = Counter(row["estado"] for row in nodes)
    by_cohort = Counter((row["cohorte"], row["estado"]) for row in nodes)
    lines = [
        f"Nómina: {args.nomina} ({len(roster)} personas)",
        f"Huella de la clave: {export.key_fingerprint(key)}",
        f"Versiones del instrumento: {dict(versions) or '-'}",
        "",
        f"Completas:     {status['completa']}",
        f"Incompletas:   {status['incompleta']}",
        f"Sin respuesta: {status['sin_respuesta']}",
        f"Tasa de respuesta (completas / nómina): {status['completa'] / len(roster):.1%}",
        "",
        "Por cohorte:",
    ]
    for cohort in sorted({p.cohort for p in roster}):
        n = sum(1 for p in roster if p.cohort == cohort)
        done = by_cohort[(cohort, "completa")]
        lines.append(f"  {cohort or '(sin cohorte)'}: {done} de {n} completas ({done / n:.1%})")
    lines += [
        "",
        f"No aceptaron participar (anónimo, no son nodos): {report['rechazos']}",
        f"Aceptaron pero no eligieron su nombre: {report['sin_identificacion']}",
    ]
    if report["fuera_de_nomina"]:
        lines.append(f"ADVERTENCIA: {report['fuera_de_nomina']} respuesta(s) con un nombre que ya no está en la nómina")
    if report["duplicados"]:
        lines.append(f"ADVERTENCIA: {report['duplicados']} persona(s) con más de una respuesta (se usó una)")
    if unresolved:
        lines.append(f"ADVERTENCIA: {unresolved} nominación(es) a códigos que ya no están en la nómina (descartadas)")
    if texts:
        lines.append(f"Revisar textos_abiertos.csv antes de compartir ({len(texts)} respuesta(s) de texto libre).")
    (out_dir / "resumen.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n".join(lines))
    print(f"\nSalida -> {out_dir}")


if __name__ == "__main__":
    main()
