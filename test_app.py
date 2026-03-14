import pytest
from models import *
from app import *
from datetime import date

# ==========================================
# CONFIGURATION BASE DE DONNÉES DE TEST
# ==========================================

@pytest.fixture
def setup_database():
    """Crée une base de données de test avant chaque test"""
    test_db = SqliteDatabase(':memory:')
    
    models_list = [Joueur, Match, EntrainementCollectif, EntrainementIndividuel, 
                   ParticipationMatch, PresenceCollectif, PresenceIndividuel, Blessure]
    
    test_db.bind(models_list)
    test_db.connect()
    test_db.create_tables(models_list)
    
    yield test_db
    
    test_db.drop_tables(models_list)
    test_db.close()

# ==========================================
# TESTS DES FONCTIONS MÉTIER - JOUEURS
# ==========================================

def test_creer_joueur(setup_database):
    """Test : Fonction creer_joueur"""
    joueur = creer_joueur("Antoine", "Griezmann", "1991-03-21", "Attaquant", "2024-01-01")
    
    assert joueur.id_joueur is not None
    assert joueur.prenom == "Antoine"
    assert joueur.nom == "Griezmann"
    assert joueur.poste == "Attaquant"

def test_obtenir_tous_joueurs(setup_database):
    """Test : Fonction obtenir_tous_joueurs"""
    creer_joueur("Kylian", "Mbappé", "1998-12-20", "Attaquant", "2024-01-01")
    creer_joueur("Antoine", "Griezmann", "1991-03-21", "Attaquant", "2024-01-01")
    
    joueurs = obtenir_tous_joueurs()
    assert joueurs.count() == 2

def test_obtenir_joueur_par_id(setup_database):
    """Test : Fonction obtenir_joueur_par_id"""
    joueur = creer_joueur("Paul", "Pogba", "1993-03-15", "Milieu", "2024-01-01")
    
    joueur_trouve = obtenir_joueur_par_id(joueur.id_joueur)
    assert joueur_trouve is not None
    assert joueur_trouve.nom == "Pogba"

def test_modifier_joueur_poste(setup_database):
    """Test : Fonction modifier_joueur_poste"""
    joueur = creer_joueur("Hugo", "Lloris", "1986-12-26", "Gardien", "2024-01-01")
    
    joueur_modifie = modifier_joueur_poste(joueur.id_joueur, "Milieu")
    assert joueur_modifie is not None
    assert joueur_modifie.poste == "Milieu"

def test_supprimer_joueur_par_id(setup_database):
    """Test : Fonction supprimer_joueur_par_id"""
    joueur = creer_joueur("Test", "Player", "1990-01-01", "Attaquant", "2024-01-01")
    id_joueur = joueur.id_joueur
    
    resultat = supprimer_joueur_par_id(id_joueur)
    assert resultat is True
    
    joueur_supprime = obtenir_joueur_par_id(id_joueur)
    assert joueur_supprime is None

# ==========================================
# TESTS DES FONCTIONS MÉTIER - MATCHS
# ==========================================

def test_creer_match(setup_database):
    """Test : Fonction creer_match"""
    match = creer_match("2024-03-15", "Paris FC", "Domicile", 3, 1)
    
    assert match.id_match is not None
    assert match.adversaire == "Paris FC"
    assert match.buts_pour == 3
    assert match.buts_contre == 1

def test_obtenir_tous_matchs(setup_database):
    """Test : Fonction obtenir_tous_matchs"""
    creer_match("2024-03-15", "Paris FC", "Domicile", 3, 1)
    creer_match("2024-03-20", "Lyon", "Extérieur", 2, 2)
    
    matchs = obtenir_tous_matchs()
    assert matchs.count() == 2

def test_modifier_score_match(setup_database):
    """Test : Fonction modifier_score_match"""
    match = creer_match("2024-03-15", "Marseille", "Domicile", 0, 0)
    
    match_modifie = modifier_score_match(match.id_match, 2, 1)
    assert match_modifie is not None
    assert match_modifie.buts_pour == 2
    assert match_modifie.buts_contre == 1

