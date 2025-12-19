# 🏆 Assistant IA CAN 2025

Un chatbot intelligent pour la Coupe d'Afrique des Nations 2025. Posez des questions sur les matchs, les équipes, l'historique et obtenez des résumés automatiques.

## Fonctionnalités

- **Chatbot Q&A** - Répondez à vos questions sur la CAN 2025
- **Résumé de match** - Générez des résumés structurés d'articles
- **Base RAG** - Recherche contextuelle dans une base vectorielle

## 🧠 Fonctionnalités principales

### 1. Chatbot informatif

Le chatbot répond aux questions concernant:
- Calendrier des matchs
- Résultats
- Classements
- Informations équipes / joueurs

### 2. Résumé automatique de match

À partir d'un texte brut, le modèle génère un résumé structuré, compatible social media.

### 3. Analyse de sentiment

Analyse des messages supporters pour déterminer:
- positif
- neutre
- négatif

### 4. Recommandation personnalisée

Suggestions de matchs, contenus vidéos, statistiques selon le profil utilisateur.

## Architecture

```
Streamlit (Frontend) → FastAPI (Backend) → RAG Pipeline → ChromaDB + Groq LLM
```

## 🔧 Technologies utilisées

| Domaine | Outils |
|---------|--------|
| Backend API | FastAPI 0.109 |
| LLM | Groq LLaMA 3.3 70B (Gratuit!) |
| RAG | ChromaDB + Sentence Transformers |
| Vector Store | ChromaDB 0.4.22 |
| Frontend | Streamlit 1.31 |
| Dev | Python 3.11 |
| Documentation | Markdown |

## 📂 Structure du projet

```
project/
│Technologies

- **Backend**: FastAPI
- **LLM**: Groq (LLaMA 3.3 - gratuit)
- **RAG**: ChromaDB + Sentence Transformers
- **Frontend**: Streamlit
- **Python**: 3.11+
│   ├── llm_interface.py
│   └── sentiment_model.py
│
├── frontend/
│   └── app.py
│
├── vectorstore/
│   └── index/
│
└── README.md
```

## 🧪 Scénarios d'usage

### Q&R football
"Qui a gagné Maroc vs Sénégal et quel était le score ?"

### Résumé match
"Résume-moi le match de l'Algérie en 100 mots."

### Sentiment supporters
"Analyse le ton global des tweets des supporters marocains."

### Recommandation
"Quels matchs dois-je suivre demain selon mes équipes préférées ?"

## 🚀 Installation rapide

### Prérequis
- Python 3.11+
- GInstallation

### Prérequis
- Python 3.11+

### 1. Clone

### 2. Créer un environnement virtuel
```bash
python -m venv venv

# Windows
venv\ScEnvironnement virtuel
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Dvariables d'environnement
```bash
# Copier le template
cp .env.example .env

# Éditer .env eation
```bash
cp .env.example .env
# Ajoutez votre clé Groq API (gratuite sur console.groq.com/keys)
```

### 5. Lancer

Terminal 1:
```bash
uvicorn api.main:app --reload
```

Terminal 2:
```bash
streamlit run frontend/app.py
```

Ouvrez http://localhost:8501
- Stats football
- Données match live API (si disponibles)

## 🎥 Démonstration

Livrables prévus:
- Vidéo explicative du chatbot
- Use case match complet

## 📌 Fonctionnalités MVP v1.0

### ✅ Implémentées

- **Chatbot Informatif CAN 2025**
  - Questions/réponses sur matchs, équipes, joueurs
  - Historique de la CAN
  - Calendrier et résultats

- **Pipeline RAG (Retrieval-Augmented Generation)**
  - Base vectorielle ChromaDB
  - Recherche sémantique contextuelle
  - Réponses basées sur documents réels

- **Résumé Automatique de Match**
  - Analyse de texte d'articles
  - Génération de résumés structurés
  - Format adapté social media

- **Interface Web Interactive**
  -À venir

- Analyse de sentiment
- Support multilingue (FR/EN/AR)
- Prédiction de résultats
# Test du pipeline RAG
python api/rag_pipeline.py

# Test de santé de l'API
curl http://localhost:8000/health
```

## 🤝 Contribuer

Les contributions sont les bienvenues ! Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails.

1. Fork le projet
2. Créez une branche (`git checkout -b feature/amazing-feature`)
3. Commit vos changements (`git commit -m 'feat: add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

Akhssas Anas

## 📄 License

MIT License - Copyright (c) 2025 [Votre Nom]