import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def vector_genre(lvr,dico_genre):
    vector = []
    for genre in dico_genre:
        if genre in lvr["Genre"]:
            vector.append(1)
        else:
            vector.append(0)
    return vector
    
def vector_genre_item(lvr,dico_genre):
    vector = []
    for genre in dico_genre:
        if genre in lvr:
            vector.append(1)
        else:
            vector.append(0)
    return vector


def genre(user=False):


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



    # dico_genre = []
    # for i in record:
    #     if i[1] not in dico_genre:
    #         dico_genre.append(i[1])

    livre_user = pd.DataFrame(
        [
            ["M1", "action"],
            ["M2", "science-fiction"],
            ["M3", "comedie"],
            ["M4", "drama"],
            ["M5", "comedie"],
            ["M6", "comedie"],
            ["M7", "drama"],
            ["M8", "action"]
        ],

        columns = ['Livre', 'Genre']
    )

    for i in range(len(record)):    
        record[i]= list(record[i])

    livre = pd.DataFrame(record, columns = ['Livre', 'Genre']) 

    livre["isTrue"] = True
    vectorAuthor = livre.pivot_table(index="Livre", columns="Genre", values="isTrue")
    vectorAuthor = vectorAuthor.fillna(0)

    print(vectorAuthor)


    # vector = vector_genre(livre_user,dico_genre)

    # livre = livre.groupby('Livre')['Genre'].apply(', '.join).reset_index()

    # livre['vector'] = livre.apply(lambda x: vector_genre_item(x.Genre,dico_genre), axis=1)


    # print(vector)
    # print(livre.iloc[2]['vector'])


    # matrix = []
    # cpt = 0
    # for vect1 in vector:
    #     matrix.append([])
    #     for vect2 in livre['vector']:
    #         matrix[cpt].append(cosine_similarity(np.array(vect1).reshape(1, -1), np.array(vect2).reshape(1, -1))[0][0].item())
    #     cpt += 1

    # print(matrix)


genre()