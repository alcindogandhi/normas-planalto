#!/bin/sh

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
cd "$SCRIPTPATH" || exit 1

rm -fr build
mkdir build
python3 src/main.py
sh src/xml_to_epub.sh
