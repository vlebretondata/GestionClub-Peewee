from models import *
 
# ==========================================
# FONCTIONS MÉTIER (TESTABLES)
# ==========================================
 
# --- Joueurs ---
 
def creer_joueur(prenom, nom, date_naissance, poste, date_arrivee):
    """Créer un joueur dans la base de données"""
    return Joueur.create(
        prenom=prenom, nom=nom, date_naissance=date_naissance,
        poste=poste, date_arrivee=date_arrivee
    )
 
def obtenir_tous_joueurs():
    """Récupérer tous les joueurs"""
    return Joueur.select()
 
def obtenir_joueur_par_id(id_joueur):
    """Récupérer un joueur par son ID"""
    return Joueur.get_or_none(Joueur.id_joueur == id_joueur)
 
def modifier_joueur_poste(id_joueur, nouveau_poste):
    """Modifier le poste d'un joueur"""
    joueur = Joueur.get_or_none(Joueur.id_joueur == id_joueur)
    if joueur:
        joueur.poste = nouveau_poste
        joueur.save()
        return joueur
    return None
 
def supprimer_joueur_par_id(id_joueur):
    """Supprimer un joueur par son ID"""
    joueur = Joueur.get_or_none(Joueur.id_joueur == id_joueur)
    if joueur:
        joueur.delete_instance()
        return True
    return False
 
# --- Matchs ---
 
def creer_match(match_date, adversaire, localisation, buts_pour, buts_contre):
    """Créer un match dans la base de données"""
    return Match.create(
        match_date=match_date, adversaire=adversaire,
        localisation=localisation, buts_pour=buts_pour, buts_contre=buts_contre
    )
 
def obtenir_tous_matchs():
    """Récupérer tous les matchs"""
    return Match.select()
 
def obtenir_match_par_id(id_match):
    """Récupérer un match par son ID"""
    return Match.get_or_none(Match.id_match == id_match)
 
def modifier_score_match(id_match, buts_pour, buts_contre):
    """Modifier le score d'un match"""
    match = Match.get_or_none(Match.id_match == id_match)
    if match:
        match.buts_pour = buts_pour
        match.buts_contre = buts_contre
        match.save()
        return match
    return None
 
def supprimer_match_par_id(id_match):
    """Supprimer un match par son ID"""
    match = Match.get_or_none(Match.id_match == id_match)
    if match:
        match.delete_instance()
        return True
    return False
 
def obtenir_matchs_gagnes():
    """Récupérer les matchs gagnés"""
    return Match.select().where(Match.buts_pour > Match.buts_contre)
 
def obtenir_matchs_perdus():
    """Récupérer les matchs perdus"""
    return Match.select().where(Match.buts_pour < Match.buts_contre)
 
def obtenir_matchs_nuls():
    """Récupérer les matchs nuls"""
    return Match.select().where(Match.buts_pour == Match.buts_contre)
 
# --- Entraînements collectifs ---

 
def creer_entrainement_collectif(date_entrainement, type_e, duree_minutes, type_entrainement_co, difficulte_co):
    """Créer un entraînement collectif"""
    return EntrainementCollectif.create(
        date_entrainement=date_entrainement, type=type_e,
        duree_minutes=duree_minutes, type_entrainement_co=type_entrainement_co,
        difficulte_co=difficulte_co
    )
 
def obtenir_tous_entrainements_collectifs():
    """Récupérer tous les entraînements collectifs"""
    return EntrainementCollectif.select()
 
 
def supprimer_entrainement_collectif_par_id(id_entrainement):
    """Supprimer un entraînement collectif"""
    entrainement = EntrainementCollectif.get_or_none(EntrainementCollectif.id_entrainement == id_entrainement)
    if entrainement:
        entrainement.delete_instance()
        return True
    return False
 
