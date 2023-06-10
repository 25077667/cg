# A powershell script to build python to exe with nuitka on Windows

# Set options for nuitka on powershell

OPTIONS="--standalone --onefile"
SRC="main.py"
OUT="cg.exe"

function build_nuitka() {
    poetry run python -m nuitka $OPTIONS $SRC -o $OUT
}
