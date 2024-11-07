import pandas as pd

# Charger les fichiers CSV
books = pd.read_csv("data/Cleaned_books.csv")
authors = pd.read_csv("data/Cleaned_authors.csv")

# Fonction pour normaliser les noms (enlever les espaces superflus et uniformiser la casse)
def normalize_name(name):
    return " ".join(name.strip().lower().split())

# Appliquer la normalisation sur les colonnes 'author' de books et 'author_name' de authors
books["normalized_author"] = books["author"].apply(normalize_name)
authors["normalized_author_name"] = authors["author_name"].apply(normalize_name)

# 1. Vérifier les doublons dans 'author_id' de authors
duplicates_in_author_id = authors[authors.duplicated(subset=['author_id'], keep=False)]

# 2. Vérifier s'il y a des noms associés à plusieurs 'author_id'
duplicate_names = authors[authors.duplicated(subset=['normalized_author_name'], keep=False)]

# 3. Résoudre les problèmes de doublons dans 'author_name'
# Exemple de résolution : Si deux noms ont le même 'author_id', garder l'un des deux (ou remplacer)
# On choisit ici de remplacer les noms multiples par le nom le plus complet (par exemple "A.E. Kirk" remplaçant "A. Kirk")
for author_id in duplicates_in_author_id['author_id'].unique():
    authors.loc[authors['author_id'] == author_id, 'normalized_author_name'] = \
        authors.loc[authors['author_id'] == author_id, 'normalized_author_name'].mode()[0]

# 4. Vérifier les auteurs présents dans 'books' mais absents de 'authors'
missing_authors = set(books["normalized_author"]) - set(authors["normalized_author_name"])

# Afficher les résultats

# Auteurs manquants
print("\nAuteurs présents dans 'books' mais absents de 'authors' :")
for author in missing_authors:
    print(author)

# Nombre d'auteurs manquants
print("\nNombre d'auteurs manquants :", len(missing_authors))

# Auteurs associés à plusieurs identifiants
print("\nAuteurs associés à plusieurs identifiants (doublons dans 'author_name') :")
print(duplicate_names[['author_id', 'author_name']])

# Doublons dans 'author_id'
print("\nDoublons dans 'author_id' de authors :")
print(duplicates_in_author_id[['author_id', 'author_name']])

# Nombre d'auteurs uniques
print("\nNombre d'auteurs uniques dans 'authors' :", authors['normalized_author_name'].nunique())
print("Nombre d'auteurs uniques dans 'books' :", books['normalized_author'].nunique())

# Auteurs ayant plusieurs noms associés (homonymes)
authors_with_multiple_names = authors[authors.duplicated(subset=['author_id'], keep=False)]
print("\nAuteurs avec plusieurs noms associés (homonymes) :")
print(authors_with_multiple_names[['author_id', 'author_name']])
