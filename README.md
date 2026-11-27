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
| [`libro-psicometria-2026/`](libro-psicometria-2026/) | Libro de clases de psicometría básica: constructos, redacción de ítems, ítems invertidos, alfa de Cronbach y análisis factorial (fuente Quarto) |
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
(requiere [Quarto](https://quarto.org) y R con los paquetes `psych`, `GPArotation`, `lavaan`, `semTools`, `qgraph` y `EGAnet`):

```bash
cd libro-psicometria-2026
quarto publish gh-pages
```

Para solo verlo en local, `quarto preview libro-psicometria-2026`.

## Pendientes (27 de noviembre de 2026)

**Comité de ética (Fase I, CFM).** Se envían `comite-etica/02-protocolo-investigacion.docx` y la carta de compromiso (`comite-etica/plantillas-vrid/`). Después, la Decanatura envía la carta al comité de la UdeC (Fase II).

- Aplicar al protocolo y a la carta a la Facultad (`.docx`):
  - hasta dos olas por semestre, desde 2027-I;
  - datos identificables hasta 4 años desde la primera encuesta;
  - «asignaturas inscritas» y las evaluaciones docentes (agregadas, docentes codificados);
  - la nómina la entregan las jefaturas de carrera después de la aprobación;
  - DEGyD y Bienestar Estudiantil en el procedimiento ante malestar.
- Completar en el protocolo: equipo donde se guardan los datos y quién lo administra, matrícula de la CFM en 2026, tipo de proyecto y financiamiento, y el nombre de quien preside el comité de la CFM.
- CV de los cuatro integrantes (solicitados), carta de compromiso firmada por Hernán y autorización de la Decanatura.
- `comite-etica/README.md` y `generar.sh` todavía apuntan a los `.md` antiguos: actualizarlos o borrarlos.

**Encuesta.**

- Teléfono de Bienestar Estudiantil en la pantalla final (Yannely). También va en el consentimiento.
- Contacto de la DISE en el consentimiento.
- Confirmar los teléfonos de la DEGyD en degyd.udec.cl.
- Lista de inscritos: se pide a cada jefatura de carrera, después de la aprobación de los comités.

**Documentos.**

- `docs/reporte-general.md` y `instrumento/decisiones.md` todavía dicen «tres olas (2026-II, 2027-I, 2027-II)».
- Libro de psicometría: volver a publicar el sitio desde `main` (`cd libro-psicometria-2026 && quarto publish gh-pages`).

## Datos

Ningún dato con nombres reales entra a este repositorio: las nóminas, la base
de respuestas y las exportaciones viven en `encuesta/data/` (excluida de git)
o fuera del repo. La clave de seudonimización y demás secretos van en
`encuesta/.streamlit/secrets.toml`, también excluido.
