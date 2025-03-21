# -*- coding: utf-8 -*-

"""
IUT de Lannion
BUT Informatique 3
SAE 5.C.01

Wizards of the West Coast

Ewan Lansonneur 3C2
Maxime Perrot 3C2

Created on 2024-10-09

This program will run the transform and load parts 
"""


#######################################
#               IMPORTS               #
#######################################

import re
import os
import pandas as pd
import numpy as np

import clean_data
import scripts.etl_scripts.csv_formulaire_table_creation as csv_formulaire_table_creation
import scripts.etl_scripts.csv_table_creation as csv_table_creation
import scripts.etl_scripts.extract_authors_from_books as extract_authors_from_books
import scripts.etl_scripts.extract_books_from_authors as extract_books_from_authors
import scripts.etl_scripts.nettoyage_pour_insertion as nettoyage_pour_insertion
import scripts.etl_scripts.generate_table_genre as generate_table_genre

#######################################
#              CONSTANTS              #
#######################################

CHEMIN_FICHIER_LIVRES = "data/bigboss_book.csv" # previously was books.csv, adapted to the default name bigboss_book.csv
CHEMIN_FICHIER_AUTEURS = "data/Big_boss_authors.csv" # previously was authors.csv, adapted to the default name Big_boss_authors.csv

CHEMIN_FICHIER_CLEAN_LIVRES = "data/Cleaned_books.csv"
CHEMIN_FICHIER_CLEAN_AUTEURS = "data/Cleaned_authors.csv"

CHEMIN_FICHIER_LIVRES_COMPLET = "data/complete_book.csv"
CHEMIN_FICHIER_AUTEURS_COMPLET = "data/complete_author.csv"

CHEMIN_LIEN_AUTEURS_LIVRES = "data/populate/link.csv"

CHEMIN_FICHIER_FORMULAIRE = "data/formulaire.csv"
CHEMIN_DATA = "data/"
CHEMIN_POPULATE = os.path.join(CHEMIN_DATA, "populate")


#######################################
#              FUNCTIONS              #
#######################################

def main():
    newpath = r'data/populate' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    os.makedirs(CHEMIN_POPULATE, exist_ok=True)

    # EXTRACT & TRANSFORM
    clean_data.main(
        chemin_fichier_livres = CHEMIN_FICHIER_LIVRES,
        chemin_fichier_auteurs = CHEMIN_FICHIER_AUTEURS,
        nouveau_chemin_livres = CHEMIN_FICHIER_CLEAN_LIVRES,
        nouveau_chemin_auteurs = CHEMIN_FICHIER_CLEAN_AUTEURS
    )


    
    extract_books_from_authors.main(
        chemin_fichier_livres_complet = CHEMIN_FICHIER_LIVRES_COMPLET
    )

    extract_authors_from_books.main(

    )

    nettoyage_pour_insertion.main(
        chemin_fichier_clean_livres = CHEMIN_FICHIER_LIVRES_COMPLET,
        chemin_fichier_livres_complet = CHEMIN_FICHIER_LIVRES_COMPLET 
    )


    csv_table_creation.main(
        books = pd.read_csv(CHEMIN_FICHIER_LIVRES_COMPLET,low_memory=False),
        authors = pd.read_csv(CHEMIN_FICHIER_AUTEURS_COMPLET,low_memory=False)
    )

    generate_table_genre.main()

    csv_formulaire_table_creation.main(
        results = pd.read_csv(CHEMIN_FICHIER_FORMULAIRE,low_memory=False)
    )

    


    

if __name__ == "__main__":
    main()
