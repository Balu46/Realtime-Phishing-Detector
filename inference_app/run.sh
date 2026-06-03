#!/bin/bash

# Upewnij się, że używamy środowiska wirtualnego
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Ustawienie ścieżki Pythona, żeby widział pliki w folderze src
export PYTHONPATH=src

# Domyślne odpalanie z urlscan, jeśli nie podano innych argumentów
if [ $# -eq 0 ]; then
    echo "Uruchamianie z domyślnym źródłem (URLScan) ze względu na awarię publicznego CertStreamu..."
    ../.venv/bin/python src/main.py --urlscan
else
    # Jeśli użytkownik podał własne argumenty (np. --mock)
    ../.venv/bin/python src/main.py "$@"
fi
