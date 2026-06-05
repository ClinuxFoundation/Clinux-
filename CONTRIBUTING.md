# Contribuindo com CLINUX

## Setup de desenvolvimento

```bash
git clone https://github.com/clinux/clinux
cd clinux
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
pre-commit install
```

Rodando testes

```bash
make test
```

Estilo de código

Usamos Black para formatação e Flake8 para linting.

```bash
make format
make lint
```

Enviando PR

1. Fork o repositório
2. Crie uma branch (git checkout -b feature/incrivel)
3. Commit suas mudanças (git commit -m 'Add: feature incrível')
4. Push para a branch (git push origin feature/incrivel)
5. Abra um Pull Request
