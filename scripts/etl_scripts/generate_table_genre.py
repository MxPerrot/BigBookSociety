# -*- coding:utf-8 -*-

"""

IUT de Lannion
BUT Informatique 3
SAE 5.C.01

Wizards of the West Coast

Maxime Perrot

Created on 2024-11-12

This module aims to generate the genre-book relation table from book, author and genre
"""


#######################################
#               IMPORTS               #
#######################################

import numpy as np
import pandas as pd
import os



#######################################
#              CONSTANTS              #
#######################################

AUTHORS_CSV = "data/complete_author.csv"
BOOKS_CSV = "data/complete_book.csv"
GENRES_FROM_AUTHORS_CSV = "data/populate/genre.csv"
PATH_DATA = "data/"
PATH_POPULATE = os.path.join(PATH_DATA, "populate")

#######################################
#              FUNCTIONS              #
#######################################


#######################################
#                MAIN                 #
#######################################

def main():

    """
    Main function
    """

    # 1. Import the csv files
    df_authors = pd.read_csv(AUTHORS_CSV)
    df_books = pd.read_csv(BOOKS_CSV)
    df_genre_from_authors = pd.read_csv(GENRES_FROM_AUTHORS_CSV) # get the genre table extracted from authors

    # 2. Clean the books dataframe:
    # reshape the data
    df_clean_books = df_books[['id','genre_and_votes']] # keep only id & genre_and_votes
    df_clean_books['genre_and_votes'] = df_clean_books['genre_and_votes'].str.split(',') # turn the str into a list of genre/vote
    df_clean_books = df_clean_books.explode('genre_and_votes', ignore_index=True) # for each genre/vote group for a book, add a line. The result is that many lines have the same book id.
    df_clean_books = df_clean_books.dropna() # drop nan values
    # split genre_and_votes
    df_clean_books[['genre', 'votes']] = df_clean_books['genre_and_votes'].str.rsplit(' ', n=1, expand=True) # split the genre and vote into two separate genre and votes columns
    df_clean_books = df_clean_books.drop('genre_and_votes', axis=1) # drop the genre_and_votes column
    # clean up the invalid data
    df_clean_books['votes'] = df_clean_books['votes'].replace('1user', '1') # if votes value is '1user', change it to 1
    df_clean_books = df_clean_books[df_clean_books['votes'].str.isdigit()] # keep only numerical values
    df_clean_books = df_clean_books[df_clean_books['votes'] >= '0'] # remove negative values
    df_clean_books['votes'] = df_clean_books['votes'].astype(int) # force convert numerical values to int
    df_clean_books['genre'] = df_clean_books['genre'].str.lower() # lowercase the genres
    df_clean_books['genre'] = df_clean_books['genre'].str.strip() # remove trailing spaces
    
    # 3. Join the books dataframe with the genre table
    df_genre_from_authors_libelle_only = df_genre_from_authors['libelle_genre'] 



    
    df_genre = df_clean_books[['genre']].drop_duplicates().sort_values('genre')
    df_genre.rename(columns={'genre': 'libelle_genre'}, inplace=True)

    df_genre['libelle_genre'] = df_genre['libelle_genre'].str.strip()

    df_genre_global = pd.merge(df_genre_from_authors_libelle_only, df_genre, on='libelle_genre', how='outer')
    df_genre_global = df_genre_global.drop_duplicates()

    df_genre_global = pd.merge(df_genre_global, df_genre_from_authors, on='libelle_genre', how='outer')

    print(df_genre_global              )

    df_genre_global = df_genre_global.sort_values(by=['id_genre'])
    df_genre_global['id_genre'] = df_genre_global.index + 1

    df_clean_books.rename(columns={'genre': 'libelle_genre', 'id' : 'id_livre', 'votes' : 'nb_votes'}, inplace=True)
    df_clean_books = pd.merge(df_clean_books, df_genre_global, on='libelle_genre', how='inner')
    df_clean_books = df_clean_books.drop(columns=['libelle_genre'])
    df_clean_books = df_clean_books.drop_duplicates()

    df_clean_books_author = df_books[['id','genre_1', 'genre_2']] 
    df_clean_books_author = df_clean_books_author.dropna(subset=['genre_1'])

    df_clean_books_author = df_clean_books_author.melt(id_vars=['id'], value_vars=['genre_1','genre_2'])
    df_clean_books_author = df_clean_books_author.drop(columns=['variable'])
    df_clean_books_author.rename(columns={'value': 'libelle_genre', 'id' : 'id_livre'}, inplace=True)
    df_clean_books_author['libelle_genre'] = df_clean_books_author['libelle_genre'].str.lower()
    df_clean_books_author['libelle_genre'] = df_clean_books_author['libelle_genre'].str.strip()

    df_books_author_genre = df_clean_books_author['libelle_genre'].drop_duplicates()

    df_genre_glob2 = pd.merge(df_books_author_genre, df_genre_global, on='libelle_genre', how='outer')
    df_genre_glob2 = df_genre_glob2.reset_index(drop=True)
    df_genre_glob2['id_genre'] = df_genre_glob2.index + 1
    df_clean_books_author = pd.merge(df_genre_glob2, df_clean_books_author, on='libelle_genre', how='inner')
    df_clean_books_temp = df_clean_books_author.drop(columns=['libelle_genre'])

    df_clean_books = pd.concat([df_clean_books,df_clean_books_temp])

    df_clean_books = df_clean_books.fillna(1)
    df_clean_books['nb_votes'] = df_clean_books['nb_votes'].astype(int)

    #df_clean_books.to_csv('livre_genre.csv',index=False)
    #df_genre_glob2.to_csv('genre.csv',index=False)

    df_clean_books = df_clean_books.drop_duplicates()
    df_genre_glob2 = df_genre_glob2.drop_duplicates()

    # df_clean_books.to_csv(os.path.join(PATH_POPULATE,"livre_genre.csv"), index=False)
    # df_genre_glob2.to_csv(os.path.join(PATH_POPULATE,"genre.csv"), index=False)

if __name__ == "__main__":
    main()