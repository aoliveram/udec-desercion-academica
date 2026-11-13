# Abandono académico en Ciencias Físicas (UdeC)

📖 **Libro de clases de psicometría básica:** <https://aoliveram.github.io/udec-desercion-academica/>

Proyecto de tesis sobre abandono académico en la carrera de Ciencias Físicas
de la Universidad de Concepción (FCFM), trabajado como curso guiado entre
octubre y diciembre de 2026. Combina redes de estudiantes (afinidad, ayuda
académica, estudio conjunto) con escalas psicológicas validadas, siguiendo el
modelo de integración de Tinto.

## Contenido

| Carpeta o archivo | Qué es |
|---|---|
| [`encuesta/`](encuesta/) | Herramienta para aplicar la encuesta, en reemplazo del Google Forms. Empezar por [`encuesta/README.md`](encuesta/README.md) |
| [`libro-psicometria-2026/`](libro-psicometria-2026/) | Libro de clases de psicometría básica: constructos, redacción de ítems, ítems invertidos y alfa de Cronbach (fuente Quarto) |
| [`docs/`](docs/) | Documentos del proyecto |
| [`docs/reporte-general.pdf`](docs/reporte-general.pdf) ([md](docs/reporte-general.md)) | **Reporte general:** el proyecto, el mapa de constructos (los que entran y los que no) y una ficha de cada uno |
| [`docs/reporte-yannely-2026.pdf`](docs/reporte-yannely-2026.pdf) ([md](docs/reporte-yannely-2026.md)) | Encuesta FCFM 2026: constructos candidatos, ejemplo completo (UCLA-3) y calendario |
| [`docs/programa-curso-2026.pdf`](docs/programa-curso-2026.pdf) | Programa del curso guiado: horario de reuniones e hitos |
| `informe-yannely-abandono-academico-udec.pdf` | Informe de agosto de 2026: problema, hipótesis, marco teórico y metodología |
| [`comite-etica/`](comite-etica/) | Presentación al Comité de Ética de la CFM: protocolo, cartas, plantillas de la VRID y lista de lo que falta |
| [`papers/`](papers/) | Lecturas de referencia |

## Ejecutar la app

Desde la raíz del repositorio (`E - udec-desercion-academica`), con la `.venv`
de `E - survey-app` (ver [`encuesta/README.md`](encuesta/README.md)):

```bash
"../E - survey-app/.venv/bin/python" encuesta/scripts/demo.py
```

Con una `.venv` propia (pasos de abajo): `python encuesta/scripts/demo.py`.

## Primeros pasos

```bash
git clone https://github.com/aoliveram/udec-desercion-academica.git
cd udec-desercion-academica/encuesta
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/demo.py       # abre la encuesta con una nómina ficticia
```

La encuesta se diseña editando un solo archivo, `encuesta/instrumento.py`.

## Libro de clases

El libro está en `libro-psicometria-2026/` y se publica en
[GitHub Pages](https://aoliveram.github.io/udec-desercion-academica/) desde la
rama `gh-pages`. Para publicarlo de nuevo después de editar un capítulo
(requiere [Quarto](https://quarto.org) y R con el paquete `psych`):

```bash
cd libro-psicometria-2026
quarto publish gh-pages
```

Para solo verlo en local, `quarto preview libro-psicometria-2026`.

## Datos

Ningún dato con nombres reales entra a este repositorio: las nóminas, la base
de respuestas y las exportaciones viven en `encuesta/data/` (excluida de git)
o fuera del repo. La clave de seudonimización y demás secretos van en
`encuesta/.streamlit/secrets.toml`, también excluido.
