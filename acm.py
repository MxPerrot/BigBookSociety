import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mca import MCA

def getHistoricEra(date):
    """
    Renvoie la période d'histoire à partir de la date en string
    """
    if type(date) == float:
        try:
            numDecennie = int(date // 10)
            if numDecennie < 149:
                return "Antiquity & Middle Ages"
            elif numDecennie < 178:
                return "Modern Age"
            elif numDecennie < 190:
                return "Contemporary times"
            elif numDecennie < 200:
                return "20th century"
            else:
                return "21th century"
        except:
            return "Unknown"
    else:
        return "Unknown"

def ajoutEpoque(df):
    df["epoque"] = df.date_published.apply(getHistoricEra)
    return df

def getGenre(genresWithVotes): 
    """
    Récupère le nom du genre simplifié à partir de la liste des genres avec leurs votes
    ex : "Poetry-Lyricism 741, Childrens 402, Classics-Greek 259, Fiction 87" => "Poetry"
    """
    if not pd.isna(genresWithVotes):
        genreWithVotes = genresWithVotes.split(",")[0]
        genre = genreWithVotes.split(" ")[0]
        singularGenre = genre.split("-")[0]
        return singularGenre
    else:
        return "None"

def ajoutGenre(df):
    df["genre"] = df.genre_and_votes.apply(getGenre)
    return df

# Chargement des données
data = pd.read_csv("data/Cleaned_books.csv")
df = pd.DataFrame(data)

# Ajout des périodes d'histoire et des genres
df = ajoutEpoque(df)
df = ajoutGenre(df)

# Suppression des entrées sans genre et des périodes inconnues du dataframe
df = df[~df['genre'].isin(["None"])]
df = df[~df['epoque'].isin(["Inconnu"])]

# Suppression des genres les moins représentés
ComptesGenres = df['genre'].value_counts()
i=0
genresARetirer=[]
for genre in ComptesGenres.index:
    if i>7:
        genresARetirer.append(genre)
    i+=1
df = df[~df['genre'].isin(genresARetirer)]

# Paramétres de la génération du graphique
plotColorPeriods = "blue"
plotColorGenre = "orange"
label_offset = 0.1

# Analyse à Correspondances Multiples (MCA) sur les genres et les périodes d'histoire
dc = pd.DataFrame(pd.get_dummies(df[["genre", "epoque"]]))
mcaFic = MCA(dc, benzecri=False)
for i, j, nom in zip(mcaFic.fs_c()[:, 0], mcaFic.fs_c()[:, 1], dc.columns):
    # Séparation des genres et des périodes d'histoire par couleur
    if nom.split("_")[0] == "epoque":
        plt.scatter(i, j, c=plotColorPeriods)
    else:
        plt.scatter(i, j, c=plotColorGenre)
    plt.text(i+label_offset, j+label_offset, nom.split("_")[1])

# Ajout du titre et des légendes
plt.title("Multiple Correspondence Analysis")
plt.legend(handles=[ 
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=plotColorPeriods, markersize=10, label='Periods'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=plotColorGenre, markersize=10, label='Genre')
])

# Affichage du graphique
plt.show()