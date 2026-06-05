"""Configuração de logging."""
import logging
from pathlib import Path
from .config import BASE_DIR

def setup_logging():
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "clinux.log"),
            logging.StreamHandler()
        ]
    )