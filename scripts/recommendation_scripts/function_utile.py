import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2
import pandas as pd
import numpy as np
import re


def genre_expand(genre):
    expanded_genre = genre.split(" ")
    res = re.split(r'[;,\s,-]+', genre)
    return res

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


print(livre['Genre'].nunique())