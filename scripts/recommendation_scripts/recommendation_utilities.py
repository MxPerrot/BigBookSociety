import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2
import pandas as pd
import numpy as np
import re
from gensim.models import Word2Vec
import itertools

def compareValeur(nomValeur, elemX, elemY):
    """
    Renvoie True (1) si ces éléments partagent la même valeur indiquée par le paramétre nomValeur sinon False (0)
    """
    return bool(elemX[nomValeur].iloc[0] == elemY[nomValeur].iloc[0])

def valeursEnCommun(nomValeur, elemX, elemY, valeurComp):
    """
    Donne un coefficient permettant de savoir à quel point deux éléments sont similaires basé sur une valeur indiquée en paramètre (nomValeur)
    """
    nbValeurEnCommun = 0
    # Si ces elements ont le même identifiant, ils sont le même
    if elemX[valeurComp].iloc[0] == elemY[valeurComp].iloc[0]:
        return 1
    # Recupère la liste des valeurs uniques de la colonne du dataframe 'nomValeur'
    listeValeursX = elemX[nomValeur].unique()
    listeValeursY = elemY[nomValeur].unique()
    # Si aucun d'entre eux n'ont de données ils sont similaires
    if len(listeValeursX) == 0 and len(listeValeursY) == 0:
        return 1
    # Si seulement l'un d'entre eux n'en a pas, ils ne partage aucune similarité
    if len(listeValeursX) == 0 or len(listeValeursY) == 0:
        return 0
    # Sinon compte le nombre de valeurs en commun
    for valeursX in listeValeursX:
        for valeursY in listeValeursY:
            if valeursX == valeursY:
                nbValeurEnCommun += 1
    # Revoie ensuite la moyenne de valeurs en commun (somme divisée par la plus grande longueur parmi les deux listes)
    if len(listeValeursX) > len(listeValeursY):
        return nbValeurEnCommun/len(listeValeursX)
    else:
        return nbValeurEnCommun/len(listeValeursY)

def calculateScore(cossim, listSim, nbVecteur):
    """
    Calcule le Score global de similarité d'une comparaison entre deux livres
    """
    # Pondère la similarité cosine par rapport au nombre de variables qu'elle prend en compte
    scoreSum = cossim * nbVecteur 
    cmpt = nbVecteur
    # Calcule la somme des similarité
    for sim in listSim:
        scoreSum += sim
        cmpt += 1
    # Renvoie la similarité moyenne (Score)
    return float(scoreSum/cmpt)

def genre_expand(genre):
    expanded_genre = genre.split(" ")
    res = re.split(r'[;,\s,-]+', genre)
    return res

def model_genre(cursor):
    cursor.execute("select id_livre,libelle_genre from BigBookSociety._livre NATURAL JOIN BigBookSociety._genre_livre NATURAL JOIN BigBookSociety._genre;")

    record = cursor.fetchall()

    for i in range(len(record)):    
        record[i]= list(record[i])

    livre = pd.DataFrame(record, columns = ['Livre', 'Genre']) 

    livre['Genre'] = livre['Genre'].apply(genre_expand)

    livre = livre.explode('Genre')

    livre = livre.groupby('Livre')['Genre'].apply(list).reset_index(name='Genre')

    model1 = Word2Vec(livre['Genre'], min_count=1,vector_size=100, window=5)

    return model1


def vect_genre(model,livre1genre,livre2genre):

    if len(livre1genre) < 1 or len(livre2genre) < 1:
        return 0

    tot = 0
    index = 0
    genres1 = []
    genres2 = []

    for i in livre1genre:
        if pd.isna(i):
            return 0
        genres1.append(genre_expand(i))
    for y in livre2genre :
        if pd.isna(y):
            return 0
        genres2.append(genre_expand(y))

    genres1 = list(itertools.chain.from_iterable(genres1))
    genres2 = list(itertools.chain.from_iterable(genres2))

    for i in genres1:
        for y in genres2:
            tot = tot + model.wv.similarity(i,y)
            index+=1
    
    return tot/index
