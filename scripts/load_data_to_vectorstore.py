"""
Script pour charger les données CSV dans ChromaDB
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.rag_pipeline import initialize_can2025_knowledge

if __name__ == "__main__":
    print("=" * 60)
    print("CHARGEMENT DES DONNÉES DANS CHROMADB")
    print("=" * 60)
    
    try:
        initialize_can2025_knowledge()
        print("\n" + "=" * 60)
        print("✅ SUCCÈS: Données chargées dans ChromaDB!")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ ERREUR: {e}")
        print("=" * 60)
        sys.exit(1)
