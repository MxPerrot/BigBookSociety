import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import norm
import function_utile as fu

NB_DIMENTION_VECTEUR = 4
NOMBRE_LIVRES_TESTES = 1000

# ----------------------------------
#  Fonctions de vectorisation 
# ----------------------------------

def vectorizeBookLength(nb_pages):
    """
    Transforme le nombre de pages en un entier servant de dimention au vecteur d'un livre
    Cet entier représente dans quelle tranche d'une échelle de taille le livre se trouve.
    (1 est un livre court, 6 étant gigantesque)
    """
    if pd.isnull(nb_pages):
        indTaille = 0
    else :
        if nb_pages > 1000:
            indTaille = 6
        elif nb_pages > 500:
            indTaille = 5
        elif nb_pages > 200:
            indTaille = 4
        elif nb_pages > 100:
            indTaille = 3
        elif nb_pages > 50:
            indTaille = 2
        else :
            indTaille = 1
    return indTaille

def vectorizeReviewNb(nb_note):
    """
    Transforme le nombre de review en un entier servant de dimention au vecteur d'un livre
    Cet entier représente dans quelle tranche d'une échelle de popularité un livre se trouve.
    (1 est un livre peu connu, 9 étant un livre très connu)
    """
    if pd.isnull(nb_note):
        indPop = 0
    else :
        if nb_note > 1000000:
            indPop = 9
        elif nb_note > 500000:
            indPop = 8
        elif nb_note > 250000:
            indPop = 7
        elif nb_note > 100000:
            indPop = 6
        elif nb_note > 50000:
            indPop = 5
        elif nb_note > 10000:
            indPop = 4
        elif nb_note > 5000:
            indPop = 3
        elif nb_note > 1000:
            indPop = 2
        else :
            indPop = 1
    return indPop

def vectorizePublishingDate(publishingDate):
    """
    Transforme l'an de la date de publication en un entier servant de dimention au vecteur d'un livre
    Cet entier représente dans quelle courant litéraire ce livre se trouve t'il.
    Les courants litéraires associés sont indiqués plus bas.
    (1 etant un livre ancien, 10 etant un livre récent)
    """
    if pd.isnull(publishingDate):
        indPeriod = 0
    else :
        date = publishingDate.year
        # Littérature moderne
        if date > 2000:
            indPeriod = 10
        # Nouveau roman
        elif date > 1970:
            indPeriod = 9
        # Dada, Surréalisme, Absurde
        elif date > 1940:
            indPeriod = 8
        # Parnasse, Symbolisme, Réalisme, Naturalisme
        elif date > 1900:
            indPeriod = 7
        # Réalisme, Naturalisme, Romantisme
        elif date > 1850:
            indPeriod = 6
        # Lumières
        elif date > 1775:
            indPeriod = 5
        # Classicisme
        elif date > 1700:
            indPeriod = 4
        # Baroque
        elif date > 1650:
            indPeriod = 3
        # Humanisme, Pléiade
        elif date > 1570:
            indPeriod = 2
        # Tout ce qui est plus ancien
        else :
            indPeriod = 1
    return indPeriod

# TODO : Vérifier le sens ce cette dimention de vecteur
def vectorizeAuthorGender(gender):
    """
    TODO
    """
    if pd.isnull(gender):
        indGender = 0
    else :
        if gender == "male":
            indGender = 1
        elif gender == "female":
            indGender = 2
        else:
            indGender = 3
    return indGender

# ----------------------------
#  Autres fonctions
# ----------------------------

def valeursEnCommun(nomValeur, livreX, livreY):
    """
    Donne un indice permettant de savoir à quel point deux livres sont proches basé sur une valeur indiquée en paramètre (nomValeur)
    """
    nbValeurEnCommun = 0
    listeValeursX = livreX[nomValeur].unique()
    listeValeursY = livreY[nomValeur].unique()
    if livreX["id_livre"].iloc[0] == livreY["id_livre"].iloc[0]:
        return 1
    if len(listeValeursX) == 0 and len(listeValeursY) == 0:
        return 1
    if len(listeValeursX) == 0 or len(listeValeursY) == 0:
        return 0
    for valeursX in listeValeursX:
        for valeursY in listeValeursY:
            if valeursX == valeursY:
                nbValeurEnCommun += 1
    if len(listeValeursX) > len(listeValeursY):
        return nbValeurEnCommun/len(listeValeursX)
    else:
        return nbValeurEnCommun/len(listeValeursY)
    
def compareValeur(nomValeur, livreX, livreY):
    """
    Renvoie True si ces livres partagent la même valeur indiquée par le paramétre nomValeur
    """
    return bool(livreX[nomValeur].iloc[0] == livreY[nomValeur].iloc[0])

def calculateScore(cossim, listSim):
    """
    Calcule le Score global de similarité d'une comparaison entre deux livres
    Fait la moyenne des indices de similarités et pondérant celui de la similarité cosine dû au fait qu'elle prends plus de valeurs en compte
    """
    scoreSum = cossim * NB_DIMENTION_VECTEUR
    cmpt = NB_DIMENTION_VECTEUR
    for sim in listSim:
        scoreSum += sim
        cmpt += 1
    return float(scoreSum/cmpt)
    
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

