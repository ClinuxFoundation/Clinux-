"""Serviço PRoot."""
from ..adapters.proot_adapter import PRootAdapter

class PRootService:
    def __init__(self):
        self.adapter = PRootAdapter()
    
    def enter(self, rootfs):
        return self.adapter.start(rootfs)
    
    def setup_rootfs(self, tarball):
        return self.adapter.extract(tarball)
