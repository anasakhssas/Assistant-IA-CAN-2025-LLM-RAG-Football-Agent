"""
API Backend FastAPI pour l'Assistant IA CAN 2025
Endpoints pour chatbot, résumé de match, sentiment, et recommandation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

# Ajout du chemin parent pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.llm_interface import LLMInterface
from api.rag_pipeline import RAGPipeline
from src.data_manager import DataManager

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Assistant IA CAN 2025",
    description="API pour un chatbot intelligent dédié à la Coupe d'Afrique des Nations 2025",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation des composants IA
try:
    llm = LLMInterface(provider="groq")
    rag = RAGPipeline()
    data_manager = DataManager()
    print("✅ Composants IA initialisés avec succès")
except Exception as e:
    print(f"⚠️ Erreur d'initialisation: {e}")
    import traceback
    traceback.print_exc()
    llm = None
    rag = None
    data_manager = None


# ============= Modèles Pydantic =============

class ChatRequest(BaseModel):
    """Requête pour le chatbot"""
    question: str
    use_rag: bool = True  # Utiliser le RAG par défaut
    
class ChatResponse(BaseModel):
    """Réponse du chatbot"""
    answer: str
    sources: Optional[List[dict]] = None

class SummaryRequest(BaseModel):
    """Requête pour résumé de match"""
    match_text: str
    
class SummaryResponse(BaseModel):
    """Réponse avec résumé"""
    summary: str

class DocumentRequest(BaseModel):
    """Requête pour ajouter des documents au RAG"""
    documents: List[dict]

class StatsResponse(BaseModel):
    """Statistiques de la base vectorielle"""
    collection_name: str
    total_documents: int
    persist_directory: str


# ============= Endpoints =============

@app.get("/")
async def root():
    """Endpoint racine - informations sur l'API"""
    return {
        "message": "Bienvenue sur l'API de l'Assistant IA CAN 2025",
        "version": "1.0.0",
        "endpoints": {
            "chatbot": "/ask",
            "resume": "/summary",
            "documents": "/documents",
            "stats": "/stats"
        }
    }

@app.get("/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {
        "status": "healthy",
        "llm_ready": llm is not None,
        "rag_ready": rag is not None
    }

