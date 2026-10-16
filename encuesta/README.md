# Encuesta (reemplazo del Google Forms)

Herramienta para aplicar la encuesta del proyecto a estudiantes de 1.º y 2.º
año de Ciencias Físicas: una página por pregunta, nominación de compañeros y
compañeras desde la nómina, escalas tipo Likert y exportación seudonimizada
para analizar las redes en R (`igraph`) o Python (`networkx`).

Es una versión limpia de `survey-app`, la herramienta que se desarrolló para
el proyecto Slep-net en colegios. Conserva su motor (persistencia, tiempos,
auditoría, retoma) y deja fuera todo lo escolar.

**Qué resuelve frente al Google Forms** (sección 1.2 del reporte del semestre):

| Problema del formulario | Aquí |
|---|---|
| La nominación permite elegir a una sola persona | Casillas: se puede marcar a varias (tope configurable, 15 por defecto) |
| Es obligatoria: quien no tiene a nadie debe inventar un lazo | Opción explícita «No hay nadie», que queda registrada como respuesta |
| No se sabe quién nomina | «¿Quién eres tú?»: cada nombre se puede elegir una sola vez |
| Una persona puede nominarse a sí misma | Su propio nombre desaparece de las listas |
| Los 76 nombres quedan en el HTML público | La nómina vive fuera de git; la app solo la muestra a quien tiene el enlace |
| No hay tiempos ni control de duplicados ni retoma | Tiempo por página, alerta de respuestas demasiado rápidas, enlace personal para retomar |

## 1. Instalación

Requiere Python 3.11 o superior. Desde la carpeta `encuesta/`:

```bash
python3 -m venv .venv
source .venv/bin/activate          # en Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

## 2. Probar la demo

```bash
python scripts/demo.py
```

Abre el navegador con la encuesta y una nómina **ficticia** de 76 nombres
(`ejemplos/ejemplo.csv`, dos cohortes). Respóndela entera, ciérrala a la
mitad y vuelve a abrir el mismo enlace (ahora con `?token=...`): retoma donde
quedó. Las respuestas de la demo quedan en `data/encuesta.db`.

## 3. Editar la encuesta

**Todo el contenido está en [`instrumento.py`](instrumento.py).** No hace
falta tocar nada más. `PREGUNTAS` es la lista de páginas, en orden. Cada
página se crea con una función de [`motor/preguntas.py`](motor/preguntas.py):

| Función | Para qué |
|---|---|
| `info(id, texto)` | Texto sin pregunta: bienvenida, instrucciones, cierre |
| `consentimiento(id, texto)` | Acepto / No acepto. «No acepto» termina la encuesta y borra lo respondido |
| `identificacion(id)` | «¿Quién eres tú?»: la persona elige su nombre de la nómina |
| `nominacion(id, texto, maximo=15)` | Casillas con la nómina, por cohorte y con buscador, más «No hay nadie» |
| `opcion_unica(id, texto, opciones)` | Una pregunta, una respuesta |
| `bloque(id, texto, items, opciones)` | Varias afirmaciones con la misma escala en una página (escalas validadas) |
| `numero(id, texto, minimo=0, maximo=None)` | Un número entero; `maximo="nomina"` usa el tamaño de la nómina |
| `abierta(id, texto)` | Texto libre (opcional) |
| `arbol(id, raiz, nodos)` | Preguntas encadenadas: «¿Trabajas?» → si dice Sí, «¿Cuántas horas?» |

Ejemplo de una escala validada como bloque:

```python
ESA = bloque(
    "esa",
    "Indica tu grado de acuerdo con cada afirmación sobre tu carrera.",
    items=[
        ("esa_01", "<texto del ítem 1, copiado del artículo de validación>"),
        ("esa_02", "<texto del ítem 2>"),
    ],
    opciones=ACUERDO_5,
    constructo="Satisfacción académica (ESA)",
    fuente="Lent et al. (2007); Vergara-Morales et al. (2018)",
    invertidos=[],
)
```

y agregar `ESA` a `PREGUNTAS` donde corresponda. `constructo`, `fuente` e
`invertidos` no cambian lo que ve quien responde, pero van al codebook de la
exportación.

**Reglas** (también al inicio de `instrumento.py`):

- Las escalas validadas se copian textuales del artículo de validación, con su
  formato de respuesta. Los ítems nuevos se marcan con `fuente=NUEVO` y pasan
  por jueces y entrevistas cognitivas.
- Cada `id` termina siendo el nombre de una columna: corto, en minúsculas, sin
  tildes ni espacios, y no se cambia una vez aplicada la encuesta.
- Subir `VERSION` cada vez que cambie algo que ve quien responde (queda
  guardada con cada respuesta).
- «Prefiero no contestar» **no** se pone entre las opciones: la app lo ofrece
  sola cuando alguien intenta avanzar sin responder, y lo registra como omisión.

Con la demo abierta, los cambios en `instrumento.py` aparecen al guardar el
archivo. Para revisar que el instrumento esté bien armado:

```bash
pytest                                       # incluye la validación del instrumento
python scripts/instrumento_a_md.py > instrumento.md   # documento para jueces y CEBB
```

## 4. La nómina

Un CSV por nómina, por ejemplo `cfisicas-2026.csv`:

```csv
N,NOMBRE,COHORTE
1,Antonia Araya Soto,Ingreso 2025
2,Benjamín Contreras Díaz,Ingreso 2026
```

- `N`: código estable de cada persona. Las nominaciones se guardan por código y
  los seudónimos se calculan desde él. **Debe ser el mismo en la ola 2** para
  que la misma persona tenga el mismo id.
- `NOMBRE`: lo que se ve en pantalla.
- `COHORTE` (opcional): agrupa las listas.

Sirve el CSV que exporta Excel (con `,` o `;`). La nómina tiene nombres reales,
así que **nunca va dentro del repositorio**: va en `data/nominas/` (excluida
de git) o en una carpeta fuera del repo, indicada con `directorio_nominas` en
`.streamlit/secrets.toml` (ver `secrets.toml.example`).

El enlace para responder es la URL de la app más `?nomina=cfisicas-2026`. Si
alguien pide salir del estudio después, se borra su fila de la nómina: sus
respuestas y los lazos hacia esa persona quedan fuera de la exportación.

Antes de la sesión, decidir con el reporte (§2.6) quién entra a la nómina
(frontera de la red).

## 5. Aplicar la encuesta

En el computador que sirve la encuesta (con `.streamlit/secrets.toml` listo):

```bash
scripts/servir_publico.sh
```

Levanta la app y un túnel de Cloudflare con HTTPS (requiere
`brew install cloudflared`) e imprime una URL pública temporal: se le agrega
`?nomina=...` y se comparte en la sala. Al terminar, `Ctrl+C` cierra todo y la
URL deja de existir. Conviene probar antes que la red de la UdeC no bloquee el
túnel.

Durante el período de aplicación:

```bash
python scripts/respaldar.py              # copia de seguridad (programarla cada hora)
python scripts/verificar_integridad.py   # confirma que nadie alteró la base
```

Si dos personas eligen el mismo nombre, la segunda ve un aviso y no puede
seguir. Si fue un error real (alguien eligió el nombre equivocado y cerró la
pestaña), se libera así, solo si esa respuesta **no** está completa:

```bash
sqlite3 data/encuesta.db "select n.self_code, r.status, r.created_at from name_claims n
  join respondents r on r.id = n.respondent_id where n.nomina='cfisicas-2026' and n.self_code='38';"