def test_supprimer_match_par_id(setup_database):
    """Test : Fonction supprimer_match_par_id"""
    match = creer_match("2024-03-30", "Nice", "Extérieur", 1, 3)
    id_match = match.id_match
    
    resultat = supprimer_match_par_id(id_match)
    assert resultat is True
    
    match_supprime = obtenir_match_par_id(id_match)
    assert match_supprime is None

def test_obtenir_matchs_gagnes(setup_database):
    """Test : Fonction obtenir_matchs_gagnes"""
    creer_match("2024-03-01", "Team A", "Domicile", 3, 1)
    creer_match("2024-03-08", "Team B", "Extérieur", 1, 2)
    creer_match("2024-03-15", "Team C", "Domicile", 2, 2)
    
    matchs_gagnes = obtenir_matchs_gagnes()
    assert matchs_gagnes.count() == 1

def test_obtenir_matchs_perdus(setup_database):
    """Test : Fonction obtenir_matchs_perdus"""
    creer_match("2024-03-01", "Team A", "Domicile", 3, 1)
    creer_match("2024-03-08", "Team B", "Extérieur", 1, 2)
    
    matchs_perdus = obtenir_matchs_perdus()
    assert matchs_perdus.count() == 1

def test_obtenir_matchs_nuls(setup_database):
    """Test : Fonction obtenir_matchs_nuls"""
    creer_match("2024-03-01", "Team A", "Domicile", 3, 1)
    creer_match("2024-03-15", "Team C", "Domicile", 2, 2)
    
    matchs_nuls = obtenir_matchs_nuls()
    assert matchs_nuls.count() == 1

# ==========================================
# TESTS DES FONCTIONS MÉTIER - ENTRAÎNEMENTS
# ==========================================

def test_creer_entrainement_collectif(setup_database):
    """Test : Fonction creer_entrainement_collectif"""
    entrainement = creer_entrainement_collectif("2024-03-10", "Collectif", 90, "Tactique", 7)
    
    assert entrainement.id_entrainement is not None
    assert entrainement.type_entrainement_co == "Tactique"
    assert entrainement.duree_minutes == 90

def test_obtenir_tous_entrainements_collectifs(setup_database):
    """Test : Fonction obtenir_tous_entrainements_collectifs"""
    creer_entrainement_collectif("2024-03-10", "Collectif", 90, "Tactique", 7)
    creer_entrainement_collectif("2024-03-12", "Collectif", 60, "Physique", 5)
    
    entrainements = obtenir_tous_entrainements_collectifs()
    assert entrainements.count() == 2

def test_modifier_entrainement_collectif(setup_database):
    """Test : Fonction modifier_entrainement_collectif"""
    entrainement = creer_entrainement_collectif("2024-03-11", "Collectif", 60, "Physique", 5)
    
    entrainement_modifie = modifier_entrainement_collectif(entrainement.id_entrainement, "Tactique", 8)
    assert entrainement_modifie is not None
    assert entrainement_modifie.type_entrainement_co == "Tactique"
    assert entrainement_modifie.difficulte_co == 8

def test_creer_entrainement_individuel(setup_database):
    """Test : Fonction creer_entrainement_individuel"""
    entrainement = creer_entrainement_individuel("2024-03-12", "Améliorer vitesse", 60, "Cardio", 8)
    
    assert entrainement.id_entrainement is not None
    assert entrainement.objectif == "Améliorer vitesse"

# ==========================================
# TESTS DES FONCTIONS MÉTIER - PARTICIPATIONS
# ==========================================

def test_creer_participation_match(setup_database):
    """Test : Fonction creer_participation_match"""
    joueur = creer_joueur("Karim", "Benzema", "1987-12-19", "Attaquant", "2024-01-01")
    match = creer_match("2024-03-15", "Monaco", "Domicile", 4, 2)
    
    participation = creer_participation_match(joueur.id_joueur, match.id_match, 90, 2, 1)
    
    assert participation.buts == 2
    assert participation.passes_decisives == 1

def test_modifier_participation_match(setup_database):
    """Test : Fonction modifier_participation_match"""
    joueur = creer_joueur("Test", "Player", "1990-01-01", "Attaquant", "2024-01-01")
    match = creer_match("2024-03-15", "Test Team", "Domicile", 1, 0)
    
    creer_participation_match(joueur.id_joueur, match.id_match, 45, 0, 0)
    
    participation_modifiee = modifier_participation_match(joueur.id_joueur, match.id_match, 90, 1, 1)
    assert participation_modifiee is not None
    assert participation_modifiee.minutes_jouees == 90
    assert participation_modifiee.buts == 1

