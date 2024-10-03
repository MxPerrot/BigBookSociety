# -*- coding:utf-8 -*-

"""
This module cleans the DataFrame generated from books.csv
"""

#######################################
#               IMPORTS               #
#######################################

import numpy as np
import pandas as pd
from io import StringIO
import re

#######################################
#              CONSTANTS              #
#######################################

COLUMNS_TYPES_BOOKS = {
    "id":int,
    "title":str,
    "series":str,
    "author":str,
    "rating_count":int,
    "review_count":int,
    "average_rating":float,
    "five_star_ratings":int,
    "four_star_ratings":int,
    "three_star_ratings":int,
    "two_star_ratings":int,
    "one_star_ratings":int,
    "number_of_pages":int,
    "date_published":str,
    "publisher":str,
    "original_title":str,
    "genre_and_votes":str,
    "isbn":str,
    "isbn13":int,
    "settings":str,
    "characters":str,
    "awards":str,
    "books_in_series":str,
    "description":str,
}

BOOKS_CSV = "data/books.csv"

COLUMNS_TYPES_AUTHORS = {
    "author_average_rating":float,
    "author_gender":str,
    "author_genres":str,
    "author_id":int,
    "author_name":str,
    "author_rating_count":int,
    "author_review_count":int,
    "birthplace":str,
    "book_average_rating":float,
    "book_id":int,
    "book_title":str,
    "genre_1":str,
    "genre_2":str,
    "num_ratings":int,
    "num_reviews":int,
    "pages":int,
    "publish_date":str
}

AUTHORS_CSV = "data/authors.csv"

UTF8_CORRESPONDANCY = {
        'Ã©': 'é',
        'Ã¨': 'è',
        'Ã¯': 'ï',
        'Ã´': 'ô',
        'Ã§': 'ç',
        'Ãª': 'ê',
        'Ã¹' : 'ù',
        'Ã¦' : 'æ',
        'Å'  : 'œ',
        'Ã«' : 'ë',
        'Ã¼' : 'ü',
        'Ã¢' : 'â',
        'â¬' : '€',
        'Â©' : '©',
        'Â¤' : '¤',
        'Ã£' : 'ã',
        'Å±' : 'ű',
        'Ãº' : 'ú',
        'Ã¶' : 'ö',
        'Ã'  : 'à'
    }

#######################################
#              FUNCTIONS              #
#######################################

def UTF8Cleaner(fileName):
    """
    Remplace les caratères mal encodés d'un fichier CSV et les renvoie sous forme de dataframe
    """
    correspondanceUTF8 = {
        'Ã©': 'é',
        'Ã¨': 'è',
        'Ã¯': 'ï',
        'Ã´': 'ô',
        'Ã§': 'ç',
        'Ãª': 'ê',
        'Ã¹' : 'ù',
        'Ã¦' : 'æ',
        'Å'  : 'œ',
        'Ã«' : 'ë',
        'Ã¼' : 'ü',
        'Ã¢' : 'â',
        'â¬' : '€',
        'Â©' : '©',
        'Â¤' : '¤',
        'Ã£' : 'ã',
        'Å±' : 'ű',
        'Ãº' : 'ú',
        'Ã¶' : 'ö',
        'Ã'  : 'à'
    }

    # Ouvre le document et le met dans une chaine
    with open(fileName, 'r') as file:
        document = file.read()

        # Remplace les caractères mal encodés par le caractère original
        for key,value in correspondanceUTF8.items() :
            #print(key + " -> " + value)
            document = document.replace(key, value)

    # Convertit la chaîne de caractères en dataframe
    csvStringIO = StringIO(document)
    data = pd.read_csv(csvStringIO, sep=',')
    df = pd.DataFrame(data)
    return df

def columnDeleter(data):
    """
    Supprime les colonnes vides et les lignes possédant des valeurs dedant
    """
    str_column="Unnamed: "
    print(f"\n--- Purge ligne vide     ---\n")
    for i in range(24,87):
        index = 0
        for y in data[str_column+str(i)]:
            if (pd.notna(y)):
                data = data.drop([index])
            index += 1
    print(f"\n--- Purge ligne vide OK ---\n")
    print(f"\n--- Purge colonnes unnamed    ---\n")
    for i in range(24,87):
        data = data.drop(columns=[str_column+str(i)])
    print(f"\n--- Purge colonnes unnamed OK ---\n")
    return data

