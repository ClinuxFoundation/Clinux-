"""Testes do comando list."""
from clinux.commands.list import execute

def test_list_empty(storage):
    class Args:
        pass
    execute(Args())
