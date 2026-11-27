#!/bin/sh
# Genera el .docx y el .pdf de cada documento de esta carpeta.
# Uso, desde comite-etica/:  ./generar.sh
set -e
cd "$(dirname "$0")"
for f in 01-carta-solicitud 02-protocolo 03-carta-autorizacion-facultad; do
  pandoc "$f.md" -o "$f.docx"
  pandoc "$f.md" -o "$f.pdf" --pdf-engine=xelatex
  echo "Escrito $f.docx y $f.pdf"
done
