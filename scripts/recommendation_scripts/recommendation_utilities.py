import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2
import pandas as pd
import numpy as np
import re
import gensim
import itertools

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

def compareValeur(nomValeur, elemX, elemY):
    """
    Renvoie True si ces éléments partagent la même valeur indiquée par le paramétre nomValeur
    """
    return bool(elemX[nomValeur].iloc[0] == elemY[nomValeur].iloc[0])

def valeursEnCommun(nomValeur, elemX, elemY, valeurComp):
    """
    Donne un indice permettant de savoir à quel point deux livres sont proches basé sur une valeur indiquée en paramètre (nomValeur)
    """
    nbValeurEnCommun = 0
    listeValeursX = elemX[nomValeur].unique()
    listeValeursY = elemY[nomValeur].unique()
    if elemX[valeurComp].iloc[0] == elemY[valeurComp].iloc[0]:
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

def calculateScore(cossim, listSim, nbVecteur):
    """
    Calcule le Score global de similarité d'une comparaison entre deux livres
    Fait la moyenne des indices de similarités et pondérant celui de la similarité cosine dû au fait qu'elle prends plus de valeurs en compte
    """
    scoreSum = cossim * nbVecteur 
    cmpt = nbVecteur
    for sim in listSim:
        scoreSum += sim
        cmpt += 1
    return float(scoreSum/cmpt)

def genre_expand(genre):
    expanded_genre = genre.split(" ")
    res = re.split(r'[;,\s,-]+', genre)
    return res

def model_genre():

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

    cursor.execute("select id_livre,libelle_genre from sae._livre NATURAL JOIN sae._genre_livre NATURAL JOIN sae._genre;")

    record = cursor.fetchall()

    for i in range(len(record)):    
        record[i]= list(record[i])

    livre = pd.DataFrame(record, columns = ['Livre', 'Genre']) 


    livre['Genre'] = livre['Genre'].apply(genre_expand)

    livre = livre.explode('Genre')

    livre = livre.groupby('Livre')['Genre'].apply(list).reset_index(name='Genre')

    model1 = gensim.models.Word2Vec(livre['Genre'], min_count=1,vector_size=100, window=5)

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

"""
model = model_genre()
print(vect_genre(model,["bdsm", "history"], ["romance, science"]))
"""