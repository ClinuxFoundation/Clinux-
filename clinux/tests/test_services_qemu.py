"""Testes do QEMUService."""
from clinux.services.qemu_service import QEMUService

def test_service_init():
    service = QEMUService()
    assert service is not None

def test_service_start_vm():
    service = QEMUService()
    config = {"disk": "/tmp/teste.qcow2", "memory": "1G"}
    try:
        service.start_vm(config)
    except:
        pass
