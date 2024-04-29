#!/bin/bash

set +e # Continue execution even if a command fails

# Pylint threshold
LINT_THRESHOLD=9.5

# find all python files, but not .venv files
python_files=$(find . -type f -name "*.py" -not -path "./.venv/*")

# run pylint and capture both stdout and stderr
echo "$python_files" | xargs poetry run python -m pylint --output-format=parseable --reports=no >pylint.out 2>&1

# Output pylint results
cat pylint.out

# Check pylint score
# Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00) ...
# Sed command to extract the score
score=$(sed -n 's/^Your code has been rated at \([0-9.]*\)\/.*/\1/p' pylint.out)

# Compare score with threshold using bc for floating point comparison
if (($(echo "$score < $LINT_THRESHOLD" | bc -l))); then
    echo "Pylint score is $score, which is below the threshold of $LINT_THRESHOLD"
    exit 1 # Uncomment this line to fail the build if the score is below the threshold
else
    echo "Pylint score is $score, which is above the threshold of $LINT_THRESHOLD"
fi
