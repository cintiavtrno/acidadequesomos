#!/bin/sh
# Reconstrói tudo na ordem certa e atualiza o index.html. Rodar de qualquer pasta: sh tools/build_all.sh
cd "$(dirname "$0")" || exit 1
set -e
python3 build_html.py && python3 build_casa_html.py && python3 build_rua_html.py && python3 build_quintal_html.py && python3 build_mundo_html.py
echo "index.html atualizado: $(ls -l ../index.html | awk '{print $5}') bytes"
