import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2
import pandas as pd
import numpy as np
import re
from gensim.models import Word2Vec
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
import itertools


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


def vect_genre(model,livre1,livre2):
     tot = 0
     index = 0
     genres1 = []
     genres2 = []

     for i in livre1:
        genres1.append(genre_expand(i))
     for y in livre2 :
        genres2.append(genre_expand(y))

     genres1 = list(itertools.chain.from_iterable(genres1))
     genres2 = list(itertools.chain.from_iterable(genres2))

     for i in genres1:
          for y in genres2:
               tot = tot + model.wv.similarity(i,y)
               index+=1
     
     return tot/index


model = model_genre()
