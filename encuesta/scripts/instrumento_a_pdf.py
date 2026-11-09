#!/usr/bin/env python3
"""Dibuja la encuesta como PDF, una pantalla por página, tal como la ve quien responde.

Sale directo de instrumento.py (mismos textos, opciones, botones y barra de
progreso que la app), así que basta volver a correrlo cuando cambie el
instrumento. Las listas de nombres son ficticias (ejemplos/ejemplo.csv).

Uso (desde la carpeta encuesta/; requiere XeLaTeX y la fuente Helvetica Neue):
    python scripts/instrumento_a_pdf.py                  # escribe ../instrumento/preguntas-encuesta.pdf
    python scripts/instrumento_a_pdf.py -o otra.pdf
    python scripts/instrumento_a_pdf.py --tex x.tex      # solo el .tex, sin compilar
"""

import argparse
import csv
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

import instrumento  # noqa: E402
from motor.preguntas import OMIT, validar  # noqa: E402

DEFAULT_PDF = HERE.parent / "instrumento" / "preguntas-encuesta.pdf"
EXAMPLE_ROSTER = HERE / "ejemplos" / "ejemplo.csv"
NAMES_PER_COHORT = 6  # cuántos nombres ficticios mostrar por cohorte

PREAMBLE = r"""
\documentclass[11pt]{article}
\usepackage[a4paper,margin=2cm]{geometry}
\usepackage{fontspec}
\setmainfont{Helvetica Neue}
\usepackage[spanish,es-noshorthands]{babel}
\usepackage{xcolor,tikz,tcolorbox,enumitem,multicol,longtable,array}
\tcbuselibrary{skins,breakable}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
\setlist{itemsep=1pt,topsep=2pt}

% Paleta de Streamlit (tema claro)
\definecolor{stText}{HTML}{31333F}
\definecolor{stMuted}{HTML}{808495}
\definecolor{stBorder}{HTML}{D6D6D8}
\definecolor{stBorderDis}{HTML}{E6E6E8}
\definecolor{stPrimary}{HTML}{FF4B4B}
\definecolor{stBlue}{HTML}{1C83E1}
\definecolor{stTrack}{HTML}{E6EAF1}
\definecolor{stField}{HTML}{F0F2F6}
\definecolor{stSuccessBg}{HTML}{DFFDE6}
\definecolor{stSuccessFg}{HTML}{177233}
\color{stText}

\newcommand{\apptitle}[1]{{\fontsize{24}{28}\selectfont\bfseries #1}\par\vspace{6pt}}
\newcommand{\stcaption}[1]{{\small\color{stMuted}#1}\par\vspace{4pt}}
\newcommand{\qlabel}[1]{{#1}\par\vspace{2pt}}
\newcommand{\qlabelbf}[1]{{\bfseries #1}\par\vspace{2pt}}
\newcommand{\radiocircle}{\tikz[baseline=-0.6ex]\draw[stBorder,line width=0.8pt,fill=white] (0,0) circle (0.16);}
\newcommand{\radio}[1]{\radiocircle\hspace{5pt}#1\par\vspace{2pt}}
% Opción de una fila horizontal: no se corta entre el círculo y su texto
\newcommand{\hradio}[1]{\mbox{\radiocircle\hspace{4pt}{\small #1}}\hspace{12pt plus 4pt}\allowbreak}
\newcommand{\radiofilled}{\tikz[baseline=-0.6ex]{\draw[stPrimary,line width=0.8pt,fill=white] (0,0) circle (0.16);\fill[stPrimary] (0,0) circle (0.08);}}
\newcommand{\hradiofilled}[1]{\mbox{\radiofilled\hspace{4pt}{\small #1}}\hspace{12pt plus 4pt}\allowbreak}
\newcommand{\checkbox}[1]{%
  \tikz[baseline=-0.6ex]\draw[stBorder,line width=0.8pt,fill=white,rounded corners=1.5pt] (-0.16,-0.16) rectangle (0.16,0.16);\hspace{5pt}{\small #1}\par\vspace{3pt}}
\newcommand{\field}[2]{% texto de ejemplo, adorno a la derecha
  \begin{tcolorbox}[enhanced,colback=stField,colframe=stField,boxrule=0pt,arc=4pt,left=8pt,right=8pt,top=6pt,bottom=6pt,width=\linewidth]
    {\color{stMuted}#1}\hfill{\color{stText}#2}
  \end{tcolorbox}\vspace{-6pt}}
\newcommand{\textareabox}{%
  \begin{tcolorbox}[enhanced,colback=stField,colframe=stField,boxrule=0pt,arc=4pt,height=60pt,width=\linewidth]
  \end{tcolorbox}\vspace{-6pt}}
\newcommand{\navbtn}[3]{%
  \ifnum#2=1 \colorlet{btnframe}{stBorder}\colorlet{btntext}{stText}%
  \else \colorlet{btnframe}{stBorderDis}\colorlet{btntext}{stMuted}\fi
  \begin{tcolorbox}[enhanced,colback=white,colframe=btnframe,boxrule=0.8pt,arc=5pt,
     width=#3,halign=center,valign=center,height=30pt,left=0pt,right=0pt,top=0pt,bottom=0pt,nobeforeafter]
    \color{btntext}#1
  \end{tcolorbox}}
\newcommand{\navrow}[4]{% texto anterior, activo, texto siguiente, activo
  \vspace{10pt}\par\noindent
  \navbtn{$\leftarrow$\ #1}{#2}{0.485\linewidth}\hfill\navbtn{#3\ $\rightarrow$}{#4}{0.485\linewidth}\par}
\newcommand{\tooltip}[1]{\par\vspace{2pt}\hfill{\footnotesize\color{stMuted}\textit{(al pasar el cursor: ``#1'')}}\par}
\newcommand{\omitprompt}[2]{% aviso, texto del botón
  \vspace{6pt}\par\noindent
  \begin{tcolorbox}[enhanced,colback=white,colframe=stBorder,boxrule=0.6pt,arc=5pt,left=10pt,right=10pt,top=8pt,bottom=8pt,width=\linewidth]
    #1\par\vspace{6pt}
    \tcbox[on line,colback=stPrimary,colframe=stPrimary,boxrule=0pt,arc=4pt,left=8pt,right=8pt,top=4pt,bottom=4pt]{\color{white}#2}
  \end{tcolorbox}\vspace{-6pt}}
\newcommand{\nextitem}{\vspace{6pt}{\color{stBorderDis}\rule{\linewidth}{0.4pt}}\par\vspace{4pt}}
\newcommand{\progress}[1]{%
  \par\noindent
  \begin{tikzpicture}
    \fill[stTrack,rounded corners=2pt] (0,0) rectangle (\linewidth,0.16);
    \fill[stBlue,rounded corners=2pt] (0,0) rectangle (#1\linewidth,0.16);
  \end{tikzpicture}\par\vspace{2pt}}
\newtcolorbox{screen}{enhanced,breakable,colback=white,colframe=stBorder,boxrule=0.6pt,arc=6pt,
  left=22pt,right=22pt,top=18pt,bottom=18pt,width=\linewidth}
\newcommand{\screenhead}[1]{\vspace*{-6pt}{\footnotesize\color{stMuted}#1}\par\vspace{4pt}}
\newcommand{\note}[1]{\par\vspace{6pt}{\footnotesize\color{stMuted}\textit{#1}}\par}
\newcommand{\meta}[1]{\par\vspace{6pt}{\footnotesize\color{stMuted}#1}\par}
"""

