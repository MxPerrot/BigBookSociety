import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/books.csv")

str_column="Unnamed: "

print(data.shape)

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
"description":str
}

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



# print(data.shape)

# def nettoyeurISBN13(data):
#     print(f"\n--- Nettoyage ISBN13    ---\n")
#     for index, cell in data['isbn13'].items():

#         if pd.isna(cell):
#             # print(f"\n--- cell {cell} is null")
#             pass

#         elif type(cell) == int:
#             pass 

#         elif (type(cell) == float or cell.isnumeric()):
#             # print(f"\n--- CONVERT {cell} to int")
#             data.loc[index, 'isbn13'] = int(cell) 

#         else:
#             # print(f"\n--- DROPPING {cell} at {index} ---\n")
#             # print(data.loc[index, 'isbn13'])
#             data = data.drop(index)    
#     print(f"\n--- Nettoyage ISBN13 OK ---\n")
#     return data

# data = nettoyeurISBN13(data)
# # print(data.shape)


def nettoyeurAverageRating(data):
    print(f"\n--- Nettoyage Average Rating    ---\n")
    #Convertie les virgules en point puis les string en float
    data['average_rating'] = data['average_rating'].replace({',': '.'}, regex=True)
    data['average_rating'] = pd.to_numeric(data['average_rating'],downcast='float')
    print(f"\n--- Nettoyage Average Rating OK ---\n")
    return data

data = nettoyeurAverageRating(data)

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

data = nettoyeurGlobal(data,booksFormat)

def chercheurAnomalie(data,Format):
    index = 0
    for i in data:
        for y in data[i]:
            if (type(y)!=Format[i] and (pd.notna(y))):
                print(y,type(y),i)
    index+=1

# chercheurAnomalie(data,booksFormat)
print(data.shape)

# 52199
# 52180

# nbr_anomalie_1 = 0
# for index, cell in data["number_of_pages"].items():
#     if pd.isna(cell):
#         pass

#     elif type(cell) == booksFormat["number_of_pages"]:
#         pass 

#     elif ((booksFormat["number_of_pages"] == float or booksFormat["number_of_pages"] == int) and (type(cell) == float or cell.isnumeric())):
#         if(booksFormat["number_of_pages"]==float):
#             data.loc[index, "number_of_pages"] = float(cell) 
#             print("a")
#         if(booksFormat["number_of_pages"]==int):
#             data.loc[index, "number_of_pages"] = int(cell) 
#             print(int(cell))
#             nbr_anomalie_1+=1

#     else:
#         data = data.drop(index)    
#         print("c")

# time.sleep(10)

# print(data["number_of_pages"])


# index = 0
# nbr_anomalie = 0
# for y in data["number_of_pages"]:
#     if (type(y)!=booksFormat["number_of_pages"] and (pd.notna(y))):
#         nbr_anomalie+=1
#     index+=1

