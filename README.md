# Abandono académico en Ciencias Físicas (UdeC)

Proyecto de tesis sobre abandono académico en la carrera de Ciencias Físicas
de la Universidad de Concepción (FCFM), trabajado como curso guiado entre
octubre y diciembre de 2026. Combina redes de estudiantes (afinidad, ayuda
académica, estudio conjunto) con escalas psicológicas validadas, siguiendo el
modelo de integración de Tinto.

## Contenido

| Carpeta o archivo | Qué es |
|---|---|
| [`encuesta/`](encuesta/) | Herramienta para aplicar la encuesta, en reemplazo del Google Forms. Empezar por [`encuesta/README.md`](encuesta/README.md) |
| `informe-yannely-abandono-academico-udec.pdf` | Informe de agosto de 2026: problema, hipótesis, marco teórico y metodología |
| [`papers/`](papers/) | Lecturas de referencia |
| `Notas.txt` | Notas y tareas de trabajo |

## Primeros pasos

```bash
git clone https://github.com/aoliveram/udec-desercion-academica.git
cd udec-desercion-academica/encuesta
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/demo.py       # abre la encuesta con una nómina ficticia
```

La encuesta se diseña editando un solo archivo, `encuesta/instrumento.py`.

## Datos

Ningún dato con nombres reales entra a este repositorio: las nóminas, la base
de respuestas y las exportaciones viven en `encuesta/data/` (excluida de git)
o fuera del repo. La clave de seudonimización y demás secretos van en
`encuesta/.streamlit/secrets.toml`, también excluido.