def modifier_entrainement_collectif(id_entrainement, type_entrainement_co, difficulte_co):
    """Modifier un entraînement collectif"""
    entrainement = EntrainementCollectif.get_or_none(EntrainementCollectif.id_entrainement == id_entrainement)
    if entrainement:
        entrainement.type_entrainement_co = type_entrainement_co
        entrainement.difficulte_co = difficulte_co
        entrainement.save()
        return entrainement
    return None
 
# --- Entraînements individuels ---
 
def creer_entrainement_individuel(date_entrainement, objectif, duree_minutes, type_entrainement_ind, difficulte_ind):
    """Créer un entraînement individuel"""
    return EntrainementIndividuel.create(
        date_entrainement=date_entrainement, objectif=objectif,
        duree_minutes=duree_minutes, type_entrainement_ind=type_entrainement_ind,
        difficulte_ind=difficulte_ind
    )
 
def obtenir_tous_entrainements_individuels():
    """Récupérer tous les entraînements individuels"""
    return EntrainementIndividuel.select()
 
def supprimer_entrainement_individuel_par_id(id_entrainement):
    """Supprimer un entraînement individuel"""
    entrainement = EntrainementIndividuel.get_or_none(EntrainementIndividuel.id_entrainement == id_entrainement)
    if entrainement:
        entrainement.delete_instance()
        return True
    return False
 
def modifier_entrainement_individuel(id_entrainement, type_entrainement_ind, difficulte_ind):
    """Modifier un entraînement individuel"""
    entrainement = EntrainementIndividuel.get_or_none(EntrainementIndividuel.id_entrainement == id_entrainement)
    if entrainement:
        entrainement.type_entrainement_ind = type_entrainement_ind
        entrainement.difficulte_ind = difficulte_ind
        entrainement.save()
        return entrainement
    return None
 
# --- Participations ---
 
def creer_participation_match(id_joueur, id_match, minutes_jouees, buts, passes_decisives):
    """Créer une participation à un match"""
    return ParticipationMatch.create(
        id_joueur=id_joueur, id_match=id_match,
        minutes_jouees=minutes_jouees, buts=buts, passes_decisives=passes_decisives
    )
 
def modifier_participation_match(id_joueur, id_match, minutes_jouees, buts, passes_decisives):
    """Modifier les stats d'une participation"""
    participation = ParticipationMatch.get_or_none(
        (ParticipationMatch.id_joueur == id_joueur) & 
        (ParticipationMatch.id_match == id_match)
    )
    if participation:
        participation.minutes_jouees = minutes_jouees
        participation.buts = buts
        participation.passes_decisives = passes_decisives
        participation.save()
        return participation
    return None
 
def supprimer_participation_match(id_joueur, id_match):
    """Supprimer une participation"""
    participation = ParticipationMatch.get_or_none(
        (ParticipationMatch.id_joueur == id_joueur) & 
        (ParticipationMatch.id_match == id_match)
    )
    if participation:
        participation.delete_instance()
        return True
    return False
 
def obtenir_stats_globales_joueur(id_joueur):
    """Calculer les stats globales d'un joueur"""
    participations = ParticipationMatch.select().where(ParticipationMatch.id_joueur == id_joueur)
    total_buts = sum(p.buts for p in participations)
    total_passes = sum(p.passes_decisives for p in participations)
    return {'total_buts': total_buts, 'total_passes': total_passes}
 
def obtenir_joueurs_dans_match(id_match):
    """Récupérer les joueurs d'un match"""
    return (ParticipationMatch
            .select(ParticipationMatch, Joueur)
            .join(Joueur)
            .where(ParticipationMatch.id_match == id_match))
 
# --- Présences ---
 
def creer_presence_collectif(id_joueur, id_entrainement, present):
    """Créer une présence à un entraînement collectif"""
    return PresenceCollectif.create(
        id_joueur=id_joueur, id_entrainement=id_entrainement, present=present
    )
 
