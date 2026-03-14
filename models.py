from peewee import *

# Connexion à la base de données SQLite du projet
db = SqliteDatabase('club_sportif.db')


class BaseModel(Model):
    class Meta:
        database = db


# Table qui va contenir les infos des joueurs
class Joueur(BaseModel):

    id_joueur = AutoField(primary_key=True)
    prenom = CharField(null=False)
    nom = CharField(null=False)
    date_naissance = DateField(null=False)
    poste = CharField(null=False)
    date_arrivee = DateField(null=False)

    class Meta:
        table_name = 'joueurs'

    def __str__(self):
        """Permet d'afficher un joueur de manière lisible"""
        return f"{self.prenom} {self.nom} ({self.poste})"

    def nom_complet(self):
        """Renvoie le prénom + le nom du joueur"""
        return f"{self.prenom} {self.nom}"

    def age(self):
        """Calcule l'âge du joueur à partir de sa date de naissance"""
        from datetime import date

        today = date.today()
        naissance = self.date_naissance

        # Si la date est en texte, on la transforme en date
        if isinstance(naissance, str):
            from datetime import datetime
            naissance = datetime.strptime(naissance, '%Y-%m-%d').date()

        return today.year - naissance.year - (
            (today.month, today.day) < (naissance.month, naissance.day)
        )

    def anciennete(self):
        """Calcule depuis combien d'années le joueur est dans le club"""
        from datetime import date

        today = date.today()
        arrivee = self.date_arrivee

        if isinstance(arrivee, str):
            from datetime import datetime
            arrivee = datetime.strptime(arrivee, '%Y-%m-%d').date()

        return today.year - arrivee.year


# Table qui stocke les matchs du club
class Match(BaseModel):

    id_match = AutoField(primary_key=True)
    match_date = DateField(null=False)
    adversaire = CharField(null=False)
    localisation = CharField(null=False)
    buts_pour = IntegerField(default=0)
    buts_contre = IntegerField(default=0)

    class Meta:
        table_name = 'matches'

    def __str__(self):
        """Affiche les infos principales du match"""
        return f"{self.match_date} - {self.adversaire} ({self.localisation}) : {self.buts_pour}-{self.buts_contre}"

    def resultat(self):
        """Indique si le match est gagné, perdu ou nul"""
        if self.buts_pour > self.buts_contre:
            return "Victoire"
        elif self.buts_pour < self.buts_contre:
            return "Défaite"
        else:
            return "Nul"

    def difference_buts(self):
        """Calcule la différence entre les buts marqués et encaissés"""
        return self.buts_pour - self.buts_contre

    def est_victoire(self):
        """Vérifie si le match est une victoire"""
        return self.buts_pour > self.buts_contre

    def est_defaite(self):
        """Vérifie si le match est une défaite"""
        return self.buts_pour < self.buts_contre

    def est_nul(self):
        """Vérifie si le match s'est terminé par un nul"""
        return self.buts_pour == self.buts_contre


# Table des entraînements collectifs de l'équipe
class EntrainementCollectif(BaseModel):

    id_entrainement = AutoField(primary_key=True)
    date_entrainement = DateField(null=False)
    type = CharField(null=True)
    duree_minutes = IntegerField()
    type_entrainement_co = CharField(null=True)
    difficulte_co = IntegerField()

    class Meta:
        table_name = 'entrainements_collectifs'

    def __str__(self):
        """Affiche un résumé de l'entraînement collectif"""
        return f"Entraînement {self.type_entrainement_co} du {self.date_entrainement} ({self.duree_minutes}min)"

    def duree_heures(self):
        """Convertit la durée de l'entraînement en heures"""
        return self.duree_minutes / 60

    def niveau_difficulte(self):
        """Transforme la difficulté (chiffre) en texte"""
        if self.difficulte_co <= 3:
            return "Facile"
        elif self.difficulte_co <= 6:
            return "Moyen"
        else:
            return "Difficile"


# Table des entraînements individuels
class EntrainementIndividuel(BaseModel):

    id_entrainement = AutoField(primary_key=True)
    date_entrainement = DateField(null=False)
    objectif = CharField(null=True)
    duree_minutes = IntegerField()
    type_entrainement_ind = CharField(null=True)
    difficulte_ind = IntegerField()

    class Meta:
        table_name = 'entrainements_individuels'

    def __str__(self):
        """Affiche un résumé de l'entraînement individuel"""
        return f"Entraînement individuel du {self.date_entrainement} - {self.objectif} ({self.duree_minutes}min)"

    def duree_heures(self):
        """Convertit la durée en heures"""
        return self.duree_minutes / 60

    def niveau_difficulte(self):
        """Retourne la difficulté sous forme de texte"""
        if self.difficulte_ind <= 3:
            return "Facile"
        elif self.difficulte_ind <= 6:
            return "Moyen"
        else:
            return "Difficile"


