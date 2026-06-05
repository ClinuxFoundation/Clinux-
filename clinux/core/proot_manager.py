"""Gerenciador PRoot - Simples e direto."""
import subprocess
import sys
import tarfile
from pathlib import Path
from .base_manager import BaseManager
from .storage_manager import StorageManager


class PRootManager(BaseManager):
    """Gerencia ambientes Linux leves usando PRoot."""
    
    def __init__(self):
        self.storage = StorageManager()
    
    def check_dependencies(self):
        """Verifica se PRoot está instalado."""
        try:
            subprocess.run(
                ["proot", "--version"],
                capture_output=True,
                check=False
            )
        except FileNotFoundError:
            print("❌ ERRO: PRoot não está instalado!")
            print("   Termux: pkg install proot")
            print("   Linux: sudo apt install proot")
            sys.exit(1)
    
    def validate(self, target):
        """Valida se o rootfs existe."""
        return Path(target).exists()
    
    def _extract_rootfs(self, archive_path, dest_dir):
        """Extrai rootfs ignorando dispositivos."""
        print(f"📦 Extraindo rootfs para {dest_dir}...")
        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        with tarfile.open(archive_path) as tar:
            for member in tar.getmembers():
                # Pula dispositivos
                if member.isdev():
                    continue
                try:
                    tar.extract(member, dest_dir)
                except (PermissionError, OSError):
                    pass
        
        # Cria diretórios essenciais
        for d in ["dev", "proc", "sys", "tmp"]:
            (dest_dir / d).mkdir(exist_ok=True)
        
        print("✅ Extração concluída!")
    
    def _find_shell(self, target):
        """Encontra shell disponível."""
        for sh in ["/bin/bash", "/bin/zsh", "/bin/ash", "/bin/sh"]:
            if (Path(target) / sh.lstrip("/")).exists():
                return sh
        return "/bin/sh"
    
    def start(self, rootfs_path):
        """Inicia ambiente PRoot."""
        self.check_dependencies()
        
        rootfs_path = Path(rootfs_path)
        if not rootfs_path.exists():
            print(f"❌ Rootfs não encontrado: {rootfs_path}")
            sys.exit(1)
        
        # Nome baseado no arquivo
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
        
        # Encontra shell
        shell = self._find_shell(target)
        
        # Comando proot simples
        cmd = [
            "proot",
            "-r", str(target),
            "-b", "/dev:/dev",
            "-b", "/proc:/proc",
            "-b", "/sys:/sys",
            "-w", "/",
            shell
        ]
        
        print(f"🌱 Iniciando ambiente PRoot '{name}'...")
        print(f"   Shell: {shell}")
        print(f"   Digite 'exit' para sair\n")
        
        subprocess.run(cmd, check=False)