def modifier_presence_collectif(id_joueur, id_entrainement, present):
    """Modifier une présence collectif"""
    presence = PresenceCollectif.get_or_none(
        (PresenceCollectif.id_joueur == id_joueur) & 
        (PresenceCollectif.id_entrainement == id_entrainement)
    )
    if presence:
        presence.present = present
        presence.save()
        return presence
    return None
 
def supprimer_presence_collectif(id_joueur, id_entrainement):
    """Supprimer une présence collectif"""
    presence = PresenceCollectif.get_or_none(
        (PresenceCollectif.id_joueur == id_joueur) & 
        (PresenceCollectif.id_entrainement == id_entrainement)
    )
    if presence:
        presence.delete_instance()
        return True
    return False
 
def creer_presence_individuel(id_joueur, id_entrainement):
    """Créer une présence à un entraînement individuel"""
    return PresenceIndividuel.create(
        id_joueur=id_joueur, id_entrainement=id_entrainement
    )
 
def supprimer_presence_individuel(id_joueur, id_entrainement):
    """Supprimer une présence individuel"""
    presence = PresenceIndividuel.get_or_none(
        (PresenceIndividuel.id_joueur == id_joueur) & 
        (PresenceIndividuel.id_entrainement == id_entrainement)
    )
    if presence:
        presence.delete_instance()
        return True
    return False
 
def obtenir_joueurs_presents_collectif(id_entrainement):
    """Récupérer les joueurs présents à un entraînement collectif"""
    return (PresenceCollectif
            .select(PresenceCollectif, Joueur)
            .join(Joueur)
            .where(PresenceCollectif.id_entrainement == id_entrainement))
 
def obtenir_joueurs_presents_individuel(id_entrainement):
    """Récupérer les joueurs présents à un entraînement individuel"""
    return (PresenceIndividuel
            .select(PresenceIndividuel, Joueur)
            .join(Joueur)
            .where(PresenceIndividuel.id_entrainement == id_entrainement))
 
# --- Blessures ---
 
def modifier_blessure(id_blessure, gravite, date_fin):
    """Modifier une blessure"""
    blessure = Blessure.get_or_none(Blessure.id_blessure == id_blessure)
    if blessure:
        blessure.gravite = gravite
        blessure.date_fin = date_fin
        blessure.save()
        return blessure
    return None
 
# ==========================================
# FONCTIONS INTERFACE (UTILISE LES FONCTIONS MÉTIER)
# ==========================================
 
def afficher_joueurs():
    """Afficher la liste des joueurs"""
    print("\n--- Liste des joueurs ---")
    joueurs = obtenir_tous_joueurs()
    for j in joueurs:
        print(f"ID: {j.id_joueur} | {j.prenom} {j.nom} | {j.poste}")
 
def afficher_matchs():
    """Afficher la liste des matchs"""
    print("\n--- Liste des matchs ---")
    matches = obtenir_tous_matchs()
    for m in matches:
        print(f"ID: {m.id_match} | {m.match_date} | {m.adversaire} | {m.buts_pour}-{m.buts_contre}")
 
def afficher_entrainements_collectifs():
    """Afficher les entraînements collectifs"""
    print("\n--- Entraînements collectifs ---")
    entrainements = obtenir_tous_entrainements_collectifs()
    for e in entrainements:
        print(f"ID: {e.id_entrainement} | {e.date_entrainement} | {e.type_entrainement_co}")
 
def afficher_entrainements_individuels():
    """Afficher les entraînements individuels"""
    print("\n--- Entraînements individuels ---")
    entrainements = obtenir_tous_entrainements_individuels()
    for e in entrainements:
        print(f"ID: {e.id_entrainement} | {e.date_entrainement} | {e.objectif}")
 
# --- Interface utilisateur ---
 
