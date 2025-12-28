"""
Interface LLM pour l'Assistant IA CAN 2025
Ce module gère les interactions avec les modèles de langage (Groq, OpenAI GPT, etc.)
"""

from typing import Optional, List, Dict
import os
from groq import Groq
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMInterface:
    """
    Interface pour interagir avec les Large Language Models
    Supporte Groq (gratuit) et OpenAI GPT
    """
    
    def __init__(self, provider: str = "groq", model_name: Optional[str] = None, temperature: float = 0.7):
        """
        Initialise l'interface LLM
        
        Args:
            provider: Fournisseur LLM ("groq" ou "openai")
            model_name: Nom du modèle à utiliser (si None, utilise le défaut du provider)
            temperature: Contrôle la créativité des réponses (0.0 = déterministe, 1.0 = créatif)
        """
        self.provider = provider.lower()
        self.temperature = temperature
        
        # Configuration selon le provider
        if self.provider == "groq":
            self.api_key = os.getenv("GROQ_API_KEY")
            if not self.api_key:
                raise ValueError("GROQ_API_KEY non trouvée dans les variables d'environnement")
            self.client = Groq(api_key=self.api_key)
            # Modèles Groq disponibles: llama-3.3-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b-32768, gemma2-9b-it
            self.model_name = model_name or "llama-3.3-70b-versatile"
        
        elif self.provider == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY non trouvée dans les variables d'environnement")
            self.client = OpenAI(api_key=self.api_key)
            self.model_name = model_name or "gpt-3.5-turbo"
        
        else:
            raise ValueError(f"Provider '{provider}' non supporté. Utilisez 'groq' ou 'openai'")
        
    def chat(self, user_message: str, context: Optional[str] = None, 
             system_prompt: Optional[str] = None) -> str:
        """
        Envoie un message au chatbot et retourne la réponse
        
        Args:
            user_message: Question ou message de l'utilisateur
            context: Contexte additionnel (documents RAG, etc.)
            system_prompt: Instructions système pour le modèle
            
        Returns:
            Réponse du modèle
        """
        # Prompt système par défaut pour le chatbot CAN 2025
        if system_prompt is None:
            system_prompt = """Tu es un assistant intelligent spécialisé dans la Coupe d'Afrique des Nations (CAN) 2025.
Tu dois répondre aux questions sur:
- Les matchs programmés et résultats
- Les équipes participantes et compositions
- Les joueurs et leurs statistiques (âge, club, buts, valeur marchande, etc.)
- L'historique de la CAN
- Les stades et l'organisation

IMPORTANT:
- Utilise TOUJOURS les informations du contexte fourni pour répondre
- Pour les questions de comparaison (meilleur, plus cher, etc.), analyse TOUS les joueurs dans le contexte
- Les valeurs marchandes sont en euros (€)
- Sois précis avec les chiffres (valeurs, buts, sélections)
- Si tu dois comparer ou classer, cite tous les joueurs pertinents du contexte

Réponds de manière précise, concise et professionnelle.
Si tu ne connais pas une information qui n'est pas dans le contexte, dis-le clairement."""

        # Construction des messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Ajout du contexte si disponible
        if context:
            messages.append({
                "role": "system",
                "content": f"Contexte additionnel:\n{context}"
            })
        
        messages.append({"role": "user", "content": user_message})
        
        # Appel à l'API OpenAI
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erreur lors de la génération de la réponse: {str(e)}"
    
    def summarize_match(self, match_text: str) -> str:
        """
        Génère un résumé automatique d'un match à partir d'un texte
        
        Args:
            match_text: Texte du rapport/article de match
            
        Returns:
            Résumé structuré du match
        """
        system_prompt = """Tu es un expert en résumé d'articles sportifs.
Génère un résumé concis et structuré du match incluant:
- Le score final
- Les moments clés (buts, cartons, occasions)
- Les performances notables
- Une conclusion courte

Format: 100-150 mots maximum, style journalistique."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Résume ce match:\n\n{match_text}"}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.5,  # Moins de créativité pour les résumés
                max_tokens=300
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erreur lors du résumé: {str(e)}"
    
    def extract_info(self, query: str, documents: List[str]) -> str:
        """
        Extrait des informations spécifiques depuis des documents
        
        Args:
            query: Question de l'utilisateur
            documents: Liste de documents pertinents
            
        Returns:
            Réponse basée sur les documents
        """
        context = "\n\n".join([f"Document {i+1}:\n{doc}" for i, doc in enumerate(documents)])
        
        system_prompt = """Tu es un assistant qui extrait des informations précises depuis des documents.
