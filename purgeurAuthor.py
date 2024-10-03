
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/authors.csv")

print(data.shape)

authorFormat ={"author_average_rating":float,
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

def nettoyeurBookAverageRating(data):
    print(f"\n--- Nettoyage Book Average Rating    ---\n")
    #Convertie les virgules en point puis les string en float
    data['book_average_rating'] = data['book_average_rating'].replace({',': '.'}, regex=True)
    data['book_average_rating'] = pd.to_numeric(data['book_average_rating'],downcast='float')
    print(f"\n--- Nettoyage Book Average Rating OK ---\n")
    return data

# data = nettoyeurBookAverageRating(data)

def nettoyeurAuthorAverageRating(data):
    print(f"\n--- Nettoyage Book Average Rating    ---\n")
    #Convertie les virgules en point puis les string en float
    data['author_average_rating'] = data['author_average_rating'].replace({',': '.'}, regex=True)
    data['author_average_rating'] = pd.to_numeric(data['author_average_rating'],downcast='float')
    print(f"\n--- Nettoyage Book Average Rating OK ---\n")
    return data

# data = nettoyeurAuthorAverageRating(data)

def nettoyeurGlobal(data,Format):
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

# data = nettoyeurGlobal(data,authorFormat)

def chercheurAnomalie(data,Format):
    index = 0
    for i in data:
        for y in data[i]:
            if (type(y)!=Format[i] and (pd.notna(y))):
                print(y,type(y),i)
    index+=1

chercheurAnomalie(data,authorFormat)
# print(data.shape)

