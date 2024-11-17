import os
import pandas as pd
import numpy as np

PATH_DATA = "data/"
PATH_POPULATE = os.path.join(PATH_DATA, "populate")

def main(books,authors):
    os.makedirs(PATH_POPULATE, exist_ok=True)

    # Listage des pays
    countries = books['settingCountry'].unique()

    countries = countries[~pd.isnull(countries)]

    # Création d'un dataframe pour la table pays
    dataset = pd.DataFrame({'nom': countries})

    dataset.index = dataset.index+1

    dataset = dataset.reset_index(names=['id_pays'])
    dataset.to_csv(os.path.join(PATH_POPULATE,"pays.csv"), index=False)

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
    settingLinkData.to_csv(os.path.join(PATH_POPULATE,"cadre_livre.csv"), index=False)
    
    settingData = settingData.drop(columns=['id_livre'])
    # settingData['annee'].astype(int) # FIXME: check if it works
    settingData.to_csv(os.path.join(PATH_POPULATE,"cadre.csv"), index=False)

    #Création d'un dataframe pour la table editeur
    publishers = books['publisher'].unique()
    publishers = publishers[~pd.isnull(publishers)]
    dataset = pd.DataFrame({'nom_editeur': publishers})
    dataset.index = dataset.index+1
    dataset = dataset.reset_index(names=['id_editeur'])
    dataset.to_csv(os.path.join(PATH_POPULATE,"editeur.csv"), index=False)


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
    booksData = booksData.rename(columns={"one_star_ratings": "nb_note_1_etoile"})
    booksData = booksData.rename(columns={"two_star_ratings": "nb_note_2_etoile"})
    booksData = booksData.rename(columns={"three_star_ratings": "nb_note_3_etoile"})
    booksData = booksData.rename(columns={"four_star_ratings": "nb_note_4_etoile"})
    booksData = booksData.rename(columns={"five_star_ratings": "nb_note_5_etoile"})
    booksData = booksData.rename(columns={"number_of_pages": "nombre_pages"})
    booksData = booksData.rename(columns={"date_published": "date_publication"})
    booksData = booksData.rename(columns={"original_title": "titre_original"})

    booksData.to_csv(os.path.join(PATH_POPULATE,"livre.csv"), index=False)

    # Listage des genres
    genre = authors['author_genres'].unique()

    # Création d'un dataframe pour la table auteurs
    authorData = authors.drop(columns=['author_genres'])
    authorData = authorData.drop_duplicates()
    authorData = authorData.drop_duplicates(subset=["author_id"], keep='first')

    authorData = authorData.rename(columns={"author_average_rating": "note_moyenne", "author_id": "id_auteur", "author_name": "nom" ,"birthplace": "origine", "author_review_count": "nb_reviews", "author_rating_count" : "nb_critiques", "author_gender" : "sexe"})
    authorData.to_csv(os.path.join(PATH_POPULATE,"auteur_sql.csv"), index=False)

    # Création dataframe pour la table genre
    genreData = pd.DataFrame({'author_genres': genre})

    genreData.index = genreData.index+1

    genreData = genreData.reset_index(names=['id_genre'])
    
    genreData = genreData.rename(columns={"author_genres": "libelle_genre"})
    genreData.to_csv(os.path.join(PATH_POPULATE,"genre.csv"), index=False)

    # Création d'un dataframe pour le lien entre les auteurs et leur genre
    genreVoteData = pd.merge(authors, genreData, left_on='author_genres', right_on="libelle_genre", how='inner')

    genreVoteData = genreVoteData[['author_id','id_genre',]]

    genreVoteData = genreVoteData.drop_duplicates()

    genreVoteData = genreVoteData.rename(columns={"author_id": "id_auteur"})
    genreVoteData.to_csv(os.path.join(PATH_POPULATE,"auteur_genre.csv"), index=False)

    # Listage
    series = books['seriesName'].dropna().unique()

    # Créer un DataFrame pour la table des séries avec un identifiant unique
    seriesData = pd.DataFrame({'seriesName': series})

    # Ajouter un identifiant unique pour chaque série
    seriesData.index = seriesData.index + 1 
    seriesData = seriesData.reset_index(names=['id_serie'])
    seriesData = seriesData.rename(columns={"seriesName": "nom_serie"})

    # Exporter le DataFrame des séries en CSV
    seriesData.to_csv(os.path.join(PATH_POPULATE,"series.csv"), index=False)


    episodeData = pd.merge(books, seriesData, left_on='seriesName', right_on="nom_serie", how='inner')

    episodeData = episodeData[['id_serie','id','episodeNumber']]

    episodeData = episodeData.rename(columns={"id": "id_livre"})
    episodeData = episodeData.rename(columns={"episodeNumber": "numero_episode"})

    episodeData.to_csv(os.path.join(PATH_POPULATE,"episode_serie.csv"), index=False)



    df_books = pd.read_csv("data/complete_book_copy.csv")
    df_genre_from_authors = genreData.copy()

    # 2. Clean the books dataframe:
    # reshape the data
    df_clean_books = df_books[['id','genre_and_votes']] # keep only id & genre_and_votes
    df_clean_books['genre_and_votes'] = df_clean_books['genre_and_votes'].str.split(',') # turn the str into a list of genre/vote
    df_clean_books = df_clean_books.explode('genre_and_votes', ignore_index=True) # for each genre/vote group for a book, add a line. The result is that many lines have the same book id.
    df_clean_books = df_clean_books.dropna() # drop nan values
    # split genre_and_votes
    df_clean_books[['genre', 'votes']] = df_clean_books['genre_and_votes'].str.rsplit(' ', n=1, expand=True) # split the genre and vote into two separate genre and votes columns
    df_clean_books = df_clean_books.drop('genre_and_votes', axis=1) # drop the genre_and_votes column
    # clean up the invalid data
    df_clean_books['votes'] = df_clean_books['votes'].replace('1user', '1') # if votes value is '1user', change it to 1
    df_clean_books = df_clean_books[df_clean_books['votes'].str.isdigit()] # keep only numerical values
    df_clean_books = df_clean_books[df_clean_books['votes'] >= '0'] # remove negative values
    df_clean_books['votes'] = df_clean_books['votes'].astype(int) # force convert numerical values to int
    df_clean_books['genre'] = df_clean_books['genre'].str.lower() # lowercase the genres
    df_clean_books['genre'] = df_clean_books['genre'].str.strip() # remove trailing spaces
    
    # 3. Join the books dataframe with the genre table
    df_genre_from_authors_libelle_only = df_genre_from_authors['libelle_genre'] 
    df_genre = df_clean_books[['genre']].drop_duplicates().sort_values('genre')
    df_genre.rename(columns={'genre': 'libelle_genre'}, inplace=True)

    df_genre['libelle_genre'] = df_genre['libelle_genre'].str.strip()

    df_genre_global = pd.merge(df_genre_from_authors_libelle_only, df_genre, on='libelle_genre', how='outer')
    df_genre_global = df_genre_global.drop_duplicates()

    df_genre_global = pd.merge(df_genre_global, df_genre_from_authors, on='libelle_genre', how='outer')

    df_genre_global = df_genre_global.sort_values(by=['id_genre'])
    df_genre_global['id_genre'] = df_genre_global.index + 1

    df_clean_books.rename(columns={'genre': 'libelle_genre', 'id' : 'id_livre', 'votes' : 'nb_votes'}, inplace=True)
    df_clean_books = pd.merge(df_clean_books, df_genre_global, on='libelle_genre', how='inner')
    df_clean_books = df_clean_books.drop(columns=['libelle_genre'])
    df_clean_books = df_clean_books.drop_duplicates()

    print("\n\n===---===\n\n",df_books.columns)
    df_clean_books_author = df_books[['id','genre_1', 'genre_2']] 
    df_clean_books_author = df_clean_books_author.dropna(subset=['genre_1'])

    df_clean_books_author = df_clean_books_author.melt(id_vars=['id'], value_vars=['genre_1','genre_2'])
    df_clean_books_author = df_clean_books_author.drop(columns=['variable'])
    df_clean_books_author.rename(columns={'value': 'libelle_genre', 'id' : 'id_livre'}, inplace=True)
    df_clean_books_author['libelle_genre'] = df_clean_books_author['libelle_genre'].str.lower()
    df_clean_books_author['libelle_genre'] = df_clean_books_author['libelle_genre'].str.strip()

    df_books_author_genre = df_clean_books_author['libelle_genre'].drop_duplicates()

    df_genre_glob2 = pd.merge(df_books_author_genre, df_genre_global, on='libelle_genre', how='outer')
    df_genre_glob2 = df_genre_glob2.reset_index(drop=True)
    df_genre_glob2['id_genre'] = df_genre_glob2.index + 1
    df_clean_books_author = pd.merge(df_genre_glob2, df_clean_books_author, on='libelle_genre', how='inner')
    df_clean_books_temp = df_clean_books_author.drop(columns=['libelle_genre'])

    df_clean_books = pd.concat([df_clean_books,df_clean_books_temp])

    df_clean_books = df_clean_books.fillna(1)
    df_clean_books['nb_votes'] = df_clean_books['nb_votes'].astype(int)
    df_clean_books = df_clean_books.drop_duplicates()
    df_clean_books.to_csv(os.path.join(PATH_POPULATE,"livre_genre.csv"),index=False)
    df_genre_glob2.to_csv(os.path.join(PATH_POPULATE,"genre.csv"),index=False)

    awardData = books[['awardDate', 'awardName']]
    awardData = awardData.drop_duplicates()

    # Ajouter une colonne 'id_prix' unique pour chaque ligne
    awardData['id_prix'] = range(1, len(awardData) + 1)

    # Supprimer les lignes où 'awardDate' ou 'awardName' est manquant
    awardData = awardData.dropna(subset=['awardName'])

    # Supprimer les doublons en conservant uniquement les lignes uniques de 'awardDate' et 'awardName'
    awardData = awardData.drop_duplicates(subset=['awardDate', 'awardName'])

    # Ajouter une colonne 'id_prix' unique pour chaque ligne après suppression des doublons
    awardData['id_prix'] = range(1, len(awardData) + 1)

    # Renommer les colonnes pour le fichier prix.csv
    awardData = awardData.rename(columns={'awardDate': 'annee_prix', 'awardName': 'nom_prix'})

    # Réorganiser les colonnes : 'id_prix' en premier, puis 'nom_prix' et 'annee_prix'
    awardData = awardData[['id_prix', 'nom_prix', 'annee_prix']]

    # Enregistrer le DataFrame dans le fichier data/populate/prix.csv
    # awardData['annee_prix'].astype(int) # FIXME: check if it works
    awardData.to_csv(os.path.join(PATH_POPULATE,"prix.csv"), index=False)

    # --- Suite du script pour générer prix_livre.csv ---
    bookData = books[['id', 'awardName', 'awardDate']]

    # Convertir les colonnes 'awardDate' et 'annee_prix' en int pour éviter les problèmes de fusion
    bookData['awardDate'] = bookData['awardDate'].astype('Int32')
    awardData['annee_prix'] = awardData['annee_prix'].astype('Int32')

    # Associer chaque livre au prix correspondant en effectuant une fusion sur 'awardName' et 'awardDate'
    awardData = pd.merge(bookData, awardData, left_on=['awardName', 'awardDate'], right_on=['nom_prix', 'annee_prix'])

    # Garder uniquement les colonnes nécessaires pour la table _prix_livre
    awardData = awardData[['id_prix', 'id']].dropna()

    # Renommer la colonne 'id' en 'id_livre'
    awardData = awardData.rename(columns={'id': 'id_livre'})

    # Supprimer les doublons dans le DataFrame
    awardData = awardData.drop_duplicates()

    # Enregistrer le DataFrame final dans un fichier CSV
    awardData.to_csv(os.path.join(PATH_POPULATE,"prix_livre.csv"), index=False)


if __name__ == "__main__":
    BOOKS_DTYPE = {
    'rating_count': 'Int32', 
    'review_count': 'Int32', 
    'five_star_ratings': 'Int32', 
    'four_star_ratings': 'Int32', 
    'three_star_ratings': 'Int32', 
    'two_star_ratings': 'Int32', 
    'one_star_ratings': 'Int32', 
    'nombre_pages': 'Int32', 
    'one_star_ratings': 'Int32'}
    
    books = pd.read_csv("data/Cleaned_books.csv", dtype=BOOKS_DTYPE)
    author = pd.read_csv("data/Cleaned_authors.csv")
    main(books,author)
