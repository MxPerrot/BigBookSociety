import pandas as pd
import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2

def setUpCursor():
    """
    Connects to the Database and returns the cursor
    """
    # loading variables from .env file
    load_dotenv() 

    connection = psycopg2.connect(
        database=os.getenv("DATABASE_NAME"), 
        user=os.getenv("USERNAME"), 
        password=os.getenv("PASSWORD"), 
        host=os.getenv("HOST"), 
        port=os.getenv("PORT")
    )

    cursor = connection.cursor()
    cursor.execute("SET SCHEMA 'sae';")

    return cursor

def getLivresUtilisateur(cursor, id_utilisateur):
    """
    Renvoie les données des livres lus par l'utilisateur donné en paramètre
    """
    # TODO Fix presence of INNER JOIN clause for _editeur and ensuing errors
    # Execute la requete SQL
    cursor.execute(f"""
        SELECT DISTINCT _livre.id_livre, _livre.titre, _livre.nb_notes, _livre.nombre_pages, _livre.date_publication, _editeur.id_editeur, _prix_livre.id_prix, _cadre.id_pays, _auteur.id_auteur, _auteur.sexe, _auteur.origine, _genre.id_genre, _genre.libelle_genre
        FROM _utilisateur 
        INNER JOIN _livre_utilisateur ON _livre_utilisateur.id_utilisateur = _utilisateur.id_utilisateur
        INNER JOIN _livre ON _livre.id_livre = _livre_utilisateur.id_livre

        INNER JOIN _editeur ON _editeur.id_editeur = _livre.id_editeur

        LEFT JOIN _prix_livre ON _livre.id_livre = _prix_livre.id_livre
                
        LEFT JOIN _cadre_livre ON _livre.id_livre = _cadre_livre.id_livre
        LEFT JOIN _cadre ON _cadre_livre.id_cadre = _cadre.id_cadre

        LEFT JOIN _auteur_livre ON _livre.id_livre = _auteur_livre.id_livre
        LEFT JOIN _auteur ON _auteur_livre.id_auteur = _auteur.id_auteur

        LEFT JOIN _genre_livre ON _livre.id_livre = _genre_livre.id_livre
        LEFT JOIN _genre ON _genre_livre.id_genre = _genre.id_genre
                
        WHERE _utilisateur.id_utilisateur = {id_utilisateur};
    """)

    userData = cursor.fetchall()

    # Si aucun livre n'est recupéré envoie un message d'erreur
    if len(userData) == 0:
        raise Exception("No books can be found for this user, either the database is operating incorrectly or this user doesn't have any book")
    
    # Reformate les données
    userBookList = [list(book) for book in userData]

    # Renvoie un Dataframe contenant les données récupérées
    return pd.DataFrame(userBookList, columns = ["id_livre", "titre", "nb_notes", "nombre_pages", "date_publication", "id_editeur", "id_prix", "id_pays", "id_auteur", "sexe_auteur", "origine_auteur", "id_genre", "genre"])

def getLivresFromIdList(cursor, idLivres):
    """
    Renvoie les données des livres dont les identifiants sont présents dans la liste mise en paramètre
    """
    # Execute la requête
    cursor.execute(f"""
        SELECT _livre.id_livre, _livre.titre, _livre.nb_notes, _livre.nombre_pages, _livre.date_publication, _editeur.id_editeur, _prix_livre.id_prix, _cadre.id_pays, _auteur.id_auteur, _auteur.sexe, _auteur.origine, _genre.id_genre, _genre.libelle_genre
        FROM _livre

        LEFT JOIN _editeur ON _editeur.id_editeur = _livre.id_editeur

        LEFT JOIN _prix_livre ON _livre.id_livre = _prix_livre.id_livre
                
        LEFT JOIN _cadre_livre ON _livre.id_livre = _cadre_livre.id_livre
        LEFT JOIN _cadre ON _cadre_livre.id_cadre = _cadre.id_cadre

        LEFT JOIN _auteur_livre ON _livre.id_livre = _auteur_livre.id_livre
        LEFT JOIN _auteur ON _auteur_livre.id_auteur = _auteur.id_auteur

        LEFT JOIN _genre_livre ON _livre.id_livre = _genre_livre.id_livre
        LEFT JOIN _genre ON _genre_livre.id_genre = _genre.id_genre

        WHERE _livre.id_livre IN {idLivres}
    """)

    bookData = cursor.fetchall()
    
    # Si aucun livre n'est recupéré envoie un message d'erreur
    if len(bookData) == 0:
        raise Exception('No book found, either there is no book with those IDs or the Database is not operating correctly\nList of book ID : '+idLivres)
    
    # Reformate les données
    bookList = [list(book) for book in bookData]

    # Renvoie un Dataframe contenant les données récupérées
    return pd.DataFrame(bookList, columns = ["id_livre", "titre", "nb_notes", "nombre_pages", "date_publication", "id_editeur", "id_prix", "id_pays", "id_auteur", "sexe_auteur", "origine_auteur", "id_genre", "genre"])

