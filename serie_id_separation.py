import pandas as pd

# Charger le fichier CSV
books = pd.read_csv("data/IGNOREME_Cleaned_books2.csv", dtype={
    'episodeNumber': 'Int32'})

series = books['seriesName'].dropna().unique()

# Créer un DataFrame pour la table des séries avec un identifiant unique
series_table = pd.DataFrame({'seriesName': series})

# Ajouter un identifiant unique pour chaque série
series_table.index = series_table.index + 1 
series_table = series_table.reset_index(names=['id_serie'])
series_table = series_table.rename(columns={"seriesName": "nom_serie"})

# Exporter le DataFrame des séries en CSV
series_table.to_csv("./SQL/series.csv", index=False)


episodeData = pd.merge(books, series_table, left_on='seriesName', right_on="nom_serie", how='inner')

episodeData = episodeData[['id_serie','id','episodeNumber']]

print(episodeData)
