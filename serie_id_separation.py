import pandas as pd

# Charger le fichier CSV
books = pd.read_csv("data/IGNOREME_Cleaned_books2.csv")

series = books['seriesName'].dropna().unique()

# Créer un DataFrame pour la table des séries avec un identifiant unique
series_table = pd.DataFrame({'seriesName': series})

# Ajouter un identifiant unique pour chaque série
series_table.index = series_table.index + 1 
series_table = series_table.reset_index(names=['id_series'])

# Exporter le DataFrame des séries en CSV
series_table.to_csv("./SQL/series.csv", index=False)