def test_supprimer_participation_match(setup_database):
    """Test : Fonction supprimer_participation_match"""
    joueur = creer_joueur("Test", "Player", "1990-01-01", "Attaquant", "2024-01-01")
    match = creer_match("2024-03-15", "Test Team", "Domicile", 1, 0)
    
    creer_participation_match(joueur.id_joueur, match.id_match, 90, 1, 0)
    
    resultat = supprimer_participation_match(joueur.id_joueur, match.id_match)
    assert resultat is True

def test_obtenir_stats_globales_joueur(setup_database):
    """Test : Fonction obtenir_stats_globales_joueur"""
    joueur = creer_joueur("Olivier", "Giroud", "1986-09-30", "Attaquant", "2024-01-01")
    
    match1 = creer_match("2024-03-01", "Team A", "Domicile", 3, 1)
    match2 = creer_match("2024-03-08", "Team B", "Extérieur", 2, 2)
    
    creer_participation_match(joueur.id_joueur, match1.id_match, 90, 2, 1)
    creer_participation_match(joueur.id_joueur, match2.id_match, 85, 1, 0)
    
    stats = obtenir_stats_globales_joueur(joueur.id_joueur)
    
    assert stats['total_buts'] == 3
    assert stats['total_passes'] == 1

def test_obtenir_joueurs_dans_match(setup_database):
    """Test : Fonction obtenir_joueurs_dans_match"""
    joueur1 = creer_joueur("Player", "One", "1990-01-01", "Attaquant", "2024-01-01")
    joueur2 = creer_joueur("Player", "Two", "1991-01-01", "Milieu", "2024-01-01")
    match = creer_match("2024-03-15", "Test Team", "Domicile", 2, 1)
    
    creer_participation_match(joueur1.id_joueur, match.id_match, 90, 1, 0)
    creer_participation_match(joueur2.id_joueur, match.id_match, 90, 1, 1)
    
    participations = obtenir_joueurs_dans_match(match.id_match)
    assert participations.count() == 2

# ==========================================
# TESTS DES FONCTIONS MÉTIER - PRÉSENCES
# ==========================================

def test_creer_presence_collectif(setup_database):
    """Test : Fonction creer_presence_collectif"""
    joueur = creer_joueur("Test", "Player", "1990-01-01", "Milieu", "2024-01-01")
    entrainement = creer_entrainement_collectif("2024-03-10", "Collectif", 90, "Tactique", 7)
    
    presence = creer_presence_collectif(joueur.id_joueur, entrainement.id_entrainement, 1)
    
    assert presence.present == 1

def test_modifier_presence_collectif(setup_database):
    """Test : Fonction modifier_presence_collectif"""
    joueur = creer_joueur("Test", "Player", "1990-01-01", "Milieu", "2024-01-01")
    entrainement = creer_entrainement_collectif("2024-03-10", "Collectif", 90, "Tactique", 7)
    
    creer_presence_collectif(joueur.id_joueur, entrainement.id_entrainement, 0)
    
    presence_modifiee = modifier_presence_collectif(joueur.id_joueur, entrainement.id_entrainement, 1)
    assert presence_modifiee is not None
    assert presence_modifiee.present == 1

def test_creer_presence_individuel(setup_database):
    """Test : Fonction creer_presence_individuel"""
    joueur = creer_joueur("Test", "Player", "1990-01-01", "Milieu", "2024-01-01")
    entrainement = creer_entrainement_individuel("2024-03-12", "Objectif test", 60, "Cardio", 8)
    
    presence = creer_presence_individuel(joueur.id_joueur, entrainement.id_entrainement)
    
    assert presence.id_joueur.id_joueur == joueur.id_joueur

# ==========================================
# TESTS DES MÉTHODES MÉTIER DES MODÈLES
# ==========================================

def test_joueur_str(setup_database):
    """Test : Méthode __str__ de Joueur"""
    joueur = creer_joueur("Antoine", "Griezmann", "1991-03-21", "Attaquant", "2024-01-01")
    assert str(joueur) == "Antoine Griezmann (Attaquant)"

