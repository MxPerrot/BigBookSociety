import pandas as pd

# Charger le fichier CSV et récupérer uniquement les colonnes souhaitées
df = pd.read_csv('data/Cleaned_books2.csv', usecols=['awardDate', 'awardName'], dtype={
    'awardDate': 'Int32'
    })

df = df.drop_duplicates()

# Ajouter une colonne 'id_prix' unique pour chaque ligne
df['id_prix'] = range(1, len(df) + 1)

# Supprimer les lignes où 'awardDate' ou 'awardName' est manquant
df = df.dropna(subset=['awardName'])

# Renommer les colonnes
df = df.rename(columns={'awardDate': 'annee_prix', 'awardName': 'nom_prix'})

# Réorganiser les colonnes : 'id_prix' en premier, puis 'nom_prix' et 'annee_prix'
df = df[['id_prix', 'nom_prix', 'annee_prix']]

# Enregistrer le DataFrame dans le fichier SQL/prix.csv
df.to_csv('SQL/prix.csv', index=False)
