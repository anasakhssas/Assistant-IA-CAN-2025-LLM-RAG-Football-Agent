"""
Pipeline RAG (Retrieval-Augmented Generation) pour l'Assistant IA CAN 2025
Ce module gère le stockage vectoriel et la récupération contextuelle de documents
"""

import os
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()


class RAGPipeline:
    """
    Pipeline RAG pour améliorer les réponses du chatbot avec des données réelles
    Utilise ChromaDB pour le stockage vectoriel et SentenceTransformer pour les embeddings
    """
    
    def __init__(self, collection_name: str = "can2025_knowledge", 
                 persist_directory: str = "./vectorstore/index"):
        """
        Initialise le pipeline RAG
        
        Args:
            collection_name: Nom de la collection ChromaDB
            persist_directory: Répertoire de persistance de la base vectorielle
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        # Initialisation du modèle d'embeddings
        print("Chargement du modèle d'embeddings...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialisation de ChromaDB
        print("Initialisation de ChromaDB...")
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Récupération ou création de la collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"Collection '{collection_name}' chargée.")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "Base de connaissances CAN 2025"}
            )
            print(f"Nouvelle collection '{collection_name}' créée.")
    
    def add_documents(self, documents: List[Dict[str, str]]) -> bool:
        """
        Ajoute des documents à la base vectorielle
        
        Args:
            documents: Liste de dicts avec 'id', 'text', et 'metadata'
            
        Returns:
            True si succès
        """
        try:
            ids = [doc['id'] for doc in documents]
            texts = [doc['text'] for doc in documents]
            metadatas = [doc.get('metadata', {}) for doc in documents]
            
            # Génération des embeddings
            embeddings = self.embedding_model.encode(texts).tolist()
            
            # Ajout à la collection
            self.collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
            print(f"{len(documents)} documents ajoutés avec succès.")
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'ajout de documents: {e}")
            return False
    
    def search(self, query: str, n_results: int = 3) -> List[Dict]:
        """
        Recherche les documents les plus pertinents pour une requête
        
        Args:
            query: Question ou requête de l'utilisateur
            n_results: Nombre de résultats à retourner
            
        Returns:
            Liste de documents pertinents avec métadonnées et scores
        """
        try:
            # Génération de l'embedding de la requête
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            # Recherche dans ChromaDB
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
            # Formatage des résultats
            documents = []
            if results['documents'] and len(results['documents']) > 0:
                for i in range(len(results['documents'][0])):
                    documents.append({
                        'id': results['ids'][0][i],
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else 0
                    })
            
            return documents
            
        except Exception as e:
            print(f"Erreur lors de la recherche: {e}")
            return []
    
    def retrieve_context(self, query: str, n_results: int = 3) -> str:
        """
        Récupère le contexte pertinent pour une requête (format texte)
        
        Args:
            query: Question de l'utilisateur
            n_results: Nombre de documents à récupérer
            
        Returns:
            Contexte formaté en texte
        """
        documents = self.search(query, n_results)
        
        if not documents:
            return "Aucun document pertinent trouvé."
        
        context = []
        for i, doc in enumerate(documents, 1):
            context.append(f"Source {i}:\n{doc['text']}\n")
        
        return "\n".join(context)
    
    def get_collection_stats(self) -> Dict:
        """
        Retourne les statistiques de la collection
        
        Returns:
            Dictionnaire avec nombre de documents et métadonnées
        """
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "total_documents": count,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            return {"error": str(e)}
    
    def delete_collection(self):
        """Supprime la collection (utile pour réinitialiser)"""
        try:
            self.client.delete_collection(name=self.collection_name)
            print(f"Collection '{self.collection_name}' supprimée.")
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")


def initialize_can2025_knowledge():
    """
    Fonction utilitaire pour initialiser la base de connaissances CAN 2025
    avec des données d'exemple
    """
    rag = RAGPipeline()
    
    # Données d'exemple sur la CAN
    sample_documents = [
        {
            "id": "can2025_info",
            "text": """La Coupe d'Afrique des Nations 2025 se déroule au Maroc du 21 décembre 2025 
            au 18 janvier 2026. C'est la 35e édition de cette compétition. 24 équipes participent, 
            réparties en 6 groupes de 4 équipes.""",
            "metadata": {"type": "info_generale", "source": "officiel"}
        },
        {
            "id": "equipes_favorites",
            "text": """Les équipes favorites pour la CAN 2025 incluent le Sénégal (champion en titre), 
            l'Égypte, le Maroc (pays hôte), l'Algérie, le Nigeria et la Côte d'Ivoire. 
            Ces équipes ont des joueurs évoluant dans les plus grands championnats européens.""",
            "metadata": {"type": "equipes", "source": "analyse"}
        },
        {
            "id": "format_competition",
            "text": """Le format de la compétition: phase de groupes (6 groupes de 4), 
            puis phase à élimination directe avec huitièmes de finale, quarts, demi-finales et finale. 
            Les deux premiers de chaque groupe se qualifient, ainsi que les 4 meilleurs troisièmes.""",
            "metadata": {"type": "reglement", "source": "officiel"}
        },
        {
            "id": "historique_maroc",
            "text": """Le Maroc a remporté la CAN en 1976. Le pays a également été demi-finaliste 
            en 2004. C'est la deuxième fois que le Maroc organise la CAN après 1988.""",
            "metadata": {"type": "historique", "source": "archives"}
        },
        {
            "id": "historique_senegal",
            "text": """Le Sénégal a remporté sa première CAN en 2022 au Cameroun, battant l'Égypte 
            aux tirs au but. Les Lions de la Teranga ont également été finalistes en 2019.""",
            "metadata": {"type": "historique", "source": "archives"}
        }
    ]
    
    # Ajout des documents
    rag.add_documents(sample_documents)
    
    # Affichage des stats
    stats = rag.get_collection_stats()
    print(f"\nStatistiques: {stats}")
    
    return rag


# Test du pipeline
if __name__ == "__main__":
    print("=== Test du Pipeline RAG ===\n")
    
    # Initialisation avec données d'exemple
    rag = initialize_can2025_knowledge()
    
    # Test de recherche
    print("\n=== Test de recherche ===")
    query = "Qui est le champion en titre de la CAN?"
    print(f"Requête: {query}\n")
    
    context = rag.retrieve_context(query, n_results=2)
    print("Contexte récupéré:")
    print(context)
    
    # Test 2
    print("\n=== Test 2 ===")
    query2 = "Où se déroule la CAN 2025?"
    print(f"Requête: {query2}\n")
    
    results = rag.search(query2, n_results=1)
    print("Résultat:")
    if results:
        print(f"- {results[0]['text']}")
