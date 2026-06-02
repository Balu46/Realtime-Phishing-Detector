#!/bin/bash

echo "======================================"
echo " Uruchamianie Testów Jednostkowych"
echo "======================================"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Aktywowanie środowiska wirtualnego..."
    source .venv/bin/activate
fi

# Check if pytest is installed, if not, use unittest module
export PYTHONPATH=src
if command -v pytest &> /dev/null; then
    echo "Uruchamianie przez pytest..."
    pytest tests/ -v
else
    echo "Uruchamianie przez wbudowany moduł unittest..."
    python -m unittest discover -s tests -v
fi

echo "======================================"
echo " Testy zakończone."
echo "======================================"