def getLivresAEvaluer(cursor, nbLivreEva):
    """
    Renvoie les données d'un nombre mis en paramètre de livres pris au hasard
    """
    # Recupère les identifiant des livres pris au hasard
    cursor.execute(f"""
        SELECT _livre.id_livre
        FROM _livre
        ORDER BY random()
        LIMIT {nbLivreEva};
    """)

    idLivresAEvaluerRaw = cursor.fetchall()

    if idLivresAEvaluerRaw == -1:
        raise Exception("No books to be found in the database, the database is likely empty, please insert data into the database before")

    # Reformate les données
    idLivresAEvaluer = tuple([livre[0] for livre in idLivresAEvaluerRaw])

    # Renvoie les données des livres
    return getLivresFromIdList(cursor, idLivresAEvaluer)


def getLivresAEvaluerTendance(cursor, nbLivreEva):
    """
    Renvoie les données d'un nombre de livres pris parmi les plus populaires
    """
    # TODO Recupère les identifiant des livres 
    cursor.execute(f"""
        SELECT b.id_livre
        FROM sae._livre b
        INNER JOIN sae._episode_serie s ON b.id_livre = s.id_livre
        WHERE numero_episode = '1'
        AND b.note_moyenne IS NOT NULL
        AND b.nb_notes IS NOT NULL
        ORDER BY random(), b.nb_notes DESC, b.note_moyenne DESC
        LIMIT {nbLivreEva};
    """)

    idLivresAEvaluerRaw = cursor.fetchall()

    if idLivresAEvaluerRaw == -1:
        raise Exception("No books to be found in the database, the database is likely empty, please insert data into the database before")

    # Reformate les données
    idLivresAEvaluer = tuple([livre[0] for livre in idLivresAEvaluerRaw])

    # Renvoie les données des livres
    return getLivresFromIdList(cursor, idLivresAEvaluer)


def getLivresAEvaluerDecouverte(cursor, nbLivreEva):
    """
    Renvoie les données d'un nombre de livres pris parmi ceux moyennement populaires mais bien notés
    """
    # TODO Recupère les identifiant des livres 
    cursor.execute(f"""
        SELECT * FROM sae._livre 
        WHERE note_moyenne is not null 
        and nb_notes>1000 
        and nb_notes<50000 
        ORDER BY random(), note_moyenne DESC 
        LIMIT {nbLivreEva};
    """)

    idLivresAEvaluerRaw = cursor.fetchall()

    if idLivresAEvaluerRaw == -1:
        raise Exception("No books to be found in the database, the database is likely empty, please insert data into the database before")

    # Reformate les données
    idLivresAEvaluer = tuple([livre[0] for livre in idLivresAEvaluerRaw])

    # Renvoie les données des livres
    return getLivresFromIdList(cursor, idLivresAEvaluer)


def getUtilisateurById(cursor, id_utilisateur):
    """
    Renvoie les données de l'utilisateur correspondant à l'identifiant donné en paramètre
    """
    cursor.execute(f"""
        SELECT 
            _utilisateur.id_utilisateur, 
            _utilisateur.sexe, 
            _utilisateur.age, 
            _utilisateur.profession, 
            _utilisateur.situation_familiale, 
            _utilisateur.frequence_lecture, 
            _utilisateur.vitesse_lecture, 
            _utilisateur.nb_livres_lus,
            _langue.id_langue,
            _motivation.id_motivation,
            _raison_achat.id_raison_achat,
            _procuration.id_procuration,
            _format.id_format
                   
        FROM _utilisateur
                   
        LEFT JOIN _utilisateur_langue ON _utilisateur.id_utilisateur = _utilisateur_langue.id_utilisateur
        LEFT JOIN _langue ON _utilisateur_langue.id_langue = _langue.id_langue
        
        LEFT JOIN _utilisateur_motivation ON _utilisateur.id_utilisateur = _utilisateur_motivation.id_utilisateur
        LEFT JOIN _motivation ON _utilisateur_motivation.id_motivation = _motivation.id_motivation

        LEFT JOIN _utilisateur_raison_achat ON _utilisateur.id_utilisateur = _utilisateur_raison_achat.id_utilisateur
        LEFT JOIN _raison_achat ON _utilisateur_raison_achat.id_raison_achat = _raison_achat.id_raison_achat

        LEFT JOIN _utilisateur_procuration ON _utilisateur.id_utilisateur = _utilisateur_procuration.id_utilisateur
        LEFT JOIN _procuration ON _utilisateur_procuration.id_procuration = _procuration.id_procuration

        LEFT JOIN _format_utilisateur ON _utilisateur.id_utilisateur = _format_utilisateur.id_utilisateur
        LEFT JOIN _format ON _format_utilisateur.id_format = _format.id_format
        
        WHERE _utilisateur.id_utilisateur = {id_utilisateur}
    """)

    utilisateur = cursor.fetchall()

    # Si aucun utilisateur n'est recupéré envoie un message d'erreur
    if len(utilisateur) == 0:
        raise Exception('User not found, either there is no user with that ID or the Database is not operating correctly.\nUser ID : '+id_utilisateur)

    # Renvoie un Dataframe contenant les données récupérées
    return pd.DataFrame(utilisateur, columns = ["id_utilisateur", "sexe", "age", "profession", "situation_familiale", "frequence_lecture", "vitesse_lecture", "nb_livres_lus", "langue", "motivation", "raison_achat", "procuration", "format"])

