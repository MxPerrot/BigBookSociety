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

# Supprimer les doublons en conservant uniquement les lignes uniques de 'awardDate' et 'awardName'
df = df.drop_duplicates(subset=['awardDate', 'awardName'])

# Ajouter une colonne 'id_prix' unique pour chaque ligne après suppression des doublons
df['id_prix'] = range(1, len(df) + 1)

# Renommer les colonnes pour le fichier prix.csv
df = df.rename(columns={'awardDate': 'annee_prix', 'awardName': 'nom_prix'})

# Réorganiser les colonnes : 'id_prix' en premier, puis 'nom_prix' et 'annee_prix'
df = df[['id_prix', 'nom_prix', 'annee_prix']]

# Enregistrer le DataFrame dans le fichier SQL/prix.csv
df.to_csv('SQL/prix.csv', index=False)

# --- Suite du script pour générer prix_livre.csv ---

# Charger de nouveau les données avec la colonne 'id' pour créer les relations prix-livre
df_livres = pd.read_csv('data/IGNOREME_Cleaned_books2.csv', usecols=['id', 'awardName', 'awardDate'])

# Convertir les colonnes 'awardDate' et 'annee_prix' en int pour éviter les problèmes de fusion
df_livres['awardDate'] = df_livres['awardDate'].astype('Int32')
df['annee_prix'] = df['annee_prix'].astype('Int32')

# Associer chaque livre au prix correspondant en effectuant une fusion sur 'awardName' et 'awardDate'
df_prix_livre = pd.merge(df_livres, df, left_on=['awardName', 'awardDate'], right_on=['nom_prix', 'annee_prix'])

# Garder uniquement les colonnes nécessaires pour la table _prix_livre
df_prix_livre = df_prix_livre[['id_prix', 'id']].dropna()

# Renommer la colonne 'id' en 'id_livre'
df_prix_livre = df_prix_livre.rename(columns={'id': 'id_livre'})

# Supprimer les doublons dans le DataFrame
df_prix_livre = df_prix_livre.drop_duplicates()

# Enregistrer le DataFrame final dans un fichier CSV
df_prix_livre.to_csv('SQL/prix_livre.csv', index=False)
