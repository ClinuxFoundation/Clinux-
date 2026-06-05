"""Adaptador QEMU."""
import subprocess

class QEMUAdapter:
    def run(self, config):
        return subprocess.run([
            "qemu-system-x86_64",
            "-m", config.get("memory", "2G"),
            "-smp", config.get("cpu", "2"),
            "-drive", f"file={config['disk']},format=qcow2",
            "-net", "user", "-net", "nic"
        ])
    
    def stop(self, name):
        subprocess.run(["pkill", "-f", f"qemu.*{name}"])
    
    def status(self, name):
        result = subprocess.run(["pgrep", "-f", f"qemu.*{name}"], capture_output=True)
        return result.returncode == 0
