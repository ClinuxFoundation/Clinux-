"""Mock do PRoot para testes."""
class MockPRoot:
    def __init__(self):
        self.calls = []
    
    def start(self, *args, **kwargs):
        self.calls.append(("start", args, kwargs))
        return type("Result", (), {"returncode": 0})()
    
    def extract(self, *args, **kwargs):
        self.calls.append(("extract", args, kwargs))
        return "/tmp/extracted"
