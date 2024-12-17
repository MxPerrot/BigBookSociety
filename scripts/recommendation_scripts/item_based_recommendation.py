import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

NB_DIMENTION_VECTEUR = 4

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

def addVector(id, vector):
    return vector[id]

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

"""
    FROM _utilisateur
    LEFT JOIN _utilisateur_genre ON _utilisateur.id_utilisateur = _utilisateur_genre.id_utilisateur
    LEFT JOIN _genre ON _genre.id_genre = _utilisateur_genre.id_genre
    LEFT JOIN _utilisateur_langue ON _utilisateur.id_utilisateur = _utilisateur_langue.id_utilisateur
    LEFT JOIN _langue ON _langue.id_langue = _utilisateur_langue.id_langue
    LEFT JOIN _utilisateur_motivation ON _utilisateur_motivation.id_utilisateur = _utilisateur.id_utilisateur
    LEFT JOIN _motivation ON _motivation.id_motivation = _utilisateur_motivation.id_motivation
    LEFT JOIN _utilisateur_procuration ON _utilisateur_procuration.id_utilisateur = _utilisateur.id_utilisateur
    LEFT JOIN _procuration ON _procuration.id_procuration = _utilisateur_procuration.id_procuration
    LEFT JOIN _utilisateur_raison_achat ON _utilisateur_raison_achat.id_utilisateur = _utilisateur.id_utilisateur
    LEFT JOIN _raison_achat ON _raison_achat.id_raison_achat = _utilisateur_raison_achat.id_raison_achat
"""

cursor.execute("""
    SELECT DISTINCT _livre.id_livre, _livre.titre, _livre.nb_notes, _livre.note_moyenne, _livre.nombre_pages, _livre.date_publication, _livre.description, _editeur.id_editeur, _editeur.nom_editeur, _prix.id_prix, _prix.annee_prix, _serie.nom_serie, _episode_serie.numero_episode, _pays.id_pays, _auteur.id_auteur, _auteur.sexe, _auteur.origine, _genre.id_genre, _genre.libelle_genre
    FROM _utilisateur 
    INNER JOIN _livre_utilisateur ON _livre_utilisateur.id_utilisateur = _utilisateur.id_utilisateur
    INNER JOIN _livre ON _livre.id_livre = _livre_utilisateur.id_livre

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
""")

dataResults = cursor.fetchall()
listResults = []

for i in dataResults:
    listResults.append(list(i))

bookDataFrame = pd.DataFrame(listResults, columns = ["id_livre", "titre", "nb_notes", "note_moyenne", "nombre_pages", "date_publication", "description", "id_editeur", "nom_editeur", "id_prix", "annee_prix", "nom_serie", "numero_episode", "id_pays", "id_auteur", "sexe_auteur", "origine_auteur", "id_genre", "genre"])

GBbookDataFrame = bookDataFrame.groupby(by="id_livre")
bookDataFrame["isTrue"] = True

"nb_notes", 
vectorPopularite = {}
"nombre_pages", 
vectorLongeurLivre = {}
"date_publication", 
vectorPeriode = {}
# "description", 
"id_editeur", 
comparaisonEditeur = []
"nom_prix", 
comparaisonPrix = []
# "nom_serie", 
# "numero_episode", 
"id_pays", 
comparaisonCadres = []
"id_auteur", 
comparaisonAuteurs = []
"sexe_auteur", 
vectorSexeAuteur = {}
"origine_auteur", 
comparaisonOriginesAuteur = []
#vectorAuthorOrigin = bookDataFrame.pivot_table(index="id_livre", columns="origine_auteur", values="isTrue")
# "id_genre",


combinedMatrixes = []
listeIdLivre = []
for livre in GBbookDataFrame:
    listeIdLivre.append(livre[0])
    livreData = bookDataFrame[bookDataFrame['id_livre'] == livre[0]]
    vectorPopularite[livre[0]] = livreData["nb_notes"].apply(vectorizeReviewNb).iloc[0]
    vectorLongeurLivre[livre[0]] = livreData["nombre_pages"].apply(vectorizeBookLength).iloc[0]
    vectorPeriode[livre[0]] = livreData["date_publication"].apply(vectorizePublishingDate).iloc[0]
    vectorSexeAuteur[livre[0]] = livreData["sexe_auteur"].apply(vectorizeAuthorGender).iloc[0]

completeBookVector = pd.DataFrame(index=listeIdLivre)

completeBookVector["id_livre"] = completeBookVector.index
completeBookVector["vecteurPopularite"] = completeBookVector.apply(lambda x:  addVector(x['id_livre'], vectorPopularite), axis=1)
completeBookVector["vectorLongeurLivre"] = completeBookVector.apply(lambda x: addVector(x['id_livre'], vectorLongeurLivre), axis=1)
completeBookVector["vectorPeriode"] = completeBookVector.apply(lambda x: addVector(x['id_livre'], vectorPeriode), axis=1)
completeBookVector["vectorSexeAuteur"] = completeBookVector.apply(lambda x: addVector(x['id_livre'], vectorSexeAuteur), axis=1)

completeBookVector = completeBookVector.drop('id_livre', axis=1)
cosineSimilarityMatrix = cosine_similarity(completeBookVector)

for i, idLivreX in enumerate(listeIdLivre):
    """comparaisonAuteurs.append([])
    comparaisonPrix.append([])
    comparaisonCadres.append([])
    comparaisonOriginesAuteur.append([])
    comparaisonEditeur.append([])"""
    combinedMatrixes.append([])

    for j, idLivreY in enumerate(listeIdLivre):
        livreXData = bookDataFrame[bookDataFrame['id_livre'] == idLivreX]
        livreYData = bookDataFrame[bookDataFrame['id_livre'] == idLivreY]

        cmpAuteur = valeursEnCommun('id_auteur', livreXData, livreYData)
        # comparaisonAuteurs[i].append(cmpAuteur)
        cmpPrix = valeursEnCommun('id_prix', livreXData, livreYData)
        # comparaisonPrix[i].append(cmpPrix)
        cmpCadres = valeursEnCommun('id_pays', livreXData, livreYData)
        # comparaisonCadres[i].append(cmpCadres)
        cmpOrigines = valeursEnCommun('origine_auteur', livreXData, livreYData)
        # comparaisonOriginesAuteur[i].append(cmpOrigines)
        cmpEditeur = compareValeur('id_editeur', livreXData, livreYData)
        # comparaisonEditeur[i].append(cmpEditeur)
        """
        if i == j:
            print("Auteur : "+str(cmpAuteur))
            print("Prix : "+str(cmpPrix))
            print("Cadre : "+str(cmpCadres))
            print("Origine : "+str(cmpOrigines))
        """
        combinedMatrixes[i].append(calculateScore(cosineSimilarityMatrix[i][j], [cmpAuteur, cmpPrix, cmpCadres, cmpOrigines, cmpEditeur]))

print(combinedMatrixes)