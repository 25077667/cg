#!/bin/bash

set -e

OPTIONS="--standalone --onefile"
OUTPUT_POSTFIX=""
NAME="cg"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OUTPUT_POSTFIX=".elf"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OPTIONS="$OPTIONS"
    OUTPUT_POSTFIX=".macho"
fi

OUTPUT_NAME="$NAME$OUTPUT_POSTFIX"

poetry run python -m nuitka $OPTIONS main.py -o $OUTPUT_NAME
