"""
Pipeline RAG (Retrieval-Augmented Generation) pour l'Assistant IA CAN 2025
Ce module gère le stockage vectoriel et la récupération contextuelle de documents
Auteur: [Votre Nom]
Projet: CAN 2025 - SBI Africa
Date: Décembre 2025"""

import os
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import pandas as pd
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
    avec TOUTES les vraies données depuis les fichiers CSV et markdown
    """
    rag = RAGPipeline()
    documents = []
    
    # Chemin vers les données
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    print("🔄 Chargement de TOUTES les données CAN 2025...\n")
    
    # 1. Charger les matchs depuis matches.csv
    try:
        matches_file = os.path.join(data_dir, 'matches.csv')
        if os.path.exists(matches_file):
            df_matches = pd.read_csv(matches_file)
            
            for idx, match in df_matches.iterrows():
                text = f"""Match {match['match_id']}: {match['team_a']} vs {match['team_b']}
Date: {match['date']} à {match['time']}
Stade: {match['stadium']}, {match['city']}
Phase: {match['stage']}
Score: {match['team_a']} {match.get('score_a', '')} - {match.get('score_b', '')} {match['team_b']}
Statut: {match['status']}
{match.get('notes', '')}"""
                
                documents.append({
                    "id": f"match_{match['match_id']}",
                    "text": text,
                    "metadata": {
                        "type": "match",
                        "match_id": str(match['match_id']),
                        "date": str(match['date']),
                        "stage": str(match['stage'])
                    }
                })
            print(f"✓ {len(df_matches)} matchs chargés")
    except Exception as e:
        print(f"⚠ Erreur matchs: {e}")
    
    # 2. Charger les équipes depuis teams.csv
    try:
        teams_file = os.path.join(data_dir, 'teams.csv')
        if os.path.exists(teams_file):
            df_teams = pd.read_csv(teams_file)
            
            for idx, team in df_teams.iterrows():
                text = f"""Équipe: {team['team_name']}
Groupe: {team['group']}
Classement FIFA: {team.get('fifa_rank', 'N/A')}
Entraîneur: {team.get('coach', 'N/A')}
Titres CAN: {team.get('titles', 0)}
Confédération: {team['confederation']}
Qualification: {team.get('qualification', 'Qualifié')}"""
                
                documents.append({
                    "id": f"team_{team['team_id']}",
                    "text": text,
                    "metadata": {
                        "type": "equipe",
                        "team_name": team['team_name'],
                        "group": str(team['group'])
                    }
                })
            print(f"✓ {len(df_teams)} équipes chargées")
    except Exception as e:
        print(f"⚠ Erreur équipes: {e}")
    
    # 3. Charger le classement depuis standings.csv
    try:
        standings_file = os.path.join(data_dir, 'standings.csv')
        if os.path.exists(standings_file):
            df_standings = pd.read_csv(standings_file)
            
            for idx, standing in df_standings.iterrows():
                text = f"""Classement {standing['group']}: {standing['team_name']}
Position: {standing['rank']}
Points: {standing['points']}
Matchs joués: {standing['played']}
Victoires: {standing['won']} | Nuls: {standing['draw']} | Défaites: {standing['lost']}
Buts pour: {standing['goals_for']} | Buts contre: {standing['goals_against']}
Différence de buts: {standing['goal_diff']}"""
                
                documents.append({
                    "id": f"standing_{standing['team_id']}",
                    "text": text,
                    "metadata": {
                        "type": "classement",
                        "team_name": standing['team_name'],
                        "group": standing['group']
                    }
                })
            print(f"✓ {len(df_standings)} classements chargés")
    except Exception as e:
        print(f"⚠ Erreur classements: {e}")
    
    # 4. Charger les meilleurs buteurs depuis top_scorers.csv
    try:
        scorers_file = os.path.join(data_dir, 'top_scorers.csv')
        if os.path.exists(scorers_file):
            df_scorers = pd.read_csv(scorers_file)
            
            for idx, scorer in df_scorers.iterrows():
                text = f"""Buteur: {scorer['player_name']} ({scorer['nationality']})
