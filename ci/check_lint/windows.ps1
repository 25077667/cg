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
    Write-Output "Temporarily disabled pylint"
}

# A function Check lint for Windows
function main() {
    check_lint
}

main