Réponds uniquement en te basant sur les documents fournis.
Si l'information n'est pas dans les documents, dis-le clairement."""

        return self.chat(query, context=context, system_prompt=system_prompt)
    
    def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """
        Analyse le sentiment d'un texte (positif, négatif, neutre)
        Utilisé pour analyser les messages de supporters sur les réseaux sociaux
        
        Args:
            text: Texte à analyser (tweet, commentaire, etc.)
            
        Returns:
            Dictionnaire avec sentiment et score
        """
        system_prompt = """Tu es un expert en analyse de sentiment pour le football.
Analyse le sentiment du message fourni et réponds UNIQUEMENT avec un JSON au format suivant:
{"sentiment": "positif|neutre|negatif", "score": 0.0-1.0, "explication": "courte raison"}

Critères:
- positif: Soutien, encouragement, joie, fierté
- neutre: Information factuelle, analyse objective
- negatif: Critique, déception, colère, frustration

Score: 0.0 (très négatif) à 1.0 (très positif)"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyse ce message de supporter:\n\n{text}"}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.3,  # Peu de créativité pour l'analyse
                max_tokens=150
            )
            
            result_text = response.choices[0].message.content
            
            # Tenter de parser le JSON
            import json
            try:
                result = json.loads(result_text)
                return result
            except json.JSONDecodeError:
                # Si le parsing échoue, extraire manuellement
                if "positif" in result_text.lower():
                    sentiment = "positif"
                    score = 0.8
                elif "negatif" in result_text.lower() or "négatif" in result_text.lower():
                    sentiment = "negatif"
                    score = 0.2
                else:
                    sentiment = "neutre"
                    score = 0.5
                
                return {
                    "sentiment": sentiment,
                    "score": score,
                    "explication": result_text
                }
            
        except Exception as e:
            return {
                "sentiment": "erreur",
                "score": 0.5,
                "explication": f"Erreur d'analyse: {str(e)}"
            }
    
    def recommend_content(self, user_preferences: Dict[str, any], available_content: List[Dict]) -> dict:
        """
        Recommande du contenu personnalisé basé sur les préférences utilisateur
        
        Args:
            user_preferences: Dictionnaire avec équipes favorites, joueurs, type de contenu
            available_content: Liste de contenus disponibles
            
        Returns:
            Liste de contenus recommandés avec scores
        """
        # Préparer le contexte
        prefs_text = f"""Préférences utilisateur:
- Équipes favorites: {', '.join(user_preferences.get('favorite_teams', []))}
- Joueurs favoris: {', '.join(user_preferences.get('favorite_players', []))}
- Types de contenu préférés: {', '.join(user_preferences.get('content_types', ['matchs', 'résumés', 'statistiques']))}"""

        content_text = "\n".join([
            f"{i+1}. {c.get('title', 'Sans titre')} - {c.get('type', 'Contenu')} - {c.get('description', '')}"
            for i, c in enumerate(available_content)
        ])
        
        system_prompt = """Tu es un système de recommandation de contenu sportif.
Analyse les préférences de l'utilisateur et recommande les 5 meilleurs contenus.
Pour chaque recommandation, fournis un score de 0 à 10 et une raison courte.

Format de réponse:
1. [Titre] - Score: X/10 - Raison: ...
2. [Titre] - Score: X/10 - Raison: ...
etc."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{prefs_text}\n\nContenus disponibles:\n{content_text}"}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.5,
                max_tokens=500
            )
            
            recommendations_text = response.choices[0].message.content
            
            # Parser les recommandations (retourner le texte brut pour simplification)
            return {
                "recommendations": recommendations_text,
                "based_on": user_preferences
            }
            
        except Exception as e:
            return {
                "recommendations": f"Erreur lors de la recommandation: {str(e)}",
                "based_on": user_preferences
            }


# Exemple d'utilisation
if __name__ == "__main__":
    # Test de l'interface
    try:
        llm = LLMInterface()
        
        # Test chatbot
        response = llm.chat("Qui a gagné la CAN 2023?")
        print("Chatbot:", response)
        
        # Test résumé
        match_text = """
        Le Maroc a remporté une victoire éclatante 3-1 contre le Sénégal en demi-finale.
        Achraf Hakimi a ouvert le score à la 23e minute. Le Sénégal a égalisé par Sadio Mané 
        en seconde période, mais Youssef En-Nesyri a marqué deux fois pour assurer la victoire.
        """
        summary = llm.summarize_match(match_text)
        print("\nRésumé:", summary)
        
    except Exception as e:
        print(f"Erreur: {e}")
