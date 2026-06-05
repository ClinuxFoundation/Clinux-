"""Interface de linha de comando principal."""

import argparse
import sys
from pathlib import Path

from .storage import Storage
from .qemu import QEMUManager
from .proot import PRootManager


def cmd_install(args):
    """Instala uma ISO Linux criando disco virtual automático."""
    qemu = QEMUManager()
    qemu.install(args.iso)


def cmd_run(args):
    """Inicia uma máquina virtual já instalada."""
    qemu = QEMUManager()
    qemu.run(args.name)


def cmd_proot(args):
    """Inicia ambiente Linux leve usando PRoot."""
    proot = PRootManager()
    proot.start(args.rootfs)


def cmd_list(args):
    """Lista VMs e rootfs disponíveis."""
    storage = Storage()
    
    vms = storage.list_vms()
    roots = storage.list_roots()
    
    if vms:
        print("\n📦 Máquinas Virtuais:")
        for vm in vms:
            print(f"  • {vm}")
    
    if roots:
        print("\n🌱 Ambientes PRoot:")
        for root in roots:
            print(f"  • {root}")
    
    if not vms and not roots:
        print("Nenhum ambiente encontrado.")


def cmd_delete(args):
    """Remove VM ou rootfs."""
    storage = Storage()
    
    # Tenta deletar como VM primeiro
    if storage.get_vm(args.name):
        storage.del_vm(args.name)
        print(f"✅ VM '{args.name}' removida.")
    # Tenta deletar como rootfs
    elif storage.get_root(args.name):
        storage.del_root(args.name)
        print(f"✅ Rootfs '{args.name}' removido.")
    else:
        print(f"❌ '{args.name}' não encontrado.")


def cmd_snapshot(args):
    """Salva ou restaura snapshot de uma VM."""
    qemu = QEMUManager()
    
    if args.action == "save":
        qemu.snapshot_save(args.name)
        print(f"✅ Snapshot salvo para '{args.name}'.")
    elif args.action == "load":
        qemu.snapshot_load(args.name)
        print(f"✅ Snapshot restaurado para '{args.name}'.")


def main():
    """Função principal da CLI."""
    parser = argparse.ArgumentParser(
        description="CLINUX - Gerenciador de ambientes Linux",
        usage="clinux <comando> [opções]"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")
    
    # install
    install_parser = subparsers.add_parser("install", help="Instalar ISO Linux")
    install_parser.add_argument("iso", help="Caminho para arquivo ISO")
    
    # run
    run_parser = subparsers.add_parser("run", help="Iniciar VM instalada")
    run_parser.add_argument("name", help="Nome da VM")
    
    # proot
    proot_parser = subparsers.add_parser("proot", help="Iniciar ambiente PRoot")
    proot_parser.add_argument("rootfs", help="Caminho para rootfs (tar.gz ou diretório)")
    
    # list
    subparsers.add_parser("list", help="Listar VMs e rootfs")
    
    # delete
    delete_parser = subparsers.add_parser("delete", help="Remover VM ou rootfs")
    delete_parser.add_argument("name", help="Nome do ambiente")
    
    # snapshot
    snap_parser = subparsers.add_parser("snapshot", help="Gerenciar snapshots")
    snap_parser.add_argument("action", choices=["save", "load"], help="Ação do snapshot")
    snap_parser.add_argument("name", help="Nome da VM")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Mapeia comandos para funções
    commands = {
        "install": cmd_install,
        "run": cmd_run,
        "proot": cmd_proot,
        "list": cmd_list,
        "delete": cmd_delete,
        "snapshot": cmd_snapshot,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()