#!/bin/bash

set -e
# Pylint threshold
LINT_THRESHOLD=9.5

# find all python files
python_files=$(find . -name "*.py" | tr '\n' ' ') 

# run pylint
poetry run python -m pylint --output-format=parseable --reports=no $python_files > pylint.out || true

# check pylint score
score=$(grep -oP '(?<=^Your\ code\ has\ been\ rated\ at\ )[0-9\.]+' pylint.out)

if (( $(echo "$score < $LINT_THRESHOLD" | bc -l) )); then
    echo "Pylint score is $score, which is below the threshold of $LINT_THRESHOLD"
    exit 1
else
    echo "Pylint score is $score, which is above the threshold of $LINT_THRESHOLD"
fi