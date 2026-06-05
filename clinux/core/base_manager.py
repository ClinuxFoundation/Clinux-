"""Classe base para gerenciadores."""
from abc import ABC, abstractmethod

class BaseManager(ABC):
    @abstractmethod
    def check_dependencies(self):
        pass
    
    @abstractmethod
    def validate(self, target):
        pass