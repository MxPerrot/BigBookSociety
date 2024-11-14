# -*- coding: utf-8 -*-

"""
IUT de Lannion
BUT Informatique 3
SAE 5.C.01

Wizards of the West Coast

Ewan Lansonneur 3C2
Maxime Perrot 3C2

Created on 2024-10-09
"""


#######################################
#               IMPORTS               #
#######################################

import re
import os
import pandas as pd
import numpy as np
from clean_data import COLUMNS_TYPES_AUTHORS,convertColumnsToRightType


#######################################
#              CONSTANTS              #
#######################################

CHEMIN_FICHIER_LIVRES = "Big_book.csv"


#######################################
#              FUNCTIONS              #
#######################################

# extrait le résultat d'une recherche findall
def extract(x):
    if isinstance(x, list) and len(x) >= 1:
        return x[0]
    else :
        return None

# extrait le résultat d'une recherche findall pour le pays (retire les parenthèses)
def extractWP(x):
    if isinstance(x, list) and len(x) >= 1:
        return x[0].replace('(','').replace(')','')
    else :
        return None

# transforme une date au format "April 15th 1988" en "1988-04-15" pour correspondre au format date de SQL
def reformatDate(dateString):

    # Au nom d'un mois associe son numéro
    month_dict = {
        "January": '01',
        "February": '02',
        "March": '03',
        "April": '04',
        "May": '05',
        "June": '06',
        "July": '07',
        "August": '08',
        "September": '09',
        "October": '10',
        "November": '11',
        "December": '12'
    }

    # Prend en compte le cas null
    if pd.isnull(dateString):
        return None

    # Récupère l'année et la formate
    year = re.findall(r'\d{4}$', dateString)
    if len(year) == 0:
        return None
    else:
        year = year[0]

    # Récupère le mois et le formate
    month = re.findall(r'^[a-zA-Z]+', dateString)
    if len(month) == 0:
        month = '01'
    else:
        month = month_dict[month[0]]

    # Récupère le jour et le formate
    day = re.findall(r'\d{1,2}(?:(?:st)|(?:nd)|(?:rd)|(?:th))', dateString)
    if len(day) == 0:
        day = '01'
    else:
        day = day[0].replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
        if len(day) < 2:
            day = '0'+day

    return year+'-'+month+'-'+day

#######################################
#                 MAIN                #
#######################################