sqlite3 data/encuesta.db "delete from name_claims where nomina='cfisicas-2026' and self_code='38';"
```

## 6. Exportar y analizar

```bash
python scripts/exportar.py --nomina cfisicas-2026
```

Necesita la clave de seudonimización (`clave_seudonimos`), que custodia el
profesor/a responsable. Escribe en `data/exportaciones/cfisicas-2026/`:

| Archivo | Contenido |
|---|---|
| `nodos.csv` | Una fila por persona de la nómina, haya respondido o no: id seudónimo, cohorte, estado, tiempos y una columna por pregunta o ítem |
| `aristas_<pregunta>.csv` | Una por generador de nombres: `desde`, `hacia` (red dirigida) |
| `codebook.csv` | Qué es cada columna, sus opciones codificadas (1, 2, …), constructo, fuente e ítems invertidos |
| `tiempos.csv` | Segundos por página y persona |
| `textos_abiertos.csv` | Respuestas de texto libre (**revisar antes de compartir**: pueden traer nombres) |
| `resumen.txt` | Tasa de respuesta por cohorte, rechazos y advertencias |

Los datos faltantes nunca quedan como celda vacía:

| Valor | Significa |
|---|---|
| `SIN_RESPUESTA` | No llegó a esa pregunta, o no respondió la encuesta |
| `OMITIDA` | Eligió «Prefiero no contestar» |
| `NO_APLICA` | Pregunta encadenada que no le correspondía (p. ej. horas de trabajo si no trabaja) |
| `<id>_n = 0` | Marcó «No hay nadie»: es una respuesta (aislamiento), no un faltante |

En R:

```r
library(igraph)
faltantes <- c("SIN_RESPUESTA", "OMITIDA", "NO_APLICA")
nodos   <- read.csv("data/exportaciones/cfisicas-2026/nodos.csv", na.strings = faltantes)
aristas <- read.csv("data/exportaciones/cfisicas-2026/aristas_g1_afinidad.csv")
g1 <- graph_from_data_frame(aristas, directed = TRUE, vertices = nodos)
```

(Si interesa distinguir los tipos de faltante, leer sin `na.strings`.)

Quienes no respondieron siguen siendo nodos: pueden haber sido nominados. No
excluir a los nodos aislados (reporte, §4).

## 7. Qué se guarda y qué no

- La base (`data/encuesta.db`, SQLite) guarda las respuestas por **código** de
  la nómina, nunca por nombre. Los enlaces de retoma y las IP solo se guardan
  como hash (las IP, solo para limitar intentos masivos).
- Un registro de auditoría encadenado por hash anota cada evento (entrar a una
  página, elegir un nombre, omitir, terminar). `verificar_integridad.py`
  detecta cualquier edición posterior de la base.
- Quien no acepta participar queda registrado solo como "no aceptó" (sin
  nombre, porque el consentimiento va antes de la identificación). Quien vuelve
  atrás y retira el consentimiento pierde todas sus respuestas guardadas.
- Un enlace completado queda de solo lectura.
- `data/` y `.streamlit/secrets.toml` están en `.gitignore`. Nunca subirlos.

## 8. Estructura

```
encuesta/
├── instrumento.py        ← la encuesta (lo único que se edita)
├── app.py                la app de Streamlit
├── motor/                persistencia, nóminas, flujo, seguridad, exportación
├── scripts/              demo, servir, respaldar, verificar, exportar, instrumento_a_md
├── ejemplos/ejemplo.csv  nómina ficticia para la demo
├── tests/                pruebas (pytest), incluida la app de punta a punta
└── data/                 base, nóminas reales y exportaciones (fuera de git)
```

Las pruebas cubren el motor y recorren la app completa sin navegador
(`streamlit.testing`): consentimiento y rechazo, omisión, «No hay nadie», tope
de nominaciones, buscador, retoma, nombre ya elegido y la exportación.
