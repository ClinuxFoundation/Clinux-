#!/usr/bin/env python3
"""Exemplo: Criar VM Ubuntu."""
import subprocess
import sys

# Adicionar clinux ao path
sys.path.insert(0, '..')

from clinux.core.storage_manager import StorageManager
from clinux.core.qemu_manager import QEMUManager

def main():
    storage = StorageManager()
    qemu = QEMUManager()
    
    iso = "ubuntu-22.04.iso"
    name = "ubuntu-example"
    
    print(f"Criando VM: {name}")
    storage.add_vm(name)
    
    print("Iniciando instalação...")
    qemu.install(iso)

if __name__ == "__main__":
    main()
