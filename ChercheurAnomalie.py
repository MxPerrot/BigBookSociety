import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/books.csv")

#cols = ["Unnamed: " + str(i) for i in range(24,86)]
str_column="Unnamed: "

#print(data.shape)

#Purge des lignes contenant des informations dans des colonnes inexistantes

print(f"\n--- Purge ligne vide     ---\n")

for i in range(24,87):
    index = 0
    for y in data[str_column+str(i)]:
        if (pd.notna(y)):
            data = data.drop([index])
        index += 1
print(f"\n--- Purge ligne vide OK ---\n")
            
#Purge des colonnes inexistantes

print(f"\n--- Purge colonnes unnamed    ---\n")

for i in range(24,87):
 data = data.drop(columns=[str_column+str(i)])

print(f"\n--- Purge colonnes unnamed OK ---\n")

#Détecter Anomalie colonne



booksFormat ={"id":int,
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


# print(data.shape)

def nettoyeurISBN13(data):
    print(f"\n--- Nettoyage ISBN13    ---\n")
    for index, cell in data['isbn13'].items():

        if pd.isna(cell):
            # print(f"\n--- cell {cell} is null")
            pass

        elif type(cell) == int:
            pass 

        elif (type(cell) == float or cell.isnumeric()):
            # print(f"\n--- CONVERT {cell} to int")
            data.loc[index, 'isbn13'] = int(cell) 

        else:
            # print(f"\n--- DROPPING {cell} at {index} ---\n")
            # print(data.loc[index, 'isbn13'])
            data = data.drop(index)    
    print(f"\n--- Nettoyage ISBN13 OK ---\n")
    return data

data = nettoyeurISBN13(data)
# print(data.shape)


def nettoyeurAverageRating(data):
    print(f"\n--- Nettoyage Average Rating    ---\n")
    #Convertie les virgules en point puis les string en float
    data['average_rating'] = data['average_rating'].replace({',': '.'}, regex=True)
    data['average_rating'] = pd.to_numeric(data['average_rating'],downcast='float')
    return data

data = nettoyeurAverageRating(data)



def chercheurAnomalie(data,booksFormat):
    index = 0
    for i in data:
        for y in data[i]:
            if (type(y)!=booksFormat[i] and (pd.notna(y))):
                print(y,type(y),i)
    index+=1

chercheurAnomalie(data,booksFormat)
