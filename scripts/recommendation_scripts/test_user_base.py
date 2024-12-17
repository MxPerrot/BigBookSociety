import os
from dotenv import load_dotenv, dotenv_values 
import psycopg2
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------------
#  Fonctions de vectorisation 
# ----------------------------------

def vectorizeBookLength(nb_pages):
    if pd.isnull(nb_pages):
        indTaille = 0
    else:
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
        else:
            indTaille = 1
    return indTaille

def vectorizeReviewNb(nb_note):
    if pd.isnull(nb_note):
        indPop = 0
    else:
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
        else:
            indPop = 1
    return indPop

def vectorizePublishingDate(publishingDate):
    if pd.isnull(publishingDate):
        indPeriod = 0
    else:
        date = publishingDate.year
        if date > 2000:
            indPeriod = 10
        elif date > 1970:
            indPeriod = 9
        elif date > 1940:
            indPeriod = 8
        elif date > 1900:
            indPeriod = 7
        elif date > 1850:
            indPeriod = 6
        elif date > 1775:
            indPeriod = 5
        elif date > 1700:
            indPeriod = 4
        elif date > 1650:
            indPeriod = 3
        elif date > 1570:
            indPeriod = 2
        else:
            indPeriod = 1
    return indPeriod

def vectorizeAuthorGender(gender):
    if pd.isnull(gender):
        indGender = 0
    else:
        if gender == "male":
            indGender = 1
        elif gender == "female":
            indGender = 2
        else:
            indGender = 3
    return indGender

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

cursor.execute("""
    SELECT DISTINCT _utilisateur.id_utilisateur, _livre.id_livre, _livre.titre, _livre.nb_notes, _livre.note_moyenne, 
                    _livre.nombre_pages, _livre.date_publication, _livre.description, _auteur.nom, _auteur.sexe
    FROM _utilisateur 
    INNER JOIN _livre_utilisateur ON _livre_utilisateur.id_utilisateur = _utilisateur.id_utilisateur
    INNER JOIN _livre ON _livre.id_livre = _livre_utilisateur.id_livre
    LEFT JOIN _auteur_livre ON _livre.id_livre = _auteur_livre.id_livre
    LEFT JOIN _auteur ON _auteur_livre.id_auteur = _auteur.id_auteur
""")

dataResults = cursor.fetchall()
listResults = []

for i in dataResults:
    listResults.append(list(i))

userDataFrame = pd.DataFrame(listResults, columns = ["id_utilisateur", "id_livre", "titre", "nb_notes", "note_moyenne", 
                                                    "nombre_pages", "date_publication", "description", "nom_auteur", "sexe_auteur"])

# Vectorisation des utilisateurs
userVector = {}
userBooks = userDataFrame.groupby('id_utilisateur')

for user, user_books in userBooks:
    userVector[user] = []
    # Vectorisation sur chaque livre lu par l'utilisateur
    for _, row in user_books.iterrows():
        # Fusionner les valeurs de chaque livre dans une seule liste
        userVector[user].extend([
            vectorizeReviewNb(row['nb_notes']),
            vectorizeBookLength(row['nombre_pages']),
            vectorizePublishingDate(row['date_publication']),
            vectorizeAuthorGender(row['sexe_auteur'])
        ])

# Conversion des vecteurs en DataFrame pour calculer la similarité
userVectorDF = pd.DataFrame.from_dict(userVector, orient='index').fillna(0)

# Affichage de la DataFrame des vecteurs utilisateurs
print("DataFrame des vecteurs des utilisateurs :")
print(userVectorDF)

# Calcul de la similarité entre utilisateurs
similarity_matrix = cosine_similarity(userVectorDF)

# Affichage de la matrice de similarité
print("Matrice de similarité entre utilisateurs :")
print(similarity_matrix)

# Affichage de la similarité entre deux utilisateurs (par exemple user 1 et user 2)
print("Similarité entre user 1 et user 2 :", similarity_matrix[0][1])
