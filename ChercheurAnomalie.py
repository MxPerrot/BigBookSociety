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


print(data.shape)

print(f"\n--- Nettoyage ISBN13    ---\n")

index = 0
nbr_case_supr = 0
for cell in data['isbn13']:

    if pd.isna(cell):
        # print(f"\n--- cell {cell} is null")
        pass

    elif type(cell) == int:
        pass 

    elif (type(cell) == float or cell.isnumeric()):
        # print(f"\n--- CONVERT {cell} to int")
        data.loc[index, 'isbn13'] = int(cell) 

    else:
        print(f"\n--- DROPPING {cell} at {index} ---\n")
        print(data.loc[index, 'isbn13'])
        data = data.drop(index)    
        nbr_case_supr+=1
    index+=1

print(f"\n--- Nettoyage ISBN13 OK ---\n")

# (52188, 24)
# print(data.shape, nbr_case_supr)
# (52180, 24) 8



def chercheurAnomalie(data,booksFormat):
    index = 0
    for i in data:
        for y in data[i]:
            if (type(y)!=booksFormat[i] and (pd.notna(y))):
                if(type(y)==str and not y.isnumeric()):
                    print(y,type(y),i)
    index+=1

chercheurAnomalie(data,booksFormat)


# B009NN5RJY <class 'str'> isbn13
# B00596V3OM <class 'str'> isbn13
# B003U2RVVQ <class 'str'> isbn13
# HSN1800000160 <class 'str'> isbn13
# 10:1984254994 <class 'str'> isbn13

# 13:9780615700 <class 'str'> isbn13
# 10:1496102266 <class 'str'> isbn13
# B07CX9MNQL <class 'str'> isbn13
# B009NN5RJY <class 'str'> isbn13
# B00596V3OM <class 'str'> isbn13
# B003U2RVVQ <class 'str'> isbn13
# HSN1800000160 <class 'str'> isbn13
# 10:1984254994 <class 'str'> isbn13


# print(f"\n--- Chercher anomalies    ---\n")


# index = 0
# for i in data:
#     for y in data[i]:
#         if (type(y)!=booksFormat[i] and (pd.notna(y))):
#             print(y,type(y),i)
#     index+=1

# print(f"\n--- Chercher anomalies OK ---\n")


# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# data = pd.read_csv("data/books.csv")

# booksFormat={"id":int,
# "title":str,
# "series":str,
# "author":str,
# "rating_count":int,
# "review_count":int,
# "average_rating":float,
# "five_star_ratings":int,
# "four_star_ratings":int,
# "three_star_ratings":int,
# "two_star_ratings":int,
# "one_star_ratings":int,
# "number_of_pages":int,
# "date_published":str,
# "publisher":str,
# "original_title":str,
# "genre_and_votes":str,
# "isbn":str,
# "isbn13":int,
# "settings":str,
# "characters":str,
# "awards":str,
# "books_in_series":str,
# "description":str,
# }

# #Nettoyeur ISBN13 Complet

# # def nettoyeurISBN(data):
#     # index = 0
#     # for i in data['isbn13']:
#     #     if ((type(i) == float or i.isnumeric()) and pd.notna(i)):
#     #         data["isbn13"] = data["isbn13"].replace([i], int(i))
#     #     elif (type(i) == int) or pd.isna(i): pass
#     #     else: 
#     #         print(i)
#     #         data = data.drop([index])
#     #     index+=1
#     # return data

# #Nettoyeur nombre_de_pages Complet

# def nettoyeurPages(data):
#     index = 0
#     for i in data['number_of_pages']:
#         if ((type(i) == float or i.isnumeric()) and pd.notna(i)):
#             data["number_of_pages"] = data["number_of_pages"].replace([i], int(i))
#         elif (type(i) == int) or pd.isna(i): pass
#         else: data = data.drop([index])
#         index+=1
#     return data


# def nettoyeurColonneVide(dat):
#     data = dat
#     str_column="Unnamed: "

#     for i in range(24,87):
#         index = 0
#         for y in data[str_column+str(i)]:
#             if (pd.notna(y)):
#                 data = data.drop([index])
#             index += 1
                
#     for i in range(24,87):
#         data = data.drop(columns=[str_column+str(i)])

#     return data









# data = nettoyeurColonneVide(data)

# # data = nettoyeurISBN(data)

# # data = nettoyeurPages(data)

# index = 0
# for i in data['isbn13']:
#     if ((type(i) == float or i.isnumeric()) and pd.notna(i)):
#         data["isbn13"] = data["isbn13"].replace([i], int(i))
#     elif (type(i) == int) or pd.isna(i): pass
#     else: 
#         print(i)
#         data = data.drop([index])
#     index+=1

# chercheurAnomalie(data,booksFormat)

