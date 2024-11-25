import os
import pandas as pd
import numpy as np

PATH_DATA = "../Wizards/formulaire/"
PATH_POPULATE = os.path.join(PATH_DATA, "populate")

def main(resultats):
    os.makedirs(PATH_POPULATE, exist_ok=True) #Créé le dossier voulu


# Si besoin, croire plutot extract_books_from_authors et extract_authors_from_books qui sont plus ou moins propres
# Mais si possible, faire ça de zéro avec la doc sur le groupe discord

# RENOMMER LES COLONNES - VERSION BIEN
# booksData = booksData.rename(columns={
#    "id": "id_livre",
#    "title": "titre",
#    "rating_count": "nb_notes",
#    "review_count": "nb_critiques",
#    "average_rating": "note_moyenne",
#    "one_star_ratings": "nb_note_1_etoile",
#    "two_star_ratings": "nb_note_2_etoile",
#    "three_star_ratings": "nb_note_3_etoile",
#    "four_star_ratings": "nb_note_4_etoile",
#    "five_star_ratings": "nb_note_5_etoile",
#    "number_of_pages": "nombre_pages",
#    "date_published": "date_publication",
#    "original_title": "titre_original"
# })

    