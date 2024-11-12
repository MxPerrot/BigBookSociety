import pandas as pd

# Charger le fichier CSV
books = pd.read_csv("Big_book.csv")

series_names = books['series'].dropna().unique()

# Créer un DataFrame pour la table des séries avec un identifiant unique
series_table = pd.DataFrame({'series_name': series_names})

# Ajouter un identifiant unique pour chaque série
series_table.index = series_table.index + 1 
series_table = series_table.reset_index(names=['id_series'])

# Exporter le DataFrame des séries en CSV
series_table.to_csv("./SQL/series.csv", index=False)
