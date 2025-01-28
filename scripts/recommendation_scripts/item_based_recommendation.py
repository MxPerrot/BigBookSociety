import pandas as pd
import numpy as np
from numpy.linalg import norm
import recommendation_utilities as ru
import database_functions as bdd

# Nombres de données prises en compte dans la création des vecteurs de livres
NB_DIMENTION_VECTEUR = 3
# Nombre de livres qui vont être testés (une valeur plus élevée peut causer des ralentissements)
NOMBRE_LIVRES_TESTES = 1000

# ----------------------------------
#  Fonctions de vectorisation 
# ----------------------------------

def vectorizeBookLength(nb_pages):
    """
    Transforme le nombre de pages en un entier servant de dimension au vecteur d'un livre
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

def defineUserBooksVect(userBookDataFrame):
    """
    Génère un dictionnaire contenant les vecteurs des livres de l'utilisateur
    """
    completeBookVector = {}

    for id_livreUsr, livreUsr in userBookDataFrame.groupby(by="id_livre"):
        # Tout les lignes d'un même livre ont les mêmes valeurs pour les colonnes suivantes, on prend donc celle de la première ligne
        popularite = int(livreUsr["nb_notes"].apply(vectorizeReviewNb).iloc[0])
        longeurLivre = int(livreUsr["nombre_pages"].apply(vectorizeBookLength).iloc[0])
        periode = int(livreUsr["date_publication"].apply(vectorizePublishingDate).iloc[0])
        completeBookVector[id_livreUsr] = (popularite, longeurLivre, periode)

    return completeBookVector

def defineBookVect(book):
    """
    Génère le vecteur du livre donné en paramètre
    """
    vecteurLivre = []
    # Tout les lignes d'un même livre ont les mêmes valeurs pour les colonnes suivantes, on prend donc celle de la première ligne
    vecteurLivre.append(int(book["nb_notes"].apply(vectorizeReviewNb).iloc[0]))
    vecteurLivre.append(int(book["nombre_pages"].apply(vectorizeBookLength).iloc[0]))
    vecteurLivre.append(int(book["date_publication"].apply(vectorizePublishingDate).iloc[0]))
    return vecteurLivre

# ----------------------------
#  Fonction principale
# ----------------------------

def recommendationItemBased(cursor, modelGenres, id_utilisateur, nbRecommendations, evaluationBookDataFrame):
    """
    Renvoie les livres les plus similaires à ceux de l'utilisateur donnée en paramètre parmi ceux à évaluer
    """

    # Crée les vecteurs des livres de l'utilisateur
    userBookDataFrame = bdd.getLivresUtilisateur(cursor, id_utilisateur)
    userBookVectors = defineUserBooksVect(userBookDataFrame)
    
    # Vérifie que l'utilisateur à bien des livres pouvant être vectorisés sinon renvoie une liste vide
    sumVect = 0
    for vect in userBookVectors.values():
        sumVect += sum(vect)
    if sumVect == 0:
        return []


    moySimCosLivres = {}
    booksScores = {}

    # Parcours des livres à tester
    for id_livreEva, livreEva in evaluationBookDataFrame.groupby(by="id_livre"):
        sumScores = 0
        cmpt = 0
        
        vecteurEva = defineBookVect(livreEva)
        # Vérifie que le livre peut être vectorisé
        if sum(vecteurEva) != 0:
            cmptCos = 0
            sumSimCosLivres = 0

            # Compare grace à la similarité cosine à quel point chaque livre utilisateur est proche du livre testé
            for id_livreUser, vecteurUser in userBookVectors.items():
                cosine = np.dot(vecteurUser,vecteurEva)/(norm(vecteurUser)*norm(vecteurEva))
                # Fait la somme des similarités
                sumSimCosLivres = sumSimCosLivres + cosine
                cmptCos += 1
            # Récupère la similarité cosine moyenne
            if cmptCos != 0:
                moySimCosLivres[id_livreEva] = float(sumSimCosLivres)/cmptCos
            else:
                moySimCosLivres[id_livreEva] = 0
        
            # Parcours les livres utilisateurs
            for id_livreUser, livreUser in userBookDataFrame.groupby(by="id_livre"):
                # Récupère les coefficients de similarité sur plusieurs critères
                cmpAuteur = ru.valeursEnCommun('id_auteur', livreEva, livreUser, "id_livre")
                cmpPrix = ru.valeursEnCommun('id_prix', livreEva, livreUser, "id_livre")
                cmpCadres = ru.valeursEnCommun('id_pays', livreEva, livreUser, "id_livre")
                cmpOrigines = ru.compareValeur('origine_auteur', livreEva, livreUser)
                cmpEditeur = ru.compareValeur('id_editeur', livreEva, livreUser)
                cmpSexe = ru.compareValeur('sexe_auteur', livreEva, livreUser)
                cmpGenre = ru.vect_genre(modelGenres, livreEva["genre"], livreUser["genre"])  
                
                cmpt += 1
                # Fait la somme des scores obtenus par un livre avec la moyenne des similarités
                sumScores += ru.calculateScore(moySimCosLivres[id_livreEva], [cmpAuteur, cmpPrix, cmpCadres, cmpOrigines, cmpEditeur, cmpGenre, cmpSexe], NB_DIMENTION_VECTEUR)
                
            # Récupère le score moyen obtenu pour le livre testé
            if cmpt > 0:
                booksScores[id_livreEva] = sumScores/cmpt
            else:
                booksScores[id_livreEva] = 0

    # Trie les livres par score puis prends les X avec les scores les plus élevés
    bestBooks = sorted(booksScores.items(), key=lambda x: x[1], reverse=True)[:nbRecommendations]

    '''
    # DEBUG : Recupère les infos des livres recommandés pour verifier leur cohérence
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

    # Revoie une liste des identifiants des livres recommandés
    return [tupl[0] for tupl in bestBooks]

# Entrainement du modèle des genres
modelGenres = ru.model_genre()
# Met en place le curseur de la connexion à la base de données
cursor = bdd.setUpCursor()
print(recommendationItemBased(cursor, modelGenres, 11, 5, bdd.getLivresAEvaluer(cursor, NOMBRE_LIVRES_TESTES)))