# Table qui relie les joueurs aux matchs auxquels ils participent
class ParticipationMatch(BaseModel):

    id = AutoField(primary_key=True)
    id_joueur = ForeignKeyField(Joueur, column_name='id_joueur')
    id_match = ForeignKeyField(Match, column_name='id_match')
    minutes_jouees = IntegerField()
    buts = IntegerField(default=0)
    passes_decisives = IntegerField(default=0)

    class Meta:
        table_name = 'participation_match'

    def __str__(self):
        """Affiche un résumé de la participation du joueur"""
        return f"{self.id_joueur.nom_complet()} - {self.minutes_jouees}min, {self.buts} buts, {self.passes_decisives} passes"

    def a_joue_match_complet(self):
        """Vérifie si le joueur a joué tout le match"""
        return self.minutes_jouees >= 90

    def contribution(self):
        """Addition des buts et passes décisives"""
        return self.buts + self.passes_decisives


# Présence des joueurs aux entraînements collectifs
class PresenceCollectif(BaseModel):

    id = AutoField(primary_key=True)
    id_joueur = ForeignKeyField(Joueur, column_name='id_joueur')
    id_entrainement = ForeignKeyField(EntrainementCollectif, column_name='id_entrainement')
    present = IntegerField(null=False)

    class Meta:
        table_name = 'presence_collectif'

    def __str__(self):
        """Affiche si le joueur était présent ou absent"""
        statut = "Présent" if self.present == 1 else "Absent"
        return f"{self.id_joueur.nom_complet()} - {statut}"

    def est_present(self):
        """Retourne True si le joueur était présent"""
        return self.present == 1


# Présence des joueurs aux entraînements individuels
class PresenceIndividuel(BaseModel):

    id = AutoField(primary_key=True)
    id_joueur = ForeignKeyField(Joueur, column_name='id_joueur')
    id_entrainement = ForeignKeyField(EntrainementIndividuel, column_name='id_entrainement')

    class Meta:
        table_name = 'presence_individuel'

    def __str__(self):
        """Affiche simplement que le joueur était présent"""
        return f"{self.id_joueur.nom_complet()} - Entraînement individuel présent"


# Table qui stocke les blessures des joueurs
class Blessure(BaseModel):

    id_blessure = AutoField(primary_key=True)
    id_joueur = ForeignKeyField(Joueur, column_name='id_joueur')
    date_blessure = DateField(null=False)
    type_blessure = CharField(null=False)
    gravite = IntegerField()
    date_debut = DateField(null=False)
    date_fin = DateField(null=True)
    id_match = ForeignKeyField(Match, null=True, column_name='id_match')
    id_entrainement_collectif = ForeignKeyField(EntrainementCollectif, null=True, column_name='id_entrainement_collectif')
    id_entrainement_individuel = ForeignKeyField(EntrainementIndividuel, null=True, column_name='id_entrainement_individuel')

    class Meta:
        table_name = 'blessures'

    def __str__(self):
        """Affiche les infos principales sur la blessure"""
        statut = "Guéri" if self.est_gueri() else "En cours"
        return f"{self.id_joueur.nom_complet()} - {self.type_blessure} (Gravité: {self.gravite}/10) - {statut}"

    def est_gueri(self):
        """Vérifie si le joueur est guéri"""
        return self.date_fin is not None

    def duree_indisponibilite(self):
        """Calcule le nombre de jours où le joueur est indisponible"""
        from datetime import date

        date_fin_calcul = self.date_fin if self.date_fin else date.today()

        debut = self.date_debut
        if isinstance(debut, str):
            from datetime import datetime
            debut = datetime.strptime(debut, '%Y-%m-%d').date()

        if isinstance(date_fin_calcul, str):
            from datetime import datetime
            date_fin_calcul = datetime.strptime(date_fin_calcul, '%Y-%m-%d').date()

        return (date_fin_calcul - debut).days

    def niveau_gravite(self):
        """Transforme le niveau de gravité en texte"""
        if self.gravite <= 3:
            return "Légère"
        elif self.gravite <= 6:
            return "Modérée"
        else:
            return "Grave"

    def contexte_blessure(self):
        """Indique dans quel contexte la blessure est arrivée"""
        if self.id_match:
            return "Match"
        elif self.id_entrainement_collectif:
            return "Entraînement collectif"
        elif self.id_entrainement_individuel:
            return "Entraînement individuel"
        else:
            return "Inconnu"


# Fonction qui crée toutes les tables dans la base de données
def initialiser_base():

    db.connect()

    db.create_tables([
        Joueur,
        Match,
        EntrainementCollectif,
        EntrainementIndividuel,
        ParticipationMatch,
        PresenceCollectif,
        PresenceIndividuel,
        Blessure
    ], safe=True)

    print("Base de données initialisée!")


if __name__ == "__main__":
    initialiser_base()
    db.close()