"""Serviço de templates."""
import json
from pathlib import Path

class TemplateService:
    def __init__(self):
        self.base = Path(__file__).parent.parent / "templates"
    
    def load_qemu_template(self, name):
        path = self.base / "qemu" / f"{name}.json"
        return json.load(open(path)) if path.exists() else {}
    
    def load_proot_template(self, name):
        path = self.base / "proot" / f"{name}.json"
        return json.load(open(path)) if path.exists() else {}
