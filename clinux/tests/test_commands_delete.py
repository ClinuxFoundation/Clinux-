"""Testes do comando delete."""
from clinux.commands.delete import execute

def test_delete_unknown(storage):
    class Args:
        name = "inexistente"
    execute(Args())
