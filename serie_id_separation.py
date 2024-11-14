import pandas as pd

# Charger le fichier CSV
books = pd.read_csv("data/Cleaned_books2.csv")

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

episodeData = episodeData.rename(columns={"id": "id_livre"})
episodeData = episodeData.rename(columns={"episodeNumber": "numero_episode"})

episodeData.to_csv("./SQL/episode_serie.csv", index=False)