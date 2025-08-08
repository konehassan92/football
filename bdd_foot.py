#!/usr/bin/env python
# coding: utf-8

# # Librairies

# In[80]:


import soccerdata as sd
import pandas as pd
from datetime import datetime, date, timedelta
import os


# In[81]:


print(sd.FBref())

fbref = sd.FBref(leagues="Big 5 European Leagues Combined", seasons=[2425])
print(fbref.__doc__)


# # BDD

# In[83]:


stat_joueurs = ['standard', 'keeper', 'keeper_adv', 'shooting', 'passing', 'passing_types', 
                'goal_shot_creation', 'defense', 'possession', 'playing_time', 'misc']
# Dictionnaire pour stocker les DataFrames
joueurs = {}

# Liste pour stocker les noms des tables créées
tables_crees = []

date_heure = datetime.now().strftime("%Y-%m-%d")

# Boucle pour traiter chaque thème/stat_joueurs
for theme in stat_joueurs:
    print(theme)
    
    # Lire les statistiques des joueurs
    joueurs[theme] = fbref.read_player_season_stats(stat_type=theme)
    
    # Modifier les colonnes du DataFrame
    joueurs[theme].columns = ['-'.join(filter(None, col)).strip() for col in joueurs[theme].columns.values]
    joueurs[theme].reset_index(inplace=True)
    joueurs[theme]["clé primaire"] = joueurs[theme]["player"].astype(str) + " - " + joueurs[theme]["team"].astype(str)
    joueurs[theme]["Date de téléchargement"] = date_heure
    joueurs[theme]["theme"] = str(theme)

    # Afficher les informations du DataFrame
    print(joueurs[theme].columns)
    print(joueurs[theme].info())
    print(joueurs[theme].shape)
    
    # Renommer les DataFrames pour utilisation séparée dans le notebook
    globals()[f'joueurs_{theme}'] = joueurs[theme]

    # Ajouter le nom de la table à la liste des tables créées
    tables_crees.append(f'joueurs_{theme}')

# Afficher la liste des tables créées
print("Tables créées:", tables_crees)


# In[84]:


stat_equipes = ['standard', 'keeper', 'keeper_adv', 'shooting', 'passing', 'passing_types', 'goal_shot_creation', 'defense', 'possession', 'playing_time', 'misc']

# Dictionnaire pour stocker les DataFrames
equipes = {}
# Liste pour stocker les noms des tables créées
tables_crees = []

# Boucle pour traiter chaque thème/stat_joueur
for theme in stat_equipes:
    print(theme)
    
    # Lire les statistiques des joueurs
    equipes[theme] = fbref.read_team_season_stats(stat_type=theme)
    
    # Modifier les colonnes du DataFrame
    equipes[theme].columns = ['-'.join(filter(None, col)).strip() for col in equipes[theme].columns.values]
    equipes[theme].reset_index(inplace=True)

    # Afficher les informations du DataFrame
    print(equipes[theme].columns)
    print(equipes[theme].info())
    print(equipes[theme].shape)
    
    # Renommer les DataFrames pour utilisation séparée dans le notebook
    globals()[f'equipes_{theme}'] = equipes[theme]
    
    # Ajouter le nom de la table à la liste des tables créées
    tables_crees.append(f'equipes_{theme}')
    

# Afficher la liste des tables créées
print("Tables créées:", tables_crees)


# # Nettoyage

# ##### Nom des nouvelles colonnes

# In[157]:


col_standard = [
    "ligue",                      # inchangé
    "saison",                      # inchangé
    "equipe",                        # inchangé
    "joueur",                      # inchangé
    "nationalite",                 # 'nation'
    "poste",                       # 'pos'
    "age",                         # 'age'
    "annee_naissance",            # 'born'

    # Temps de jeu
    "matchs_joues",               # 'Playing Time-MP'
    "titularisations",            # 'Playing Time-Starts'
    "minutes_jouees",            # 'Playing Time-Min'
    "matchs_90_minutes",         # 'Playing Time-90s'

    # Performance
    "buts",                       # 'Performance-Gls'
    "passes_decisives",          # 'Performance-Ast'
    "buts_plus_passes",          # 'Performance-G+A'
    "buts_hors_penalty",         # 'Performance-G-PK'
    "penaltys_marques",          # 'Performance-PK'
    "penaltys_tentes",           # 'Performance-PKatt'
    "cartons_jaunes",            # 'Performance-CrdY'
    "cartons_rouges",            # 'Performance-CrdR'

    # Expected (statistiques attendues)
    "buts_attendus",                         # 'Expected-xG'
    "buts_attendus_hors_penalty",           # 'Expected-npxG'
    "passes_attendues",                     # 'Expected-xAG'
    "buts_hors_penalty_plus_passes_attendues", # 'Expected-npxG+xAG'

    # Progression
    "conduites_progressives",     # 'Progression-PrgC'
    "passes_progressives",        # 'Progression-PrgP'
    "passes_progressives_recues", # 'Progression-PrgR'

    # Par 90 minutes
    "buts_par_90",                              # 'Per 90 Minutes-Gls'
    "passes_decisives_par_90",                 # 'Per 90 Minutes-Ast'
    "buts_plus_passes_par_90",                 # 'Per 90 Minutes-G+A'
    "buts_hors_penalty_par_90",                # 'Per 90 Minutes-G-PK'
    "buts_plus_passes_hors_penalty_par_90",    # 'Per 90 Minutes-G+A-PK'
    "buts_attendus_par_90",                    # 'Per 90 Minutes-xG'
    "passes_attendues_par_90",                 # 'Per 90 Minutes-xAG'
    "buts_plus_passes_attendues_par_90",       # 'Per 90 Minutes-xG+xAG'
    "buts_attendus_hors_penalty_par_90",       # 'Per 90 Minutes-npxG'
    "buts_hors_penalty_plus_passes_attendues_90", # 'Per 90 Minutes-npxG+xAG'

    # Autres
    "cle_primaire",               # 'clé primaire'
    "date_telechargement",        # 'Date de téléchargement'
    "theme"                       # 'theme'
]


