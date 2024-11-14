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
from clean_data import COLUMNS_TYPES_AUTHORS,convertColumnsToRightType,main


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

    # clean_data()
    

    ##################################################################
    #
    #  BOOKS FROM AUTHORS CSV FILE
    #
    ##################################################################


    # Load Clean CSVs
    authors = pd.read_csv(CHEMIN_FICHIER_CLEAN_AUTEURS)
    books = pd.read_csv(CHEMIN_FICHIER_CLEAN_LIVRES)

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



    # Linking of books with different IDs yet a similar TITLE
    rows_authors_books = authors.loc[authors['book_title'].isin(books['title'])]
    rows_books_books = books.loc[books['title'].isin(authors['book_title'])]

    common_books_titles_but_not_ID = rows_authors_books.loc[~rows_authors_books['book_id'].isin(common_books_id) & (rows_authors_books['book_title'].isin(rows_books_books['title']))]
    common_books_titles_but_not_ID = common_books_titles_but_not_ID[col_list]

    link_dataframe = pd.concat([link_dataframe,common_books_titles_but_not_ID])



    #Create and link books present in author but not in books.csv
    rows_authors_books_big = authors.loc[(~authors['book_title'].isin(books['title']) & (~authors['book_id'].isin(common_books_id)))]

    link_dataframe = pd.concat([link_dataframe,rows_authors_books_big[col_list]])

    rows_authors_books_big = rows_authors_books_big.drop(columns=['author_average_rating', 'num_reviews', 'num_ratings', 'author_gender','author_genres','author_id','author_rating_count','author_review_count','birthplace'])
    rows_authors_books_big = rows_authors_books_big.rename(columns={"book_id": "id","author_name": "author","book_average_rating": "average_rating","book_title": "title","pages": "number_of_pages","publish_date": "date_published"})

    complete_book = pd.concat([books,rows_authors_books_big])
    complete_book = complete_book.drop(columns=['author'])
    complete_book = complete_book.drop_duplicates()

    ##################################################################
    #
    #  AUTHORS FROM BOOKS CSV FILE
    #
    ##################################################################

    # TODO: Update csv import
    # Charger les fichiers CSV
    link_path = "link.csv"

    authors = pd.read_csv(CHEMIN_FICHIER_CLEAN_AUTEURS)  # Charger le fichier existant
    books = pd.read_csv(CHEMIN_FICHIER_CLEAN_LIVRES)  # Charger le fichier existant

    # Split the authors' names into a list of names and separate genres
    books['author'] = books['author'].str.split(',')
    books = books.explode('author', ignore_index=True)
    books['author'] = books['author'].str.lstrip()

    # Get a list of books in the authors ("book_title" column)
    authors_in_authors = authors["author_name"].unique()

    # Check for all ids in books_in_authors that are also in books["id"]
    authors_in_books = books["author"].unique()

    # List all the authors to be implemented in the auteur.csv
    common_author_name = np.intersect1d(authors_in_authors, authors_in_books)
    rows_books_author_big = books.loc[~books['author'].isin(authors['author_name'])]
    max_author_id = authors["author_id"].max() if not authors.empty else 0
    author_a_implemente = rows_books_author_big['author'].drop_duplicates().to_frame()
    author_a_implemente.index = author_a_implemente.index + max_author_id
    author_a_implemente = author_a_implemente.reset_index()

    # Merge Complete_author with the new datagrame and create the links
    rows_books_author_big = pd.merge(rows_books_author_big, author_a_implemente, on='author', how='inner')
    rows_books_author_big = rows_books_author_big.rename(columns={"index": "author_id","id": "book_id"})

    col_list = ['book_id', 'author_id']
    link_dataframe = pd.concat([link_dataframe,rows_books_author_big[col_list]])

    author_a_implemente = author_a_implemente.rename(columns={"index": "author_id","author": "author_name"})
    author_a_implemente = author_a_implemente.reset_index(drop=True)

    # Mettre à jour Complete_author
    complete_author = pd.concat([authors, author_a_implemente])

    complete_author['author_genres'] = complete_author['author_genres'].str.split(',')
    complete_author = complete_author.explode('author_genres', ignore_index=True)
    
    #Supprimer les colonnes non souhaitées de Complete_author
    complete_author = complete_author.drop(columns=["book_average_rating", "book_id", "book_title", "genre_1", "genre_2", "num_ratings", "num_reviews", "pages", "publish_date"])
    complete_author = complete_author.loc[complete_author["author_genres"] != "" ]
    complete_author = complete_author.drop_duplicates()
    complete_author = convertColumnsToRightType(complete_author,COLUMNS_TYPES_AUTHORS)



    ##################################################################
    #
    #  UNPACKING OF THE DATA
    #
    ##################################################################


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
    complete_book['settingsClean'] = complete_book['settings'].str.findall(patternSetting)
    # Duplique les lignes pour n'avoir qu'un setting par ligne
    complete_book = complete_book.explode('settingsClean', ignore_index=True)

    # Crée une colonne contenant le nom du pays du setting
    complete_book['settingCountry'] = complete_book['settingsClean'].str.findall(patternPays).apply(extractWP)

    # Crée une colonne contenant la date du setting
    complete_book['settingDate'] = complete_book['settingsClean'].str.findall(patternChiffre).apply(extract)

    # Crée une colonne contenant le lieu du setting
    complete_book['settingLoc'] = complete_book['settingsClean'].str.findall(patternName).apply(extract)

    # Crée une liste contenant les différents awards séparés
    complete_book['awardsClean'] = complete_book['awards'].str.split(', ')

    # Duplique les lignes pour n'avoir qu'un award par ligne
    complete_book = complete_book.explode('awardsClean', ignore_index=True)

    # Crée une colonne contenant la date d'obtention de l'award
    complete_book['awardDate'] = complete_book['awardsClean'].str.findall(patternDate).apply(extractWP)

    # Crée une colonne contenant le nom de l'award
    complete_book['awardName'] = complete_book['awardsClean'].str.findall(patternName).apply(extract)

    # Crée une colonne contenant le nombre de l'épisode d'une série de livres
    complete_book['episodeNumber'] = complete_book['series'].str.findall(patternEpNum).apply(extract)

    # Crée une colonne contenant le nom de la série
    complete_book['seriesName'] = complete_book['series'].str.replace('(','').str.findall(patternName).apply(extract)

    # Crée une colonne contenant la date de publication du livre au bon format (Date SQL)
    complete_book['date_published'] = complete_book['date_published'].apply(reformatDate)

    # Supprime les colonnes non utilisées
    complete_book = complete_book.drop(columns = ['settings'])
    complete_book = complete_book.drop(columns = ['awards'])
    complete_book = complete_book.drop(columns = ['settingsClean'])
    complete_book = complete_book.drop(columns = ['awardsClean'])
    complete_book = complete_book.drop(columns = ['series'])

    # complete_author
    # complete_book
    # link_dataframe

    ##################################################################
    #
    #  CREATION OF TABLE CSV FILE
    #
    ##################################################################


    # Storage of the cleaned csv contents
    authors = complete_author

    genre = authors['author_genres'].unique()

    author_without_genre = authors.drop(columns=['author_genres'])

    author_without_genre = author_without_genre.drop_duplicates()

    author_without_genre = author_without_genre.drop_duplicates(subset=["author_id"], keep='first')


    # Création dataframe pour la table genre
    genre_from_author = pd.DataFrame({'author_genres': genre})

    genre_from_author.index = genre_from_author.index+1

    genre_from_author = genre_from_author.reset_index(names=['id_genre'])

    #Création lien auteur-genre
    auteur_genre = pd.merge(authors, genre_from_author, on='author_genres', how='inner')

    auteur_genre = auteur_genre.drop(columns=['author_average_rating','author_gender','author_genres','author_name','author_rating_count','author_review_count','birthplace'])

    auteur_genre = auteur_genre.drop_duplicates()

    #Format CSV
    auteur_genre = auteur_genre.rename(columns={"author_id": "id_auteur"})
    auteur_genre.to_csv("./SQL/auteur_genre.csv", index=False)

    # LAISSER EN COMMENTAIRE, VUE PLUS TARD DANS PROGRAMME MAXIME
    # genre_from_author = genre_from_author.rename(columns={"author_genres": "libelle_genre"})
    # genre_from_author.to_csv("./SQL/genre.csv", index=False)

    author_without_genre = author_without_genre.rename(columns={"author_average_rating": "note_moyenne", "author_id": "id_auteur", "author_name": "nom" ,"birthplace": "origine", "author_review_count": "nb_reviews", "author_rating_count" : "nb_critiques", "author_gender" : "sexe"})
    author_without_genre.to_csv("./SQL/auteur_sql.csv", index=False)






    # TODO: Update csv import
    books = complete_book

    countries = books['settingCountry'].unique()

    countries = countries[~pd.isnull(countries)]

    # Création d'un dataframe pour la table pays
    dataset = pd.DataFrame({'nom': countries})

    dataset.index = dataset.index+1

    dataset = dataset.reset_index(names=['id_pays'])
    dataset.to_csv("./SQL/pays.csv", index=False)

    #Création d'un dataframe pour la table setting
    settingData = pd.merge(books, dataset, left_on='settingCountry', right_on="nom", how='inner')
    settingData = settingData[['id','settingDate','settingLoc','id_pays']]
    settingData = settingData.drop_duplicates()
    settingData = settingData.rename(columns={"settingDate": "annee"})
    settingData = settingData.rename(columns={"settingLoc": "localisation"})
    settingData = settingData.rename(columns={"id": "id_livre"})

    settingData.index = settingData.index+1
    settingData = settingData.reset_index(names=['id_cadre'])

    # Création d'un dataframe pour le lien entre les livres et leur setting
    settingLinkData = settingData[['id_cadre','id_livre']]
    settingLinkData = settingLinkData.drop_duplicates()
    settingLinkData.to_csv("./SQL/cadre_livre.csv", index=False)

    settingData = settingData.drop(columns=['id_livre'])
    settingData.to_csv("./SQL/cadre.csv", index=False)

    #Création d'un dataframe pour la table editeur
    publishers = books['publisher'].unique()
    publishers = publishers[~pd.isnull(publishers)]
    dataset = pd.DataFrame({'nom_editeur': publishers})
    dataset.index = dataset.index+1
    dataset = dataset.reset_index(names=['id_editeur'])
    dataset.to_csv("./SQL/editeur.csv", index=False)


    #Création d'un dataframe pour la table livres
    publisherLinkData = pd.merge(books, dataset, left_on='publisher', right_on="nom_editeur", how='inner')
    booksData = publisherLinkData[['id','title','rating_count','review_count','average_rating','five_star_ratings','four_star_ratings','three_star_ratings','two_star_ratings','one_star_ratings','number_of_pages','date_published','original_title','isbn','isbn13','description','id_editeur']]
    booksData = booksData.drop_duplicates()
    booksData = booksData.drop_duplicates(subset=['id'],keep='first')

    booksData = booksData.rename(columns={"id": "id_livre"})
    booksData = booksData.rename(columns={"title": "titre"})
    booksData = booksData.rename(columns={"rating_count": "nb_notes"})
    booksData = booksData.rename(columns={"review_count": "nb_critiques"})
    booksData = booksData.rename(columns={"average_rating": "note_moyenne"})
    booksData = booksData.rename(columns={"one_star_ratings": "nb_notes_1_etoile"})
    booksData = booksData.rename(columns={"two_star_ratings": "nb_notes_2_etoile"})
    booksData = booksData.rename(columns={"three_star_ratings": "nb_notes_3_etoile"})
    booksData = booksData.rename(columns={"four_star_ratings": "nb_notes_4_etoile"})
    booksData = booksData.rename(columns={"five_star_ratings": "nb_notes_5_etoile"})
    booksData = booksData.rename(columns={"number_of_pages": "nombre_pages"})
    booksData = booksData.rename(columns={"date_published": "date_publication"})
    booksData = booksData.rename(columns={"original_title": "titre_original"})

    booksData.to_csv("./SQL/livre.csv", index=False)

    # 1. Import the csv files
    df_authors = complete_author
    df_books = complete_book
    df_genre_from_authors = genre_from_author # get the genre table extracted from authors

    # 2. Clean the books dataframe:
    # reshape the data
    df_clean_books = df_books[['id','genre_and_votes']] # keep only id & genre_and_votes
    df_clean_books['genre_and_votes'] = df_clean_books['genre_and_votes'].str.split(',') # turn the str into a list of genre/vote
    df_clean_books = df_clean_books.explode('genre_and_votes', ignore_index=True) # for each genre/vote group for a book, add a line. The result is that many lines have the same book id.
    df_clean_books = df_clean_books.dropna() # drop nan values
    # split genre_and_votes
    #TODO: HANDLE ERROR STR SPLIT ON SPACE WHERE GENRE HAS MULTIPLE WORD LIKE: YOUNG ADULT 161
    df_clean_books[['genre', 'votes']] = df_clean_books['genre_and_votes'].str.rsplit(' ', 1, expand=True) # split the genre and vote into two separate genre and votes columns
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

    df_clean_books.to_csv('SQL/livre_genre.csv',index=False)
    df_genre_glob2.to_csv('SQL/genre.csv',index=False)

    


if __name__ == "__main__":
    main()
