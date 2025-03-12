# -*- coding: utf-8 -*-

"""
IUT de Lannion
BUT Informatique 3
SAE 5.C.01

Wizards of the West Coast

Maxime Perrot 3C2

Created on 2024-10-09
"""


#######################################
#               IMPORTS               #
#######################################

import os
import pandas as pd

import analysis_scripts.pages_by_genre              as pages_by_genre
import analysis_scripts.genre_by_rating             as genre_by_rating
import analysis_scripts.genre_by_gender             as genre_by_gender
import analysis_scripts.common_genres               as common_genres
import analysis_scripts.acp_rating_by_page_number   as acp_rating_by_page_number
import analysis_scripts.acm_genre_by_era            as acm_genre_by_era


#######################################
#                 MAIN                #
#######################################

def main():

    print("""
┌───────────────────────────┐
│ IUT de Lannion            │
│ BUT Informatique 3        │
│ SAE 5.C.01                │
│                           │
│ Wizards of the West Coast │
│                           │
│ Nathan Bracquart          │
│ Damien Goupil             │
│ Ewan Lansonneur           │
│ Florian Normand           │
│ Maxime Perrot             │
├───────────────────────────┘""")

    # Importing the cleaned data

    print("├─ Importing books")
    books = pd.read_csv("data/Cleaned_books.csv")

    print("├─ Importing authors")
    authors = pd.read_csv("data/Cleaned_authors.csv")

    # Creating the graphs folder

    if not os.path.exists("graphs"):
        os.makedirs("graphs")

    # Running the analysis scripts

    print("├─ Starting analysis scripts")

    print("│ ├─ Pages by genre...", end=" ", flush=True)
    pages_by_genre.main(books)
    print("OK")

    print("│ ├─ Genre by rating...", end=" ", flush=True)
    genre_by_rating.main(books)
    print("OK")

    print("│ ├─ Genre by gender...", end=" ", flush=True)
    genre_by_gender.main(authors)
    print("OK")

    print("│ ├─ Common genres...", end=" ", flush=True)
    common_genres.main(books)
    print("OK")

    print("│ ├─ ACP rating by page number...", end=" ", flush=True)
    acp_rating_by_page_number.main(books)
    print("OK")

    print("│ ├─ ACM genre by era...", end=" ", flush=True)
    acm_genre_by_era.main(books)
    print("OK")

    print("│ OK")
    print("├─ Graphs are available in the graphs folder")
    print("""├───────────────────────────┐
│    END OF THE PROGRAM     │
└───────────────────────────┘
""")

if __name__ == "__main__":
    main()