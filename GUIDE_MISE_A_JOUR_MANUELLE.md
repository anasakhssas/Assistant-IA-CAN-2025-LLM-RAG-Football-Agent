# 📝 Guide de Mise à Jour Manuelle - CAN 2025

## 🎯 Principe Simple

**Vous éditez les fichiers CSV dans `data/`**, c'est tout!

## 📁 Fichiers à Mettre à Jour

### 1. **data/matches.csv** - Scores des matchs

```csv
match_id,date,time,stage,team_a,team_b,stadium,city,score_a,score_b,status,notes
1,2025-12-21,18:00,Phase de groupes,Maroc,Guinée,Stade Mohammed V,Rabat,2,0,Terminé,
2,2025-12-21,21:00,Phase de groupes,Sénégal,Nigeria,Stade Prince Moulay Abdellah,Rabat,1,1,Terminé,
```

**Colonnes importantes:**
- `score_a`, `score_b` - Les scores
- `status` - `À venir`, `En cours`, `Mi-temps`, `Terminé`

### 2. **data/teams.csv** - Informations équipes

```csv
team_id,team_name,group,fifa_rank,confederation,coach,titles,qualification
1,Maroc,A,13,CAF,Walid Regragui,1,Pays hôte
```

### 3. **data/players.csv** - Statistiques joueurs

```csv
player_id,name,team,position,age,goals_international,caps,...
1,Achraf Hakimi,Maroc,Défenseur,26,9,70,...
```

## 🔄 Workflow Quotidien

### **Étape 1: Ouvrir le fichier**
```bash
# Avec VSCode
code data/matches.csv

# Ou avec Excel
start excel data/matches.csv

# Ou avec Notepad
notepad data/matches.csv
```

### **Étape 2: Modifier les données**

**Exemple - Ajouter un score:**
```
Avant: 3,2025-12-22,18:00,Phase de groupes,Égypte,Ghana,Stade Mohammed V,Rabat,,,À venir,

Après:  3,2025-12-22,18:00,Phase de groupes,Égypte,Ghana,Stade Mohammed V,Rabat,2,1,Terminé,
```

### **Étape 3: Sauvegarder**
- `Ctrl + S` dans VSCode/Notepad
- Sauvegarder dans Excel

### **Étape 4: Vérifier l'API**

L'API recharge automatiquement (grâce à `--reload`):
```bash
# Si l'API tourne déjà avec --reload, rien à faire!
# Elle détecte le changement et recharge ChromaDB
```

Si besoin de redémarrer manuellement:
```bash
# Terminal uvicorn
Ctrl+C
uvicorn api.main:app --reload
```

## ⚡ Mise à Jour Rapide

### Scénario: Match vient de se terminer

1. **Ouvrir** `data/matches.csv`
2. **Trouver** la ligne du match (par match_id ou équipes)
3. **Modifier**:
   - Colonne `score_a`: score équipe A
   - Colonne `score_b`: score équipe B
   - Colonne `status`: `Terminé`
4. **Sauvegarder** (`Ctrl+S`)
5. **Terminé!** L'API se met à jour automatiquement

**Temps total**: 30 secondes

## 📊 Exemples de Modifications

### Ajouter un nouveau match
```csv
14,2025-12-25,21:00,Quarts de finale,Maroc,Égypte,Stade Mohammed V,Rabat,,,À venir,
```

### Mettre à jour un classement
```csv
# Dans teams.csv
1,Maroc,A,13,CAF,Walid Regragui,1,Pays hôte,3,2,1,0,5,1
  # Ajoutez: pts,J,V,N,D,BP,BC
```

### Ajouter un joueur
```csv
# Dans players.csv
61,Youssef En-Nesyri,Maroc,Attaquant,26,22,52,25000000,Fenerbahçe,...
```

## ✅ Avantages

- 🚀 **Ultra rapide**: 30 secondes par mise à jour
- 🎯 **Simple**: Juste éditer un CSV
- 💪 **Contrôle total**: Vous décidez de tout
- 🔒 **Fiable**: Pas de dépendance API
- 📝 **Flexible**: Excel, VSCode, Notepad, tout fonctionne

## 🛠️ Outils Recommandés

### VSCode (recommandé)
```bash
code data/matches.csv
```
- Coloration syntaxique
- Formatage automatique
- Extension "Rainbow CSV"

### Excel
- Interface familière
- Filtres et tris faciles
- ⚠️ Attention à l'encodage UTF-8

### Notepad++
- Léger et rapide
- UTF-8 par défaut

## 🔄 Structure Actuelle

```
data/
├── matches.csv          # 13 matchs (à mettre à jour quotidiennement)
├── teams.csv            # 24 équipes
├── players.csv          # 60 joueurs
└── history/
    └── can_historique.md   # Historique CAN enrichi
```

## 💡 Astuces

**Backup avant modification:**
```bash
# Copier le fichier avant modification
Copy-Item data/matches.csv data/matches_backup.csv
```

**Vérifier le format CSV:**
- Séparateur: `,` (virgule)
- Encodage: UTF-8
- Pas d'espaces avant/après les virgules

**Tester après modification:**
```bash
# Ouvrir l'interface Streamlit
streamlit run frontend/app.py

# Poser une question: "Quel est le score du match Maroc vs Guinée?"
```

## 🚀 Mise en Production

Votre système est maintenant:
- ✅ **Simple**: Pas de complexité API
- ✅ **Fiable**: Données sous votre contrôle
- ✅ **Rapide**: Mise à jour en 30 secondes
- ✅ **Complet**: 126 documents indexés
- ✅ **Fonctionnel**: Tests à 100%

## 📞 Questions Fréquentes

**Q: Dois-je redémarrer l'API après chaque modification?**
R: Non! Avec `--reload`, l'API détecte les changements automatiquement.

**Q: Puis-je modifier plusieurs fichiers CSV à la fois?**
R: Oui! Modifiez tous les CSV nécessaires, sauvegardez, l'API rechargera tout.

**Q: Et si je fais une erreur dans le CSV?**
R: Gardez un backup. Le CSV est simple à corriger.

**Q: Combien de temps pour mettre à jour tous les scores du jour?**
R: 2-3 minutes maximum pour 3-4 matchs.

---

**Workflow final**: Éditer CSV → Sauvegarder → Terminé! 🎉