Équipe: {scorer['team']}
Âge: {scorer['age']} ans
Buts: {scorer['goals']}
Passes décisives: {scorer['assists']}
Matchs joués: {scorer['matches_played']}
Minutes jouées: {scorer['minutes_played']}"""
                
                documents.append({
                    "id": f"scorer_{scorer['player_id']}",
                    "text": text,
                    "metadata": {
                        "type": "buteur",
                        "player_name": scorer['player_name'],
                        "team": scorer['team']
                    }
                })
            print(f"✓ {len(df_scorers)} buteurs chargés")
    except Exception as e:
        print(f"⚠ Erreur buteurs: {e}")
    
    # 5. Charger les meilleurs passeurs depuis top_assists.csv
    try:
        assists_file = os.path.join(data_dir, 'top_assists.csv')
        if os.path.exists(assists_file):
            df_assists = pd.read_csv(assists_file)
            
            for idx, assister in df_assists.iterrows():
                text = f"""Passeur: {assister['player_name']} ({assister['nationality']})
Équipe: {assister['team']}
Âge: {assister['age']} ans
Passes décisives: {assister['assists']}
Buts: {assister['goals']}
Matchs joués: {assister['matches_played']}"""
                
                documents.append({
                    "id": f"assist_{assister['player_id']}",
                    "text": text,
                    "metadata": {
                        "type": "passeur",
                        "player_name": assister['player_name'],
                        "team": assister['team']
                    }
                })
            print(f"✓ {len(df_assists)} passeurs chargés")
    except Exception as e:
        print(f"⚠ Erreur passeurs: {e}")
    
    # 6. Charger les statistiques des équipes depuis team_statistics.csv
    try:
        team_stats_file = os.path.join(data_dir, 'team_statistics.csv')
        if os.path.exists(team_stats_file):
            df_team_stats = pd.read_csv(team_stats_file)
            
            for idx, stats in df_team_stats.iterrows():
                text = f"""Statistiques de {stats['team_name']}
Matchs joués: {stats['matches_played']}
Victoires: {stats['wins']} | Nuls: {stats['draws']} | Défaites: {stats['losses']}
Buts marqués: {stats['goals_for']}
Buts encaissés: {stats['goals_against']}
Clean sheets: {stats['clean_sheets']}
Matchs sans marquer: {stats['failed_to_score']}"""
                
                documents.append({
                    "id": f"stats_{stats['team_id']}",
                    "text": text,
                    "metadata": {
                        "type": "statistiques_equipe",
                        "team_name": stats['team_name']
                    }
                })
            print(f"✓ {len(df_team_stats)} statistiques équipes chargées")
    except Exception as e:
        print(f"⚠ Erreur stats équipes: {e}")
    
    # 7. Charger les stades depuis venues.csv
    try:
        venues_file = os.path.join(data_dir, 'venues.csv')
        if os.path.exists(venues_file):
            df_venues = pd.read_csv(venues_file)
            
            for idx, venue in df_venues.iterrows():
                text = f"""Stade: {venue['stadium_name']}
Ville: {venue['city']}
Pays: {venue['country']}
Capacité: {venue.get('capacity', 'N/A')} places"""
                
                documents.append({
                    "id": f"venue_{idx}",
                    "text": text,
                    "metadata": {
                        "type": "stade",
                        "stadium_name": venue['stadium_name'],
                        "city": venue['city']
                    }
                })
            print(f"✓ {len(df_venues)} stades chargés")
    except Exception as e:
        print(f"⚠ Erreur stades: {e}")
    
    # 8. Charger l'historique depuis can_historique.md
    try:
        history_file = os.path.join(data_dir, 'history', 'can_historique.md')
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history_content = f.read()
            
            # Diviser en sections
            sections = history_content.split('##')
            for i, section in enumerate(sections):
                if section.strip():
                    documents.append({
                        "id": f"historique_{i}",
                        "text": section.strip(),
                        "metadata": {
                            "type": "historique",
                            "source": "can_historique.md"
                        }
                    })
            print(f"✓ Historique CAN chargé")
    except Exception as e:
        print(f"⚠ Erreur historique: {e}")
    
    # Ajout des documents
    if documents:
        rag.add_documents(documents)
        stats = rag.get_collection_stats()
        print(f"\n✅ Base de connaissances complète: {stats['total_documents']} documents")
    else:
        print("⚠ Aucun document chargé")
    
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
