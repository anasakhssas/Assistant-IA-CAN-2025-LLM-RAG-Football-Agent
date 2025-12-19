"""
Utilitaires pour la gestion des données CAN
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
from config import logger, DATA_DIR


class DataManager:
    """Gestionnaire centralisé des données CAN"""
    
    def __init__(self):
        self.data_dir = DATA_DIR
        self.matches_file = self.data_dir / "matches.csv"
        self.teams_file = self.data_dir / "teams.csv"
        self.history_file = self.data_dir / "history" / "can_historique.md"
    
    def load_matches(self) -> Optional[pd.DataFrame]:
        """Charge les matchs depuis le CSV"""
        try:
            if self.matches_file.exists():
                df = pd.read_csv(self.matches_file)
                logger.info(f"✓ {len(df)} matchs chargés")
                return df
            else:
                logger.warning(f"Fichier {self.matches_file} introuvable")
                return None
        except Exception as e:
            logger.error(f"Erreur chargement matchs: {e}")
            return None
    
    def load_teams(self) -> Optional[pd.DataFrame]:
        """Charge les équipes depuis le CSV"""
        try:
            if self.teams_file.exists():
                df = pd.read_csv(self.teams_file)
                logger.info(f"✓ {len(df)} équipes chargées")
                return df
            else:
                logger.warning(f"Fichier {self.teams_file} introuvable")
                return None
        except Exception as e:
            logger.error(f"Erreur chargement équipes: {e}")
            return None
    
    def load_history(self) -> Optional[str]:
        """Charge l'historique depuis le markdown"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                logger.info(f"✓ Historique CAN chargé")
                return content
            else:
                logger.warning(f"Fichier {self.history_file} introuvable")
                return None
        except Exception as e:
            logger.error(f"Erreur chargement historique: {e}")
            return None
    
    def get_match_by_id(self, match_id: int) -> Optional[Dict]:
        """Récupère un match par son ID"""
        df = self.load_matches()
        if df is not None:
            match = df[df['match_id'] == match_id]
            if not match.empty:
                return match.iloc[0].to_dict()
        return None
    
    def get_team_by_name(self, team_name: str) -> Optional[Dict]:
        """Récupère une équipe par son nom"""
        df = self.load_teams()
        if df is not None:
            team = df[df['team_name'].str.lower() == team_name.lower()]
            if not team.empty:
                return team.iloc[0].to_dict()
        return None
    
    def get_matches_by_team(self, team_name: str) -> List[Dict]:
        """Récupère tous les matchs d'une équipe"""
        df = self.load_matches()
        if df is not None:
            matches = df[
                (df['team_a'].str.lower() == team_name.lower()) |
                (df['team_b'].str.lower() == team_name.lower())
            ]
            return matches.to_dict('records')
        return []
    
    def get_stats(self) -> Dict:
        """Récupère les statistiques globales"""
        matches_df = self.load_matches()
        teams_df = self.load_teams()
        
        stats = {
            'total_matches': len(matches_df) if matches_df is not None else 0,
            'total_teams': len(teams_df) if teams_df is not None else 0,
            'completed_matches': 0,
            'upcoming_matches': 0
        }
        
        if matches_df is not None:
            stats['completed_matches'] = len(matches_df[matches_df['status'] == 'Terminé'])
            stats['upcoming_matches'] = len(matches_df[matches_df['status'] == 'À venir'])
        
        return stats


# Instance globale
data_manager = DataManager()
