"""Modelo de snapshot."""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Snapshot:
    name: str
    vm_name: str
    created: datetime = None
    size: str = "0"
