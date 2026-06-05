"""Gerenciador de rede para VMs."""
import subprocess

class NetworkManager:
    @staticmethod
    def user_network():
        return ["-net", "user", "-net", "nic"]
    
    @staticmethod
    def bridge_network(iface="br0"):
        return ["-net", "bridge,br=" + iface]
    
    @staticmethod
    def port_forward(host_port, guest_port):
        return [f"hostfwd=tcp::{host_port}-:{guest_port}"]
