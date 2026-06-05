"""Gerenciador PRoot com fallback QEMU para Termux."""
import subprocess
import sys
import tarfile
import shutil
from pathlib import Path
from .base_manager import BaseManager
from .storage_manager import StorageManager


class PRootManager(BaseManager):
    def __init__(self):
        self.storage = StorageManager()
        self.is_termux = Path("/data/data/com.termux/files").exists()
    
    def check_dependencies(self):
        if not shutil.which("proot"):
            print("❌ Instale proot:")
            print("   Termux: pkg install proot")
            print("   Linux: sudo apt install proot")
            sys.exit(1)
    
    def validate(self, target):
        return Path(target).exists()
    
    def _extract_rootfs(self, archive_path, dest_dir):
        print(f"📦 Extraindo rootfs...")
        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        with tarfile.open(archive_path) as tar:
            for member in tar.getmembers():
                if member.isdev():
                    continue
                try:
                    tar.extract(member, dest_dir)
                except:
                    pass
        
        for d in ["dev", "proc", "sys", "tmp"]:
            (dest_dir / d).mkdir(exist_ok=True)
        
        print("✅ Extração concluída!")
    
    def _find_shell(self, target):
        for sh in ["/bin/bash", "/bin/zsh", "/bin/ash", "/bin/sh"]:
            if (Path(target) / sh.lstrip("/")).exists():
                return sh
        return "/bin/sh"
    
    def _find_qemu(self, target):
        """Detecta se precisa de QEMU e qual binário usar."""
        # Verifica arquitetura do binário
        shell = self._find_shell(target)
        shell_path = Path(target) / shell.lstrip("/")
        
        try:
            result = subprocess.run(
                ["file", str(shell_path)], capture_output=True, text=True
            )
            
            if "ARM aarch64" in result.stdout:
                host = subprocess.run(
                    ["uname", "-m"], capture_output=True, text=True
                )
                if "aarch64" not in host.stdout:
                    # Host não é ARM64, precisa de QEMU
                    if shutil.which("qemu-aarch64"):
                        return "qemu-aarch64"
            elif "Intel 80386" in result.stdout:
                if shutil.which("qemu-i386"):
                    return "qemu-i386"
            elif "x86-64" in result.stdout:
                if shutil.which("qemu-x86_64"):
                    return "qemu-x86_64"
        except:
            pass
        
        return None
    
    def start(self, rootfs_path):
        self.check_dependencies()
        
        rootfs_path = Path(rootfs_path)
        if not rootfs_path.exists():
            print(f"❌ Rootfs não encontrado: {rootfs_path}")
            sys.exit(1)
        
        name = rootfs_path.stem.replace(".tar", "")
        
        # Extrai se for tarball
        if str(rootfs_path).endswith((".tar.gz", ".tgz", ".tar")):
            dest = self.storage.roots / name
            if not dest.exists() or not any(dest.iterdir()):
                self._extract_rootfs(rootfs_path, dest)
            target = dest
        else:
            target = rootfs_path
        
        # Registra
        if not self.storage.get_root(name):
            self.storage.add_root(name, target)
        
        shell = self._find_shell(target)
        qemu = self._find_qemu(target)
        
        # Monta comando
        cmd = ["proot", "-r", str(target)]
        
        # Adiciona QEMU se necessário
        if qemu:
            print(f"🔄 Usando {qemu} para tradução de binários...")
            cmd.extend(["-q", qemu])
        
        cmd.extend([
            "-b", "/dev:/dev",
            "-b", "/proc:/proc",
            "-b", "/sys:/sys",
            "-w", "/",
            shell
        ])
        
        print(f"🌱 Iniciando ambiente PRoot '{name}'...")
        print(f"   Shell: {shell}")
        print(f"   Digite 'exit' para sair\n")
        
        subprocess.run(cmd, check=False)
