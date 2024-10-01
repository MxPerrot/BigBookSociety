import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO

# Remplace les caratères mal encodés d'un fichier CSV et les renvoie sous forme de dataframe
def nettoyageUTF8(nomFichier):
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
    with open(nomFichier, 'r') as file:
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

def ajoutLongeurDescription(df):
    df['description_length'] = df["description"].str.count(' ')+1
    return df

def ajoutLongeurTitre(df):
    df['title_length'] = df["title"].str.len()
    return df

def ajoutLongeurSerie(df):
    df['series_length'] = df["books_in_series"].str.count(',')+1
    return df

nomFichierCSV = 'data/books.csv'
df = nettoyageUTF8(nomFichierCSV)
df = ajoutLongeurDescription(df)
df = ajoutLongeurTitre(df)
df = ajoutLongeurSerie(df)

