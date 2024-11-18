# -*- coding:utf-8 -*- 

import pandas as pd
import numpy as np
from clean_data import COLUMNS_TYPES_AUTHORS,convertColumnsToRightType
import os

def main():
    """
    Main function
    """

    # Charger les fichiers CSV
    authors_path = "data/complete_author.csv"
    clean_authors_path = "data/Cleaned_authors.csv"
    books_path = "data/Cleaned_books.csv"
    link_path = "data/populate/link.csv"

    authors = pd.read_csv(clean_authors_path)  # Charger le fichier existant
    books = pd.read_csv(books_path)  # Charger le fichier existant

    books['author'] = books['author'].str.split(',')
    books = books.explode('author', ignore_index=True)
    books['author'] = books['author'].str.lstrip()

    # Get a list of books in the authors ("book_title" column)
    authors_in_authors = authors["author_name"].unique()

    # Check for all ids in books_in_authors that are also in books["id"]
    authors_in_books = books["author"].unique()

    common_author_name = np.intersect1d(authors_in_authors, authors_in_books)

    rows_books_author_big = books.loc[~books['author'].isin(authors['author_name'])]

    max_author_id = authors["author_id"].max() if not authors.empty else 0

    author_a_implemente = rows_books_author_big['author'].drop_duplicates().to_frame()

    author_a_implemente.index = author_a_implemente.index + max_author_id

    author_a_implemente = author_a_implemente.reset_index()

    rows_books_author_big = pd.merge(rows_books_author_big, author_a_implemente, on='author', how='inner')

    rows_books_author_big = rows_books_author_big.rename(columns={"index": "author_id","id": "book_id"})
    link_dataframe = pd.read_csv(link_path)

    col_list = ['book_id', 'author_id']

    link_dataframe = pd.concat([link_dataframe,rows_books_author_big[col_list]])

    author_a_implemente = author_a_implemente.rename(columns={"index": "author_id","author": "author_name"})

    author_a_implemente = author_a_implemente.reset_index(drop=True)

    # Mettre à jour BigAuthor
    bigAuthor = pd.concat([authors, author_a_implemente])

    bigAuthor['author_genres'] = bigAuthor['author_genres'].str.split(',')
    bigAuthor = bigAuthor.explode('author_genres', ignore_index=True)

    #TODO réglér problème .O

    #Supprimer les colonnes non souhaitées de BigAuthor
    bigAuthor = bigAuthor.drop(columns=["book_average_rating", "book_id", "book_title", "genre_1", "genre_2", "num_ratings", "num_reviews", "pages", "publish_date"])


    print(type(bigAuthor["author_genres"][1]))


    
    bigAuthor = bigAuthor.loc[bigAuthor["author_genres"] != "" ]

    bigAuthor = bigAuthor.drop_duplicates()

    bigAuthor = convertColumnsToRightType(bigAuthor,COLUMNS_TYPES_AUTHORS)

    link_dataframe = link_dataframe.rename(columns={"book_id": "id_livre", "author_id": "id_auteur"})

    link_dataframe = link_dataframe.drop_duplicates()

    bigAuthor.to_csv(authors_path, index=False)
    link_dataframe.to_csv(link_path, index=False)

    # # Vérifier si BigAuthor.csv existe déjà
    # if os.path.exists(authors_path):
    #     authors = pd.read_csv(authors_path)  # Charger le fichier existant
    # else:
    #     authors = pd.DataFrame(columns=["author_average_rating", "author_gender", "author_genres", "author_id", 
    #                                     "author_name", "author_rating_count", "author_review_count", 
    #                                     "birthplace", "book_average_rating", "book_id", "book_title", 
    #                                     "genre_1", "genre_2", "num_ratings", "num_reviews", "pages", 
    #                                     "publish_date"])  # Si le fichier n'existe pas, on en crée un vide

    # # Charger Cleaned_authors.csv pour récupérer les auteurs qui ne sont pas dans BigAuthor
    # clean_authors = pd.read_csv(clean_authors_path)

    # # Ajouter les auteurs de Cleaned_authors à BigAuthor si ce n'est pas déjà fait
    # max_author_id = authors["author_id"].max() if not authors.empty else 0
    # existing_authors = set(authors["author_name"])

    # # Ajouter les auteurs de Cleaned_authors à BigAuthor si ils n'existent pas déjà
    # new_authors = []
    # for _, row in clean_authors.iterrows():
    #     author_name = row["author_name"]
    #     if author_name not in existing_authors:
    #         max_author_id += 1
    #         new_authors.append({
    #             "author_id": max_author_id,
    #             "author_name": author_name,
    #             "author_average_rating": row.get("author_average_rating", np.nan),
    #             "author_gender": row.get("author_gender", np.nan),
    #             "author_genres": row.get("author_genres", np.nan),
    #             "author_rating_count": row.get("author_rating_count", np.nan),
    #             "author_review_count": row.get("author_review_count", np.nan),
    #             "birthplace": row.get("birthplace", np.nan),
    #             "book_average_rating": np.nan,  # Pas encore disponible dans BigAuthor
    #             "book_id": np.nan,              # Pas encore disponible dans BigAuthor
    #             "book_title": np.nan,           # Pas encore disponible dans BigAuthor
    #             "genre_1": np.nan,              # Pas encore disponible dans BigAuthor
    #             "genre_2": np.nan,              # Pas encore disponible dans BigAuthor
    #             "num_ratings": np.nan,          # Pas encore disponible dans BigAuthor
    #             "num_reviews": np.nan,          # Pas encore disponible dans BigAuthor
    #             "pages": np.nan,                # Pas encore disponible dans BigAuthor
    #             "publish_date": np.nan          # Pas encore disponible dans BigAuthor
    #         })
    #         existing_authors.add(author_name)

    # # Ajouter les nouveaux auteurs à BigAuthor
    # if new_authors:
    #     authors = pd.concat([authors, pd.DataFrame(new_authors)], ignore_index=True)

    # # Charger les livres
    # books = pd.read_csv(books_path)
    # link_df = pd.read_csv(link_path) if os.path.exists(link_path) else pd.DataFrame(columns=["book_id", "author_id"])

    # # Liste pour stocker les nouveaux liens entre les livres et les auteurs
    # new_links = []

    # books['author'] = books['author'].str.split(',')
    # books = books.explode('author', ignore_index=True)


    # Traitement des livres et auteurs dans Cleaned_books.csv
    # for _, row in books.iterrows():
    #     book_id = row["id"]
    #     authors_str = row["author"]  # Colonne contenant les noms des auteurs
    #     os.system('cls' if os.name == 'nt' else 'clear')
    #     print(f"Chargement auteur: {barre}/{len(books)}")
    #     barre+=1

    #     if pd.notna(authors_str):  # Vérifie que ce n'est pas une valeur NaN
    #         author_name = authors_str

    #         # Vérifier si l'auteur existe déjà dans BigAuthor
    #         author_row = authors[authors["author_name"] == author_name]

    #         if author_row.empty:
    #                 # Si l'auteur n'existe pas, ajouter un nouvel ID et l'inclure dans BigAuthor
    #                 max_author_id += 1
    #                 authors = pd.concat([authors, pd.DataFrame({
    #                     "author_id": [max_author_id],author_rating_count
    #                     "author_name": [author_name],
    #                     "author_average_rating": [np.nan],
    #                     "author_gender": [np.nan],
    #                     "author_genres": [np.nan],
    #                     "author_rating_count": [np.nan],
    #                     "author_review_count": [np.nan],
    #                     "birthplace": [np.nan],
    #                     "book_average_rating": [np.nan],
    #                     "book_id": [book_id],
    #                     "book_title": [row["title"]],
    #                     "genre_1": [row.get("genre_1", np.nan)],
    #                     "genre_2": [row.get("genre_2", np.nan)],
    #                     "num_ratings": [row.get("num_ratings", np.nan)],
    #                     "num_reviews": [row.get("num_reviews", np.nan)],
    #                     "pages": [row.get("pages", np.nan)],
    #                     "publish_date": [row.get("publish_date", np.nan)],
    #                 })], ignore_index=True)
    #                 author_id = max_author_id
    #         else:
    #                 # Sinon, utiliser l'ID existant
    #                 author_id = author_row.iloc[0]["author_id"]

    #         # Ajouter une nouvelle association dans new_links
    #         new_links.append({
    #             "book_id": book_id,
    #             "author_id": author_id
    #         })

    # Créer un DataFrame pour les nouvelles associations
    # new_links_df = pd.DataFrame(new_links)

    # # Combiner link_df avec les nouvelles associations sans duplications
    # link_df = pd.concat([link_df, new_links_df]).drop_duplicates(ignore_index=True)

    # # Réorganiser les colonnes de BigAuthor pour qu'elles correspondent à l'ordre de Cleaned_authors
    # authors = authors[[
    #     "author_average_rating", "author_gender", "author_genres", "author_id", "author_name", 
    #     "author_rating_count", "author_review_count", "birthplace", "book_average_rating", "book_id", 
    #     "book_title", "genre_1", "genre_2", "num_ratings", "num_reviews", "pages", "publish_date"
    # ]]

    # # Supprimer les colonnes non souhaitées de BigAuthor
    # authors = authors.drop(columns=["book_average_rating", "book_id", "book_title", "genre_1", "genre_2", 
    #                                 "num_ratings", "num_reviews", "pages", "publish_date"])

    # authors['author_genres'] = authors['author_genres'].str.split(',')
    # authors = authors.explode('author_genres', ignore_index=True)

    # # Enregistrer les nouveaux fichiers CSV
    # authors.to_csv(authors_path, index=False)  # Mettre à jour BigAuthor.csv
    # link_df.to_csv(link_path, index=False)  # Mettre à jour link.csv
    # print("Les fichiers ont été mis à jour avec succès.")

if __name__ == "__main__":
    main()
