"""Adaptador de armazenamento."""
import json
from pathlib import Path

class StorageAdapter:
    def __init__(self, base):
        self.base = Path(base)
    
    def read_json(self, path):
        with open(self.base / path) as f:
            return json.load(f)
    
    def write_json(self, path, data):
        with open(self.base / path, "w") as f:
            json.dump(data, f)
    
    def exists(self, path):
        return (self.base / path).exists()
    
    def list_dir(self, path):
        return list((self.base / path).iterdir())
