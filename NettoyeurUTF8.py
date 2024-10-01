import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO

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
    'Ã': 'à'
}

# Ouvre le document et le met dans une chaine
with open('data/books.csv', 'r') as file:
    document = file.read()

    # Remplace les caractères mal encodés par le caractère original
    for key,value in correspondanceUTF8.items() :
        print(key + " -> " + value)
        document = document.replace(key, value)

csvStringIO = StringIO(document)
data = pd.read_csv(csvStringIO, sep=',')

df = pd.DataFrame(data)
print(data.head())

print(df['description'])