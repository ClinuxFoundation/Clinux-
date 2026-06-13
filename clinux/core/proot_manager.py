"""Gerenciador PRoot - Suporte completo para Android e PC."""
import subprocess
import sys
import tarfile
import shutil
from pathlib import Path
from .base_manager import BaseManager
from .storage_manager import StorageManager
from clinux.adapters.proot_adapter import PRootAdapter


class PRootManager(BaseManager):
    def __init__(self):
        self.storage = StorageManager()
        self.adapter = PRootAdapter()
        self.is_termux = Path("/data/data/com.termux/files").exists()
        self.is_android = Path("/system/build.prop").exists()
    
    def check_dependencies(self):
        """Verifica dependências do PRoot."""
        if not shutil.which("proot"):
            print("❌ Instale proot:")
            if self.is_termux:
                print("   Termux: pkg install proot")
            else:
                print("   Linux: sudo apt install proot")
            sys.exit(1)
    
    def validate(self, target):
        """Valida se o alvo existe e é um rootfs válido."""
        target_path = Path(target)
        if not target_path.exists():
            return False
        
        # Verifica se tem estrutura mínima de rootfs
        bin_dir = target_path / "bin"
        etc_dir = target_path / "etc"
        return bin_dir.exists() and etc_dir.exists()
    
    def _extract_rootfs(self, archive_path, dest_dir):
        """Extrai rootfs usando o adapter."""
        print(f"📦 Extraindo rootfs...")
        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with tarfile.open(archive_path) as tar:
                for member in tar.getmembers():
                    if member.isdev():
                        continue
                    try:
                        tar.extract(member, dest_dir)
                    except Exception as e:
                        print(f"⚠️  Erro ao extrair {member.name}: {e}")
            
            # Cria diretórios essenciais com permissões corretas
            essential_dirs = {
                "dev": 0o755,
                "proc": 0o555,
                "sys": 0o555,
                "tmp": 0o1777,
                "home": 0o755,
                "root": 0o700,
                "run": 0o755,
            }
            
            for d, perms in essential_dirs.items():
                dir_path = dest_dir / d
                dir_path.mkdir(exist_ok=True)
                try:
                    dir_path.chmod(perms)
                except OSError as e:
                    if d in ["proc", "sys"]:
                        print(f"ℹ️  Permissões especiais para {d} não aplicáveis: {e}")
                    else:
                        print(f"⚠️  Não foi possível definir permissões para {d}: {e}")
            
            # Valida binários críticos após extração
            if not self._validate_shell_available(dest_dir):
                print("⚠️  Aviso: Nenhum shell encontrado no rootfs")
            
            print("✅ Extração concluída!")
        except Exception as e:
            print(f"❌ Erro na extração: {e}")
            raise
    
    def _validate_shell_available(self, rootfs_path):
        """Valida se pelo menos um shell está disponível."""
        shells = ["/bin/bash", "/bin/zsh", "/bin/ash", "/bin/sh"]
        for sh in shells:
            shell_path = rootfs_path / sh.lstrip("/")
            # Check if path exists (handles both regular files and symlinks)
            if shell_path.exists() or shell_path.is_symlink():
                return True
        return False
    
    def _find_shell(self, target):
        """Encontra shell disponível no rootfs."""
        shells = ["/bin/bash", "/bin/zsh", "/bin/ash", "/bin/sh"]
        target_path = Path(target)
        
        for sh in shells:
            shell_path = target_path / sh.lstrip("/")
            # Check if path exists (handles both regular files and symlinks)
            if shell_path.exists() or shell_path.is_symlink():
                return sh
        
        # Se nenhum shell foi encontrado, tenta alternativas
        bin_dir = target_path / "bin"
        if bin_dir.exists():
            # Procura por qualquer arquivo executável que pareça um shell
            try:
                for item in bin_dir.iterdir():
                    if item.is_file() or item.is_symlink():
                        # Verifica se é um shell comum
                        if item.name in ["sh", "bash", "zsh", "ash", "busybox"]:
                            return f"/bin/{item.name}"
            except Exception:
                pass
            
            # Se encontrou busybox, usa como fallback
            busybox_path = bin_dir / "busybox"
            if busybox_path.exists() or busybox_path.is_symlink():
                return "/bin/busybox"
        
        # Se nenhum shell foi encontrado, isso é um erro crítico
        bin_contents = []  # Inicializa a variável aqui
        print(f"❌ Erro crítico: Nenhum shell foi encontrado no rootfs")
        print(f"   Shells procurados: {', '.join(shells)}")
        print(f"   Rootfs path: {target}")
        
        if bin_dir.exists():
            try:
                bin_contents = list(bin_dir.glob('*'))
            except Exception:
                bin_contents = ["<erro ao listar diretório>"]
        print(f"   Conteúdo do diretório bin: {bin_contents}")
        raise FileNotFoundError(f"Nenhum shell disponível em {target}")
    
    def start(self, rootfs_path):
        """Inicia ambiente PRoot.
        
        Args:
            rootfs_path: Caminho para o rootfs (arquivo tar ou diretório)
        """
        self.check_dependencies()
        
        rootfs_path = Path(rootfs_path)
        if not rootfs_path.exists():
            print(f"❌ Rootfs não encontrado: {rootfs_path}")
            sys.exit(1)
        
        name = rootfs_path.stem.replace(".tar", "")
        
        # Extrai se for arquivo tar
        if str(rootfs_path).endswith((".tar.gz", ".tgz", ".tar")):
            dest = self.storage.roots / name
            if not dest.exists() or not any(dest.iterdir()):
                self._extract_rootfs(rootfs_path, dest)
            target = dest
        else:
            target = rootfs_path
        
        # Valida o target antes de prosseguir
        if not self.validate(target):
            print(f"❌ Rootfs inválido: estrutura mínima não encontrada")
            sys.exit(1)
        
        # Registra no storage
        if not self.storage.get_root(name):
            self.storage.add_root(name, target)
        
        # Encontra shell (levanta exceção se não encontrado)
        try:
            shell = self._find_shell(target)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            sys.exit(1)
        
        # Inicia com o adapter
        print(f"🌱 Iniciando ambiente PRoot '{name}'...")
        print(f"   Shell: {shell}")
        print(f"   Plataforma: {'Termux/Android' if self.is_termux else 'Linux'}")
        print(f"   Digite 'exit' para sair\n")
        
        try:
            self.adapter.start(str(target), shell=shell)
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
        except Exception as e:
            print(f"❌ Erro: {e}")
            sys.exit(1)
    
    def run_command(self, rootfs_path, command):
        """Executa comando dentro do PRoot.
        
        Args:
            rootfs_path: Caminho para o rootfs
            command: Comando a executar (string ou lista)
        
        Returns:
            Código de retorno
        """
        self.check_dependencies()
        
        rootfs_path = Path(rootfs_path)
        if not rootfs_path.exists():
            print(f"❌ Rootfs não encontrado: {rootfs_path}")
            return 1
        
        # Valida o rootfs antes de executar
        if not self.validate(rootfs_path):
            print(f"❌ Rootfs inválido: estrutura mínima não encontrada")
            return 1
        
        try:
            result = self.adapter.run_command(str(rootfs_path), command)
            return result.returncode
        except Exception as e:
            print(f"❌ Erro ao executar comando: {e}")
            return 1
    
    def extract_rootfs(self, archive_path, dest_dir):
        """Extrai rootfs manualmente.
        
        Args:
            archive_path: Caminho do arquivo tar
            dest_dir: Diretório de destino
        
        Returns:
            Caminho do diretório extraído
        """
        # Usa o método interno em vez de depender do adapter
        self._extract_rootfs(archive_path, dest_dir)
        return dest_dir                for item in bin_dir.iterdir():
                    if item.is_file() or item.is_symlink():
                        # Verifica se é um shell comum
                        if item.name in ["sh", "bash", "zsh", "ash", "busybox"]:
                            return f"/bin/{item.name}"
                        possible_shells.append(item.name)
            except Exception:
                pass
            
            # Se encontrou busybox, usa como fallback
            busybox_path = bin_dir / "busybox"
            if busybox_path.exists() or busybox_path.is_symlink():
                return "/bin/busybox"
        
        # Se nenhum shell foi encontrado, isso é um erro crítico
        print(f"❌ Erro crítico: Nenhum shell foi encontrado no rootfs")
        print(f"   Shells procurados: {', '.join(shells)}")
        print(f"   Rootfs path: {target}")
        bin_contents = []
        if bin_dir.exists():
            try:
                bin_contents = list(bin_dir.glob('*'))
            except Exception:
                bin_contents = ["<erro ao listar diretório>"]
        print(f"   Conteúdo do diretório bin: {bin_contents}")
        raise FileNotFoundError(f"Nenhum shell disponível em {target}")
    
    def start(self, rootfs_path):
        """Inicia ambiente PRoot.
        
        Args:
            rootfs_path: Caminho para o rootfs (arquivo tar ou diretório)
        """
        self.check_dependencies()
        
        rootfs_path = Path(rootfs_path)
        if not rootfs_path.exists():
            print(f"❌ Rootfs não encontrado: {rootfs_path}")
            sys.exit(1)
        
        name = rootfs_path.stem.replace(".tar", "")
        
        # Extrai se for arquivo tar
        if str(rootfs_path).endswith((".tar.gz", ".tgz", ".tar")):
            dest = self.storage.roots / name
            if not dest.exists() or not any(dest.iterdir()):
                self._extract_rootfs(rootfs_path, dest)
            target = dest
        else:
            target = rootfs_path
        
        # Registra no storage
        if not self.storage.get_root(name):
            self.storage.add_root(name, target)
        
        # Encontra shell (levanta exceção se não encontrado)
        try:
            shell = self._find_shell(target)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            sys.exit(1)
        
        # Inicia com o adapter
        print(f"🌱 Iniciando ambiente PRoot '{name}'...")
        print(f"   Shell: {shell}")
        print(f"   Plataforma: {'Termux/Android' if self.is_termux else 'Linux'}")
        print(f"   Digite 'exit' para sair\n")
        
        try:
            self.adapter.start(str(target), shell=shell)
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
        except Exception as e:
            print(f"❌ Erro: {e}")
            sys.exit(1)
    
    def run_command(self, rootfs_path, command):
        """Executa comando dentro do PRoot.
        
        Args:
            rootfs_path: Caminho para o rootfs
            command: Comando a executar (string ou lista)
        
        Returns:
            Código de retorno
        """
        self.check_dependencies()
        
        rootfs_path = Path(rootfs_path)
        if not rootfs_path.exists():
            print(f"❌ Rootfs não encontrado: {rootfs_path}")
            return 1
        
        try:
            result = self.adapter.run_command(str(rootfs_path), command)
            return result.returncode
        except Exception as e:
            print(f"❌ Erro ao executar comando: {e}")
            return 1
    
    def extract_rootfs(self, archive_path, dest_dir):
        """Extrai rootfs manualmente.
        
        Args:
            archive_path: Caminho do arquivo tar
            dest_dir: Diretório de destino
        
        Returns:
            Caminho do diretório extraído
        """
        return self.adapter.extract(archive_path, dest_dir)
