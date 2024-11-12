import pandas as pd
import numpy as np

books = pd.read_csv("data/IGNOREME_Cleaned_books2.csv", dtype={
    'rating_count': 'Int32', 
    'review_count': 'Int32', 
    'five_star_ratings': 'Int32', 
    'four_star_ratings': 'Int32', 
    'three_star_ratings': 'Int32', 
    'two_star_ratings': 'Int32', 
    'one_star_ratings': 'Int32', 
    'nombre_pages': 'Int32', 
    'one_star_ratings': 'Int32'
})

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
