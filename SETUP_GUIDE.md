# Assistant IA CAN 2025

## 🚀 Guide de démarrage rapide

### 1. Installation

```bash
# Cloner le projet
git clone https://github.com/anasakhssas/Assistant-IA-CAN-2025-LLM-RAG-Football-Agent.git
cd Assistant-IA-CAN-2025-LLM-RAG-Football-Agent

# Créer environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Activer l'environnement (Linux/Mac)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copier le fichier de configuration
cp .env.example .env

# Éditer .env et ajouter votre clé OpenAI
# OPENAI_API_KEY=votre_clé_ici
```

### 3. Initialiser la base de données vectorielle (optionnel)

```bash
# Exécuter le script d'initialisation RAG
python api/rag_pipeline.py
```

### 4. Lancer l'API backend

```bash
# Démarrer FastAPI
uvicorn api.main:app --reload --port 8000
```

L'API sera accessible sur: http://localhost:8000

Documentation API: http://localhost:8000/docs

### 5. Lancer l'interface utilisateur

```bash
# Dans un nouveau terminal, avec l'environnement activé
streamlit run frontend/app.py
```

L'interface sera accessible sur: http://localhost:8501

## 📋 Fonctionnalités implémentées

### ✅ Fonctionnalités principales (Core Features)

1. **Chatbot Informatif CAN 2025** ✅
   - Interface LLM avec GPT
   - Réponses aux questions sur matchs, équipes, joueurs
   - Système de prompts spécialisés

2. **Moteur RAG (Retrieval-Augmented Generation)** ✅
   - Pipeline complet avec ChromaDB
   - Embeddings avec SentenceTransformer
   - Recherche sémantique contextuelle
   - Base de connaissances CAN 2025

3. **Résumé Automatique de Match** ✅
   - Génération de résumés structurés
   - Format adapté social media
   - Extraction des moments clés

## 🏗️ Architecture

```
Assistant IA CAN 2025/
├── api/
│   ├── main.py              # API FastAPI
│   └── rag_pipeline.py      # Pipeline RAG
│
├── models/
│   └── llm_interface.py     # Interface LLM
│
├── frontend/
│   └── app.py               # Interface Streamlit
│
├── data/
│   ├── matches.csv          # Données matchs
│   ├── teams.csv            # Données équipes
│   └── history/
│       └── can_historique.md
│
├── vectorstore/
│   └── index/               # Base ChromaDB
│
├── requirements.txt
├── .env.example
└── README.md
```

## 🔌 Endpoints API

- `GET /` - Informations API
- `GET /health` - Status de santé
- `POST /ask` - Poser une question au chatbot
- `POST /summary` - Résumer un match
- `POST /documents` - Ajouter des documents au RAG
- `GET /stats` - Statistiques de la base vectorielle
- `GET /search` - Recherche directe dans la base

## 📊 Données disponibles

- Matchs CAN 2025 (calendrier, résultats)
- Équipes participantes (24 équipes)
- Historique CAN (palmarès, records)
- Documents de référence

## 🧪 Tests

### Tester l'interface LLM

```bash
python models/llm_interface.py
```

### Tester le pipeline RAG

```bash
python api/rag_pipeline.py
```

### Tester l'API

```bash
# Avec curl
curl http://localhost:8000/health

# Ou via Swagger UI
# http://localhost:8000/docs
```

## 📝 Prochaines étapes

### À implémenter:

- [ ] Analyse de sentiment (NLP)
- [ ] Recommandations personnalisées
- [ ] Multilingue (FR/EN/AR)
- [ ] Prédiction de résultats
- [ ] Interface audio

## 🐛 Dépannage

### Problème: API non accessible

```bash
# Vérifier que l'API tourne
curl http://localhost:8000/health

# Relancer l'API
uvicorn api.main:app --reload
```

### Problème: Erreur OpenAI API

```bash
# Vérifier la clé API dans .env
echo $OPENAI_API_KEY  # Linux/Mac
echo %OPENAI_API_KEY%  # Windows

# Vérifier le format dans .env
OPENAI_API_KEY=sk-...
```

### Problème: ChromaDB erreur

```bash
# Réinitialiser la base vectorielle
rm -rf vectorstore/index
python api/rag_pipeline.py
```

## 📚 Documentation

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI API](https://platform.openai.com/docs)
- [ChromaDB](https://docs.trychroma.com/)
- [Streamlit](https://docs.streamlit.io/)

## 👤 Auteur

Développé dans le cadre du projet CAN 2025 – SBI Africa

## 📄 Licence

MIT License
