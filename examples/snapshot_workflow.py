#!/usr/bin/env python3
"""Exemplo: Fluxo de trabalho com snapshots."""
import sys
sys.path.insert(0, '..')

from clinux.core.snapshot_manager import SnapshotManager

def main():
    snap = SnapshotManager()
    vm_name = "ubuntu-example"
    
    print(f"Salvando snapshot da VM: {vm_name}")
    snap.save(vm_name)
    
    print("Snapshot salvo! Use 'clinux snapshot load' para restaurar.")
    print(f"Snapshots disponíveis:")
    print(snap.list_snapshots(vm_name))

if __name__ == "__main__":
    main()
