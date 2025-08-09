#!/usr/bin/env python
# coding: utf-8

# # Librairies

# In[ ]:


!pip install soccerdata


# In[2]:


import soccerdata as sd
import pandas as pd
from datetime import datetime, date, timedelta
import os


# In[3]:


print(sd.FBref())

fbref = sd.FBref(leagues="Big 5 European Leagues Combined", seasons=[2425])
print(fbref.__doc__)


# # BDD

# In[5]:


stat_joueurs = ['standard', 'keeper', 'keeper_adv', 'shooting', 'passing', 'passing_types', 
                'goal_shot_creation', 'defense', 'possession', 'playing_time', 'misc']
# Dictionnaire pour stocker les DataFrames
joueurs = {}

# Liste pour stocker les noms des tables créées
tables_crees = []


# Boucle pour traiter chaque thème/stat_joueurs
for theme in stat_joueurs:
    print(theme)
    
    # Lire les statistiques des joueurs
    joueurs[theme] = fbref.read_player_season_stats(stat_type=theme)
    
    # Modifier les colonnes du DataFrame
    joueurs[theme].columns = ['-'.join(filter(None, col)).strip() for col in joueurs[theme].columns.values]
    joueurs[theme].reset_index(inplace=True)
    joueurs[theme]["clé primaire"] = joueurs[theme]["player"].astype(str) + " - " + joueurs[theme]["team"].astype(str)
        
    # Renommer les DataFrames pour utilisation séparée dans le notebook
    globals()[f'joueurs_{theme}'] = joueurs[theme]

    # Ajouter le nom de la table à la liste des tables créées
    tables_crees.append(f'joueurs_{theme}')

# Afficher la liste des tables créées
print("Tables créées:", tables_crees)


# In[6]:


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

# In[9]:


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
]

col_gardiens_1 = [
    "ligue",                   # league
    "saison",                  # season
    "equipe",                  # team
    "joueur",                  # player
    "nationalite",             # nation
    "poste",                   # pos
    "age",                     # age
    "annee_naissance",         # born
    "temps_90s",               # 90s

    # Buts concédés
    "buts_encaisses",          # Goals-GA
    "penaltys_encaisses",      # Goals-PKA
    "coup_francs_encaisses",   # Goals-FK
    "corners_encaisses",       # Goals-CK
    "csc_encaisses",           # Goals-OG

    # Indicateurs Buts Attendues Après Tir (PSxG)
    "buts_att_ps",                # Buts attendus après tir (probabilité d'arrêt du gardien)
    "buts_att_ps_par_tir_cadre",  # Buts attendus après tir par tir cadré (difficulté des arrêts)
    "diff_buts_att_ps_encaisses", # Différence entre buts attendus après tir et buts encaissés (efficacité du gardien)
    "diff_buts_att_ps_encaisses_90", # Différence PSxG - buts encaissés par 90 min (performance normalisée)

    # Passes longues (lancées)
    "passes_longues_reussies", # Launched-Cmp
    "passes_longues_tentees",  # Launched-Att
    "passes_longues_pct",      # Launched-Cmp%

    # Passes du gardien
    "passes_tentees_gk",       # Passes-Att (GK)
    "remises_a_la_main",       # Passes-Thr
    "passes_lance_pct",        # Passes-Launch%
    "longueur_moyenne_passe",  # Passes-AvgLen

    # Dégagements au pied (goal kicks)
    "degagements_tentes",      # Goal Kicks-Att
    "degagements_pct_longs",   # Goal Kicks-Launch%
    "longueur_moyenne_degagement", # Goal Kicks-AvgLen

    # Centres subis
    "centres_subis",           # Crosses-Opp
    "centres_interceptes",     # Crosses-Stp
    "centres_interceptes_pct", # Crosses-Stp%

    # Gardien-libéro (Sweeper)
    "actions_def_hors_surface",      # Sweeper-#OPA
    "actions_def_hors_surface_par90",# Sweeper-#OPA/90
    "distance_moy_actions_def",      # Sweeper-AvgDist

    # Colonnes générales
    "cle_primaire",            # clé primaire
]


