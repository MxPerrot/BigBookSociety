import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2

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


print(tendance(10))