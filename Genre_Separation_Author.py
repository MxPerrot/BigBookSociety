import pandas as pd
import numpy as np

authors = pd.read_csv("BigAuthor.csv")

genre = authors['author_genres'].unique()

author_without_genre = authors.drop(columns=['author_genres'])

# Création dataframe pour la table genre
dataset = pd.DataFrame({'author_genres': genre})

dataset.index = dataset.index+1

dataset = dataset.reset_index(names=['id_genre'])

#Création lien auteur-genre
auteur_genre = pd.merge(authors, dataset, on='author_genres', how='inner')

auteur_genre = auteur_genre.drop(columns=['author_average_rating','author_gender','author_genres','author_name','author_rating_count','author_review_count','birthplace'])

auteur_genre = auteur_genre.drop_duplicates()

#Format CSV
auteur_genre = auteur_genre.rename(columns={"author_id": "id_author"})
auteur_genre.to_csv("./SQL/auteur_genre.csv", index=False)

dataset = dataset.rename(columns={"author_genres": "libelle_genre"})
dataset.to_csv("./SQL/genre.csv", index=False)

author_without_genre = author_without_genre.rename(columns={"author_average_rating": "note_moyenne", "author_id": "id_auteur", "author_name": "nom" ,"birthplace": "origine", "author_review_count": "nb_reviews", "author_rating_count" : "nb_critiques", "author_gender" : "sexe"})
author_without_genre.to_csv("./SQL/auteur_sql.csv", index=False)