col_tirs = [
    "ligue",                 # league
    "saison",                # season
    "equipe",                # team
    "joueur",                # player
    "nationalite",           # nation
    "poste",                 # pos
    "age",                   # age
    "annee_naissance",       # born
    "temps_90s",             # 90s

    # Statistiques Standard de tirs
    "buts",                  # Standard-Gls (Buts marqués)
    "tirs_totaux",           # Standard-Sh (Tirs totaux, sans pénaltys)
    "tirs_cadres",           # Standard-SoT (Tirs cadrés, sans pénaltys)
    "pct_tirs_cadres",       # Standard-SoT% (Pourcentage de tirs cadrés)
    "tirs_par_90",           # Standard-Sh/90 (Tirs totaux par 90 minutes)
    "tirs_cadres_par_90",    # Standard-SoT/90 (Tirs cadrés par 90 minutes)
    "buts_par_tir",          # Standard-G/Sh (Buts par tir)
    "buts_par_tir_cadre",    # Standard-G/SoT (Buts par tir cadré)
    "distance_moy_tir",      # Standard-Dist (Distance moyenne des tirs en yards)
    "tirs_coup_franc",       # Standard-FK (Tirs sur coups francs)
    "penaltys_marques",      # Standard-PK (Pénaltys marqués)
    "penaltys_tentes",       # Standard-PKatt (Pénaltys tentés)

    # Indicateurs attendus (Expected)
    "buts_attendus_xg",          # Expected-xG (Buts attendus)
    "buts_attendus_np_xg",       # Expected-npxG (Buts attendus hors pénaltys)
    "buts_attendus_np_xg_par_tir", # Expected-npxG/Sh (Buts attendus hors pénaltys par tir)
    "diff_buts_buts_attendus",   # Expected-G-xG (Différence buts réels - buts attendus)
    "diff_buts_np_buts_attendus",# Expected-np:G-xG (Différence buts hors pénaltys - buts attendus hors pénaltys)

    # Colonnes générales
    "cle_primaire",          # clé primaire
]


col_passes = [
    "ligue",                  # league
    "saison",                 # season
    "equipe",                 # team
    "joueur",                 # player
    "nationalite",            # nation
    "poste",                  # pos
    "age",                    # age
    "annee_naissance",        # born
    "temps_90s",              # 90s Joué (minutes jouées divisées par 90)

    # Passes totales
    "passes_reussies",        # Total-Cmp : Passes réussies (y compris centres, corners, touches, coups francs, dégagements)
    "passes_tentees",         # Total-Att : Passes tentées (idem)
    "pct_reussite_passes",    # Total-Cmp% : Pourcentage de passes réussies (minimum 30 minutes jouées)
    "distance_totale_passes", # Total-TotDist : Distance totale parcourue par les passes réussies (en yards)
    "distance_progressive",   # Total-PrgDist : Distance progressive vers le but adverse des passes réussies (en yards)

    # Passes courtes (5 à 15 yards)
    "passes_courtes_reussies", # Short-Cmp : Passes courtes réussies
    "passes_courtes_tentees",  # Short-Att : Passes courtes tentées
    "pct_reussite_courtes",    # Short-Cmp% : % réussite passes courtes (minimum 30 minutes jouées)

    # Passes moyennes (15 à 30 yards)
    "passes_moyennes_reussies", # Medium-Cmp : Passes moyennes réussies
    "passes_moyennes_tentees",  # Medium-Att : Passes moyennes tentées
    "pct_reussite_moyennes",    # Medium-Cmp% : % réussite passes moyennes (minimum 30 minutes jouées)

    # Passes longues (> 30 yards)
    "passes_longues_reussies",  # Long-Cmp : Passes longues réussies
    "passes_longues_tentees",   # Long-Att : Passes longues tentées
    "pct_reussite_longues",     # Long-Cmp% : % réussite passes longues (minimum 30 minutes jouées)

    # Passes décisives et expected assists
    "passes_decisives",         # Ast : Passes décisives
    "buts_attendus_passe_decisive", # xAG : Buts attendus suite à une passe décisive
    "passes_attendues",         # Expected-xA : Passes attendues (probabilité d’assister un but)
    "diff_passes_decisives_attendues", # Expected-A-xAG : Différence passes décisives et passes attendues

    # Passes clés et progression
    "passes_cles",             # KP : Passes clés menant directement à un tir
    "passes_dans_tiers_final", # 1/3 : Passes complétées dans le dernier tiers du terrain (hors coups francs)
    "passes_dans_surface_penalite", # PPA : Passes dans la surface de réparation (hors coups francs)
    "centres_dans_surface_penalite", # CrsPA : Centres dans la surface (hors coups francs)
    "passes_progressives",     # PrgP : Passes progressives vers le but adverse (au moins 10 yards ou dans la surface)

    # Colonnes générales
    "cle_primaire",            # clé primaire
]