def ajouter_joueur():
    """Interface pour ajouter un joueur"""
    print("\n--- Ajouter un nouveau joueur ---")
    prenom = input("Prénom : ")
    nom = input("Nom : ")
    date_naissance = input("Date de naissance (AAAA-MM-JJ) : ")
    poste = input("Poste : ")
    date_arrivee = input("Date d'arrivée (AAAA-MM-JJ) : ")
    
    try:
        creer_joueur(prenom, nom, date_naissance, poste, date_arrivee)
        print("Joueur ajouté")
    except Exception as e:
        print(f"Erreur : {e}")
 
def ajouter_match():
    """Interface pour ajouter un match"""
    print("\n--- Ajouter un nouveau match ---")
    match_date = input("Date du match (AAAA-MM-JJ) : ")
    adversaire = input("Adversaire : ")
    localisation = input("Localisation (Domicile/Extérieur) : ")
    buts_pour = int(input("Buts pour : "))
    buts_contre = int(input("Buts contre : "))
    
    try:
        creer_match(match_date, adversaire, localisation, buts_pour, buts_contre)
        print("Match ajouté")
    except Exception as e:
        print(f"Erreur : {e}")
 
def ajouter_entrainement_collectif():
    """Interface pour ajouter un entraînement collectif"""
    print("\n--- Ajouter un entraînement collectif ---")
    date_entrainement = input("Date (AAAA-MM-JJ) : ")
    type_e = input("Type : ")
    duree_minutes = int(input("Durée (minutes) : "))
    type_entrainement_co = input("Type d'entraînement (Tactique/Physique/Technique) : ")
    difficulte_co = int(input("Difficulté (1-10) : "))
    
    try:
        creer_entrainement_collectif(date_entrainement, type_e, duree_minutes, type_entrainement_co, difficulte_co)
        print("Entraînement collectif ajouté")
    except Exception as e:
        print(f"Erreur : {e}")
 
def ajouter_entrainement_individuel():
    """Interface pour ajouter un entraînement individuel"""
    print("\n--- Ajouter un entraînement individuel ---")
    date_entrainement = input("Date (AAAA-MM-JJ) : ")
    objectif = input("Objectif : ")
    duree_minutes = int(input("Durée (minutes) : "))
    type_entrainement_ind = input("Type d'entraînement (Cardio/Technique/Force) : ")
    difficulte_ind = int(input("Difficulté (1-10) : "))
    
    try:
        creer_entrainement_individuel(date_entrainement, objectif, duree_minutes, type_entrainement_ind, difficulte_ind)
        print("Entraînement individuel ajouté")
    except Exception as e:
        print(f"Erreur : {e}")
 
def ajouter_participation_match():
    """Interface pour enregistrer une participation"""
    print("\n--- Enregistrer la participation d'un joueur à un match ---")
    afficher_joueurs()
    afficher_matchs()
    
    id_joueur = int(input("\nID du joueur : "))
    id_match = int(input("ID du match : "))
    minutes_jouees = int(input("Minutes jouées : "))
    buts = int(input("Buts marqués : "))
    passes_decisives = int(input("Passes décisives : "))
    
    try:
        creer_participation_match(id_joueur, id_match, minutes_jouees, buts, passes_decisives)
        print("Participation enregistrée")
    except Exception as e:
        print(f"Erreur : {e}")
 
def ajouter_presence_collectif():
    """Interface pour enregistrer une présence collectif"""
    print("\n--- Enregistrer la présence à un entraînement collectif ---")
    afficher_joueurs()
    afficher_entrainements_collectifs()
    
    id_joueur = int(input("\nID du joueur : "))
    id_entrainement = int(input("ID de l'entraînement : "))
    present = int(input("Présent (1=Oui, 0=Non) : "))
    
    try:
        creer_presence_collectif(id_joueur, id_entrainement, present)
        print("Présence enregistrée")
    except Exception as e:
        print(f"Erreur : {e}")
 