def main():
    """
    Main function
    """
    

    ##################################################################
    #
    #  BOOKS FROM AUTHORS CSV FILE
    #
    ##################################################################


    # Load authors.csv
    authors = pd.read_csv("data/Cleaned_authors.csv")

    # Load books.csv
    books = pd.read_csv("data/Cleaned_books.csv")

    # Get a list of books in the authors ("book_title" column)
    books_in_authors = authors["book_id"].unique()

    # Check for all ids in books_in_authors that are also in books["id"]
    books_in_books = books["id"].unique()

    # Get the common ids between books_in_authors and books_in_books

    common_books_id = np.intersect1d(books_in_authors, books_in_books)
    
    rows_authors_books = authors.loc[authors['book_id'].isin(common_books_id)]

    col_list = ['book_id', 'author_id']

    link_dataframe = rows_authors_books[col_list]

    link_dataframe = link_dataframe.drop_duplicates(subset = ['book_id','author_id'], keep=False)

    ###### Analysis of books with different IDs yet a similar TITLE
    rows_authors_books = authors.loc[authors['book_title'].isin(books['title'])]
    rows_books_books = books.loc[books['title'].isin(authors['book_title'])]

    common_books_titles_but_not_ID = rows_authors_books.loc[~rows_authors_books['book_id'].isin(common_books_id) & (rows_authors_books['book_title'].isin(rows_books_books['title']))]

    common_books_titles_but_not_ID = common_books_titles_but_not_ID[col_list]

    link_dataframe = pd.concat([link_dataframe,common_books_titles_but_not_ID])

    rows_authors_books_big = authors.loc[(~authors['book_title'].isin(books['title']) & (~authors['book_id'].isin(common_books_id)))]

    link_dataframe = pd.concat([link_dataframe,rows_authors_books_big[col_list]])

    rows_authors_books_big = rows_authors_books_big.drop(columns=['author_average_rating', 'num_reviews', 'num_ratings', 'author_gender','author_genres','author_id','author_rating_count','author_review_count','birthplace'])

    rows_authors_books_big = rows_authors_books_big.rename(columns={"book_id": "id","author_name": "author","book_average_rating": "average_rating","book_title": "title","pages": "number_of_pages","publish_date": "date_published"})

    bigBook = pd.concat([books,rows_authors_books_big])

    bigBook = bigBook.drop(columns=['author'])

    bigBook = bigBook.drop_duplicates()

    bigBook.to_csv("Big_book.csv", index=False)
    link_dataframe.to_csv("link.csv", index=False)


    ##################################################################
    #
    #  AUTHORS FROM BOOKS CSV FILE
    #
    ##################################################################


    # Charger les fichiers CSV
    authors_path = "BigAuthor.csv"
    clean_authors_path = "data/Cleaned_authors.csv"
    books_path = "data/Cleaned_books.csv"
    link_path = "link.csv"

    authors = pd.read_csv(clean_authors_path)  # Charger le fichier existant
    books = pd.read_csv(books_path)  # Charger le fichier existant

    books['author'] = books['author'].str.split(',')
    books = books.explode('author', ignore_index=True)
    books['author'] = books['author'].str.lstrip()

    # Get a list of books in the authors ("book_title" column)
    authors_in_authors = authors["author_name"].unique()

    # Check for all ids in books_in_authors that are also in books["id"]
    authors_in_books = books["author"].unique()

    common_author_name = np.intersect1d(authors_in_authors, authors_in_books)

    rows_books_author_big = books.loc[~books['author'].isin(authors['author_name'])]

    max_author_id = authors["author_id"].max() if not authors.empty else 0

    author_a_implemente = rows_books_author_big['author'].drop_duplicates().to_frame()

    author_a_implemente.index = author_a_implemente.index + max_author_id

    author_a_implemente = author_a_implemente.reset_index()

    rows_books_author_big = pd.merge(rows_books_author_big, author_a_implemente, on='author', how='inner')

    rows_books_author_big = rows_books_author_big.rename(columns={"index": "author_id","id": "book_id"})
    link_dataframe = pd.read_csv(link_path)

    col_list = ['book_id', 'author_id']

    link_dataframe = pd.concat([link_dataframe,rows_books_author_big[col_list]])

    author_a_implemente = author_a_implemente.rename(columns={"index": "author_id","author": "author_name"})

    author_a_implemente = author_a_implemente.reset_index(drop=True)

    # Mettre à jour BigAuthor
    bigAuthor = pd.concat([authors, author_a_implemente])

    bigAuthor['author_genres'] = bigAuthor['author_genres'].str.split(',')
    bigAuthor = bigAuthor.explode('author_genres', ignore_index=True)
    
    #Supprimer les colonnes non souhaitées de BigAuthor
    bigAuthor = bigAuthor.drop(columns=["book_average_rating", "book_id", "book_title", "genre_1", "genre_2", "num_ratings", "num_reviews", "pages", "publish_date"])
    
    bigAuthor = bigAuthor.loc[bigAuthor["author_genres"] != "" ]

    bigAuthor = bigAuthor.drop_duplicates()

    bigAuthor = convertColumnsToRightType(bigAuthor,COLUMNS_TYPES_AUTHORS)

    bigAuthor.to_csv(authors_path, index=False)
    link_dataframe.to_csv(link_path, index=False)

    ##################################################################
    #
    #  UNPACKING OF THE DATA
    #
    ##################################################################

    # Lit le fichier CSV avec les données brutes
    df = pd.read_csv(CHEMIN_FICHIER_LIVRES)

    # Pattern regex pour séparer les différents settings
    patternSetting = r'(?:[A-Za-z\.]+(?:, |\s)?)+(?:,\d+)?(?:\([a-zA-Z\s]+\))?'
    # Pattern regex pour extraire le nom du pays dans le setting
    patternPays = r'\([a-zA-Z\s]+\)'
    # Pattern regex pour extraire un nombre d'une chaîne de caratères 
    patternChiffre = r'\d+'
    # Pattern regex pour extraire un nom d'une chaîne
    patternName = r'^(?:[\w\.\/\-\'\:éèïôçêùæœëüâ€©¤ãűúöäà]+(?:, |\s)?)+[\w\.\/\-\'\:éèïôçêùæœëüâ€©¤ãűúöäà]+'
    # Pattern regex pour extraire une date entourée de parenthèses 
    patternDate = r'\(\d+\)'
    # Pattern regex pour extraire un numéro d'épisode 
    patternEpNum = r'#[\d.-]+'

    # Crée une liste contenant les différents settings séparés
    df['settingsClean'] = df['settings'].str.findall(patternSetting)
    # Duplique les lignes pour n'avoir qu'un setting par ligne
    df = df.explode('settingsClean', ignore_index=True)

    # Crée une colonne contenant le nom du pays du setting
    df['settingCountry'] = df['settingsClean'].str.findall(patternPays).apply(extractWP)

    # Crée une colonne contenant la date du setting
    df['settingDate'] = df['settingsClean'].str.findall(patternChiffre).apply(extract)

    # Crée une colonne contenant le lieu du setting
    df['settingLoc'] = df['settingsClean'].str.findall(patternName).apply(extract)

    # Crée une liste contenant les différents awards séparés
    df['awardsClean'] = df['awards'].str.split(', ')

    # Duplique les lignes pour n'avoir qu'un award par ligne
    df = df.explode('awardsClean', ignore_index=True)

    # Crée une colonne contenant la date d'obtention de l'award
    df['awardDate'] = df['awardsClean'].str.findall(patternDate).apply(extractWP)

    # Crée une colonne contenant le nom de l'award
    df['awardName'] = df['awardsClean'].str.findall(patternName).apply(extract)

    # Crée une colonne contenant le nombre de l'épisode d'une série de livres
    df['episodeNumber'] = df['series'].str.findall(patternEpNum).apply(extract)

    # Crée une colonne contenant le nom de la série
    df['seriesName'] = df['series'].str.replace('(','').str.findall(patternName).apply(extract)

    # Crée une colonne contenant la date de publication du livre au bon format (Date SQL)
    df['date_published'] = df['date_published'].apply(reformatDate)

    # Supprime les colonnes non utilisées
    df = df.drop(columns = ['settings'])
    df = df.drop(columns = ['awards'])
    df = df.drop(columns = ['settingsClean'])
    df = df.drop(columns = ['awardsClean'])
    df = df.drop(columns = ['series'])

    df.to_csv('./data/Cleaned_books2.csv', index=False)

    ##################################################################
    #
    #  CREATION OF TABLE CSV FILE
    #
    ##################################################################


    # Storage of the cleaned csv contents
    authors = pd.read_csv("BigAuthor.csv")

    genre = authors['author_genres'].unique()

    author_without_genre = authors.drop(columns=['author_genres'])

    author_without_genre = author_without_genre.drop_duplicates()

    author_without_genre = author_without_genre.drop_duplicates(subset=["author_id"], keep='first')


    # Création dataframe pour la table genre
    dataset = pd.DataFrame({'author_genres': genre})

    dataset.index = dataset.index+1

    dataset = dataset.reset_index(names=['id_genre'])

    #Création lien auteur-genre
    auteur_genre = pd.merge(authors, dataset, on='author_genres', how='inner')

    auteur_genre = auteur_genre.drop(columns=['author_average_rating','author_gender','author_genres','author_name','author_rating_count','author_review_count','birthplace'])

    auteur_genre = auteur_genre.drop_duplicates()

    #Format CSV
    auteur_genre = auteur_genre.rename(columns={"author_id": "id_auteur"})
    auteur_genre.to_csv("./SQL/auteur_genre.csv", index=False)

    dataset = dataset.rename(columns={"author_genres": "libelle_genre"})
    dataset.to_csv("./SQL/genre.csv", index=False)

    author_without_genre = author_without_genre.rename(columns={"author_average_rating": "note_moyenne", "author_id": "id_auteur", "author_name": "nom" ,"birthplace": "origine", "author_review_count": "nb_reviews", "author_rating_count" : "nb_critiques", "author_gender" : "sexe"})
    author_without_genre.to_csv("./SQL/auteur_sql.csv", index=False)

    

if __name__ == "__main__":
    main()
