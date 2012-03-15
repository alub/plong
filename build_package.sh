#!/bin/sh

OUT_DIR=3d_printing

cd `dirname $0`

set -e

cd setup_doc
make empty
make

cd ../userDocumentation
make empty
make

cd ..

rm -r											"$OUT_DIR"
mkdir											"$OUT_DIR"
cp setup_doc/setup_doc.pdf						"$OUT_DIR/install.pdf"
cp userDocumentation/userDoc.pdf				"$OUT_DIR/documentation.pdf"

cp startup.blend								"$OUT_DIR"
mkdir -p 										"$OUT_DIR/scripts/modules"
cp scripts/modules/*.py							"$OUT_DIR/scripts/modules"
mkdir -p										"$OUT_DIR/scripts/startup"
cp scripts/startup/printing_preprocessing.py	"$OUT_DIR/scripts/startup"

tar czvf "$OUT_DIR.tar.gz" "$OUT_DIR"