"""Testes do PRootService."""
from clinux.services.proot_service import PRootService

def test_service_init():
    service = PRootService()
    assert service is not None
