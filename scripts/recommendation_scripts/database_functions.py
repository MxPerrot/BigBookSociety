import pandas as pd
import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2
import random as rd

def setUpConnection():
    """
    Connects to the Database
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

    return connection


def setUpCursor(connection):
    """
    Returns the cursor
    """

    cursor = connection.cursor()
    cursor.execute("SET SCHEMA 'sae';")

    return cursor

def turnIterableIntoSqlList(iterable):
    first = True
    chaineListe = ""
    for elem in iterable:
        if first:
            chaineListe += str(elem)
            first = False
        else:
            chaineListe += ", "+str(elem)
    return chaineListe

def getIdLivresUtilisateur(cursor, id_utilisateur):
    cursor.execute("""
        SELECT DISTINCT _livre.id_livre
        FROM _utilisateur 
        INNER JOIN _livre_utilisateur ON _livre_utilisateur.id_utilisateur = _utilisateur.id_utilisateur
        INNER JOIN _livre ON _livre.id_livre = _livre_utilisateur.id_livre
        WHERE _utilisateur.id_utilisateur = %s;
    """,(id_utilisateur,))

    userData = cursor.fetchall()

    # Si aucun livre n'est recupéré envoie un message d'erreur
    if len(userData) == 0:
        raise Exception("No books can be found for this user, either the database is operating incorrectly or this user doesn't have any book")
    
    return

def getLivresUtilisateur(cursor, id_utilisateur):
    """
    Renvoie les données des livres lus par l'utilisateur donné en paramètre
    """

    listIdLivres = tuple(getIdLivresUtilisateur(cursor, id_utilisateur))

    # TODO Fix presence of INNER JOIN clause for _editeur and ensuing errors
    userBookList = getLivresFromIdList(cursor, listIdLivres)

    # Renvoie un Dataframe contenant les données récupérées
    return pd.DataFrame(userBookList, columns = ["id_livre", "titre", "nb_notes", "nombre_pages", "date_publication", "id_editeur", "id_prix", "id_pays", "id_auteur", "sexe_auteur", "origine_auteur", "id_genre", "genre"])

def getLivresFromIdList(cursor, idLivres):
    """
    Renvoie les données des livres dont les identifiants sont présents dans la liste mise en paramètre
    """
    # Execute la requête
    cursor.execute("""
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

        WHERE _livre.id_livre IN %s
    """,(idLivres,))

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
    cursor.execute("""
        SELECT _livre.id_livre
        FROM _livre
        ORDER BY random()
        LIMIT %s;
    """,(nbLivreEva,))

    idLivresAEvaluerRaw = cursor.fetchall()

    if idLivresAEvaluerRaw == -1:
        raise Exception("No books to be found in the database, the database is likely empty, please insert data into the database before")

    # Reformate les données
    idLivresAEvaluer = tuple([livre[0] for livre in idLivresAEvaluerRaw])

    # Renvoie les données des livres
    return getLivresFromIdList(cursor, idLivresAEvaluer)

def getIdLivresTendance(cursor, nbLivreEva):
    """
    Renvoie les ids d'un nombre de livres pris parmi les plus populaires
    """
    cursor.execute("""
        SELECT b.id_livre
        FROM sae._livre b
        INNER JOIN sae._episode_serie s ON b.id_livre = s.id_livre
        WHERE numero_episode = '1'
        AND b.note_moyenne IS NOT NULL
        AND b.nb_notes IS NOT NULL
        ORDER BY b.nb_notes DESC, b.note_moyenne DESC
        LIMIT %s;
    """,(nbLivreEva,))

    idLivresAEvaluerRaw = cursor.fetchall()

    if idLivresAEvaluerRaw == -1:
        raise Exception("No books to be found in the database, the database is likely empty, please insert data into the database before")

    # Reformate les données
    idLivresAEvaluer = tuple([livre[0] for livre in idLivresAEvaluerRaw])

    return idLivresAEvaluer

def getLivresAEvaluerTendance(cursor, nbLivreEva):
    """
    Renvoie les données d'un nombre de livres pris parmi les plus populaires
    """
    idLivresAEvaluer = getIdLivresTendance(cursor, nbLivreEva)

    # Renvoie les données des livres
    return getLivresFromIdList(cursor, idLivresAEvaluer)


def getLivresAEvaluerDecouverte(cursor, nbLivreEva):
    """
    Renvoie les données d'un nombre de livres pris parmi ceux moyennement populaires mais bien notés
    """
    cursor.execute("""
        SELECT _livre.id_livre FROM sae._livre 
        WHERE note_moyenne is not null 
        and nb_notes>1000 
        and nb_notes<50000 
        ORDER BY random(), note_moyenne DESC 
        LIMIT %s;
    """,(nbLivreEva,))

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
    cursor.execute("""
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
        
        WHERE _utilisateur.id_utilisateur = %s
    """,(id_utilisateur,))

    utilisateur = cursor.fetchall()

    # Si aucun utilisateur n'est recupéré envoie un message d'erreur
    if len(utilisateur) == 0:
        raise Exception('User not found, either there is no user with that ID or the Database is not operating correctly.\nUser ID : '+ str(id_utilisateur))

    # Renvoie un Dataframe contenant les données récupérées
    return pd.DataFrame(utilisateur, columns = ["id_utilisateur", "sexe", "age", "profession", "situation_familiale", "frequence_lecture", "vitesse_lecture", "nb_livres_lus", "langue", "motivation", "raison_achat", "procuration", "format"])

def getUtilisateursFromIdList(cursor, idUtilisateurs):
    """
    Renvoie les données des utilisateur dont l'identifiant correspond à l'un de ceux dans la liste mise en paramètre
    """
    cursor.execute("""
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

        WHERE _utilisateur.id_utilisateur IN %s
    """,(idUtilisateurs,))

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
    cursor.execute("""
        SELECT _utilisateur.id_utilisateur
        FROM _utilisateur
        ORDER BY random()
        LIMIT %s;
    """,(nbUtilisateurEva,))
    
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
    cursor.execute("""
        SELECT DISTINCT _livre.id_livre
        FROM _utilisateur 
        INNER JOIN _livre_utilisateur ON _livre_utilisateur.id_utilisateur = _utilisateur.id_utilisateur
        INNER JOIN _livre ON _livre.id_livre = _livre_utilisateur.id_livre

        WHERE _utilisateur.id_utilisateur = %s;
    """,(id_utilisateur,))

    userData = cursor.fetchall()

    # Si aucun utilisateur n'a été récupéré renvoie -1, indiquant qu'aucune donnée n'a été récupérée
    if len(userData) == 0:
        return -1
    
    # Reformate les données
    userIdBookList = [list(book)[0] for book in userData]

    # Renvoie les identifiants des livres
    return userIdBookList

def getBookIdSameAuthor(cursor, user_id, limit):
    """
    Sélectionne les livres lus/aimé par l'utilisateur
    Pour chaque regarde et sauvegarde l'auteur
    Récupère autre livre populaire de l'auteur avec id de livres différent
    Renvoie
    """

    cursor.execute("""
    SELECT id_auteur,id_livre FROM sae._utilisateur 
    NATURAL JOIN sae._livre_utilisateur 
    NATURAL JOIN sae._auteur_livre
    WHERE id_utilisateur = %s;
    """, (user_id,))

    record = cursor.fetchall()

    liste_livre_lu = []

    for i in record:
        liste_livre_lu.append(i[1])

    liste_livre_recommender = []

    for i in record:
        cursor.execute("""
        SELECT id_livre FROM sae._auteur_livre
        NATURAL JOIN sae._livre
        WHERE id_auteur = %s;
        """, (i[0],))
        livres = cursor.fetchall()
        for y in livres:
            if (y[0] not in liste_livre_lu) & (y[0] not in liste_livre_recommender):
                liste_livre_recommender.append(y)

    for y in range(len(liste_livre_recommender)):
        liste_livre_recommender[y] = liste_livre_recommender[y][0]


    return rd.sample(liste_livre_recommender, limit)

def getBookIdInSeries(cursor, user):
    """
    Sélectionne les livres lus/aimé par l'utilisateur
    Pour chaque regarde si dans une série
    Si oui récupère livre suivant dans série
    Renvoie
    """
    cursor.execute("""
    SELECT id_livre FROM sae._utilisateur NATURAL JOIN sae._livre_utilisateur NATURAL JOIN sae._episode_serie WHERE id_utilisateur = %s;
    """, (user,))

    record = cursor.fetchall()

    liste_continuer_lecture = []
    
    for y in record:
        cursor.execute("""
        SELECT id_serie,numero_episode FROM sae._episode_serie WHERE id_livre = %s;
        """, (y[0],))
        serie = cursor.fetchall()

        
        if serie[0][1] is not None and serie[0][1].isdigit():
            episode = int(serie[0][1])+1

            cursor.execute("""
            SELECT id_livre FROM sae._episode_serie WHERE numero_episode = '%s' AND id_serie='%s';
            """, (episode,serie[0][0]))
            livre = cursor.fetchall()
            liste_continuer_lecture.append(livre[0][0])

    return liste_continuer_lecture

def getAuthorById(cursor, id):
    cursor.execute(f"""
    SELECT nom, origine, sexe, note_moyenne, nb_reviews, nb_critiques 
    FROM _auteur
    WHERE id_auteur = %s;
    """, (id,))

    authorRaw = cursor.fetchall()

    # Si aucun utilisateur n'a été récupéré renvoie -1, indiquant qu'aucune donnée n'a été récupérée
    if len(authorRaw) == 0:
        return -1

    # Reformate les données
    #TODO author = [list(author) for author in authorRaw]

    return authorRaw[0]

def changeUserData(idUtil,key,value):
    return -1

def ajoutClause(recherche,ajoutWhere):
    if ajoutWhere:
        recherche += "WHERE "
        ajoutWhere=False
    else:
        recherche += "AND "
    return (recherche,ajoutWhere)

def getAllGenres(cursor):
    cursor.execute(f"""
    SELECT id_genre, libelle_genre 
    FROM _genre;
    """)

    genresRaw = cursor.fetchall()

    # Reformate les données
    genres = [list(genre) for genre in genresRaw]

    return genres

def getAllAuthors(cursor):
    cursor.execute(f"""
    SELECT _auteur.id_auteur, _auteur.nom 
    FROM _auteur;
    """)

    authorsRaw = cursor.fetchall()

    # Reformate les données
    authors = [list(author) for author in authorsRaw]

    return authors

def rechercheLivre(cursor, pageNum=1, paginTaille=20, titre=None, auteurs=None, genres=None, minNote=None, maxNote=None):
    baseQuery = """
        SELECT DISTINCT _livre.id_livre, _livre.titre
        FROM _livre
        LEFT JOIN _genre_livre ON _livre.id_livre = _genre_livre.id_livre
        LEFT JOIN _auteur_livre ON _livre.id_livre = _auteur_livre.id_livre
        WHERE 1=1
    """
    parameterList = []
    # Add general filters if present
    if auteurs:
        baseQuery += " AND id_auteur = ANY(%s) "
        parameterList.append(auteurs)
    
    if genres:
        baseQuery += " AND id_genre = ANY(%s) "
        parameterList.append(genres)
    
    if minNote is not None:
        baseQuery += " AND note_moyenne >= %s "
        parameterList.append(minNote)
    
    if maxNote is not None:
        baseQuery += " AND note_moyenne <= %s "
        parameterList.append(maxNote)
    
    if titre:
        # Create a CTE that combines:
        #  - an exact match (priority 1)
        #  - a "starts with" match (priority 2)
        combinedQuery = f"""
            WITH combined AS (
                SELECT id_livre, titre, 1 AS priority 
                FROM ({baseQuery}) AS filtered_books
                WHERE LOWER(titre) = LOWER(%s)
                UNION ALL
                SELECT id_livre, titre, 2 AS priority 
                FROM ({baseQuery}) AS filtered_books
                WHERE LOWER(titre) LIKE LOWER(CONCAT(%s,'%%'))
                UNION ALL
                SELECT id_livre, titre, 3 AS priority
                FROM ({baseQuery}) AS filtered_books
                WHERE LOWER(titre) LIKE LOWER(CONCAT('%%',%s,'%%'))
            )
            SELECT id_livre, titre, MIN(priority) AS priority
            FROM combined
            GROUP BY id_livre, titre
            ORDER BY priority
            LIMIT %s OFFSET %s
        """
        parameterList.append(titre)
        parameterList = parameterList+parameterList+parameterList
        finalQuery = combinedQuery
    else:
        finalQuery = baseQuery + " ORDER BY _livre.id_livre LIMIT %s OFFSET %s"
    
    parameterList.append(paginTaille)
    parameterList.append(paginTaille * (pageNum - 1))
    
    print(finalQuery)  # For debugging
    cursor.execute(finalQuery,parameterList)
    rawBookData = cursor.fetchall()
    print("--------------------------------")
    print(rawBookData) # For debugging
    # Extract the list of book IDs
    bookIdList = [row[0] for row in rawBookData]
    print("--------------------------------")
    print(bookIdList) # For debugging
    return bookIdList


def rechercheAuteur(cursor, nom):
    cursor.execute("""
        SELECT DISTINCT _auteur.id_auteur, nom, origine, sexe, note_moyenne, libelle_genre
        FROM _auteur
        LEFT JOIN _auteur_genre ON _auteur_genre.id_auteur = _auteur.id_auteur
        LEFT JOIN _genre ON _genre.id_genre = _auteur_genre.id_genre
        WHERE nom LIKE '%%%s%%';
    """,(nom,))
    # This chain is because we need to wrap the %s to insert the string with the joker %, we need to double it to make it work
    
    rawAuthorData = cursor.fetchall()
    
    # Reformate les données
    authors = [list(author) for author in rawAuthorData]

    return authors

#connexion = setUpConnection()
#cursor = setUpCursor(connexion)
#print(getLivresUtilisateur(cursor, 131))
