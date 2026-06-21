#!/bin/bash
set -euo pipefail

MVP_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$MVP_DIR/.venv"

cd "$MVP_DIR"

PYTHON_BIN="${AML_PYTHON:-}"

if [ -z "$PYTHON_BIN" ]; then
    for candidate in "$VENV_DIR/bin/python" "$(command -v python3)" "/opt/anaconda3/bin/python"; do
        if [ -x "$candidate" ] && "$candidate" -c "import streamlit, pandas, sklearn, xgboost, shap" 2>/dev/null; then
            PYTHON_BIN="$candidate"
            break
        fi
    done
fi

if [ -z "$PYTHON_BIN" ]; then
    echo "Creating local Python environment..."
    python3 -m venv "$VENV_DIR"
    echo "Installing project dependencies..."
    "$VENV_DIR/bin/python" -m pip install -r requirements.txt
    PYTHON_BIN="$VENV_DIR/bin/python"
fi

echo "Starting AML Detection System..."
echo "Using Python: $PYTHON_BIN"
echo "Open http://localhost:8501 if the browser does not open automatically."
exec "$PYTHON_BIN" -m streamlit run app1.1.py "$@"
