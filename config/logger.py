"""
Configuration du logging pour toute l'application
"""

import logging
import sys
from pathlib import Path
from config.settings import LOG_LEVEL, LOG_FILE, LOG_FORMAT

def setup_logging(name: str = None) -> logging.Logger:
    """
    Configure et retourne un logger
    
    Args:
        name: Nom du logger (utilise __name__ du module appelant)
    
    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name or __name__)
    
    # Éviter la duplication des handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Format
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler pour le fichier
    if LOG_FILE:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Logger par défaut
logger = setup_logging("can2025")