col_pass_types = [
    "ligue",                  # league
    "saison",                 # season
    "equipe",                 # team
    "joueur",                 # player
    "nationalite",            # nation
    "poste",                  # pos
    "age",                    # age
    "annee_naissance",        # born
    "temps_90s",              # 90s (minutes jouées divisées par 90)

    # Passes tentées
    "passes_tentees",         # Att : Passes tentées (inclut passes en jeu, corners, touches, coups francs, dégagements)

    # Types de passes
    "passes_vives",           # Pass Types-Live : Passes en jeu (live-ball passes)
    "passes_mortes",          # Pass Types-Dead : Passes arrêtées (dead-ball passes, ex : coups francs, corners, touches, dégagements)
    "passes_coups_francs",    # Pass Types-FK : Passes tentées sur coups francs
    "passes_passees_en_rupture", # Pass Types-TB : Passes en profondeur (through balls)
    "passes_deviation_large", # Pass Types-Sw : Passes transversales (> 40 yards de largeur)
    "centres",                # Pass Types-Crs : Centres
    "touches_reprises",       # Pass Types-TI : Touches de balle (throw-ins)
    "corners_tentes",         # Pass Types-CK : Corners tentés

    # Corners - type
    "corners_entrant",        # Corner Kicks-In : Corners rentrants (inswinging)
    "corners_sortant",        # Corner Kicks-Out : Corners sortants (outswinging)
    "corners_droits",         # Corner Kicks-Str : Corners directs (straight)

    # Résultats des passes
    "passes_reussies",        # Outcomes-Cmp : Passes réussies (inclut tous types)
    "passes_hors_jeu",        # Outcomes-Off : Passes hors-jeu
    "passes_bloquees",        # Outcomes-Blocks : Passes bloquées par adversaire

    # Colonnes générales
    "cle_primaire",           # clé primaire
]

col_def = [
    "ligue",                # league
    "saison",               # season
    "equipe",               # team
    "joueur",               # player
    "nationalite",          # nation
    "poste",                # pos
    "age",                  # age
    "annee_naissance",      # born
    "temps_90s",            # 90s (minutes jouées divisées par 90)

    # Tacles
    "nombre_tacles",                 # Tackles-Tkl : Nombre de tacles effectués
    "tacles_gagnes",                 # Tackles-TklW : Tacles gagnés (possession récupérée)
    "tacles_dans_1_3_defensif",     # Tackles-Def 3rd : Tacles dans le tiers défensif
    "tacles_dans_1_3_central",      # Tackles-Mid 3rd : Tacles dans le tiers central
    "tacles_dans_1_3_offensif",     # Tackles-Att 3rd : Tacles dans le tiers offensif

    # Duels / Challenges
    "dribbleurs_tacles",             # Challenges-Tkl : Nombre de dribbleurs taclés
    "duels_tentés",                  # Challenges-Att : Nombre de duels/challenges tentés (échoués + réussis)
    "pourcentage_dribbleurs_tacles",# Challenges-Tkl% : % de dribbleurs taclés (réussite)
    "duels_perdus",                  # Challenges-Lost : Duels/challenges perdus

    # Dégagements / Blocks
    "nombre_blocages",               # Blocks-Blocks : Nombre de blocages (du ballon)
    "tirs_blocques",                 # Blocks-Sh : Nombre de tirs bloqués
    "passes_blocquees",              # Blocks-Pass : Nombre de passes bloquées

    # Interceptions
    "interceptions",                 # Int : Interceptions

    # Tacles + Interceptions
    "tacles_plus_interceptions",    # Tkl+Int : Total tacles + interceptions

    # Dégagements
    "degagements",                  # Clr : Dégagements

    # Erreurs
    "erreurs",                     # Err : Erreurs menant à un tir adverse

    # Colonnes générales
    "cle_primaire",                # clé primaire
]

