"""Mock do QEMU para testes."""
class MockQEMU:
    def __init__(self):
        self.calls = []
    
    def run(self, *args, **kwargs):
        self.calls.append(("run", args, kwargs))
        return type("Result", (), {"returncode": 0})()
    
    def install(self, *args, **kwargs):
        self.calls.append(("install", args, kwargs))
        return type("Result", (), {"returncode": 0})()
    
    def snapshot_save(self, *args, **kwargs):
        self.calls.append(("snapshot_save", args, kwargs))
        return type("Result", (), {"returncode": 0})()
    
    def snapshot_load(self, *args, **kwargs):
        self.calls.append(("snapshot_load", args, kwargs))
        return type("Result", (), {"returncode": 0})()
