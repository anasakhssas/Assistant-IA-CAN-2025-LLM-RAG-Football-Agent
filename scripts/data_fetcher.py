"""
Script pour récupérer les données de la CAN 2025 depuis l'API-Football
et mettre à jour automatiquement les fichiers CSV
Auteur: [Votre Nom]
Projet: CAN 2025 - SBI Africa
Date: Décembre 2025"""

import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class CANDataFetcher:
    def __init__(self):
        self.api_key = os.getenv('FOOTBALL_API_KEY')  # API-Football direct key
        # Utiliser l'API directe de api-football.com (pas RapidAPI)
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-apisports-key': self.api_key
        }
        # ID de la compétition CAN 2025 (Africa Cup of Nations)
        self.league_id = 6  # Africa Cup of Nations (ID trouvé via API)
        self.season = 2025
        
    def fetch_teams(self):
        """Récupère la liste des équipes participantes à la CAN 2025"""
        url = f"{self.base_url}/teams"
        params = {
            'league': self.league_id,
            'season': self.season
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            teams = []
            if data['response']:
                for item in data['response']:
                    team = item['team']
                    teams.append({
                        'team_id': team['id'],
                        'team_name': team['name'],
                        'group': 'TBD',  # Sera mis à jour après le tirage
                        'fifa_rank': 0,  # À compléter manuellement
                        'confederation': 'CAF',
                        'coach': 'TBD',
                        'titles': 0,
                        'qualification': 'Qualifié'
                    })
            
            return teams
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des équipes: {e}")
            return []
    
    def fetch_matches(self):
        """Récupère les matchs de la CAN 2025"""
        url = f"{self.base_url}/fixtures"
        params = {
            'league': self.league_id,
            'season': self.season
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            matches = []
            if data['response']:
                for idx, fixture in enumerate(data['response'], 1):
                    match_date = datetime.fromisoformat(fixture['fixture']['date'].replace('Z', '+00:00'))
                    
                    # Déterminer le statut
                    status_map = {
                        'TBD': 'À venir',
                        'NS': 'À venir',
                        'FT': 'Terminé',
                        'LIVE': 'En cours',
                        'HT': 'Mi-temps',
                        'PST': 'Reporté'
                    }
                    status = status_map.get(fixture['fixture']['status']['short'], 'À venir')
                    
                    matches.append({
                        'match_id': idx,
                        'date': match_date.strftime('%Y-%m-%d'),
                        'time': match_date.strftime('%H:%M'),
                        'stage': fixture['league']['round'],
                        'team_a': fixture['teams']['home']['name'],
                        'team_b': fixture['teams']['away']['name'],
                        'stadium': fixture['fixture']['venue']['name'] or 'TBD',
                        'city': fixture['fixture']['venue']['city'] or 'TBD',
                        'score_a': fixture['goals']['home'] if fixture['goals']['home'] is not None else '',
                        'score_b': fixture['goals']['away'] if fixture['goals']['away'] is not None else '',
                        'status': status,
                        'notes': ''
                    })
            
            return matches
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matchs: {e}")
            return []
    
    def fetch_standings(self):
        """Récupère le classement des groupes"""
        url = f"{self.base_url}/standings"
        params = {
            'league': self.league_id,
            'season': self.season
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            standings = {}
            standings_list = []
            
            if data['response'] and len(data['response']) > 0:
                for league_standing in data['response'][0]['league']['standings']:
                    for team_data in league_standing:
                        team_id = team_data['team']['id']
                        standings[team_id] = {
                            'group': team_data['group'],
                            'rank': team_data['rank'],
                            'points': team_data['points'],
                            'played': team_data['all']['played'],
                            'won': team_data['all']['win'],
                            'draw': team_data['all']['draw'],
                            'lost': team_data['all']['lose']
                        }
                        
                        # Pour le fichier CSV
                        standings_list.append({
                            'team_id': team_id,
                            'team_name': team_data['team']['name'],
                            'group': team_data['group'],
                            'rank': team_data['rank'],
                            'points': team_data['points'],
                            'played': team_data['all']['played'],
                            'won': team_data['all']['win'],
                            'draw': team_data['all']['draw'],
                            'lost': team_data['all']['lose'],
                            'goals_for': team_data['all']['goals']['for'],
                            'goals_against': team_data['all']['goals']['against'],
                            'goal_diff': team_data['goalsDiff']
                        })
            
            return standings, standings_list
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du classement: {e}")
            return {}, []
    
    def fetch_top_scorers(self):
        """Récupère les meilleurs buteurs de la CAN 2025"""
        url = f"{self.base_url}/players/topscorers"
        params = {
            'league': self.league_id,
            'season': self.season
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            scorers = []
            if data['response']:
                for item in data['response']:
                    player = item['player']
                    stats = item['statistics'][0] if item['statistics'] else {}
                    
                    scorers.append({
                        'player_id': player['id'],
                        'player_name': player['name'],
                        'age': player['age'],
                        'nationality': player['nationality'],
                        'team': stats.get('team', {}).get('name', 'N/A'),
                        'goals': stats.get('goals', {}).get('total', 0),
                        'assists': stats.get('goals', {}).get('assists', 0),
                        'matches_played': stats.get('games', {}).get('appearences', 0),
                        'minutes_played': stats.get('games', {}).get('minutes', 0),
                        'photo': player.get('photo', '')
                    })
            
            return scorers
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des buteurs: {e}")
            return []
    
    def fetch_top_assists(self):
        """Récupère les meilleurs passeurs de la CAN 2025"""
        url = f"{self.base_url}/players/topassists"
        params = {
            'league': self.league_id,
            'season': self.season
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            assisters = []
            if data['response']:
                for item in data['response']:
                    player = item['player']
                    stats = item['statistics'][0] if item['statistics'] else {}
                    
                    assisters.append({
                        'player_id': player['id'],
                        'player_name': player['name'],
                        'age': player['age'],
                        'nationality': player['nationality'],
                        'team': stats.get('team', {}).get('name', 'N/A'),
                        'assists': stats.get('goals', {}).get('assists', 0),
                        'goals': stats.get('goals', {}).get('total', 0),
                        'matches_played': stats.get('games', {}).get('appearences', 0)
                    })
            
            return assisters
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des passeurs: {e}")
            return []
    
    def fetch_team_statistics(self):
        """Récupère les statistiques détaillées de toutes les équipes"""
        url = f"{self.base_url}/teams/statistics"
        
        stats_list = []
        
        # On devrait d'abord récupérer les équipes pour avoir leurs IDs
        teams = self.fetch_teams()
        
        for team in teams[:5]:  # Limiter à 5 équipes pour ne pas dépasser le quota
            params = {
                'league': self.league_id,
                'season': self.season,
                'team': team['team_id']
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data['response']:
                    stats = data['response']
                    fixtures = stats.get('fixtures', {})
                    goals = stats.get('goals', {})
                    
                    stats_list.append({
                        'team_id': team['team_id'],
                        'team_name': team['team_name'],
                        'matches_played': fixtures.get('played', {}).get('total', 0),
                        'wins': fixtures.get('wins', {}).get('total', 0),
                        'draws': fixtures.get('draws', {}).get('total', 0),
                        'losses': fixtures.get('loses', {}).get('total', 0),
                        'goals_for': goals.get('for', {}).get('total', {}).get('total', 0),
                        'goals_against': goals.get('against', {}).get('total', {}).get('total', 0),
                        'clean_sheets': stats.get('clean_sheet', {}).get('total', 0),
                        'failed_to_score': stats.get('failed_to_score', {}).get('total', 0)
                    })
                    
            except Exception as e:
                print(f"⚠️  Erreur stats pour {team['team_name']}: {e}")
                continue
        
        return stats_list
    
    def fetch_venues(self):
        """Récupère la liste des stades utilisés pour la CAN 2025"""
        # On extrait les stades depuis les matchs
        matches = self.fetch_matches()
        
        venues = {}
        for match in matches:
            stadium = match['stadium']
            city = match['city']
            
            if stadium != 'TBD' and stadium not in venues:
                venues[stadium] = {
                    'stadium_name': stadium,
                    'city': city,
                    'country': 'Maroc',
                    'capacity': 0  # À compléter manuellement
                }
        
        return list(venues.values())
    
    def update_csv_files(self):
        """Met à jour tous les fichiers CSV avec les données récupérées"""
        data_dir = os.path.dirname(__file__)
        
        print("🔄 Récupération COMPLÈTE des données de la CAN 2025...\n")
        total_files = 0
        
        # 1. Récupérer et mettre à jour les matchs
        print("📊 [1/7] Récupération des matchs...")
        matches = self.fetch_matches()
        if matches:
            df_matches = pd.DataFrame(matches)
            matches_file = os.path.join(data_dir, 'matches.csv')
            df_matches.to_csv(matches_file, index=False, encoding='utf-8')
            print(f"✅ {len(matches)} matchs → matches.csv")
            total_files += 1
        else:
            print("⚠️  Aucun match trouvé")
        
        # 2. Récupérer et mettre à jour les équipes
        print("\n📊 [2/7] Récupération des équipes...")
        teams = self.fetch_teams()
        standings_dict = {}
        standings_list = []
        
        if teams:
            # Récupérer le classement pour les groupes
            standings_dict, standings_list = self.fetch_standings()
            
            # Mettre à jour les groupes
            for team in teams:
                if team['team_id'] in standings_dict:
                    team['group'] = standings_dict[team['team_id']]['group']
            
            df_teams = pd.DataFrame(teams)
            teams_file = os.path.join(data_dir, 'teams.csv')
            df_teams.to_csv(teams_file, index=False, encoding='utf-8')
            print(f"✅ {len(teams)} équipes → teams.csv")
            total_files += 1
        else:
            print("⚠️  Aucune équipe trouvée")
        
        # 3. Sauvegarder le classement des groupes
        print("\n📊 [3/7] Récupération du classement...")
        if standings_list:
            df_standings = pd.DataFrame(standings_list)
            standings_file = os.path.join(data_dir, 'standings.csv')
            df_standings.to_csv(standings_file, index=False, encoding='utf-8')
            print(f"✅ {len(standings_list)} positions → standings.csv")
            total_files += 1
        else:
            print("⚠️  Classement non disponible")
        
        # 4. Récupérer les meilleurs buteurs
        print("\n📊 [4/7] Récupération des meilleurs buteurs...")
        scorers = self.fetch_top_scorers()
        if scorers:
            df_scorers = pd.DataFrame(scorers)
            scorers_file = os.path.join(data_dir, 'top_scorers.csv')
            df_scorers.to_csv(scorers_file, index=False, encoding='utf-8')
            print(f"✅ {len(scorers)} buteurs → top_scorers.csv")
            total_files += 1
        else:
            print("⚠️  Statistiques buteurs non disponibles")
        
        # 5. Récupérer les meilleurs passeurs
        print("\n📊 [5/7] Récupération des meilleurs passeurs...")
        assisters = self.fetch_top_assists()
        if assisters:
            df_assisters = pd.DataFrame(assisters)
            assisters_file = os.path.join(data_dir, 'top_assists.csv')
            df_assisters.to_csv(assisters_file, index=False, encoding='utf-8')
            print(f"✅ {len(assisters)} passeurs → top_assists.csv")
            total_files += 1
        else:
            print("⚠️  Statistiques passeurs non disponibles")
        
        # 6. Récupérer les statistiques des équipes
        print("\n📊 [6/7] Récupération des statistiques équipes...")
        team_stats = self.fetch_team_statistics()
        if team_stats:
            df_team_stats = pd.DataFrame(team_stats)
            team_stats_file = os.path.join(data_dir, 'team_statistics.csv')
            df_team_stats.to_csv(team_stats_file, index=False, encoding='utf-8')
            print(f"✅ {len(team_stats)} équipes → team_statistics.csv")
            total_files += 1
        else:
            print("⚠️  Statistiques équipes non disponibles")
        
        # 7. Récupérer les stades
        print("\n📊 [7/7] Extraction des stades...")
        venues = self.fetch_venues()
        if venues:
            df_venues = pd.DataFrame(venues)
            venues_file = os.path.join(data_dir, 'venues.csv')
            df_venues.to_csv(venues_file, index=False, encoding='utf-8')
            print(f"✅ {len(venues)} stades → venues.csv")
            total_files += 1
        else:
            print("⚠️  Aucun stade trouvé")
        
        print("\n" + "=" * 60)
        print(f"✨ Mise à jour terminée! {total_files} fichiers CSV créés/mis à jour")
        print("=" * 60)
        
        return total_files


def main():
    """Fonction principale"""
    print("=" * 60)
    print("🏆 CAN 2025 - Récupération automatique des données")
    print("=" * 60)
    print()
    
    # Vérifier la clé API
    api_key = os.getenv('FOOTBALL_API_KEY')
    if not api_key:
        print("❌ ERREUR: Clé API manquante!")
        print()
        print("📝 Instructions:")
        print("1. Créer un compte gratuit sur RapidAPI: https://rapidapi.com")
        print("2. S'abonner à l'API-Football: https://rapidapi.com/api-sports/api/api-football")
        print("3. Copier votre clé API")
        print("4. Ajouter dans .env: FOOTBALL_API_KEY=votre_cle_ici")
        print()
        print("💡 Limitation gratuite: 100 requêtes/jour")
        return
    
    # Créer l'instance et récupérer les données
    fetcher = CANDataFetcher()
    files_created = fetcher.update_csv_files()
    
    if files_created > 0:
        print()
        print("📁 Fichiers créés dans le dossier data/:")
        print("   • matches.csv          - Tous les matchs avec scores")
        print("   • teams.csv            - 24 équipes participantes")
        print("   • standings.csv        - Classement des groupes")
        print("   • top_scorers.csv      - Meilleurs buteurs")
        print("   • top_assists.csv      - Meilleurs passeurs")
        print("   • team_statistics.csv  - Statistiques détaillées")
        print("   • venues.csv           - Stades utilisés")
        print()
        print("🔄 Pour recharger la base vectorielle avec les nouvelles données:")
        print("   1. Supprimer: vectorstore/index/")
        print("   2. Redémarrer l'API: uvicorn api.main:app --reload")


if __name__ == "__main__":
    main()