def test_joueur_nom_complet(setup_database):
    """Test : Méthode nom_complet de Joueur"""
    joueur = creer_joueur("Kylian", "Mbappé", "1998-12-20", "Attaquant", "2024-01-01")
    assert joueur.nom_complet() == "Kylian Mbappé"

def test_joueur_age(setup_database):
    """Test : Méthode age de Joueur"""
    joueur = creer_joueur("Test", "Player", "2000-01-01", "Attaquant", "2024-01-01")
    age = joueur.age()
    assert age >= 24  # L'âge dépend de la date actuelle

def test_match_resultat(setup_database):
    """Test : Méthode resultat de Match"""
    match_victoire = creer_match("2024-03-15", "Team A", "Domicile", 3, 1)
    match_defaite = creer_match("2024-03-16", "Team B", "Extérieur", 1, 3)
    match_nul = creer_match("2024-03-17", "Team C", "Domicile", 2, 2)
    
    assert match_victoire.resultat() == "Victoire"
    assert match_defaite.resultat() == "Défaite"
    assert match_nul.resultat() == "Nul"

def test_match_est_victoire(setup_database):
    """Test : Méthodes est_victoire, est_defaite, est_nul de Match"""
    match = creer_match("2024-03-15", "Team A", "Domicile", 3, 1)
    
    assert match.est_victoire() is True
    assert match.est_defaite() is False
    assert match.est_nul() is False

def test_match_difference_buts(setup_database):
    """Test : Méthode difference_buts de Match"""
    match = creer_match("2024-03-15", "Team A", "Domicile", 4, 2)
    assert match.difference_buts() == 2

def test_entrainement_collectif_niveau_difficulte(setup_database):
    """Test : Méthode niveau_difficulte de EntrainementCollectif"""
    entrainement_facile = creer_entrainement_collectif("2024-03-10", "Collectif", 90, "Tactique", 2)
    entrainement_moyen = creer_entrainement_collectif("2024-03-11", "Collectif", 90, "Physique", 5)
    entrainement_difficile = creer_entrainement_collectif("2024-03-12", "Collectif", 90, "Technique", 9)
    
    assert entrainement_facile.niveau_difficulte() == "Facile"
    assert entrainement_moyen.niveau_difficulte() == "Moyen"
    assert entrainement_difficile.niveau_difficulte() == "Difficile"

def test_participation_contribution(setup_database):
    """Test : Méthode contribution de ParticipationMatch"""
    joueur = creer_joueur("Test", "Player", "1990-01-01", "Attaquant", "2024-01-01")
    match = creer_match("2024-03-15", "Test Team", "Domicile", 3, 1)
    
    participation = creer_participation_match(joueur.id_joueur, match.id_match, 90, 2, 1)
    assert participation.contribution() == 3  # 2 buts + 1 passe

def test_participation_a_joue_match_complet(setup_database):
    """Test : Méthode a_joue_match_complet de ParticipationMatch"""
    joueur = creer_joueur("Test", "Player", "1990-01-01", "Attaquant", "2024-01-01")
    match = creer_match("2024-03-15", "Test Team", "Domicile", 1, 0)
    
    participation_complete = creer_participation_match(joueur.id_joueur, match.id_match, 90, 1, 0)
    assert participation_complete.a_joue_match_complet() is True
    
    # Créer un autre joueur et match pour tester le cas incomplet
    joueur2 = creer_joueur("Test2", "Player2", "1991-01-01", "Milieu", "2024-01-01")
    match2 = creer_match("2024-03-16", "Test Team2", "Domicile", 1, 0)
    participation_incomplete = creer_participation_match(joueur2.id_joueur, match2.id_match, 45, 0, 0)
    assert participation_incomplete.a_joue_match_complet() is False

def test_presence_collectif_est_present(setup_database):
    """Test : Méthode est_present de PresenceCollectif"""
    joueur = creer_joueur("Test", "Player", "1990-01-01", "Milieu", "2024-01-01")
    entrainement = creer_entrainement_collectif("2024-03-10", "Collectif", 90, "Tactique", 7)
    
    presence = creer_presence_collectif(joueur.id_joueur, entrainement.id_entrainement, 1)
    assert presence.est_present() is True
