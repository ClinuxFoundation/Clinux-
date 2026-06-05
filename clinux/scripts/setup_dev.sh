#!/bin/bash
# Setup do ambiente de desenvolvimento

python -m venv venv
source venv/bin/activate
pip install -e .
pip install pytest black flake8 mypy
pre-commit install

echo "✅ Ambiente dev configurado!"
