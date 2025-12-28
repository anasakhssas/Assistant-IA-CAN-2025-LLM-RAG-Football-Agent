"""
Interface Streamlit pour l'Assistant IA CAN 2025
Interface utilisateur simple pour interagir avec le chatbot
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Assistant IA CAN 2025",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL de l'API (à modifier selon votre configuration)
API_URL = "http://localhost:8000"

# ============= Fonctions utilitaires =============

def check_api_health():
    """Vérifie si l'API est accessible"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def ask_chatbot(question, use_rag=True):
    """Envoie une question au chatbot"""
    try:
        response = requests.post(
            f"{API_URL}/ask",
            json={"question": question, "use_rag": use_rag},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Erreur {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def summarize_match(match_text):
    """Génère un résumé de match"""
    try:
        response = requests.post(
            f"{API_URL}/summary",
            json={"match_text": match_text},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Erreur {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_stats():
    """Récupère les statistiques de la base vectorielle"""
    try:
        response = requests.get(f"{API_URL}/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def analyze_sentiment(text):
    """Analyse le sentiment d'un texte"""
    try:
        response = requests.post(
            f"{API_URL}/sentiment",
            json={"text": text},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Erreur {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_recommendations(favorite_teams, favorite_players, content_types):
    """Obtient des recommandations personnalisées"""
    try:
        response = requests.post(
            f"{API_URL}/recommendations",
            json={
                "favorite_teams": favorite_teams,
                "favorite_players": favorite_players,
                "content_types": content_types
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Erreur {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


# ============= Interface principale =============

# Titre et description
st.title("⚽ Assistant IA CAN 2025")
st.markdown("### Votre compagnon intelligent pour la Coupe d'Afrique des Nations")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Vérification de l'API
    api_status = check_api_health()
    if api_status:
        st.success("✅ API connectée")
    else:
        st.error("❌ API non disponible")
        st.info("Lancez l'API avec: `uvicorn api.main:app --reload`")
    
    st.divider()
    
    # Mode RAG
    use_rag = st.checkbox("Utiliser RAG", value=True, 
                          help="Utilise la base de connaissances pour des réponses plus précises")
    
    st.divider()
    
    # Statistiques
    st.header("📊 Statistiques")
    stats = get_stats()
    if stats:
        st.metric("Documents", stats.get('total_documents', 0))
        st.caption(f"Collection: {stats.get('collection_name', 'N/A')}")
    
    st.divider()
    
    # À propos
    st.header("ℹ️ À propos")
    st.markdown("""
    Cet assistant utilise:
    - 🤖 GPT (LLM)
    - 📚 RAG (ChromaDB)
    - ⚡ FastAPI
    - 🎨 Streamlit
    """)

# Onglets principaux
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chatbot", "📝 Résumé Match", "📊 Analyse Sentiment", "💡 Recommandations", "📖 Guide"])

# ===== Onglet Chatbot =====
with tab1:
    st.header("Posez vos questions sur la CAN 2025")
    
    # Exemples de questions
    st.markdown("**Exemples de questions:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏆 Qui est le champion en titre?"):
            st.session_state.question = "Qui est le champion en titre de la CAN?"
    
    with col2:
        if st.button("📅 Où se déroule la CAN 2025?"):
            st.session_state.question = "Où et quand se déroule la CAN 2025?"
    
    with col3:
        if st.button("⚽ Équipes favorites?"):
            st.session_state.question = "Quelles sont les équipes favorites pour la CAN 2025?"
    
    # Zone de texte pour la question
    question = st.text_area(
        "Votre question:",
        value=st.session_state.get('question', ''),
        height=100,
        placeholder="Ex: Quel est le format de la compétition CAN 2025?"
    )
    
    # Bouton d'envoi
    if st.button("Envoyer", type="primary", disabled=not api_status):
        if question:
            with st.spinner("🤔 Réflexion en cours..."):
                result = ask_chatbot(question, use_rag)
                
                if "error" in result:
                    st.error(f"❌ Erreur: {result['error']}")
                else:
                    # Affichage de la réponse
                    st.markdown("### 💬 Réponse:")
                    st.info(result.get('answer', 'Pas de réponse'))
                    
                    # Affichage des sources (si RAG)
                    if use_rag and result.get('sources'):
                        with st.expander("📚 Sources utilisées"):
                            for i, source in enumerate(result['sources'], 1):
                                st.markdown(f"**Source {i}:** {source.get('id', 'N/A')}")
                                st.caption(source.get('text', ''))
                                st.divider()
        else:
            st.warning("⚠️ Veuillez entrer une question")

# ===== Onglet Résumé de match =====
with tab2:
    st.header("📝 Résumé Automatique de Match")
    st.markdown("Collez le texte d'un article ou rapport de match pour obtenir un résumé structuré.")
    
    # Texte exemple
    example_text = """Le Maroc a remporté une victoire éclatante 3-1 contre le Sénégal en demi-finale de la CAN 2025. 
Le match s'est déroulé au Stade Mohammed V de Casablanca devant 60,000 spectateurs.

Achraf Hakimi a ouvert le score à la 23e minute sur un coup franc magnifique. Le Sénégal a réagi en égalisant 
par Sadio Mané en seconde période (67e minute), mais Youssef En-Nesyri a marqué deux fois (75e et 88e) pour 
assurer la qualification du Maroc pour la finale.

L'entraîneur marocain s'est félicité de la performance de ses joueurs, soulignant leur détermination et 
leur esprit d'équipe. Le Maroc affrontera l'Égypte en finale dimanche prochain."""

    if st.button("Charger exemple"):
        st.session_state.match_text = example_text
    
    # Zone de texte
    match_text = st.text_area(
        "Texte du match:",
        value=st.session_state.get('match_text', ''),
        height=300,
        placeholder="Collez ici le texte du rapport de match..."
    )
    
    # Bouton de résumé
    if st.button("Générer le résumé", type="primary", disabled=not api_status):
        if match_text:
            with st.spinner("📝 Génération du résumé..."):
                result = summarize_match(match_text)
                
                if "error" in result:
                    st.error(f"❌ Erreur: {result['error']}")
                else:
                    st.markdown("### ✨ Résumé:")
                    st.success(result.get('summary', 'Pas de résumé'))
        else:
            st.warning("⚠️ Veuillez entrer un texte de match")

# ===== Onglet Analyse de Sentiment =====
with tab3:
    st.header("📊 Analyse de Sentiment des Supporters")
    st.markdown("Analysez l'opinion des supporters sur les réseaux sociaux (Twitter, Facebook, etc.)")
    
    # Exemples de messages
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("😊 Message positif"):
            st.session_state.sentiment_text = "Incroyable victoire ! Le Maroc a dominé de bout en bout. Quelle équipe magnifique, fier d'être Marocain ! 🇲🇦⚽🏆"
    
    with col2:
        if st.button("😐 Message neutre"):
            st.session_state.sentiment_text = "Match nul 1-1 entre le Sénégal et l'Égypte. Résultat équitable vu le déroulement du match."
    
    with col3:
        if sAnalyse de sentiment
    - Analysez l'opinion des supporters sur les réseaux sociaux
    - Détection automatique: positif, neutre, ou négatif
    - Score de confiance et explication détaillée
    
    ### 4️⃣ Recommandations personnalisées
    - Contenu adapté à vos équipes et joueurs favoris
    - Suggestions de matchs, statistiques, articles
    - Expérience personnalisée pour chaque fan
    
    ### 5️⃣ t.button("😞 Message négatif"):
            st.session_state.sentiment_text = "Déçu par la performance de l'équipe aujourd'hui. Trop d'erreurs, pas d'intensité. On mérite mieux que ça."
    
    # Zone de texte
    sentiment_text = st.text_area(
        "Message à analyser:",
        value=st.session_state.get('sentiment_text', ''),
        height=150,
        placeholder="Collez ici un tweet, commentaire Facebook, ou message de supporter..."
    )
    
    # Bouton d'analyse
    if st.button("Analyser le sentiment", type="primary", disabled=not api_status):
        if sentiment_text:
            with st.spinner("🔍 Analyse en cours..."):
                result = analyze_sentiment(sentiment_text)
                
                if "error" in result:
                    st.error(f"❌ Erreur: {result['error']}")
                else:
                    sentiment = result.get('sentiment', 'neutre')
                    score = result.get('score', 0.0)
                    explication = result.get('explication', '')
                    
                    # Affichage visuel du sentiment
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        if sentiment == "positif":
                            st.success(f"### 😊 {sentiment.upper()}")
                            st.progress(score, text=f"Score: {score:.2f}")
                        elif sentiment == "negatif":
                            st.error(f"### 😞 {sentiment.upper()}")
                            st.progress(score, text=f"Score: {score:.2f}")
                        else:
                            st.info(f"### 😐 {sentiment.upper()}")
                            st.progress(score, text=f"Score: {score:.2f}")
                    
                    with col2:
                        st.markdown("**Explication:**")
                        st.write(explication)
        else:
            st.warning("⚠️ Veuillez entrer un message à analyser")

# ===== Onglet Recommandations =====
with tab4:
    st.header("💡 Recommandations Personnalisées")
    st.markdown("Obtenez des recommandations de contenu basées sur vos préférences")
    
    # Formulaire de préférences
    st.subheader("📝 Vos préférences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Équipes favorites:**")
        favorite_teams = st.multiselect(
            "Sélectionnez vos équipes",
            ["Maroc", "Sénégal", "Égypte", "Algérie", "Nigeria", "Cameroun", "Côte d'Ivoire", "Ghana"],
            default=[]
        )
    
    with col2:
        st.markdown("**Joueurs favoris:**")
        favorite_players = st.multiselect(
            "Sélectionnez vos joueurs",
            ["Mohamed Salah", "Sadio Mané", "Achraf Hakimi", "Riyad Mahrez", "Victor Osimhen", "Youssef En-Nesyri"],
            default=[]
        )
    
    st.markdown("**Types de contenu préférés:**")
    content_types = st.multiselect(
        "Que souhaitez-vous voir?",
        ["matchs", "résumés", "statistiques", "analyses", "calendrier", "classements", "vidéos", "articles"],
        default=["matchs", "résumés", "statistiques"]
    )
    
    # Bouton pour obtenir les recommandations
    if st.button("Obtenir mes recommandations", type="primary", disabled=not api_status):
        if favorite_teams or favorite_players:
            with st.spinner("🎯 Génération de recommandations..."):
                result = get_recommendations(favorite_teams, favorite_players, content_types)
                
                if "error" in result:
                    st.error(f"❌ Erreur: {result['error']}")
                else:
                    st.markdown("### ✨ Vos recommandations personnalisées:")
                    st.success(result.get('recommendations', 'Pas de recommandations'))
                    
                    # Affichage des critères utilisés
                    with st.expander("🔍 Basé sur vos préférences"):
                        based_on = result.get('based_on', {})
                        if based_on.get('favorite_teams'):
                            st.markdown(f"**Équipes:** {', '.join(based_on['favorite_teams'])}")
                        if based_on.get('favorite_players'):
                            st.markdown(f"**Joueurs:** {', '.join(based_on['favorite_players'])}")
                        if based_on.get('content_types'):
                            st.markdown(f"**Types de contenu:** {', '.join(based_on['content_types'])}")
        else:
            st.warning("⚠️ Veuillez sélectionner au moins une équipe ou un joueur favori")

# ===== Onglet Guide =====
with tab5:
    st.header("📖 Guide d'utilisation")
    
    st.markdown("""
    ## 🎯 Fonctionnalités principales
    
    ### 1️⃣ Chatbot informatif
    - Répondez aux questions sur la CAN 2025
    - Informations sur matchs, équipes, joueurs, classements
    - Mode RAG pour des réponses basées sur données réelles
    
    ### 2️⃣ Résumé automatique
    - Analysez un texte d'article de match
    - Générez un résumé concis et structuré
    - Format adapté aux réseaux sociaux
    
    ### 3️⃣ Base de connaissances
    - Documents stockés dans ChromaDB
    - Recherche sémantique intelligente
    - Contexte enrichi pour les réponses
    
    ## 🚀 Comment démarrer
    
    1. **Lancer l'API backend**
    ```bash
    uvicorn api.main:app --reload
    ```
    
    2. **Lancer l'interface Streamlit**
    ```bash
    streamlit run frontend/app.py
    ```
    
    3. **Configurer les variables d'environnement**
    - Créer un fichier `.env`
    - Ajouter `OPENAI_API_KEY=votre_clé`
    
    ## 💡 Exemples de questions
    
    - "Quand commence la CAN 2025?"
    - "Qui sont les favoris pour gagner?"
    - "Quel est le format de la compétition?"
    - "Quelle est l'histoire du Maroc à la CAN?"
    
    ## 📞 Support
    
    Pour toute question ou problème, consultez la documentation du projet.
    """)

# Footer
st.divider()
st.caption("🏆 Assistant IA CAN 2025 - Développé avec FastAPI, LangChain, ChromaDB et Streamlit")