col_possession = [
    "ligue",                # league
    "saison",               # season
    "equipe",               # team
    "joueur",               # player
    "nationalite",          # nation
    "poste",                # pos
    "age",                  # age
    "annee_naissance",      # born
    "temps_90s",            # 90s (minutes jouées divisées par 90)

    # Touches de balle
    "touches_ballon",            # Touches-Touches : Nombre de touches de balle (recevoir, dribbler, passer compte comme 1)
    "touches_dans_surface_def",  # Touches-Def Pen : Touches dans la surface défensive
    "touches_dans_tiers_def",    # Touches-Def 3rd : Touches dans le tiers défensif
    "touches_dans_tiers_central",# Touches-Mid 3rd : Touches dans le tiers central
    "touches_dans_tiers_off",    # Touches-Att 3rd : Touches dans le tiers offensif
    "touches_dans_surface_off",  # Touches-Att Pen : Touches dans la surface offensive
    "touches_ballon_jeu",        # Touches-Live : Touches en jeu (hors corners, coups francs, touches, dégagements, penalties)

    # Dribbles / Take-Ons
    "dribbles_tentes",           # Take-Ons-Att : Tentatives de dribbles face à un défenseur
    "dribbles_reussis",          # Take-Ons-Succ : Dribbles réussis
    "pourcentage_reussite_dribble", # Take-Ons-Succ% : % de dribbles réussis
    "dribbles_subis",            # Take-Ons-Tkld : Nombre de fois taclé pendant un dribble
    "pourcentage_tacles_sur_dribble", # Take-Ons-Tkld% : % de tacles subis pendant un dribble

    # Courses avec le ballon
    "courses_total",             # Carries-Carries : Nombre de courses avec le ballon
    "distance_totale_courses",   # Carries-TotDist : Distance totale parcourue avec le ballon (yards)
    "distance_progressive_courses", # Carries-PrgDist : Distance progressive avec le ballon (vers le but adverse)
    "courses_progressives",      # Carries-PrgC : Courses progressives (au moins 10 yards vers le but dans les 6 derniers passes)
    "courses_dans_1_3_off",      # Carries-1/3 : Courses dans le tiers offensif
    "courses_dans_surface_off",  # Carries-CPA : Courses dans la surface de réparation adverse
    "mauvaises_receptions",     # Carries-Mis : Nombre de mauvaises réceptions / contrôles ratés
    "ballon_perdu",              # Carries-Dis : Nombre de pertes de balle après tacle adverse (hors dribbles)

    # Réceptions de passes
    "passes_recues",             # Receiving-Rec : Passes reçues avec succès
    "passes_recues_progressives",# Receiving-PrgR : Passes reçues progressives (vers le but adverse)

    # Colonnes générales
    "cle_primaire",             # clé primaire
]


