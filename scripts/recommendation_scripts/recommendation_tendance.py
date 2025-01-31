import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2
import random


def tendance(limit):

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


    cursor.execute(f"""
    SELECT b.id_livre
    FROM sae._livre b
    INNER JOIN sae._episode_serie s ON b.id_livre = s.id_livre
    WHERE numero_episode = '1'
    AND b.note_moyenne IS NOT NULL
    AND b.nb_notes IS NOT NULL
    ORDER BY b.nb_notes DESC, b.note_moyenne DESC
    LIMIT {limit};
    """)

    record = cursor.fetchall()

    list=[]

    for i in range(len(record)):
        list.append(record[i][0])

    return list

def same_author(user, limit):
    """
    Sélectionne les livres lus/aimé par l'utilisateur
    Pour chaque regarde et sauvegarde l'auteur
    Récupère autre livre populaire de l'auteur avec id de livres différent
    Renvoie
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

    cursor = connection.cursor()


    cursor.execute(f"""
    SELECT id_auteur,id_livre FROM sae._utilisateur 
    NATURAL JOIN sae._livre_utilisateur 
    NATURAL JOIN sae._auteur_livre
    WHERE id_utilisateur = {user};
    """)

    record = cursor.fetchall()

    liste_livre_lu = []

    for i in record:
        liste_livre_lu.append(i[1])

    liste_livre_recommender = []

    for i in record:
        cursor.execute(f"""
        SELECT id_livre FROM sae._auteur_livre
        NATURAL JOIN sae._livre
        WHERE id_auteur = {i[0]};
        """)
        livres = cursor.fetchall()
        for y in livres:
            if (y not in liste_livre_lu) & (y not in liste_livre_recommender):
                liste_livre_recommender.append(y)

    for y in range(len(liste_livre_recommender)):
        liste_livre_recommender[y] = liste_livre_recommender[y][0]


    return random.sample(liste_livre_recommender, limit)


def in_series(user):
    """
    Sélectionne les livres lus/aimé par l'utilisateur
    Pour chaque regarde si dans une série
    Si oui récupère livre suivant dans série
    Renvoie
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

    cursor = connection.cursor()


    cursor.execute(f"""
    SELECT id_livre FROM sae._utilisateur NATURAL JOIN sae._livre_utilisateur NATURAL JOIN sae._episode_serie WHERE id_utilisateur = {user};
    """)

    record = cursor.fetchall()

    liste_continuer_lecture = []
    
    for y in record:
        cursor.execute(f"""
        SELECT id_serie,numero_episode FROM sae._episode_serie WHERE id_livre = {y[0]};
        """)
        serie = cursor.fetchall()

        if serie[0][1] is not None:
            episode = int(serie[0][1])+1

            cursor.execute(f"""
            SELECT id_livre FROM sae._episode_serie WHERE numero_episode = '{episode}';
            """)
            livre = cursor.fetchall()
            liste_continuer_lecture.append(livre[0][0])

    return liste_continuer_lecture

def decouverte(limit):

    load_dotenv() 

    connection = psycopg2.connect(
        database=os.getenv("DATABASE_NAME"), 
        user=os.getenv("USERNAME"), 
        password=os.getenv("PASSWORD"), 
        host=os.getenv("HOST"), 
        port=os.getenv("PORT")
    )

    cursor = connection.cursor()

    cursor.execute(f"""
    SELECT * FROM sae._livre 
    WHERE note_moyenne is not null 
    and nb_notes>1000 
    and nb_notes<50000 
    ORDER BY note_moyenne DESC 
    LIMIT {limit};
    """)

    # 

    record = cursor.fetchall()

print(same_author(69, 5))
print(in_series(9))