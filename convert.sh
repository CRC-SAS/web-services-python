#!/usr/bin/env bash

rm -rf apidoc_files

jupyter nbconvert --to markdown apidoc.ipynb

sed -zi "s/\(\`\`\`\)\(\n[a-z#%]\)/\1 python\2/g" apidoc.md
sed -i "s/^\(usuario_default = '\).*\('\)/\1********\2/g" apidoc.md
sed -i "s/^\(clave_default   = '\).*\('\)/\1********\2/g" apidoc.md
sed -i "s/^\(    |\)/|/g" apidoc.md

mv apidoc.md README.md
