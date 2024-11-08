# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np

def main():
    """
    Main function
    """
    
    # Charger authors.csv
    authors = pd.read_csv("data/Cleaned_authors.csv")

    # Charger books.csv
    books = pd.read_csv("data/Cleaned_books.csv")

    # Charger link.csv existant sans colonne de `link_id`
    link_dataframe = pd.read_csv("link.csv")

    # Récupérer l'ID maximum d'auteur déjà présent
    max_author_id = authors['author_id'].max()

    # Extraire les auteurs uniques de books.csv qui ne sont pas dans authors
    books_authors = books[['author', 'id']].drop_duplicates()
    existing_authors = authors['author_name'].unique()
    new_authors = books_authors[~books_authors['author'].isin(existing_authors)]

    # Créer une copie explicite de new_authors
    new_authors = new_authors.copy()

    # Assigner de nouveaux ID aux auteurs manquants
    new_authors['author_id'] = range(max_author_id + 1, max_author_id + 1 + len(new_authors))

    # Créer un DataFrame temporaire pour stocker les nouveaux liens
    new_link_dataframe = pd.DataFrame(columns=['book_id', 'author_id'])

    # Associer chaque auteur dans books avec son ID et générer les nouveaux liens
    for _, row in books.iterrows():
        book_id = row['id']
        author_name = row['author']
        
        # Vérifier si l'auteur est déjà dans authors
        if author_name in existing_authors:
            # Récupérer l'ID de l'auteur existant
            author_id = authors.loc[authors['author_name'] == author_name, 'author_id'].values[0]
        else:
            # Sinon, récupérer l'ID nouvellement assigné dans new_authors
            author_id = new_authors.loc[new_authors['author'] == author_name, 'author_id'].values[0]
        
        # Vérifier si ce lien existe déjà dans link_dataframe
        if not ((link_dataframe['book_id'] == book_id) & (link_dataframe['author_id'] == author_id)).any():
            # Ajouter la paire (book_id, author_id) sans `link_id`
            new_link_dataframe = pd.concat([
                new_link_dataframe,
                pd.DataFrame([[book_id, author_id]], columns=['book_id', 'author_id'])
            ], ignore_index=True)

    # Créer le DataFrame Big_author en combinant authors et new_authors
    big_author_df = pd.concat([authors, new_authors[['author_id', 'author']]], ignore_index=True)
    big_author_df = big_author_df.rename(columns={'author': 'author_name'})

    # Ajouter les nouveaux liens au fichier link.csv existant
    link_dataframe = pd.concat([link_dataframe, new_link_dataframe], ignore_index=True)

    # Sauvegarder les fichiers mis à jour
    big_author_df.to_csv("Big_author.csv", index=False)
    link_dataframe.to_csv("link.csv", index=False)
    print("Fichiers 'Big_author.csv' et 'link.csv' mis à jour avec succès.")

if __name__ == "__main__":
    main()