def ajouter_presence_individuel():
    """Interface pour enregistrer une présence individuel"""
    print("\n--- Enregistrer la présence à un entraînement individuel ---")
    afficher_joueurs()
    afficher_entrainements_individuels()
    
    id_joueur = int(input("\nID du joueur : "))
    id_entrainement = int(input("ID de l'entraînement : "))
    
    try:
        creer_presence_individuel(id_joueur, id_entrainement)
        print("Présence enregistrée")
    except Exception as e:
        print(f"Erreur : {e}")
 
def supprimer_joueur():
    """Interface pour supprimer un joueur"""
    afficher_joueurs()
    id_joueur = int(input("\nID du joueur à supprimer : "))
    
    if supprimer_joueur_par_id(id_joueur):
        print("Joueur supprimé")
    else:
        print("Joueur introuvable")
 
def supprimer_match():
    """Interface pour supprimer un match"""
    afficher_matchs()
    id_match = int(input("\nID du match à supprimer : "))
    
    if supprimer_match_par_id(id_match):
        print("Match supprimé")
    else:
        print("Match introuvable")
 
def supprimer_entrainement_collectif():
    """Interface pour supprimer un entraînement collectif"""
    afficher_entrainements_collectifs()
    id_entrainement = int(input("\nID de l'entraînement à supprimer : "))
    
    if supprimer_entrainement_collectif_par_id(id_entrainement):
        print("Entraînement supprimé")
    else:
        print("Entraînement introuvable")
 
def supprimer_entrainement_individuel():
    """Interface pour supprimer un entraînement individuel"""
    afficher_entrainements_individuels()
    id_entrainement = int(input("\nID de l'entraînement à supprimer : "))
    
    if supprimer_entrainement_individuel_par_id(id_entrainement):
        print("Entraînement supprimé")
    else:
        print("Entraînement introuvable")
 
def supprimer_participation_match_ui():
    """Interface pour supprimer une participation"""
    id_joueur = int(input("ID du joueur : "))
    id_match = int(input("ID du match : "))
    
    if supprimer_participation_match(id_joueur, id_match):
        print("Participation supprimée")
    else:
        print("Participation introuvable")
 
def supprimer_presence_collectif_ui():
    """Interface pour supprimer une présence collectif"""
    id_joueur = int(input("ID du joueur : "))
    id_entrainement = int(input("ID de l'entraînement : "))
    
    if supprimer_presence_collectif(id_joueur, id_entrainement):
        print("Présence supprimée")
    else:
        print("Présence introuvable")
 
def supprimer_presence_individuel_ui():
    """Interface pour supprimer une présence individuel"""
    id_joueur = int(input("ID du joueur : "))
    id_entrainement = int(input("ID de l'entraînement : "))
    
    if supprimer_presence_individuel(id_joueur, id_entrainement):
        print("Présence supprimée")
    else:
        print("Présence introuvable")
 
def modifier_stats_participation_ui():
    """Interface pour modifier stats participation"""
    id_joueur = int(input("ID du joueur : "))
    id_match = int(input("ID du match : "))
    minutes_jouees = int(input("Minutes jouées : "))
    buts = int(input("Buts : "))
    passes_decisives = int(input("Passes décisives : "))
    
    if modifier_participation_match(id_joueur, id_match, minutes_jouees, buts, passes_decisives):
        print("Statistiques mises à jour")
    else:
        print("Participation introuvable")
 
def modifier_presence_collectif_ui():
    """Interface pour modifier présence collectif"""
    id_joueur = int(input("ID du joueur : "))
    id_entrainement = int(input("ID de l'entraînement : "))
    present = int(input("Présent (1=Oui, 0=Non) : "))
    
    if modifier_presence_collectif(id_joueur, id_entrainement, present):
        print("Présence mise à jour")
    else:
        print("Présence introuvable")
 
