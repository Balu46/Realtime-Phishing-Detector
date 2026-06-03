#!/bin/bash
# Skrypt uruchamiający trening modelu

cd "$(dirname "$0")"

# Activate the venv from the parent directory if you want, or just call it directly:
../.venv/bin/python src/train.py "$@"
