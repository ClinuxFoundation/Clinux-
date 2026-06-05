"""Serviço QEMU."""
from ..adapters.qemu_adapter import QEMUAdapter

class QEMUService:
    def __init__(self):
        self.adapter = QEMUAdapter()
    
    def start_vm(self, config):
        return self.adapter.run(config)
    
    def stop_vm(self, name):
        return self.adapter.stop(name)
    
    def status(self, name):
        return self.adapter.status(name)