def modifier_details_match_ui():
    """Interface pour modifier détails match"""
    afficher_matchs()
    id_match = int(input("\nID du match : "))
    buts_pour = int(input("Buts pour : "))
    buts_contre = int(input("Buts contre : "))
    
    if modifier_score_match(id_match, buts_pour, buts_contre):
        print("Match mis à jour")
    else:
        print("Match introuvable")
 
def modifier_info_joueur_ui():
    """Interface pour modifier info joueur"""
    afficher_joueurs()
    id_joueur = int(input("\nID du joueur : "))
    nouveau_poste = input("Nouveau poste : ")
    
    if modifier_joueur_poste(id_joueur, nouveau_poste):
        print("Joueur mis à jour")
    else:
        print("Joueur introuvable")
 
def modifier_entrainement_collectif_ui():
    """Interface pour modifier entraînement collectif"""
    afficher_entrainements_collectifs()
    id_entrainement = int(input("\nID de l'entraînement : "))
    type_entrainement_co = input("Type d'entraînement : ")
    difficulte_co = int(input("Difficulté (1-10) : "))
    
    if modifier_entrainement_collectif(id_entrainement, type_entrainement_co, difficulte_co):
        print("Entraînement mis à jour")
    else:
        print("Entraînement introuvable")
 
def modifier_entrainement_individuel_ui():
    """Interface pour modifier entraînement individuel"""
    afficher_entrainements_individuels()
    id_entrainement = int(input("\nID de l'entraînement : "))
    type_entrainement_ind = input("Type d'entraînement : ")
    difficulte_ind = int(input("Difficulté (1-10) : "))
    
    if modifier_entrainement_individuel(id_entrainement, type_entrainement_ind, difficulte_ind):
        print("Entraînement mis à jour")
    else:
        print("Entraînement introuvable")
 
def modifier_blessure_ui():
    """Interface pour modifier blessure"""
    id_blessure = int(input("ID de la blessure : "))
    gravite = int(input("Gravité (1-10) : "))
    date_fin = input("Date de fin (AAAA-MM-JJ) : ")
    
    if modifier_blessure(id_blessure, gravite, date_fin):
        print("Blessure mise à jour")
    else:
        print("Blessure introuvable")
 
def details_match_ui():
    """Interface pour afficher détails match"""
    afficher_matchs()
    id_match = int(input("\nID du match : "))
    
    match = obtenir_match_par_id(id_match)
    if match:
        print(f"\nDate: {match.match_date}")
        print(f"Adversaire: {match.adversaire}")
        print(f"Localisation: {match.localisation}")
        print(f"Score: {match.buts_pour}-{match.buts_contre}")
    else:
        print("Match introuvable")
 
def stats_joueur_specifique_ui():
    """Interface pour afficher stats joueur"""
    afficher_joueurs()
    id_joueur = int(input("\nID du joueur : "))
    
    joueur = obtenir_joueur_par_id(id_joueur)
    if joueur:
        print(f"\nPrénom: {joueur.prenom}")
        print(f"Nom: {joueur.nom}")
        print(f"Date de naissance: {joueur.date_naissance}")
        print(f"Poste: {joueur.poste}")
        print(f"Date d'arrivée: {joueur.date_arrivee}")
    else:
        print("Joueur introuvable")
 
def joueurs_dans_match_ui():
    """Interface pour afficher joueurs dans un match"""
    afficher_matchs()
    id_match = int(input("\nID du match : "))
    
    participations = obtenir_joueurs_dans_match(id_match)
    
    print("\n--- Joueurs ayant participé ---")
    for p in participations:
        print(f"{p.id_joueur.prenom} {p.id_joueur.nom} | {p.minutes_jouees}min | {p.buts} buts | {p.passes_decisives} passes")
 
def joueurs_presents_collectif_ui():
    """Interface pour afficher joueurs présents collectif"""
    afficher_entrainements_collectifs()
    id_entrainement = int(input("\nID de l'entraînement : "))
    
    presences = obtenir_joueurs_presents_collectif(id_entrainement)
    
    print("\n--- Joueurs présents ---")
    for p in presences:
        statut = "Présent" if p.present == 1 else "Absent"
        print(f"{p.id_joueur.prenom} {p.id_joueur.nom} | {statut}")
 
