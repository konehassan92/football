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

# In[ ]:


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


# In[ ]:


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


# In[ ]:


equipes_standard


# In[ ]:


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