col_tps_jeu = [
    "ligue",                # league
    "saison",               # season
    "equipe",               # team
    "joueur",               # player
    "nationalite",          # nation
    "poste",                # pos
    "age",                  # age
    "annee_naissance",      # born

    # Temps de jeu
    "matchs_joues",             # Playing Time-MP : Matchs joués par le joueur ou l’équipe
    "minutes_jouees",           # Playing Time-Min : Minutes jouées au total
    "minutes_par_match",        # Playing Time-Mn/MP : Minutes jouées en moyenne par match joué
    "pourcentage_minutes",      # Playing Time-Min% : Pourcentage de minutes jouées par rapport au total de l’équipe
    "temps_90s",                # Playing Time-90s : Minutes jouées divisées par 90

    # Titularisations
    "titularisations",          # Starts-Starts : Nombre de matchs commencés en tant que titulaire
    "minutes_par_titularisation", # Starts-Mn/Start : Minutes jouées en moyenne par match commencé
    "matchs_complets",          # Starts-Compl : Nombre de matchs joués en entier

    # Remplacements
    "entrées_remplacement",     # Subs-Subs : Nombre de matchs joués en tant que remplaçant
    "minutes_par_remplacement", # Subs-Mn/Sub : Minutes jouées en moyenne par match en tant que remplaçant
    "remplaçant_non_utilisé",   # Subs-unSub : Nombre de fois remplaçant non utilisé

    # Succès de l’équipe
    "points_par_match",          # Team Success-PPM : Moyenne de points par match avec le joueur sur le terrain
    "buts_pour_sur_terrain",    # Team Success-onG : Buts marqués par l’équipe lorsque le joueur est sur le terrain
    "buts_contre_sur_terrain",  # Team Success-onGA : Buts encaissés par l’équipe lorsque le joueur est sur le terrain
    "plus_moins",               # Team Success-+/- : Différence buts marqués - buts encaissés avec le joueur sur le terrain
    "plus_moins_par_90",        # Team Success-+/-90 : Plus/Moins par 90 minutes

    "plus_moins_net_90",        # Team Success-On-Off : Différence nette plus/moins par 90 minutes sur terrain vs hors terrain

    # Succès de l’équipe (xG)
    "xg_sur_terrain",           # Team Success (xG)-onxG : Buts attendus par l’équipe avec le joueur sur le terrain
    "xga_sur_terrain",          # Team Success (xG)-onxGA : Buts attendus encaissés par l’équipe avec le joueur sur le terrain
    "xg_plus_moins",            # Team Success (xG)-xG+/- : Différence buts attendus marqués - encaissés
    "xg_plus_moins_par_90",     # Team Success (xG)-xG+/-90 : Plus/Moins de buts attendus par 90 minutes
    "xg_plus_moins_net_90",     # Team Success (xG)-On-Off : Différence nette plus/moins de buts attendus par 90 minutes sur terrain vs hors terrain

    # Colonnes générales
    "cle_primaire",             # clé primaire
]

col_autres = [
    "ligue",                # league
    "saison",               # season
    "equipe",               # team
    "joueur",               # player
    "nationalite",          # nation
    "poste",                # pos
    "age",                  # age
    "annee_naissance",      # born
    "temps_90s",            # 90s (minutes jouées divisées par 90)

    # Cartons et fautes
    "cartons_jaunes",           # Performance-CrdY : Cartons jaunes
    "cartons_rouges",           # Performance-CrdR : Cartons rouges
    "second_carton_jaune",      # Performance-2CrdY : Deuxième carton jaune
    "fautes_commises",          # Performance-Fls : Fautes commises
    "fautes_subies",            # Performance-Fld : Fautes subies
    "hors_jeu",                 # Performance-Off : Hors-jeu
    "centres",                  # Performance-Crs : Centres
    "interceptions",            # Performance-Int : Interceptions
    "tacles_gagnes",            # Performance-TklW : Tacles gagnés
    "penalties_gagnes",         # Performance-PKwon : Penalties gagnés
    "penalties_concedes",       # Performance-PKcon : Penalties concédés
    "buts_contre_son_camp",    # Performance-OG : Buts contre son camp
    "recuperations_ballon",     # Performance-Recov : Récupérations de balle

    # Duels aériens
    "duels_aeriens_gagnes",     # Aerial Duels-Won : Duels aériens gagnés
    "duels_aeriens_perdus",     # Aerial Duels-Lost : Duels aériens perdus
    "pourcentage_duels_aeriens_gagnes", # Aerial Duels-Won% : Pourcentage de duels aériens gagnés

    # Colonnes générales
    "cle_primaire",             # clé primaire
]


# ## Joueurs

# In[11]:


joueurs_standard.columns = col_standard
joueurs_playing_time.columns = col_tps_jeu
joueurs_keeper.columns = col_gardien
joueurs_keeper_adv.columns = col_gardiens_1
joueurs_shooting.columns = col_tirs
joueurs_goal_shot_creation.columns = col_actions_creation
joueurs_passing.columns = col_passes
joueurs_passing_types.columns = col_pass_types
joueurs_possession.columns = col_possession
joueurs_defense.columns = col_def
joueurs_misc.columns = col_autres