def joueurs_presents_individuel_ui():
    """Interface pour afficher joueurs présents individuel"""
    afficher_entrainements_individuels()
    id_entrainement = int(input("\nID de l'entraînement : "))
    
    presences = obtenir_joueurs_presents_individuel(id_entrainement)
    
    print("\n--- Joueurs présents ---")
    for p in presences:
        print(f"{p.id_joueur.prenom} {p.id_joueur.nom}")
 
def stats_globales_joueur_ui():
    """Interface pour afficher stats globales joueur"""
    afficher_joueurs()
    id_joueur = int(input("\nID du joueur : "))
    
    joueur = obtenir_joueur_par_id(id_joueur)
    if joueur:
        stats = obtenir_stats_globales_joueur(id_joueur)
        print(f"\nStatistiques de {joueur.prenom} {joueur.nom}")
        print(f"Total buts: {stats['total_buts']}")
        print(f"Total passes décisives: {stats['total_passes']}")
    else:
        print("Joueur introuvable")
 
def matchs_gagnes_ui():
    """Interface pour afficher matchs gagnés"""
    print("\n--- Matchs gagnés ---")
    matches = obtenir_matchs_gagnes()
    for m in matches:
        print(f"{m.match_date} | {m.adversaire} | {m.buts_pour}-{m.buts_contre}")
 
def matchs_perdus_ui():
    """Interface pour afficher matchs perdus"""
    print("\n--- Matchs perdus ---")
    matches = obtenir_matchs_perdus()
    for m in matches:
        print(f"{m.match_date} | {m.adversaire} | {m.buts_pour}-{m.buts_contre}")
 
def matchs_nuls_ui():
    """Interface pour afficher matchs nuls"""
    print("\n--- Matchs nuls ---")
    matches = obtenir_matchs_nuls()
    for m in matches:
        print(f"{m.match_date} | {m.adversaire} | {m.buts_pour}-{m.buts_contre}")
 
# ==========================================
# SOUS-MENUS
# ==========================================
 
def menu_ajouter():
    while True:
        print("\n" + "="*50)
        print("  AJOUTER DES DONNÉES")
        print("="*50)
        print("1. Ajouter un joueur")
        print("2. Ajouter un match")
        print("3. Ajouter un entraînement collectif")
        print("4. Ajouter un entraînement individuel")
        print("5. Ajouter une participation à un match")
        print("6. Ajouter une présence (collectif)")
        print("7. Ajouter une présence (individuel)")
        print("0. Retour")
        
        choix = input("\nChoix : ")
        
        if choix == '1': ajouter_joueur()
        elif choix == '2': ajouter_match()
        elif choix == '3': ajouter_entrainement_collectif()
        elif choix == '4': ajouter_entrainement_individuel()
        elif choix == '5': ajouter_participation_match()
        elif choix == '6': ajouter_presence_collectif()
        elif choix == '7': ajouter_presence_individuel()
        elif choix == '0': break
        else: print("Choix invalide")
        
        input("\nAppuyez sur Entrée...")
 
def menu_supprimer():
    while True:
        print("\n" + "="*50)
        print("  SUPPRIMER DES DONNÉES")
        print("="*50)
        print("1. Supprimer un joueur")
        print("2. Supprimer un match")
        print("3. Supprimer un entraînement collectif")
        print("4. Supprimer un entraînement individuel")
        print("5. Supprimer une participation")
        print("6. Supprimer une présence (collectif)")
        print("7. Supprimer une présence (individuel)")
        print("0. Retour")
        
        choix = input("\nChoix : ")
        
        if choix == '1': supprimer_joueur()
        elif choix == '2': supprimer_match()
        elif choix == '3': supprimer_entrainement_collectif()
        elif choix == '4': supprimer_entrainement_individuel()
        elif choix == '5': supprimer_participation_match_ui()
        elif choix == '6': supprimer_presence_collectif_ui()
        elif choix == '7': supprimer_presence_individuel_ui()
        elif choix == '0': break
        else: print("Choix invalide")
        
        input("\nAppuyez sur Entrée...")
 
