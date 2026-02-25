#!/bin/bash

# This script sets up the project from scratch

# Variables for the setup
PYTHON_VERSION="3.14"

echo ">>> setting up the project"

echo ">>> installing Python version $PYTHON_VERSION"
uv python install "$PYTHON_VERSION"

echo ">>> creating virtual environment"
# Remove existing virtual environment
rm -rf .venv
# Pin python version and create the virtual environment
uv python pin "$PYTHON_VERSION"
uv venv --python "$PYTHON_VERSION"

# Activate the virtual environment
./activate.sh

echo ">>> installing the dependencies"
uv pip install --overrides requirements.txt -r requirements.txt

# It can be the case that any installation step creates a uv.lock file
# We handle our dependencies using the pyproject.toml file and not uv.lock
echo ">>> removing uv lock files"
rm -f uv.lock

echo -e "✅ Setup erfolgreich abgeschlossen!"


SELECT * FROM gym_data LIMIT 1;