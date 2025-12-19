"""
Gestionnaire d'exceptions personnalisées
"""


class CANException(Exception):
    """Exception de base pour l'application CAN"""
    pass


class ConfigurationError(CANException):
    """Erreur de configuration"""
    pass


class APIError(CANException):
    """Erreur liée aux appels API"""
    pass


class DataNotFoundError(CANException):
    """Données introuvables"""
    pass


class LLMError(CANException):
    """Erreur liée au LLM"""
    pass


class RAGError(CANException):
    """Erreur liée au RAG"""
    pass
