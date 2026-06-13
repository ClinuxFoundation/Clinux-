"""Adaptador PRoot melhorado para Android e PC."""
import subprocess
import tarfile
import shutil
import sys
from pathlib import Path


class PRootAdapter:
    """Adapter para PRoot com suporte melhorado para Android e PC."""
    
    def __init__(self):
        self.is_termux = Path("/data/data/com.termux/files").exists()
        self.is_android = Path("/system/build.prop").exists()
    
    def start(self, rootfs, shell="/bin/bash", bind_mounts=None):
        """Inicia PRoot com rootfs especificado.
        
        Args:
            rootfs: Caminho para o rootfs
            shell: Shell a executar (padrão: /bin/bash)
            bind_mounts: Lista de bind mounts adicionais [('src', 'dest'), ...]
        
        Returns:
            Código de retorno do subprocess
        """
        self._check_dependencies()
        
        rootfs_path = Path(rootfs)
        if not rootfs_path.exists():
            raise FileNotFoundError(f"Rootfs não encontrado: {rootfs}")
        
        # Prepara o rootfs (cria diretórios e mounts necessários)
        self._prepare_rootfs(rootfs_path)
        
        cmd = self._build_proot_command(rootfs_path, shell, bind_mounts)
        
        try:
            result = subprocess.run(cmd, check=False)
            return result.returncode
        except Exception as e:
            print(f"❌ Erro ao executar PRoot: {e}", file=sys.stderr)
            return 1
    
    def extract(self, tarball, dest):
        """Extrai arquivo tar para destino.
        
        Args:
            tarball: Caminho do arquivo tar
            dest: Diretório de destino
        
        Returns:
            Caminho do diretório extraído
        """
        dest_path = Path(dest)
        dest_path.mkdir(parents=True, exist_ok=True)
        
        try:
            with tarfile.open(tarball) as tar:
                tar.extractall(dest_path)
            return str(dest_path)
        except Exception as e:
            print(f"❌ Erro ao extrair tarball: {e}", file=sys.stderr)
            raise
    
    def _prepare_rootfs(self, rootfs_path):
        """Prepara o rootfs criando diretórios e permissões necessárias."""
        try:
            # Garante que /tmp existe e tem permissões corretas
            tmp_dir = rootfs_path / "tmp"
            tmp_dir.mkdir(exist_ok=True)
            try:
                tmp_dir.chmod(0o1777)
            except OSError:
                pass
            
            # Garante que /run existe (necessário para PRoot em Termux)
            run_dir = rootfs_path / "run"
            run_dir.mkdir(exist_ok=True)
            try:
                run_dir.chmod(0o755)
            except OSError:
                pass
            
            # Cria /dev, /proc, /sys se não existirem
            for d in ["dev", "proc", "sys"]:
                dir_path = rootfs_path / d
                dir_path.mkdir(exist_ok=True)
            
            # Cria /root se não existir (working directory)
            root_home = rootfs_path / "root"
            root_home.mkdir(exist_ok=True)
            try:
                root_home.chmod(0o700)
            except OSError:
                pass
                
            # Garante que diretórios essenciais para libs existem
            for d in ["lib", "lib64", "usr/lib", "usr/local/lib"]:
                lib_dir = rootfs_path / d
                lib_dir.mkdir(parents=True, exist_ok=True)
                
        except OSError as e:
            # Algumas operações podem falhar dependendo do filesystem
            pass
    
    def _check_dependencies(self):
        """Verifica se proot está instalado."""
        if not shutil.which("proot"):
            self._print_install_instructions()
            sys.exit(1)
        
        # Se em Termux, verifica suporte para QEMU
        if self.is_termux:
            self._check_termux_qemu()
    
    def _check_termux_qemu(self):
        """Verifica suporte QEMU em Termux."""
        # Verifica arquitetura
        try:
            result = subprocess.run(
                ["uname", "-m"],
                capture_output=True,
                text=True,
                check=False
            )
            arch = result.stdout.strip()
            
            # Se for ARM64, pode precisar de QEMU para x86_64
            if arch == "aarch64":
                # Opcional: avisar sobre possível necessidade de QEMU
                if not shutil.which("qemu-aarch64-static"):
                    print("⚠️  Para melhor compatibilidade com outras arquiteturas, considere instalar QEMU")
        except:
            pass
    
    def _print_install_instructions(self):
        """Exibe instruções de instalação."""
        print("❌ PRoot não está instalado!")
        print("\n📦 Instruções de instalação:")
        
        if self.is_termux:
            print("   Termux:")
            print("      pkg update")
            print("      pkg install proot")
            print("      pkg install proot-distro (opcional)")
        else:
            print("   Linux (Debian/Ubuntu):")
            print("      sudo apt update")
            print("      sudo apt install proot")
            print("\n   Linux (Fedora/RHEL):")
            print("      sudo dnf install proot")
            print("\n   Linux (Arch):")
            print("      sudo pacman -S proot")
        
        print("\n   Android (Termux):")
        print("      Acesse: https://termux.com/")
    
    def _build_proot_command(self, rootfs_path, shell, bind_mounts):
        """Constrói comando proot com argumentos apropriados.
        
        Args:
            rootfs_path: Path object do rootfs
            shell: Shell a usar
            bind_mounts: Bind mounts adicionais
        
        Returns:
            Lista com comando proot
        """
        cmd = ["proot"]
        
        # Argumentos para melhorar compatibilidade
        cmd.extend(["-q", "execve"])  # Quiet mode para erros de execve
        
        # Bind mounts essenciais - apenas monta se existirem no HOST
        essential_binds = [
            ("/dev", "/dev"),
            ("/proc", "/proc"),
            ("/sys", "/sys"),
        ]
        
        if self.is_termux:
            # Em Termux, adiciona bind mounts específicos
            essential_binds.extend([
                ("/data/data/com.termux", "/data/data/com.termux"),
                ("/system", "/system"),
            ])
            
            # Cria um diretório temporário seguro em Termux se necessário
            termux_tmp = Path("/data/data/com.termux/files/usr/tmp")
            termux_tmp.mkdir(parents=True, exist_ok=True)
            try:
                termux_tmp.chmod(0o1777)
            except OSError:
                pass
        
        # Root filesystem
        cmd.extend(["-r", str(rootfs_path)])
        
        # Working directory - usa /root em vez de / para evitar problemas
        cmd.extend(["-w", "/root"])
        
        # Bind mounts essenciais - verifica existência no HOST
        for src, dest in essential_binds:
            src_path = Path(src)
            if src_path.exists():
                cmd.extend(["-b", f"{src}:{dest}"])
        
        # /tmp sempre precisa estar acessível - tenta usar o tmpfs do host
        tmp_path = Path("/tmp")
        if tmp_path.exists():
            try:
                cmd.extend(["-b", "/tmp:/tmp"])
            except Exception:
                pass
        
        # Em Termux, usa o /tmp específico do Termux
        if self.is_termux:
            termux_tmp_path = Path("/data/data/com.termux/files/usr/tmp")
            if termux_tmp_path.exists():
                # Tenta usar tmpdir para evitar problemas de permissão
                cmd.extend(["-t", str(termux_tmp_path)])
        
        # Bind mounts adicionais
        if bind_mounts:
            for src, dest in bind_mounts:
                src_path = Path(src)
                if src_path.exists():
                    cmd.extend(["-b", f"{src}:{dest}"])
        
        # Shell
        if shell:
            cmd.append(shell)
        
        return cmd
    
    def run_command(self, rootfs, command, shell=False, bind_mounts=None):
        """Executa comando dentro do PRoot.
        
        Args:
            rootfs: Caminho do rootfs
            command: Comando a executar (string ou lista)
            shell: Se True, executa como shell
            bind_mounts: Bind mounts adicionais
        
        Returns:
            CompletedProcess do subprocess
        """
        self._check_dependencies()
        
        rootfs_path = Path(rootfs)
        if not rootfs_path.exists():
            raise FileNotFoundError(f"Rootfs não encontrado: {rootfs}")
        
        # Prepara o rootfs
        self._prepare_rootfs(rootfs_path)
        
        if isinstance(command, str) and not shell:
            command = command.split()
        
        proot_cmd = self._build_proot_command(rootfs_path, "", bind_mounts)
        
        # Remove shell do final se vazio
        if proot_cmd and proot_cmd[-1] == "":
            proot_cmd = proot_cmd[:-1]
        
        if isinstance(command, list):
            proot_cmd.extend(command)
        else:
            proot_cmd.extend(["/bin/ash", "-c", command])
        
        try:
            result = subprocess.run(proot_cmd, check=False)
            return result
        except Exception as e:
            print(f"❌ Erro ao executar comando em PRoot: {e}", file=sys.stderr)
            raise
