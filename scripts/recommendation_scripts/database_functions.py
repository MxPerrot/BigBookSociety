import pandas as pd
import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2

def setUpCursor():
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
    # TODO Fix presence of INNER JOIN clause for _editeur and ensuing errors
    cursor.execute(f"""
        SELECT DISTINCT _livre.id_livre, _livre.titre, _livre.nb_notes, _livre.note_moyenne, _livre.nombre_pages, _livre.date_publication, _livre.description, _editeur.id_editeur, _editeur.nom_editeur, _prix.id_prix, _prix.annee_prix, _pays.id_pays, _auteur.id_auteur, _auteur.sexe, _auteur.origine, _genre.id_genre, _genre.libelle_genre
        FROM _utilisateur 
        INNER JOIN _livre_utilisateur ON _livre_utilisateur.id_utilisateur = _utilisateur.id_utilisateur
        INNER JOIN _livre ON _livre.id_livre = _livre_utilisateur.id_livre

        INNER JOIN _editeur ON _editeur.id_editeur = _livre.id_editeur

        LEFT JOIN _prix_livre ON _livre.id_livre = _prix_livre.id_livre
        LEFT JOIN _prix ON _prix_livre.id_prix = _prix.id_prix
                
        LEFT JOIN _cadre_livre ON _livre.id_livre = _cadre_livre.id_livre
        LEFT JOIN _cadre ON _cadre_livre.id_cadre = _cadre.id_cadre
        LEFT JOIN _pays ON _cadre.id_pays = _pays.id_pays

        LEFT JOIN _auteur_livre ON _livre.id_livre = _auteur_livre.id_livre
        LEFT JOIN _auteur ON _auteur_livre.id_auteur = _auteur.id_auteur

        LEFT JOIN _genre_livre ON _livre.id_livre = _genre_livre.id_livre
        LEFT JOIN _genre ON _genre_livre.id_genre = _genre.id_genre
                
        WHERE _utilisateur.id_utilisateur = {id_utilisateur};
    """)

    userData = cursor.fetchall()

    if len(userData) == 0:
        return -1
    
    userBookList = [list(book) for book in userData]

    return pd.DataFrame(userBookList, columns = ["id_livre", "titre", "nb_notes", "note_moyenne", "nombre_pages", "date_publication", "description", "id_editeur", "nom_editeur", "id_prix", "annee_prix", "id_pays", "id_auteur", "sexe_auteur", "origine_auteur", "id_genre", "genre"])

def getLivresFromIdList(cursor, idLivres):
    cursor.execute(f"""
        SELECT _livre.id_livre, _livre.titre, _livre.nb_notes, _livre.note_moyenne, _livre.nombre_pages, _livre.date_publication, _livre.description, _editeur.id_editeur, _editeur.nom_editeur, _prix.id_prix, _prix.annee_prix, _serie.nom_serie, _episode_serie.numero_episode, _pays.id_pays, _auteur.id_auteur, _auteur.sexe, _auteur.origine, _genre.id_genre, _genre.libelle_genre
        FROM _livre

        LEFT JOIN _editeur ON _editeur.id_editeur = _livre.id_editeur

        LEFT JOIN _prix_livre ON _livre.id_livre = _prix_livre.id_livre
        LEFT JOIN _prix ON _prix_livre.id_prix = _prix.id_prix
                
        LEFT JOIN _episode_serie ON _livre.id_livre = _episode_serie.id_livre
        LEFT JOIN _serie ON _episode_serie.id_serie = _serie.id_serie
                
        LEFT JOIN _cadre_livre ON _livre.id_livre = _cadre_livre.id_livre
        LEFT JOIN _cadre ON _cadre_livre.id_cadre = _cadre.id_cadre
        LEFT JOIN _pays ON _cadre.id_pays = _pays.id_pays

        LEFT JOIN _auteur_livre ON _livre.id_livre = _auteur_livre.id_livre
        LEFT JOIN _auteur ON _auteur_livre.id_auteur = _auteur.id_auteur

        LEFT JOIN _genre_livre ON _livre.id_livre = _genre_livre.id_livre
        LEFT JOIN _genre ON _genre_livre.id_genre = _genre.id_genre

        WHERE _livre.id_livre IN {idLivres}
    """)

    bookData = cursor.fetchall()
    
    if len(bookData) == 0:
        return -1
  
    bookList = [list(book) for book in bookData]

    return pd.DataFrame(bookList, columns = ["id_livre", "titre", "nb_notes", "note_moyenne", "nombre_pages", "date_publication", "description", "id_editeur", "nom_editeur", "id_prix", "annee_prix", "nom_serie", "numero_episode", "id_pays", "id_auteur", "sexe_auteur", "origine_auteur", "id_genre", "genre"])

