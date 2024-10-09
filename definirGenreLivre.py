import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

def main(show_graph=False):

    data = pd.read_csv("data/Cleaned_books.csv")
    df = pd.DataFrame(data)

    df = ajoutGenre(df)

    # -----------------------------------------------
    # Création du premier graphe camembert des genres
    # -----------------------------------------------

    df["Genres Plus Communs"] = df["genre"]

    # Récupère le nombre de chaque genre
    frequencies = df["Genres Plus Communs"].value_counts()

    # Remplace les noms de genre avec moins de 800 occurences par 'Other'
    condition = frequencies<=800
    mask_obs = frequencies[condition].index
    mask_dict = dict.fromkeys(mask_obs, "Other")
    df2 = df["Genres Plus Communs"].replace(mask_dict)

    # Retire les entrées sans genre
    df2 = df2[df2.str.contains("None") == False]

    df2 = df2.value_counts()

    # Crée le pie chart
    plt.rcParams['axes.titley'] = 1.0 
    plt.rcParams['axes.titlepad'] = 25
    plt.title("Most common genres")
    plt.pie(df2, labels=df2.index, rotatelabels=True)
    plt.savefig("./graphs/PieChart_MostCommonGenre", bbox_inches="tight")
    if show_graph:  plt.show()

    # ----------------------------------------------
    # Création du second graphe camembert des genres
    # ----------------------------------------------

    plt.clf()
    df["Genres Moins Communs"] = df["genre"]

    # Récupère le nombre de chaque genre
    frequencies = df["Genres Moins Communs"].value_counts()

    # Remplace les noms de genre avec plus de 800 occurences par 'To remove' pour qu'il puissent être aisément supprimés (celles déja présentes dans le premier graphe)
    conditionSup = 800 <= frequencies
    mask_obsSup = frequencies[conditionSup].index
    mask_dictSup = dict.fromkeys(mask_obsSup, "To Remove")
    df2 = df["Genres Moins Communs"].replace(mask_dictSup)

    # Remplace les noms de genre avec moins de 180 occurences par 'Other'
    conditionInf = frequencies <= 180
    mask_obsInf = frequencies[conditionInf].index
    mask_dictInf = dict.fromkeys(mask_obsInf, "Other")
    df2 = df2.replace(mask_dictInf)

    # Retire les entrées déja présentes dans le premier graphe
    df2 = df2[df2.str.contains("To Remove") == False]
    df2 = df2.value_counts()

    # Crée le pie chart
    plt.title("Less common genres")
    plt.pie(df2, labels=df2.index, rotatelabels=True)
    plt.savefig("./graphs/PieChart_LessCommonGenre", bbox_inches="tight")
    if show_graph:  plt.show()

if __name__ == "__main__":
    main()