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


#######################################
#              CONSTANTS              #
#######################################

AUTHORS_CSV = "data/Cleaned_authors.csv"
BOOKS_CSV = "data/Cleaned_books.csv"
GENRES_FROM_AUTHORS_CSV = "SQL/genre.csv"

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

    df_authors = pd.read_csv(AUTHORS_CSV)
    df_books = pd.read_csv(BOOKS_CSV)

    df_clean_books = df_books[['id','genre_and_votes']] 

    # turn the str into a list of genre/vote
    df_clean_books['genre_and_votes'] = df_clean_books['genre_and_votes'].str.split(',')

    # for each genre/vote group for a book, add a line. The result is that many lines have the same book id.
    df_clean_books = df_clean_books.explode('genre_and_votes', ignore_index=True)

    # drop nan values
    df_clean_books.dropna(inplace=True)

    print(df_clean_books)

    # extract vote from genre_and_votes column 
    # e.g.: 
    #              id              genre_and_votes
    # 0        630104              Young Adult 161
    # 1        630104                   Mystery 45
    # 2        630104                   Romance 32
    # 
    # returns
    # 
    #              id              genre            votes
    # 0        630104              Young Adult      161
    # 1        630104                   Mystery     45
    # 2        630104                   Romance     32
    # 


    # split the genre and vote into genre and votes columns
    df_clean_books[['genre', 'votes']] = df_clean_books['genre_and_votes'].str.rsplit(' ', 1, expand=True)

    # drop the genre_and_votes column
    df_clean_books.drop('genre_and_votes', axis=1, inplace=True)

    #print(f"\n-*- CLEAN BOOKS DF -*-\n{df_clean_books}")

    # print all the lines where vote is nan or null
    #print(f"\n-*- ALL NULL LINES -*-\n{df_clean_books[df_clean_books['votes'].isnull()]}")

    # print all the lines where vote is not numeric
    #print(f"\n-*- NON-NUMERIC VOTES -*-\n{df_clean_books[~df_clean_books['votes'].str.isdigit()].to_string()}")

    # clean up the invalid data:

    # if votes value is '1user', change it to 1
    df_clean_books['votes'] = df_clean_books['votes'].replace('1user', '1')

    # for all values equal to '0' or any other negative value in a string, remove the row
    # convert to int and remove negative values
    df_clean_books = df_clean_books[df_clean_books['votes'].str.isdigit()]
    df_clean_books = df_clean_books[df_clean_books['votes'] >= '0']

    #print(f"\n-*- CLEAN BOOKS DF -*-\n{df_clean_books}")


    # print all the lines where vote is not numeric after cleaning up the invalid data
    #print(f"\n-*- NON-NUMERIC VOTES AFTER CLEANING -*-\n{df_clean_books[~df_clean_books['votes'].str.isdigit()].to_string()}")


    df_clean_books['votes'] = df_clean_books['votes'].astype(int)
    df_clean_books['genre'] = df_clean_books['genre'].str.lower()

    print(f"\n-*- CLEAN BOOKS DF -*-\n{df_clean_books}")

    df_genre = df_clean_books[['genre']].drop_duplicates().sort_values('genre').reset_index(drop=True)
    # make an id_genre column from the index + 1
    df_genre['id_genre'] = df_genre.index + 1
    
    # rename 'genre' to 'libelle_genre'
    df_genre.rename(columns={'genre': 'libelle_genre'}, inplace=True)

    # make id_genre the first column
    df_genre = df_genre[['id_genre', 'libelle_genre']]


    # get the genre table extracted from authors
    df_genre_from_authors = pd.read_csv(GENRES_FROM_AUTHORS_CSV)

    print(df_genre.head())
    print(df_genre.shape)
    print(df_genre_from_authors.head())
    print(df_genre_from_authors.shape)

    # TOTAL 1762 genres

    # try merging the two
    INTERSECTION = pd.merge(df_genre,df_genre_from_authors, how='inner', on=['user_id'])
    print(INTERSECTION.shape)
    print(INTERSECTION.shape())
    df_genre = pd.concat([df_genre,df_genre_from_authors]).drop_duplicates()

    print(df_genre.shape)

    # we now need a table for the relationship between books and their genres.
    # each book can have 0..* genres. This is represented by the table

    
    # print(f"\n-*- DF GENRE -*-\n{df_genre.to_string()}")


if __name__ == "__main__":
    main()