"""
Script de test pour vérifier si l'API-Football fonctionne
"""

import requests
import os
from dotenv import load_dotenv
import json

# Charger les variables d'environnement
load_dotenv()

def test_api_connection():
    """Teste la connexion à l'API-Football"""
    
    print("=" * 60)
    print("🧪 TEST DE L'API-FOOTBALL")
    print("=" * 60)
    print()
    
    # Récupérer la clé API
    api_key = os.getenv('FOOTBALL_API_KEY')
    
    if not api_key or api_key == 'your_rapidapi_key_here':
        print("❌ ERREUR: Clé API manquante ou invalide dans .env")
        print()
        print("📝 Instructions:")
        print("1. Créer un compte sur https://rapidapi.com")
        print("2. S'abonner à API-Football: https://rapidapi.com/api-sports/api/api-football")
        print("3. Choisir le plan GRATUIT (100 requêtes/jour)")
        print("4. Copier votre clé API")
        print("5. Mettre à jour FOOTBALL_API_KEY dans .env")
        return
    
    print(f"🔑 Clé API détectée: {api_key[:10]}...{api_key[-5:]}")
    print()
    
    # Configuration pour API-Football direct (pas RapidAPI)
    base_url = "https://v3.football.api-sports.io"
    headers = {
        'x-apisports-key': api_key
    }
    
    # Test 1: Statut de l'API
    print("📊 Test 1: Vérification du statut de l'API...")
    try:
        response = requests.get(f"{base_url}/status", headers=headers)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Connexion réussie!")
            print(f"   Account: {data['response']['account']}")
            print(f"   Requêtes restantes: {data['response']['requests']['current']}/{data['response']['requests']['limit_day']}")
        elif response.status_code == 403:
            print("   ❌ Erreur 403: Non autorisé")
            print(f"   Message: {response.json().get('message', 'N/A')}")
            print("   → Vérifiez que vous êtes abonné à l'API-Football sur RapidAPI")
        elif response.status_code == 429:
            print("   ❌ Erreur 429: Quota dépassé")
            print("   → Vous avez atteint la limite de 100 requêtes/jour")
        else:
            print(f"   ❌ Erreur {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print()
    
    # Test 2: Recherche de la CAN 2025
    print("📊 Test 2: Recherche de la compétition CAN 2025...")
    try:
        response = requests.get(
            f"{base_url}/leagues",
            headers=headers,
            params={'name': 'Africa Cup of Nations', 'season': 2025}
        )
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data['response']:
                print("   ✅ CAN 2025 trouvée!")
                league = data['response'][0]['league']
                print(f"   ID: {league['id']}")
                print(f"   Nom: {league['name']}")
                print(f"   Pays: {data['response'][0]['country']['name']}")
            else:
                print("   ⚠️  CAN 2025 non disponible dans l'API")
                print("   → Les données ne sont peut-être pas encore publiées")
        else:
            print(f"   ❌ Erreur {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print()
    
    # Test 3: Récupération de matchs récents
    print("📊 Test 3: Récupération de matchs africains récents...")
    try:
        response = requests.get(
            f"{base_url}/fixtures",
            headers=headers,
            params={'league': 1, 'last': 5}  # CAN league ID = 1
        )
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            matches = data['response']
            if matches:
                print(f"   ✅ {len(matches)} matchs récupérés")
                for match in matches[:3]:
                    home = match['teams']['home']['name']
                    away = match['teams']['away']['name']
                    score_home = match['goals']['home'] or '-'
                    score_away = match['goals']['away'] or '-'
                    print(f"   • {home} {score_home} - {score_away} {away}")
            else:
                print("   ⚠️  Aucun match trouvé")
        else:
            print(f"   ❌ Erreur {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print()
    print("=" * 60)
    print("📝 RÉSUMÉ")
    print("=" * 60)
    print()
    print("Si tous les tests passent ✅:")
    print("→ Vous pouvez exécuter: python scripts/data_fetcher.py")
    print()
    print("Si erreur 403 ❌:")
    print("→ Abonnez-vous à l'API sur https://rapidapi.com/api-sports/api/api-football")
    print()
    print("Si erreur 429 ❌:")
    print("→ Attendez demain (quota de 100 requêtes/jour)")
    print()


if __name__ == "__main__":
    test_api_connection()