col_gardien = [
    "ligue",                          # inchangé
    "saison",                          # inchangé
    "equipe",                            # inchangé
    "joueur",                          # inchangé
    "nationalite",                     # nation
    "poste",                           # pos
    "age",                             # age
    "annee_naissance",                # born

    # Temps de jeu
    "matchs_joues",                   # Playing Time-MP
    "titularisations",                # Playing Time-Starts
    "minutes_jouees",                # Playing Time-Min
    "matchs_90_minutes",             # 90s

    # Performance défensive gardien
    "buts_encaisses",                # Performance-GA
    "buts_encaisses_par_90",        # Performance-GA90
    "tirs_cadres_subis",            # Performance-SoTA
    "arrets",                        # Performance-Saves
    "pourcentage_arrets",           # Performance-Save%
    "victoires",                     # Performance-W
    "nuls",                          # Performance-D
    "defaites",                      # Performance-L
    "clean_sheets",                 # Performance-CS
    "pourcentage_clean_sheets",    # Performance-CS%

    # Penaltys
    "penaltys_tentes",              # Penalty Kicks-PKatt
    "penaltys_concedes",           # Penalty Kicks-PKA
    "penaltys_arretes",            # Penalty Kicks-PKsv
    "penaltys_rates",              # Penalty Kicks-PKm
    "pourcentage_arrets_penalty", # Penalty Kicks-Save%

    # Métadonnées
    "cle_primaire",                 # clé primaire
    "date_telechargement",          # Date de téléchargement
    "theme"                         # theme
]


col_actions_creation = [
    "ligue",                      # Ligue
    "saison",                     # Saison
    "equipe",                     # Équipe
    "joueur",                     # Joueur
    "nationalite",                # Nationalité
    "poste",                      # Poste
    "age",                        # Âge
    "annee_naissance",            # Année de naissance
    "temps_90s",                  # Temps de jeu en équivalent 90 minutes

    # Actions menant à un tir
    "action_tir_total",           # Total d’actions menant à un tir
    "action_tir_par_90",          # Actions menant à un tir par 90 minutes
    "action_tir_passes_vives",    # Passes en jeu menant à un tir
    "action_tir_passes_mortes",   # Passes arrêtées menant à un tir
    "action_tir_dribbles",        # Dribbles menant à un tir
    "action_tir_tirs",            # Tirs menant à un autre tir
    "action_tir_fautes_subies",   # Fautes subies menant à un tir
    "action_tir_actions_def",     # Actions défensives menant à un tir

    # Actions menant à un but
    "action_but_total",           # Total d’actions menant à un but
    "action_but_par_90",          # Actions menant à un but par 90 minutes
    "action_but_passes_vives",    # Passes en jeu menant à un but
    "action_but_passes_mortes",   # Passes arrêtées menant à un but
    "action_but_dribbles",        # Dribbles menant à un but
    "action_but_tirs",            # Tirs menant à un but
    "action_but_fautes_subies",   # Fautes subies menant à un but
    "action_but_actions_def",     # Actions défensives menant à un but

    # Autres colonnes techniques
    "cle_primaire",               # Clé primaire
    "date_telechargement",        # Date de téléchargement
    "theme"                       # Thème
]


# ## Joueurs

# In[123]:


joueurs_standard.columns = col_standard
joueurs_standard.columns


# In[135]:


joueurs_keeper.columns = col_gardien
joueurs_keeper.columns


# In[153]:


joueurs_goal_shot_creation.columns = col_tirs_creation
joueurs_goal_shot_creation.columns


# In[86]:


import nbformat
from nbconvert import PythonExporter

notebook_filename = "bdd_foot.ipynb"
script_filename = "bdd_foot.py"

with open(notebook_filename) as f:
    nb = nbformat.read(f, as_version=4)

exporter = PythonExporter()
source, _ = exporter.from_notebook_node(nb)

with open(script_filename, "w") as f:
    f.write(source)

