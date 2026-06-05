#!/bin/bash
# Executar todos os testes

echo "Executando testes..."
pytest tests/ -v --cov=clinux --cov-report=html

echo "✅ Testes concluídos!"
