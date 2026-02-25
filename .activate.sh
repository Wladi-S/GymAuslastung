#!/bin/bash

# This script activates the virtual environment

echo ">>> activate virtual environment"
# Activate the virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source .venv/Scripts/activate
else
    # MacOS or Linux
    source .venv/bin/activate
fi