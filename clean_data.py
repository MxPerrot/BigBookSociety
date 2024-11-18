# -*- coding:utf-8 -*-

"""

IUT de Lannion
BUT Informatique 3
SAE 5.C.01

Wizards of the West Coast

Maxime Perrot
Nathan Bracquart
Florian Normand
Damien Goupil
Ewan Lansonneur

Created on 2024-10-08

This module cleans the DataFrame generated from books.csv
"""

#######################################
#               IMPORTS               #
#######################################

import numpy as np
import pandas as pd
from io import StringIO
import re
import chardet
import unicodedata
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
        'Ã¤' : 'ä',
        'Ã'  : 'à',
        # Caractères invisibles impossibles à remplacer cachés dans la chaine si dessous
        'â'  : "'",
        'â²' : "'"
    }


#######################################
#              FUNCTIONS              #
#######################################

def normalize_text(text):
    if not isinstance(text, str):
        return text
    return unicodedata.normalize('NFKC', text)  # Or 'NFKD' for decomposed form

def encodeInUTF8(fileName):
    """
    Remplace les caratères mal encodés d'un fichier CSV et les renvoie sous forme de dataframe
    """
    
    # Ouvre le document et le met dans une chaine
    with open(fileName, 'r',encoding="utf8") as file:
        document = file.read()

        # Remplace les caractères mal encodés par le caractère original
        for key,value in UTF8_CORRESPONDANCY.items() :
            document = document.replace(key, value)

    # Convertit la chaîne de caractères en dataframe
    csvStringIO = StringIO(document)
    data = pd.read_csv(csvStringIO, sep=',')
    df = pd.DataFrame(data)

    return df

    # with open(fileName, 'rb') as f:
    #     result = chardet.detect(f.read(10000))  # Read the first 10,000 bytes
    # print(result)  # {'encoding': 'utf-8', 'confidence': 0.99}
    # encoding = result['encoding']

    # # Use the detected encoding
    # df = pd.read_csv(fileName, encoding=encoding, encoding_errors='replace')
    # return df
    # Normalize Unicode

    # df = pd.read_csv(fileName, encoding='utf-8')

    # # Apply normalization
    # for col in df.columns:
    #     df[col] = df[col].apply(normalize_text)

    # return df

def pruneEmptyColumns(data):
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

def convertStrToFloat(data,id):
    """"
    Convertie les virgules en point puis les string en float
    """
    print(f"\n--- Nettoyage {id}    ---\n")
    data[id] = data[id].replace({',': '.'}, regex=True)
    data[id] = pd.to_numeric(data[id],downcast='float')
    print(f"\n--- Nettoyage {id} OK ---\n")
    return data

def convertColumnsToRightType(data,Format):
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


def yearStrToInt(date_str):
    """
    Fonction pour extraire l'année, gérer les cas où la date
    est au format BC, et gérer les valeurs manquantes

    returns year as an int
    """
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

def formatDate(data):
    """
    Appliquer la fonction à la colonne 'date_published' et stocker le résultat dans une colonne temporaire
    """
    
    data['date_published_formated'] = data['date_published'].apply(yearStrToInt)

    return data

def removeLeadingTrailingSpaces(df,format):
    """
    for every column of the dataframe supposed to be a string,
    apply the strip function to its content
    
    df : pandas DataFrame
    format : type of column dict for the dataframe 
    """

    for column in df.columns:
        if format.get(column) == str:
            df[column] = df[column].str.strip()
    return df


#######################################
#                MAIN                 #
#######################################

def main(
        chemin_fichier_livres,
        chemin_fichier_auteurs,
        nouveau_chemin_livres,
        nouveau_chemin_auteurs
        ):

    """
    Main function
    """
    
    # Cleaning
    books_data = encodeInUTF8(chemin_fichier_livres)
    books_data = pruneEmptyColumns(books_data)
    books_data = convertStrToFloat(books_data,"average_rating")
    books_data = convertColumnsToRightType(books_data,COLUMNS_TYPES_BOOKS)
    books_data = removeLeadingTrailingSpaces(books_data,COLUMNS_TYPES_BOOKS)
    books_data = formatDate(books_data)

    # Adding rows for additional analysis
    books_data.to_csv('./data/Cleaned_books.csv', index=False)


    # Cleaning
    authors_data = encodeInUTF8(chemin_fichier_auteurs)
    authors_data = convertStrToFloat(authors_data,"book_average_rating")
    authors_data = convertStrToFloat(authors_data,"author_average_rating")
    authors_data = convertColumnsToRightType(authors_data,COLUMNS_TYPES_AUTHORS)
    authors_data = removeLeadingTrailingSpaces(authors_data,COLUMNS_TYPES_AUTHORS)
    authors_data.to_csv('./data/Cleaned_authors.csv', index=False)



if __name__ == "__main__":
    main("data/books.csv","data/authors.csv","data/Cleaned_books.csv","data/Cleaned_authors.csv")