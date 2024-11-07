import pandas as pd

# Charger les fichiers CSV
books = pd.read_csv("data/Cleaned_books.csv")
authors = pd.read_csv("data/Cleaned_authors.csv")

# Fonction pour compter le nombre d'author_id uniques
def count_unique_authors(df):
    return df["author_id"].nunique()

# Fonction pour compter le nombre d'author_name uniques
def count_unique_author_names(df):
    return df["author_name"].nunique()

# Correction : remplacer "A. Kirk" par "A.E. Kirk" pour l'author_id 5393357
authors.loc[(authors["author_id"] == 5393357) & (authors["author_name"] == "A. Kirk"), "author_name"] = "A.E. Kirk"

# Comptage après la correction
unique_authors_count = count_unique_authors(authors)
unique_author_names_count = count_unique_author_names(authors)

# Affichage des résultats après correction
print("Nombre d'auteurs uniques :", unique_authors_count)
print("Nombre de noms d'auteurs uniques :", unique_author_names_count)

# Fonction pour détecter les homonymes : noms associés à plusieurs identifiants
def find_homonyms(df):
    name_id_counts = df.groupby("author_name")["author_id"].nunique()
    homonyms = name_id_counts[name_id_counts > 1]
    return homonyms

# Exécuter la vérification des homonymes
homonyms = find_homonyms(authors)

# Affichage des résultats de la vérification des homonymes
print("\nNoms d'auteurs associés à plusieurs identifiants :")
print(homonyms)
print("\nNombre total de noms d'auteurs ayant plusieurs identifiants :", len(homonyms))