def getUtilisateursFromIdList(cursor, idUtilisateurs):
    """
    Renvoie les données des utilisateur dont l'identifiant correspond à l'un de ceux dans la liste mise en paramètre
    """
    cursor.execute(f"""
        SELECT 
            _utilisateur.id_utilisateur, 
            _utilisateur.sexe, 
            _utilisateur.age, 
            _utilisateur.profession, 
            _utilisateur.situation_familiale, 
            _utilisateur.frequence_lecture, 
            _utilisateur.vitesse_lecture, 
            _utilisateur.nb_livres_lus,
            _langue.id_langue,
            _motivation.id_motivation,
            _raison_achat.id_raison_achat,
            _procuration.id_procuration,
            _format.id_format
                   
        FROM _utilisateur

        LEFT JOIN _utilisateur_langue ON _utilisateur.id_utilisateur = _utilisateur_langue.id_utilisateur
        LEFT JOIN _langue ON _utilisateur_langue.id_langue = _langue.id_langue
        
        LEFT JOIN _utilisateur_motivation ON _utilisateur.id_utilisateur = _utilisateur_motivation.id_utilisateur
        LEFT JOIN _motivation ON _utilisateur_motivation.id_motivation = _motivation.id_motivation

        LEFT JOIN _utilisateur_raison_achat ON _utilisateur.id_utilisateur = _utilisateur_raison_achat.id_utilisateur
        LEFT JOIN _raison_achat ON _utilisateur_raison_achat.id_raison_achat = _raison_achat.id_raison_achat

        LEFT JOIN _utilisateur_procuration ON _utilisateur.id_utilisateur = _utilisateur_procuration.id_utilisateur
        LEFT JOIN _procuration ON _utilisateur_procuration.id_procuration = _procuration.id_procuration

        LEFT JOIN _format_utilisateur ON _utilisateur.id_utilisateur = _format_utilisateur.id_utilisateur
        LEFT JOIN _format ON _format_utilisateur.id_format = _format.id_format

        WHERE _utilisateur.id_utilisateur IN {idUtilisateurs}
    """)

    userData = cursor.fetchall()
    
    # Si aucun utilisateur n'est recupéré envoie un message d'erreur
    if len(userData) == 0:
        raise Exception('No user found, either there is no user with those IDs or the Database is not operating correctly\nList of user ID : '+idUtilisateurs)
        
    
    # Reformate les données
    userList = [list(user) for user in userData]

    # Renvoie un Dataframe contenant les données récupérées
    return pd.DataFrame(userList, columns = ["id_utilisateur", "sexe", "age", "profession", "situation_familiale", "frequence_lecture", "vitesse_lecture", "nb_livres_lus", "langue", "motivation", "raison_achat", "procuration", "format"])


def getUtilisateursAEvaluer(cursor, nbUtilisateurEva):
    """
    Renvoie les données d'un nombre mis en paramètres d'utilisateurs pris au hasard
    """
    # Recupère les identifiant d'utilisateurs pris au hasard
    cursor.execute(f"""
        SELECT _utilisateur.id_utilisateur
        FROM _utilisateur
        ORDER BY random()
        LIMIT {nbUtilisateurEva};
    """)
    
    idUtilisateursAEvaluerRaw = cursor.fetchall()

    # Si aucun utilisateur n'est recupéré envoie un message d'erreur
    if len(idUtilisateursAEvaluerRaw) == 0:
        raise Exception('No user to be found in the database, the database is likely empty, please insert data into the database before')

    # Reformate les données
    idUtilisateursAEvaluer = tuple([utilisateur[0] for utilisateur in idUtilisateursAEvaluerRaw])

    # Renvoie les données des livres
    return getUtilisateursFromIdList(cursor, idUtilisateursAEvaluer)
    

def getIdLivresUtilisateur(cursor, id_utilisateur):
    """
    Renvoie les identifiants des livres préférés de l'utilisateur mis en paramètre
    """
    # Execute la requête
    cursor.execute(f"""
        SELECT DISTINCT _livre.id_livre
        FROM _utilisateur 
        INNER JOIN _livre_utilisateur ON _livre_utilisateur.id_utilisateur = _utilisateur.id_utilisateur
        INNER JOIN _livre ON _livre.id_livre = _livre_utilisateur.id_livre

        WHERE _utilisateur.id_utilisateur = {id_utilisateur};
    """)

    userData = cursor.fetchall()

    # Si aucun utilisateur n'a été récupéré envoie un message d'erreur
    if len(userData) == 0:
        raise Exception("No books can be found for this user, either the database is operating incorrectly or this user doesn't have any book")
    
    # Reformate les données
    userIdBookList = [list(book)[0] for book in userData]

    # Renvoie les identifiants des livres
    return userIdBookList