def getLivresAEvaluer(cursor):
    cursor.execute(f"""
        SELECT _livre.id_livre
        FROM _livre
        ORDER BY random()
        LIMIT {NOMBRE_LIVRES_TESTES};
    """)

    idLivresAEvaluerRaw = cursor.fetchall()
    idLivresAEvaluer = tuple([livre[0] for livre in idLivresAEvaluerRaw])

    cursor.execute(f"""
        SELECT _livre.id_livre, _livre.titre, _livre.nb_notes, _livre.note_moyenne, _livre.nombre_pages, _livre.date_publication, _livre.description, _editeur.id_editeur, _editeur.nom_editeur, _prix.id_prix, _prix.annee_prix, _serie.nom_serie, _episode_serie.numero_episode, _pays.id_pays, _auteur.id_auteur, _auteur.sexe, _auteur.origine, _genre.id_genre, _genre.libelle_genre
        FROM _livre

        INNER JOIN _editeur ON _editeur.id_editeur = _livre.id_editeur

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

        WHERE _livre.id_livre IN {idLivresAEvaluer}
    """)

    bookData = cursor.fetchall()
    
    if len(bookData) == 0:
        return -1
  
    bookList = [list(book) for book in bookData]

    return pd.DataFrame(bookList, columns = ["id_livre", "titre", "nb_notes", "note_moyenne", "nombre_pages", "date_publication", "description", "id_editeur", "nom_editeur", "id_prix", "annee_prix", "nom_serie", "numero_episode", "id_pays", "id_auteur", "sexe_auteur", "origine_auteur", "id_genre", "genre"])

def defineUserVect(userBookDataFrame):
    completeBookVector = {}

    for id_livreUsr, livreUsr in userBookDataFrame.groupby(by="id_livre"):
        # Tout les lignes d'un même livre ont les mêmes valeurs pour les colonnes suivantes, on prend donc celle de la première ligne
        popularite = int(livreUsr["nb_notes"].apply(vectorizeReviewNb).iloc[0])
        longeurLivre = int(livreUsr["nombre_pages"].apply(vectorizeBookLength).iloc[0])
        periode = int(livreUsr["date_publication"].apply(vectorizePublishingDate).iloc[0])
        sexeAuteur = int(livreUsr["sexe_auteur"].apply(vectorizeAuthorGender).iloc[0])
        completeBookVector[id_livreUsr] = (popularite, longeurLivre, periode, sexeAuteur)

    return completeBookVector

def defineBookVect(book):
    vecteurLivre = []
    # Tout les lignes d'un même livre ont les mêmes valeurs pour les colonnes suivantes, on prend donc celle de la première ligne
    vecteurLivre.append(int(book["nb_notes"].apply(vectorizeReviewNb).iloc[0]))
    vecteurLivre.append(int(book["nombre_pages"].apply(vectorizeBookLength).iloc[0]))
    vecteurLivre.append(int(book["date_publication"].apply(vectorizePublishingDate).iloc[0]))
    vecteurLivre.append(int(book["sexe_auteur"].apply(vectorizeAuthorGender).iloc[0]))
    return vecteurLivre

def recommendationItemBased(cursor, modelGenres, id_utilisateur, nbRecommendations):
    userBookDataFrame = getLivresUtilisateur(cursor, id_utilisateur)
    userBookVectors = defineUserVect(userBookDataFrame)

    evaluationBookDataFrame = getLivresAEvaluer(cursor)
    vecteursLivres = {}
    moySimCosLivres = {}

    for id_livreEva, livreEva in evaluationBookDataFrame.groupby(by="id_livre"):
        vecteursLivres[id_livreEva] = defineBookVect(livreEva)
    
    for id_livreEva, vecteurEva in vecteursLivres.items():
        cmpt = 0
        sumSimCosLivres = 0
        for id_livreUser, vecteurUser in userBookVectors.items():
            cosine = np.dot(vecteurUser,vecteurEva)/(norm(vecteurUser)*norm(vecteurEva))
            sumSimCosLivres = sumSimCosLivres + cosine
            cmpt += 1

        if cmpt != 0:
            moySimCosLivres[id_livreEva] = float(sumSimCosLivres)/cmpt
        else:
            moySimCosLivres[id_livreEva] = 0
    
    booksScores = {}

    for id_livreEva, livreEva in evaluationBookDataFrame.groupby(by="id_livre"):
        sumScores = 0
        cmpt = 0

        for id_livreUser, livreUser in userBookDataFrame.groupby(by="id_livre"):

            cmpAuteur = valeursEnCommun('id_auteur', livreEva, livreUser)
            cmpPrix = valeursEnCommun('id_prix', livreEva, livreUser)
            cmpCadres = valeursEnCommun('id_pays', livreEva, livreUser)
            cmpOrigines = valeursEnCommun('origine_auteur', livreEva, livreUser)
            cmpEditeur = compareValeur('id_editeur', livreEva, livreUser)
            cmpGenre = fu.vect_genre(modelGenres, livreEva["genre"], livreUser["genre"])  
            
            cmpt += 1
            sumScores += calculateScore(moySimCosLivres[id_livreEva], [cmpAuteur, cmpPrix, cmpCadres, cmpOrigines, cmpEditeur, cmpGenre])
            
        if cmpt > 0:
            booksScores[id_livreEva] = sumScores/cmpt
        else:
            booksScores[id_livreEva] = 0

    bestBooks = sorted(booksScores.items(), key=lambda x: x[1], reverse=True)[:nbRecommendations]

    '''
    for (key,value) in bestBooks:
        cursor.execute(f"""
        SELECT _livre.titre, _genre.libelle_genre
        FROM _livre
        LEFT JOIN _genre_livre ON _livre.id_livre = _genre_livre.id_livre
        LEFT JOIN _genre ON _genre_livre.id_genre = _genre.id_genre
        WHERE _livre.id_livre = {key};
        """)
        print(cursor.fetchall())
    print(userBookDataFrame)
    '''

    return [tupl[0] for tupl in bestBooks]

modelGenres = fu.model_genre()
cursor = setUpCursor()
print(recommendationItemBased(cursor, modelGenres, 11, 5))