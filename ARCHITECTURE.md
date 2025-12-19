# Assistant IA CAN 2025

## 📁 Architecture du Projet

```
Intelligence-Artificielle-LLM-Assistant-intelligent-CAN-2025/
│
├── api/                          # Backend FastAPI
│   ├── __init__.py
│   ├── main.py                   # Point d'entrée API
│   └── rag_pipeline.py           # Pipeline RAG avec ChromaDB
│
├── models/                       # Modèles LLM
│   ├── __init__.py
│   └── llm_interface.py          # Interface Groq/OpenAI
│
├── frontend/                     # Interface Streamlit
│   └── app.py                    # Application web
│
├── data/                         # Données CAN
│   ├── matches.csv               # Matchs
│   ├── teams.csv                 # Équipes
│   ├── standings.csv             # Classements (généré par API)
│   ├── top_scorers.csv           # Buteurs (généré par API)
│   ├── top_assists.csv           # Passeurs (généré par API)
│   ├── team_statistics.csv       # Stats équipes (généré par API)
│   ├── venues.csv                # Stades (généré par API)
│   └── history/
│       └── can_historique.md     # Historique CAN
│
├── scripts/                      # Scripts utilitaires
│   ├── data_fetcher.py           # Récupération données API-Football
│   ├── test_api_football.py      # Test connexion API
│   └── load_data_to_vectorstore.py # Chargement ChromaDB
│
├── config/                       # Configuration centralisée
│   ├── __init__.py
│   ├── settings.py               # Paramètres globaux
│   └── logger.py                 # Configuration logging
│
├── src/                          # Code source utilitaire
│   ├── __init__.py
│   ├── data_manager.py           # Gestionnaire de données
│   └── exceptions.py             # Exceptions personnalisées
│
├── scripts/                      # Scripts utilitaires
│   ├── test_api_football.py      # Test de l'API
│   ├── test_api_advanced.py      # Tests avancés
│   └── find_can_id.py            # Trouver l'ID CAN
│
├── tests/                        # Tests unitaires
│   ├── .gitignore
│   └── test_data_manager.py      # Tests DataManager
│
├── vectorstore/                  # Base vectorielle ChromaDB
│   └── index/                    # Index persistant
│
├── logs/                         # Fichiers de log
│   └── .gitkeep
│
├── .env                          # Variables d'environnement (secret)
├── .env.example                  # Template configuration
├── .gitignore                    # Fichiers ignorés par Git
├── requirements.txt              # Dépendances Python
├── start.bat                     # Script de démarrage Windows
├── README.md                     # Documentation principale
├── SETUP_GUIDE.md                # Guide d'installation
├── CONTRIBUTING.md               # Guide de contribution
├── FUNCTIONALITIES.md            # Liste des fonctionnalités
├── UPDATE_DATA.md                # Guide mise à jour données
└── LICENSE                       # Licence MIT
```

## 🔧 Principes de l'Architecture

### 1. **Séparation des responsabilités**
- `api/` : Logique backend et endpoints
- `models/` : Interaction avec les LLMs
- `frontend/` : Interface utilisateur
- `data/` : Données et récupération
- `config/` : Configuration centralisée
- `src/` : Utilitaires réutilisables

### 2. **Configuration centralisée**
- Toutes les variables dans `config/settings.py`
- Chargement depuis `.env`
- Validation au démarrage

### 3. **Logging unifié**
- Configuration dans `config/logger.py`
- Logs console + fichier
- Niveaux configurables

### 4. **Gestion des données**
- `DataManager` pour accès centralisé
- Cache et optimisation
- Validation des données

### 5. **Tests**
- Tests unitaires dans `tests/`
- Tests d'intégration possibles
- Scripts de test dans `scripts/`

## 🚀 Utilisation

### Démarrage rapide
```bash
# Démarrer tout
start.bat

# Ou manuellement
uvicorn api.main:app --reload
streamlit run frontend/app.py
```

### Mise à jour des données
```bash
python scripts/data_fetcher.py
```

### Tests
```bash
python scripts/test_api_football.py
python -m pytest tests/
```

## 📊 Flux de données

1. **Récupération** : `scripts/data_fetcher.py` → API-Football → CSV
2. **Indexation** : `api/rag_pipeline.py` → CSV → ChromaDB
3. **Requête** : User → Frontend → API → RAG + LLM → Réponse

## 🔐 Sécurité

- `.env` jamais commité (dans `.gitignore`)
- `.env.example` pour template
- Validation des clés API au démarrage
- Logs sans données sensibles