TYPE_NAMES = {
    "info": "texto",
    "consent": "consentimiento",
    "self_id": "identificación",
    "roster_checklist": "nominación",
    "radio": "opción única",
    "likert_block": "bloque de ítems",
    "number": "número",
    "text": "texto libre",
    "branching_tree": "preguntas encadenadas",
}

_SPECIAL = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "→": r"$\rightarrow$",
}


def esc(text):
    return "".join(_SPECIAL.get(ch, ch) for ch in str(text))


def inline(text):
    """Escapa y convierte el **negrita** y *cursiva* del Markdown de la app."""
    out = esc(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", out)
    out = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\\emph{\1}", out)
    return out


def markdown(text):
    """El Markdown simple que usan los textos del instrumento: párrafos y viñetas."""
    blocks = []
    for para in text.split("\n\n"):
        lines = para.split("\n")
        if all(line.startswith("- ") for line in lines):
            items = "\n".join(rf"\item {inline(line[2:])}" for line in lines)
            blocks.append(r"\begin{itemize}[leftmargin=14pt]" + "\n" + items + "\n" + r"\end{itemize}")
        else:
            blocks.append(inline(" ".join(lines)))
    return "\\par\\vspace{6pt}\n".join(blocks) + r"\par\vspace{2pt}"


def fake_roster():
    """Algunos nombres ficticios por cohorte, en el orden de la app. El primero es quien responde."""
    with open(EXAMPLE_ROSTER, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    by_cohort = {}
    for row in rows:
        by_cohort.setdefault(row["COHORTE"], []).append(row["NOMBRE"])
    return {c: sorted(names)[:NAMES_PER_COHORT] for c, names in sorted(by_cohort.items())}


class Doc:
    def __init__(self, questions):
        self.questions = questions
        self.total = len(questions)
        self.roster = fake_roster()
        first_cohort = next(iter(self.roster))
        self.self_name = self.roster[first_cohort][0]
        self.shown_radio_omit = False
        self.shown_block_omit = False

    # --- piezas comunes ---------------------------------------------------

    def head(self, n, q):
        return "\n".join(
            [
                r"\begin{screen}",
                rf"\screenhead{{Pantalla {n} de {self.total} \quad·\quad id: \texttt{{{esc(q['id'])}}} "
                rf"\quad·\quad {TYPE_NAMES[q['type']]}}}",
                rf"\apptitle{{{esc(instrumento.TITULO)}}}",
                rf"\progress{{{n / self.total:.3f}}}",
                rf"\stcaption{{Página {n} de {self.total}}}",
            ]
        )

    def foot(self, n, q, *, next_active=True, tooltip=None):
        is_last = n == self.total
        if is_last:
            next_label = "Enviar"
        elif n == 1 and q["type"] == "info":
            next_label = "Comenzar"
        else:
            next_label = "Siguiente"
        lines = [rf"\navrow{{Anterior}}{{{0 if n == 1 else 1}}}{{{next_label}}}{{{1 if next_active else 0}}}"]
        if tooltip:
            lines.append(rf"\tooltip{{{esc(tooltip)}}}")
        lines.append(r"\end{screen}")
        meta = [m for m in (q.get("construct"), q.get("source")) if m]
        if meta:
            lines.append(rf"\meta{{{esc(' · '.join(meta))}}}")
        lines.append(r"\newpage")
        return "\n".join(lines)

    # --- un dibujo por tipo de página ---------------------------------------

    def info(self, q):
        return markdown(q["label"])

    def consent(self, q):
        radios = "\n".join(rf"\radio{{{esc(o)}}}" for o in q["options"])
        return (
            markdown(q["label"])
            + "\n\\vspace{4pt}\n\\qlabel{Tu decisión}\n"
            + radios
            + rf"\note{{Si se marca «{esc(q['decline'])}», el botón de avanzar dice \emph{{Terminar}}: "
            r"la encuesta se cierra y se borra lo que se haya respondido.}"
        )

    def self_id(self, q):
        names = [f"{name} · {cohort}" for cohort, people in self.roster.items() for name in people]
        listing = "\n".join(rf"{esc(n)}\par" for n in names)
        return (
            rf"\qlabel{{{inline(q['label'])}}}"
            + "\n"
            + r"\field{Busca tu nombre...}{$\vee$}"
            + r"\note{Al desplegar aparece la nómina completa, ordenada por cohorte y nombre; se puede "
            r"escribir para filtrar. Cada nombre se puede elegir una sola vez. Por ejemplo:}"
            + "\n\\begin{multicols}{2}\\footnotesize\n"
            + listing
            + "\n\\end{multicols}"
        )

    def roster_checklist(self, q):
        parts = [
            rf"\qlabelbf{{{inline(q['label'])}}}",
            rf"\stcaption{{No hay un número correcto. Puedes marcar hasta {q['max_selections']}; llevas 0.}}",
            r"\field{Buscar por nombre}{}",
            r"\vspace{6pt}",
        ]
        for cohort, people in self.roster.items():
            others = [p for p in people if p != self.self_name]
            parts.append(rf"\qlabelbf{{{esc(cohort)}}}")
            parts.append(
                r"\begin{multicols}{3}\raggedcolumns\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000"
            )
            parts.extend(rf"\checkbox{{{esc(p)}}}" for p in others)
            parts.append(r"\end{multicols}")
        parts.append(r"{\color{stBorderDis}\rule{\linewidth}{0.4pt}}\par\vspace{4pt}")
        parts.append(rf"\checkbox{{{esc(q['nobody_label'])}}}")
        parts.append(
            rf"\note{{Al llegar a {q['max_selections']} marcados, las casillas restantes se desactivan. "
            rf"«{esc(q['nobody_label'])}» se desactiva si hay alguien marcado. La lista real tiene a toda "
            r"la nómina, menos a quien responde.}"
        )
        return "\n".join(parts)

    def radio(self, q):
        parts = [rf"\qlabelbf{{{inline(q['label'])}}}"]
        parts.extend(rf"\radio{{{esc(o)}}}" for o in q["options"])
        if not self.shown_radio_omit:
            self.shown_radio_omit = True
            parts.append(rf"\omitprompt{{No has seleccionado una respuesta.}}{{{esc(OMIT)}}}")
            parts.append(
                r"\note{El recuadro aparece solo si se aprieta \emph{Siguiente} sin haber respondido; "
                r"igual en todas las preguntas de una sola respuesta.}"
            )
        return "\n".join(parts)

    def likert_block(self, q):
        parts = [rf"\qlabelbf{{{inline(q['label'])}}}", r"\vspace{2pt}"]
        example = not self.shown_block_omit  # el primer bloque muestra el aviso de omisión
        for i, item in enumerate(q["items"], start=1):
            if i > 1:
                parts.append(r"\nextitem")
            parts.append(rf"\qlabel{{{i}. {inline(item['label'])}}}")
            # En el ejemplo, la primera afirmación aparece respondida (primera opción).
            options = "".join(
                rf"\hradiofilled{{{esc(o)}}}" if example and i == 1 and j == 0 else rf"\hradio{{{esc(o)}}}"
                for j, o in enumerate(q["options"])
            )
            parts.append(r"{\raggedright " + options + r"\par}")
        if example:
            self.shown_block_omit = True
            n = len(q["items"])
            parts.append(
                rf"\omitprompt{{Te falta responder {n - 1} de {n} afirmaciones.}}"
                r"{Prefiero no contestar las que faltan}"
            )
            parts.append(
                r"\note{Ejemplo con una sola afirmación respondida. El recuadro aparece solo si se aprieta "
                r"\emph{Siguiente} con afirmaciones sin responder; quedan como «Prefiero no contestar» "
                r"solo las que faltan. En el celular, las opciones de cada afirmación se ven una debajo de otra.}"
            )
        return "\n".join(parts)

    def number(self, q):
        if q["max_value"] == "nomina":
            rango = "Va desde 0 hasta el tamaño de la nómina, menos quien responde."
        elif q["max_value"] is not None:
            rango = f"Va desde {q['min_value']} hasta {q['max_value']}."
        else:
            rango = f"Desde {q['min_value']}, sin tope."
        stepper = (
            r"\tcbox[on line,colback=white,colframe=stBorder,boxrule=0.6pt,arc=3pt,size=small,left=6pt,right=6pt]{$-$}\,"
            r"\tcbox[on line,colback=white,colframe=stBorder,boxrule=0.6pt,arc=3pt,size=small,left=6pt,right=6pt]{$+$}"
        )
        return (
            rf"\qlabelbf{{{inline(q['label'])}}}"
            + "\n"
            + rf"\field{{Escribe un número}}{{{stepper}}}"
            + rf"\note{{{esc(rango)} Se puede escribir o usar los botones + y -.}}"
        )

    def text(self, q):
        return rf"\qlabelbf{{{inline(q['label'])}}}" + "\n" + r"\textareabox"

    def branching_tree(self, q):
        parts = [
            r"\note{Preguntas encadenadas: se ve una; al responderla aparece debajo la que corresponde, "
            r"y las anteriores quedan visibles. Aquí se muestran todas.}",
            r"\vspace{4pt}",
        ]
        for node_id, node in q["tree"].items():
            parts.append(rf"{{\footnotesize\color{{stMuted}}Nodo \texttt{{{esc(node_id)}}}}}\par")
            parts.append(rf"\qlabel{{{inline(node['label'])}}}")
            for option in node["options"]:
                nxt = node["branches"].get(option)
                arrow = (
                    rf"\ {{\footnotesize\color{{stMuted}}$\rightarrow$ sigue con \texttt{{{esc(nxt)}}}}}"
                    if nxt
                    else ""
                )
                parts.append(rf"\radio{{{esc(option)}{arrow}}}")
            parts.append(r"\vspace{6pt}")
        return "\n".join(parts)

    # --- documento ----------------------------------------------------------

    def screen(self, n, q):
        body = getattr(self, q["type"])(q)
        if q["type"] == "consent":
            return "\n".join(
                [self.head(n, q), body, self.foot(n, q, next_active=False, tooltip="Debes indicar si aceptas participar para continuar.")]
            )
        if q["type"] == "self_id":
            return "\n".join(
                [self.head(n, q), body, self.foot(n, q, next_active=False, tooltip="Debes seleccionar tu nombre para continuar.")]
            )
        return "\n".join([self.head(n, q), body, self.foot(n, q)])

    def contents(self):
        rows = []
        for n, q in enumerate(self.questions, start=1):
            what = q.get("construct") or TYPE_NAMES[q["type"]]
            if q["type"] == "likert_block":
                what += f" ({len(q['items'])} ítems)"
            rows.append(rf"{n} & \texttt{{{esc(q['id'])}}} & {esc(what)} \\")
        return (
            r"{\small\begin{longtable}{@{}r>{\raggedright}p{5.6cm}>{\raggedright\arraybackslash}p{9.0cm}@{}}"
            "\n"
            r"\textbf{Pantalla} & \textbf{id} & \textbf{Qué es} \\ \hline" + "\n" + "\n".join(rows) + "\n"
            r"\end{longtable}}"
        )

    def intro(self):
        n_items = sum(len(q["items"]) if q["type"] == "likert_block" else 1 for q in self.questions if q["type"] != "info")
        cohorts = " y ".join(self.roster)
        return rf"""
\vspace*{{1.5cm}}
{{\fontsize{{22}}{{26}}\selectfont\bfseries {esc(instrumento.TITULO)}}}\par\vspace{{6pt}}
{{\large\color{{stMuted}} Las pantallas tal como las ve un estudiante}}\par
\vspace{{2pt}}{{\small\color{{stMuted}} Versión {esc(instrumento.VERSION)} del instrumento}}\par
\vspace{{0.8cm}}

Cada página de este documento reproduce una pantalla de la aplicación, en el mismo orden y con los
mismos textos, opciones y botones que ve quien responde. Se responde una pantalla, se avanza, y recién
ahí aparece la siguiente. Debajo de cada pantalla, en gris, va el constructo y la fuente (eso no lo ve
quien responde).

\textbf{{Los nombres son ficticios.}} Sirven solo para mostrar cómo se ven las preguntas que listan
a la nómina; aquí van {NAMES_PER_COHORT} por cohorte ({esc(cohorts)}). En la aplicación real la lista
tiene a toda la nómina, agrupada por cohorte y con buscador. Quien responde en este ejemplo,
{esc(self.self_name)}, se identifica en su pantalla y por eso no aparece en las listas de nominación.

Ninguna opción viene marcada de antemano. Si se aprieta \emph{{Siguiente}} sin responder, la pantalla
no avanza: aparece un aviso con un botón rojo para omitir, que registra la omisión como
«{esc(OMIT)}» (se ilustra una vez para una pregunta de opción única y una vez para un bloque de
ítems). El consentimiento y la identificación no se pueden omitir.

Total: \textbf{{{self.total} pantallas}} y {n_items} preguntas o ítems, más la pantalla final de
agradecimiento.

\vspace{{0.4cm}}
{self.contents()}
\newpage
"""

    def final(self):
        return r"""
\begin{screen}
\screenhead{Pantalla final \quad·\quad tras pulsar \emph{Enviar}}
\apptitle{""" + esc(instrumento.TITULO) + r"""}
\begin{tcolorbox}[enhanced,colback=stSuccessBg,colframe=stSuccessBg,boxrule=0pt,arc=4pt,left=10pt,right=10pt,top=8pt,bottom=8pt,width=\linewidth]
  {\color{stSuccessFg}¡Gracias! Tus respuestas ya quedaron guardadas.}
\end{tcolorbox}
\note{El enlace personal queda en solo lectura: si se vuelve a abrir, muestra esta misma pantalla.}
\end{screen}
"""

    def latex(self):
        screens = "\n".join(self.screen(n, q) for n, q in enumerate(self.questions, start=1))
        return PREAMBLE + "\n\\begin{document}\n" + self.intro() + screens + self.final() + "\n\\end{document}\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_PDF, help="PDF de salida")
    parser.add_argument("--tex", type=Path, help="escribir solo el .tex en esta ruta, sin compilar")
    args = parser.parse_args()

    problemas = validar(instrumento.PREGUNTAS)
    if problemas:
        sys.exit("El instrumento tiene problemas:\n" + "\n".join(f"- {p}" for p in problemas))

    tex = Doc(instrumento.PREGUNTAS).latex()
    if args.tex:
        args.tex.write_text(tex, encoding="utf-8")
        return

    if shutil.which("xelatex") is None:
        sys.exit("No se encontró xelatex. Instala TeX (p. ej. MacTeX) o usa --tex para obtener solo el .tex.")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "preguntas-encuesta.tex"
        src.write_text(tex, encoding="utf-8")
        for _ in range(2):  # dos pasadas para la tabla larga
            result = subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-halt-on-error", src.name],
                cwd=tmp,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                sys.exit("xelatex falló:\n" + result.stdout[-3000:])
        args.output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(Path(tmp) / "preguntas-encuesta.pdf", args.output)
    print(f"Escrito {args.output}")


if __name__ == "__main__":
    main()
