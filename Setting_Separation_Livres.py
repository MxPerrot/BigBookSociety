import pandas as pd
import numpy as np

books = pd.read_csv("data/Cleaned_books2.csv")

countries = books['settingCountry'].unique()

countries = countries[~pd.isnull(countries)]

# Création dataframe pour la table pays
dataset = pd.DataFrame({'nom': countries})

dataset.index = dataset.index+1

dataset = dataset.reset_index(names=['id_pays'])
dataset.to_csv("./SQL/pays.csv", index=False)

#Création lien auteur-genre
paysSetting = pd.merge(books, dataset, left_on='settingCountry', right_on="nom", how='inner')
paysSetting = paysSetting.drop(columns=['seriesName','episode'])
print(paysSetting)


