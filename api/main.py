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
    print("✅ Composants IA initialisés avec succès")
except Exception as e:
    print(f"⚠️ Erreur d'initialisation: {e}")
    import traceback
    traceback.print_exc()
    llm = None
    rag = None


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
            # Recherche de documents pertinents
            retrieved_docs = rag.search(request.question, n_results=3)
            
            if retrieved_docs:
                context = rag.retrieve_context(request.question, n_results=3)
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
