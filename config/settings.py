"""
Configuration centralisée de l'application
Auteur: [Votre Nom]
Projet: CAN 2025 - SBI Africa
Date: Décembre 2025"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Chemins du projet
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
VECTORSTORE_DIR = BASE_DIR / "vectorstore" / "index"
LOGS_DIR = BASE_DIR / "logs"

# Créer les dossiers s'ils n'existent pas
LOGS_DIR.mkdir(exist_ok=True)
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

# ============= LLM Configuration =============
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1000"))

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")

# ============= RAG Configuration =============
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "can2025_knowledge")
PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", str(VECTORSTORE_DIR))
N_RESULTS = int(os.getenv("N_RESULTS", "3"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# ============= API Configuration =============
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# ============= Frontend Configuration =============
API_URL = os.getenv("API_URL", "http://localhost:8000")
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))

# ============= API-Football Configuration =============
FOOTBALL_API_BASE_URL = "https://v3.football.api-sports.io"
FOOTBALL_LEAGUE_ID = 6  # Africa Cup of Nations
FOOTBALL_SEASON = 2025

# ============= Logging Configuration =============
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "app.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Validation des clés API requises
def validate_config():
    """Valide la configuration"""
    errors = []
    
    if LLM_PROVIDER == "groq" and not GROQ_API_KEY:
        errors.append("GROQ_API_KEY manquante dans .env")
    
    if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY manquante dans .env")
    
    if errors:
        raise ValueError(f"Erreurs de configuration: {', '.join(errors)}")
    
    return True


# Exporter toutes les configurations
__all__ = [
    "BASE_DIR",
    "DATA_DIR",
    "VECTORSTORE_DIR",
    "LOGS_DIR",
    "LLM_PROVIDER",
    "LLM_MODEL",
    "LLM_TEMPERATURE",
    "LLM_MAX_TOKENS",
    "GROQ_API_KEY",
    "OPENAI_API_KEY",
    "FOOTBALL_API_KEY",
    "COLLECTION_NAME",
    "PERSIST_DIRECTORY",
    "N_RESULTS",
    "EMBEDDING_MODEL",
    "API_HOST",
    "API_PORT",
    "DEBUG",
    "API_URL",
    "STREAMLIT_PORT",
    "FOOTBALL_API_BASE_URL",
    "FOOTBALL_LEAGUE_ID",
    "FOOTBALL_SEASON",
    "LOG_LEVEL",
    "LOG_FILE",
    "LOG_FORMAT",
    "validate_config",
]
