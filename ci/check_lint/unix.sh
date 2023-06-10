#!/bin/bash

set -e
# Pylint threshold
LINT_THRESHOLD=9.5

# find all python files, but not .venv files
python_files=$(find . -type f -name "*.py" -not -path "./.venv/*")

# run pylint
echo "$python_files" | xargs poetry run python -m pylint --output-format=parseable --reports=no >pylint.out

# check pylint score
# Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00) ...
# Sed command to extract the score
score=$(sed -n 's/^Your code has been rated at \([0-9.]*\)\/.*/\1/p' pylint.out)

if (($(echo "$score < $LINT_THRESHOLD" | bc -l))); then
    echo "Pylint score is $score, which is below the threshold of $LINT_THRESHOLD"
    exit 1
else
    echo "Pylint score is $score, which is above the threshold of $LINT_THRESHOLD"
fi