def getLivresAEvaluer(cursor, nbLivreEva):
    cursor.execute(f"""
        SELECT _livre.id_livre
        FROM _livre
        ORDER BY random()
        LIMIT {nbLivreEva};
    """)

    idLivresAEvaluerRaw = cursor.fetchall()
    idLivresAEvaluer = tuple([livre[0] for livre in idLivresAEvaluerRaw])

    return getLivresFromIdList(cursor, idLivresAEvaluer)


def getLivresAEvaluerTendance(cursor, nbLivreEva):
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
    idLivresAEvaluer = tuple([livre[0] for livre in idLivresAEvaluerRaw])

    return getLivresFromIdList(cursor, idLivresAEvaluer)


def getLivresAEvaluerDecouverte(cursor, nbLivreEva):
    cursor.execute(f"""
        SELECT * FROM sae._livre 
        WHERE note_moyenne is not null 
        and nb_notes>1000 
        and nb_notes<50000 
        ORDER BY random(), note_moyenne DESC 
        LIMIT {nbLivreEva};
    """)

    idLivresAEvaluerRaw = cursor.fetchall()
    idLivresAEvaluer = tuple([livre[0] for livre in idLivresAEvaluerRaw])

    return getLivresFromIdList(cursor, idLivresAEvaluer)


def getUtilisateurById(cursor, id_utilisateur):
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

    return pd.DataFrame(utilisateur, columns = ["id_utilisateur", "sexe", "age", "profession", "situation_familiale", "frequence_lecture", "vitesse_lecture", "nb_livres_lus", "langue", "motivation", "raison_achat", "procuration", "format"])

def getUtilisateursFromIdList(cursor, idUtilisateurs):
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
    
    if len(userData) == 0:
        return -1
    
    userList = [list(user) for user in userData]
    return pd.DataFrame(userList, columns = ["id_utilisateur", "sexe", "age", "profession", "situation_familiale", "frequence_lecture", "vitesse_lecture", "nb_livres_lus", "langue", "motivation", "raison_achat", "procuration", "format"])


def getUtilisateursAEvaluer(cursor, nbUtilisateurEva):
    cursor.execute(f"""
        SELECT _utilisateur.id_utilisateur
        FROM _utilisateur
        ORDER BY random()
        LIMIT {nbUtilisateurEva};
    """)
    
    idUtilisateursAEvaluerRaw = cursor.fetchall()
    idUtilisateursAEvaluer = tuple([utilisateur[0] for utilisateur in idUtilisateursAEvaluerRaw])

    return getUtilisateursFromIdList(cursor, idUtilisateursAEvaluer)
    

    
def getIdLivresUtilisateur(cursor, id_utilisateur):
    cursor.execute(f"""
        SELECT DISTINCT _livre.id_livre
        FROM _utilisateur 
        INNER JOIN _livre_utilisateur ON _livre_utilisateur.id_utilisateur = _utilisateur.id_utilisateur
        INNER JOIN _livre ON _livre.id_livre = _livre_utilisateur.id_livre

        WHERE _utilisateur.id_utilisateur = {id_utilisateur};
    """)

    userData = cursor.fetchall()

    if len(userData) == 0:
        return -1
    
    userIdBookList = [list(book)[0] for book in userData]

    return userIdBookList