def menu_modifier():
    while True:
        print("\n" + "="*50)
        print("  MODIFIER DES DONNÉES")
        print("="*50)
        print("1. Modifier stats participation")
        print("2. Modifier présence collectif")
        print("3. Modifier détails match")
        print("4. Modifier info joueur")
        print("5. Modifier entraînement collectif")
        print("6. Modifier entraînement individuel")
        print("7. Modifier blessure")
        print("0. Retour")
        
        choix = input("\nChoix : ")
        
        if choix == '1': modifier_stats_participation_ui()
        elif choix == '2': modifier_presence_collectif_ui()
        elif choix == '3': modifier_details_match_ui()
        elif choix == '4': modifier_info_joueur_ui()
        elif choix == '5': modifier_entrainement_collectif_ui()
        elif choix == '6': modifier_entrainement_individuel_ui()
        elif choix == '7': modifier_blessure_ui()
        elif choix == '0': break
        else: print("Choix invalide")
        
        input("\nAppuyez sur Entrée...")
 
def menu_consulter():
    while True:
        print("\n" + "="*50)
        print("  CONSULTER DES DONNÉES")
        print("="*50)
        print("1. Liste des joueurs")
        print("2. Liste des matchs")
        print("3. Détails d'un match")
        print("4. Stats d'un joueur")
        print("5. Joueurs dans un match")
        print("6. Joueurs présents (collectif)")
        print("7. Joueurs présents (individuel)")
        print("8. Stats globales d'un joueur")
        print("9. Matchs gagnés")
        print("10. Matchs perdus")
        print("11. Matchs nuls")
        print("12. Liste entraînements collectifs")
        print("13. Liste entraînements individuels")
        print("0. Retour")
        
        choix = input("\nChoix : ")
        
        if choix == '1': afficher_joueurs()
        elif choix == '2': afficher_matchs()
        elif choix == '3': details_match_ui()
        elif choix == '4': stats_joueur_specifique_ui()
        elif choix == '5': joueurs_dans_match_ui()
        elif choix == '6': joueurs_presents_collectif_ui()
        elif choix == '7': joueurs_presents_individuel_ui()
        elif choix == '8': stats_globales_joueur_ui()
        elif choix == '9': matchs_gagnes_ui()
        elif choix == '10': matchs_perdus_ui()
        elif choix == '11': matchs_nuls_ui()
        elif choix == '12': afficher_entrainements_collectifs()
        elif choix == '13': afficher_entrainements_individuels()
        elif choix == '0': break
        else: print("Choix invalide")
        
        input("\nAppuyez sur Entrée...")
 
# ==========================================
# MENU PRINCIPAL
# ==========================================
 
def menu_principal():
    while True:
        print("\n" + "="*50)
        print("  GESTION CLUB SPORTIF")
        print("="*50)
        print("1. Ajouter des données")
        print("2. Supprimer des données")
        print("3. Modifier des données")
        print("4. Consulter des données")
        print("0. Quitter")
        
        choix = input("\nChoix : ")
        
        if choix == '1': menu_ajouter()
        elif choix == '2': menu_supprimer()
        elif choix == '3': menu_modifier()
        elif choix == '4': menu_consulter()
        elif choix == '0':
            print("Au revoir !")
            break
        else:
            print("Choix invalide")
 
# ==========================================
# LANCEMENT
# ==========================================
 
if __name__ == "__main__":
    initialiser_base()
    menu_principal()
    db.close()
 