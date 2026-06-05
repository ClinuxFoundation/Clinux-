"""Interface de linha de comando principal."""
import argparse
import sys
from .core.storage_manager import StorageManager
from .core.qemu_manager import QEMUManager
from .core.proot_manager import PRootManager

def main():
    parser = argparse.ArgumentParser(description="CLINUX")
    sub = parser.add_subparsers(dest="cmd")
    
    sub.add_parser("install").add_argument("iso")
    sub.add_parser("run").add_argument("name")
    sub.add_parser("proot").add_argument("rootfs")
    sub.add_parser("list")
    sub.add_parser("delete").add_argument("name")
    snap = sub.add_parser("snapshot")
    snap.add_argument("action", choices=["save","load"])
    snap.add_argument("name")
    
    args = parser.parse_args()
    
    storage = StorageManager()
    qemu = QEMUManager()
    proot = PRootManager()
    
    if args.cmd == "install":
        qemu.install(args.iso)
    elif args.cmd == "run":
        qemu.run(args.name)
    elif args.cmd == "proot":
        proot.start(args.rootfs)
    elif args.cmd == "list":
        print("VMs:", storage.list_vms())
        print("Rootfs:", storage.list_roots())
    elif args.cmd == "delete":
        storage.delete(args.name)
    elif args.cmd == "snapshot":
        if args.action == "save":
            qemu.snapshot_save(args.name)
        else:
            qemu.snapshot_load(args.name)