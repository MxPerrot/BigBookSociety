import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/books.csv")

#cols = ["Unnamed: " + str(i) for i in range(24,86)]
str_column="Unnamed: "

#print(data.shape)

#Purge des lignes contenant des informations dans des colonnes inexistantes

for i in range(24,87):
    index = 0
    for y in data[str_column+str(i)]:
        if (pd.notna(y)):
            data = data.drop([index])
        index += 1
            
#Purge des colonnes inexistantes

for i in range(24,87):
 data = data.drop(columns=[str_column+str(i)])

#Détecter Anomalie colonne



booksFormat={"id":int,
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

# Nettoyeur ISBN13 Complet

# index = 0
# for i in data['isbn13']:
#     if ((type(i) == float or i.isnumeric()) and pd.notna(i)):
#         data["isbn13"] = data["isbn13"].replace([i], int(i))
#     elif (type(i) == int) or pd.isna(i): pass
#     else: data = data.drop([index])
#     index+=1

index = 0
for i in data:
    if (i!="isbn13"):
        for y in data[i]:
            if (type(y)!=booksFormat[i] and (pd.notna(y))):
                print(y,type(y),i)
    index+=1