@app.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """
    Endpoint principal du chatbot
    Répond aux questions sur la CAN 2025
    """
    if not llm:
        raise HTTPException(status_code=503, detail="LLM non initialisé")
    
    try:
        # Si RAG activé, récupérer le contexte
        context = None
        sources = None
        
        if request.use_rag and rag:
            # Déterminer le nombre de résultats selon la question
            # Plus de résultats pour les questions sur les joueurs/équipes
            question_lower = request.question.lower()
            keywords_team = ['joueurs', 'équipe', 'composition', 'effectif', 'liste', 'roster', 'sélection']
            keywords_comparison = ['cher', 'valeur', 'prix', 'meilleur', 'plus', 'top', 'classement']
            
            # Détection spéciale pour les questions sur la valeur/prix
            if any(kw in question_lower for kw in ['cher', 'valeur', 'prix']) and data_manager:
                # Utiliser directement la fonction get_most_valuable_players
                top_players = data_manager.get_most_valuable_players(limit=10)
                if top_players:
                    # Créer un contexte structuré avec les joueurs les plus chers
                    context_lines = ["Voici les joueurs les plus chers de la CAN 2025:\n"]
                    for i, p in enumerate(top_players, 1):
                        context_lines.append(f"{i}. {p['player_name']} ({p['team']}) - {p['club']}")
                        context_lines.append(f"   Valeur marchande: {p['market_value']:,} €")
                        context_lines.append(f"   Poste: {p['position']}, Âge: {p['age']} ans\n")
                    context = "\n".join(context_lines)
                    
                    sources = [{"id": f"player_{p['player_id']}", 
                               "text": f"{p['player_name']} - {p['market_value']:,} €",
                               "metadata": {"type": "joueur", "player_name": p['player_name']}}
                              for p in top_players[:5]]
            
            # Détection spéciale pour les meilleurs buteurs d'une équipe
            elif any(kw in question_lower for kw in ['buteur', 'meilleur buteur', 'top buteur']) and data_manager:
                # Extraire le nom de l'équipe
                teams = ['maroc', 'sénégal', 'égypte', 'nigeria', 'cameroun', 'algérie', 'côte d\'ivoire', 
                        'ghana', 'tunisie', 'mali', 'guinée', 'burkina faso']
                team_found = next((t for t in teams if t in question_lower), None)
                
                if team_found:
                    # Récupérer les meilleurs buteurs de cette équipe
                    top_scorers = data_manager.get_top_scorers_by_team(team_found, limit=5)
                    if top_scorers:
                        context_lines = [f"Meilleurs buteurs de l'équipe {team_found.capitalize()}:\n"]
                        for i, p in enumerate(top_scorers, 1):
                            context_lines.append(f"{i}. {p['player_name']} - {p['goals_international']} buts internationaux")
                            context_lines.append(f"   Club: {p['club']}, Poste: {p['position']}")
                            context_lines.append(f"   Sélections: {p['caps']}, Âge: {p['age']} ans\n")
                        context = "\n".join(context_lines)
                        
                        sources = [{"id": f"player_{p['player_id']}", 
                                   "text": f"{p['player_name']} - {p['goals_international']} buts",
                                   "metadata": {"type": "joueur", "player_name": p['player_name']}}
                                  for p in top_scorers[:3]]
            
            # Sinon, utiliser la recherche RAG normale
            if not context:
                # Utiliser 10 résultats si la question porte sur des joueurs/équipes ou des comparaisons
                n_results = 10 if (any(kw in question_lower for kw in keywords_team) or 
                                 any(kw in question_lower for kw in keywords_comparison)) else 3
            
                # Recherche de documents pertinents
                retrieved_docs = rag.search(request.question, n_results=n_results)
                
                if retrieved_docs:
                    context = rag.retrieve_context(request.question, n_results=n_results)
                    sources = [
                        {
                            "id": doc['id'],
                            "text": doc['text'][:200] + "...",  # Extrait
                            "metadata": doc.get('metadata', {})
                        }
                        for doc in retrieved_docs
                    ]
        
        # Génération de la réponse
        answer = llm.chat(request.question, context=context)
        
        return ChatResponse(answer=answer, sources=sources)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.post("/summary", response_model=SummaryResponse)
async def summarize_match(request: SummaryRequest):
    """
    Génère un résumé automatique d'un match
    À partir d'un texte d'article ou rapport de match
    """
    if not llm:
        raise HTTPException(status_code=503, detail="LLM non initialisé")
    
    try:
        summary = llm.summarize_match(request.match_text)
        return SummaryResponse(summary=summary)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.post("/documents")
async def add_documents(request: DocumentRequest):
    """
    Ajoute des documents à la base vectorielle RAG
    Format attendu: [{"id": "...", "text": "...", "metadata": {...}}]
    """
    if not rag:
        raise HTTPException(status_code=503, detail="RAG non initialisé")
    
    try:
        success = rag.add_documents(request.documents)
        
        if success:
            return {
                "message": f"{len(request.documents)} documents ajoutés avec succès",
                "total_documents": rag.get_collection_stats()['total_documents']
            }
        else:
            raise HTTPException(status_code=500, detail="Échec de l'ajout de documents")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Retourne les statistiques de la base vectorielle
    """
    if not rag:
        raise HTTPException(status_code=503, detail="RAG non initialisé")
    
    try:
        stats = rag.get_collection_stats()
        return StatsResponse(**stats)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/search")
async def search_documents(query: str, n_results: int = 3):
    """
    Recherche directe dans la base vectorielle
    """
    if not rag:
        raise HTTPException(status_code=503, detail="RAG non initialisé")
    
    try:
        results = rag.search(query, n_results=n_results)
        return {
            "query": query,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


# Point d'entrée pour uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