# Liste de tuples (DataFrame, prefixe)
dfs_prefixes = [
    (joueurs_standard, "standard"),
    (joueurs_playing_time, "temps_jeu"),
    (joueurs_keeper, "gardien"),
    (joueurs_keeper_adv, "gardien_avance"),
    (joueurs_shooting, "tirs"),
    (joueurs_goal_shot_creation, "actions_creation"),
    (joueurs_passing, "passes"),
    (joueurs_passing_types, "types_passes"),
    (joueurs_possession, "possession"),
    (joueurs_defense, "defense"),
    (joueurs_misc, "autre")
]

key_cols = ["ligue", "saison", "equipe", "joueur", "nationalite", "poste", "age", "annee_naissance"]

for df, prefix in dfs_prefixes:
    new_columns = []
    for col in df.columns:
        if col in key_cols:
            new_columns.append(col)  # on garde le nom d'origine pour les clés
        else:
            new_columns.append(f"{prefix}_{col}")  # on ajoute le préfixe pour les autres colonnes
    df.columns = new_columns


print("Colonnes joueurs_standard :", joueurs_standard.columns.tolist())
print("*"*100)
print("Colonnes joueurs_playing_time :", joueurs_playing_time.columns.tolist())
print("*"*100)
print("Colonnes joueurs_keeper :", joueurs_keeper.columns.tolist())
print("*"*100)
print("*"*100)
print("Colonnes joueurs_keeper_adv :", joueurs_keeper_adv.columns.tolist())
print("*"*100)
print("Colonnes joueurs_shooting :", joueurs_shooting.columns.tolist())
print("*"*100)
print("Colonnes joueurs_goal_shot_creation :", joueurs_goal_shot_creation.columns.tolist())
print("*"*100)
print("Colonnes joueurs_passing :", joueurs_passing.columns.tolist())
print("*"*100)
print("Colonnes joueurs_passing_types :", joueurs_passing_types.columns.tolist())
print("*"*100)
print("Colonnes joueurs_possession :", joueurs_possession.columns.tolist())
print("*"*100)
print("Colonnes joueurs_defense :", joueurs_defense.columns.tolist())
print("*"*100)
print("Colonnes joueurs_misc :", joueurs_misc.columns.tolist())


# # Featuring engeniering

# In[86]:


# Extraction des DataFrames renommés dans une liste
dfs_renamed = [df for df, _ in dfs_prefixes]

# Fusion successive sur les colonnes clés
df_joueurs = dfs_renamed[0]
for df in dfs_renamed[1:]:
    df_joueurs = pd.merge(df_joueurs, df, on=key_cols, how='outer')

# Afficher les premières colonnes du résultat pour vérification
df_joueurs.columns
df_joueurs["date_chargement"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# In[92]:


df_joueurs


# In[90]:


#Exemple de selection
df = df_joueurs[key_cols + df_joueurs.filter(regex=r'^types_passes').columns.tolist()]
print(df["ligue"].unique())
print(df["equipe"].unique())
df[df["equipe"].str.contains("Marseille")]


# # Export sur Supabase en ligne

# In[94]:


from supabase import create_client, Client
import pandas as pd

key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNlcWx5bnV1cnR2YWZ2amhhc2VpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDc3MzA1NSwiZXhwIjoyMDcwMzQ5MDU1fQ.JNdpPJGyvL_zoEJEkAQQtNGMSA80pQwJMu33o2A4nyo"
url = "https://seqlynuurtvafvjhasei.supabase.co"

supabase: Client = create_client(url, key)

batch_size = 100

# Remplace les NaN par None pour éviter erreur JSON
records = df_joueurs.where(pd.notnull(df_joueurs), None).to_dict(orient='records')

for i in range(0, len(records), batch_size):
    batch = records[i:i+batch_size]
    response = supabase.table("joueurs").insert(batch).execute()

    # Gestion erreur selon attributs disponibles
    if hasattr(response, "error") and response.error is not None:
        print(f"Erreur lors de l'insertion batch {i} - {i+len(batch)} :", response.error)
        break
    elif hasattr(response, "status_code") and response.status_code >= 400:
        print(f"Erreur HTTP {response.status_code} lors de l'insertion batch {i} - {i+len(batch)}")
        break
    else:
        print(f"Lignes {i} à {i+len(batch)} insérées avec succès.")

