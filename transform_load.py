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


#######################################
#              CONSTANTS              #
#######################################

CHEMIN_FICHIER_LIVRES = "data/books.csv"
CHEMIN_FICHIER_AUTEURS = "data/authors.csv"

CHEMIN_FICHIER_CLEAN_LIVRES = "data/Cleaned_books.csv"
CHEMIN_FICHIER_CLEAN_AUTEURS = "data/Cleaned_authors.csv"

CHEMIN_FICHIER_LIVRES_COMPLET = "data/Complete_book.csv"
CHEMIN_FICHIER_AUTEURS_COMPLET = "data/Complete_author.csv"

CHEMIN_LIEN_AUTEURS_LIVRES = "SQL/link.csv"


#######################################
#              FUNCTIONS              #
#######################################

def main():

    # EXTRACT & TRANSFORM
    clean_data.main(
        chemin_fichier_livres = CHEMIN_FICHIER_LIVRES
        chemin_fichier_auteurs = CHEMIN_FICHIER_AUTEURS,
        nouveau_chemin_livres = CHEMIN_FICHIER_CLEAN_LIVRES,
        nouveau_chemin_auteurs = CHEMIN_FICHIER_CLEAN_AUTEURS
    )

    # TODO la suite, verifier nouveau_chemin fonctionne


    

if __name__ == "__main__":
    main()
