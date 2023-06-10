# Check lint for Windows

# A function Collect all python files into a list
function collect_python_files() {
    # Collect all python files into a list in powershell
    $python_files = Get-ChildItem -Path . -Recurse -Include *.py

    return $python_files
}

# A function Check lint for Windows
function check_lint() {
    # Check lint for Windows
    $python_files = collect_python_files
    $threshold = 9.5

    # Invoke the pylint command for each python file
    foreach ($file in $python_files) {
        $pylint_result = poetry run python -m pylint $file
        $pylint_score = $pylint_result[-1].Split(" ")[-1]
        $pylint_score = $pylint_score.Replace("(", "")
        $pylint_score = $pylint_score.Replace(")", "")

        if ($pylint_score -lt $threshold) {
            echo "Pylint score is lower than threshold: $pylint_score"
            exit 1
        }
    }
}

# A function Check lint for Windows
function main() {
    check_lint
}

main