#!/bin/bash

set -e

OPTIONS="--standalone --onefile"
OUTPUT_POSTFIX=""
NAME="cg"

ARCH=$(uname -m)

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OUTPUT_POSTFIX=".elf"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OPTIONS="$OPTIONS"
    OUTPUT_POSTFIX=".macho"
fi

OUTPUT_NAME="$NAME-$ARCH$OUTPUT_POSTFIX"

poetry run python -m nuitka $OPTIONS main.py -o $OUTPUT_NAME
