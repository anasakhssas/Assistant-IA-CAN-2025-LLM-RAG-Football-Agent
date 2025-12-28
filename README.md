# 🏆 Assistant IA CAN 2025

Un assistant intelligent complet pour la Coupe d'Afrique des Nations 2025. Posez des questions, obtenez des résumés de matchs, analysez le sentiment des supporters et recevez des recommandations personnalisées.

## ✨ Fonctionnalités

- **💬 Chatbot Q&A** - Répondez à vos questions sur la CAN 2025 avec RAG
- **📝 Résumé de match** - Générez des résumés structurés d'articles
- **📊 Analyse de sentiment** - Analysez l'opinion des supporters (positif/neutre/négatif)
- **💡 Recommandations personnalisées** - Contenu adapté à vos équipes et joueurs favoris
- **🔍 Base RAG** - Recherche contextuelle dans 126+ documents

## 🧠 Cas d'usage détaillés

### 1. Chatbot informatif

Le chatbot répond aux questions concernant:
- Calendrier des matchs et horaires
- Résultats en temps réel
- Classements des groupes
- Informations équipes / joueurs
- Historique de la CAN (1957-2024)
- Statistiques détaillées

**Exemples de questions:**
- "Qui est le champion en titre?"
- "Quel est le format de la CAN 2025?"
- "Quelle est la valeur de Mohamed Salah?"

### 2. Résumé automatique de match

À partir d'un texte brut (article, rapport), génère un résumé structuré:
- Score final et buteurs
- Moments clés du match
- Déclarations importantes
- Format adapté aux réseaux sociaux

### 3. Analyse de sentiment

Analyse des messages supporters (tweets, commentaires) pour déterminer:
- **Positif** 😊 - Joie, fierté, enthousiasme
- **Neutre** 😐 - Observation factuelle
- **Négatif** 😞 - Déception, frustration

Inclut un score de confiance (0.0-1.0) et une explication détaillée.

### 4. Recommandations personnalisées

Suggestions de contenu basées sur:
- Équipes favorites (Maroc, Sénégal, Égypte, etc.)
- Joueurs favoris (Salah, Mané, Hakimi, etc.)
- Types de contenu (matchs, statistiques, analyses, vidéos)

Recommandations intelligentes avec explications de pertinence.

## 🎯 Architecture

```
┌─────────────────────────────────────────┐
│      Frontend (Streamlit)               │
│  - 5 onglets: Chatbot, Résumé,          │
│    Sentiment, Recommandations, Guide    │
│  - Interface responsive et intuitive    │
└──────────────┬──────────────────────────┘
               │ HTTP/REST API
               ▼
┌─────────────────────────────────────────┐
│       Backend (FastAPI)                 │
│  - 9 endpoints REST                     │
│  - Validation Pydantic                  │
│  - Gestion d'erreurs robuste            │
└──────────┬──────────────────────────────┘
           │
           ├─────────────┬─────────────┐
           ▼             ▼             ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │   LLM    │  │   RAG    │  │   Data   │
    │(Groq API)│  │(ChromaDB)│  │ Manager  │
    │LLaMA 3.3 │  │126+ docs │  │9 CSV files│
    └──────────┘  └──────────┘  └──────────┘
```

## 🔧 Technologies utilisées

| Domaine | Outils | Version |
|---------|--------|---------|
| Backend API | FastAPI | 0.109 |
| LLM | Groq (LLaMA 3.3 70B) | Gratuit! |
| RAG | ChromaDB | 0.4.22 |
| Embeddings | Sentence Transformers | all-MiniLM-L6-v2 |
| Frontend | Streamlit | 1.31 |
| Python | Python | 3.11+ |
| Vector Store | ChromaDB PersistentClient | Local |
| HTTP Client | Requests | Latest |

## 📂 Structure du projet

```
├── api/
│   ├── main.py              # FastAPI app avec 9 endpoints
│   ├── rag_pipeline.py      # Pipeline RAG avec ChromaDB
│   └── data_manager.py      # Gestion des données CSV
│
├── models/
│   ├── llm_interface.py     # Interface LLM (Groq/OpenAI)
│   │   - chat()             # Chatbot
│   │   - summarize_match()  # Résumé
│   │   - analyze_sentiment() # Sentiment (NOUVEAU)
│   │   - recommend_content() # Recommandations (NOUVEAU)
│
├── frontend/
│   └── app.py               # Interface Streamlit (5 onglets)
│
├── data/
│   ├── csv/                 # 9 fichiers CSV (matchs, équipes, etc.)
│   ├── historique/          # champions.md, records.md
│   ├── equipes/             # senegal.md, maroc.md, egypte.md
│   ├── joueurs/             # mohamed_salah.md
│   └── competition/         # format.md
│
├── 💬 Q&R Football
**Question:** "Qui a gagné Maroc vs Sénégal et quel était le score ?"  
**Réponse:** Utilise RAG pour chercher dans la base et répond avec contexte.

### 📝 Résumé Match
**Input:** Article long de 500 mots sur un match  
**Output:** Résumé structuré en 100 mots avec score, buteurs, moments clés

### 📊 Sentiment Supporters
**Input:** "Incroyable victoire ! Fier d'être Marocain ! 🇲🇦⚽🏆"  
**Output:** Sentiment: Positif (Score: 0.95) - Message enthousiaste exprimant fierté

### 💡 Recommandations
**Profil:** Équipes favorites: Maroc, Sénégal | Joueurs: Hakimi, Mané  
**Output:** Top 5 contenus recommandés avec scores de pertinence
### Q&R football
"Quit

### 1. Cloner le repo
```bash
git clone <repo-url>
cd Intelligence-Artificielle-LLM-Assistant-intelligent-CAN-2025-
```t supporters
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

MIT License - Copyright (c) 2025 Akhssas Anas