def converterStrFloat(data,id):
    """"
    Convertie les virgules en point puis les string en float
    """
    print(f"\n--- Nettoyage {id}    ---\n")
    data[id] = data[id].replace({',': '.'}, regex=True)
    data[id] = pd.to_numeric(data[id],downcast='float')
    print(f"\n--- Nettoyage {id} OK ---\n")
    return data

def columnTypeFormater(data,Format):
    """
    Adapte toute les colonnes aux formats demandés et supprime les lignes problématiques
    """
    print(f"\n--- Nettoyage Global---\n")
    for i in data:
        print(f"\n--- Nettoyage {i} ---\n")
        try:
            if(Format[i]!=str):
                data[i] = data[i].fillna(-1).astype(Format[i])
            data[i] = pd.to_numeric(data[i], Format[i])
        except :
            for index, cell in data[i].items():
                if pd.isna(cell):

                    pass

                elif type(cell) == Format[i]:
                    pass 

                elif ((Format[i] == float or Format[i] == int) and (type(cell) == int or type(cell) == float or cell.isnumeric())):
                    if(Format[i]==float):
                        data.loc[index, i] = float(cell) 
                    if(Format[i]==int):
                        data.loc[index, i] = int(cell) 

                else:
                    data = data.drop(index)    
        print(f"\n--- Nettoyage {i} OK ---\n")
    print(f"\n--- Nettoyage Global OK ---\n")
    return data


# Fonction pour extraire l'année, gérer les cas où la date est au format BC, et gérer les valeurs manquantes
def extract_year_no_nan(date_str):
    if isinstance(date_str, str):
        date_str = date_str.strip()
        
        # Vérifier les dates avant notre ère (BC) et retourner l'année négative
        if 'BC' in date_str:
            year_match = re.search(r'(\d+)', date_str)
            if year_match:
                return -int(year_match.group(1))
        
        # Extraire l'année des formats de date habituels
        year_match = re.search(r'(\d{4})', date_str)
        if year_match:
            return int(year_match.group(1))
        
        return 0

def dateCleaner(data):
# Appliquer la fonction à la colonne 'date_published' et stocker le résultat dans une colonne temporaire
    data['date_published_formated'] = data['date_published'].apply(extract_year_no_nan)

    # Replacer la colonne 'date_published' par la nouvelle colonne formattée
    data['date_published'] = data['date_published_formated']

    # Supprimer colonne temporaire
    data = data.drop(columns=['date_published_formated'])

    return data

def addDescriptionLength(df):
    df['description_length'] = df["description"].str.count(' ')+1
    return df

def addTitleLength(df):
    df['title_length'] = df["title"].str.len()
    return df

def addSeriesLength(df):
    df['series_length'] = df["books_in_series"].str.count(',')+1
    return df


#######################################
#                MAIN                 #
#######################################

def main():
    """
    Main function
    """
    
    books_data = UTF8Cleaner(BOOKS_CSV)
    books_data = columnDeleter(books_data)
    books_data = converterStrFloat(books_data,"average_rating")
    books_data = columnTypeFormater(books_data,COLUMNS_TYPES_BOOKS)
    books_data = dateCleaner(books_data)
    books_data = addDescriptionLength(books_data)
    books_data = addTitleLength(books_data)
    books_data = addSeriesLength(books_data)
    books_data.to_csv('./data/Cleaned_books.csv', index=False)


    authors_data = UTF8Cleaner(AUTHORS_CSV)
    authors_data = converterStrFloat(authors_data,"book_average_rating")
    authors_data = converterStrFloat(authors_data,"author_average_rating")
    authors_data = columnTypeFormater(authors_data,COLUMNS_TYPES_AUTHORS)
    authors_data.to_csv('./data/Cleaned_authors.csv', index=False)



if __name__ == "__main__":
    main()