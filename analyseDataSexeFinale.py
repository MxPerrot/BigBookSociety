import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
Path("./graphs").mkdir(parents=True, exist_ok=True)



def getGenre(genres): 
    """
    Récupère le nom du genre simplifié à partir de la liste des genres avec leurs votes
    ex : "Poetry-Lyricism 741, Childrens 402, Classics-Greek 259, Fiction 87" => "Poetry"
    """
    if not pd.isna(genres):
        genre = genres.split(",")[0]
        singularGenre = genre.split("-")[0]
        return singularGenre
    else:
        return "None"

def ajoutGenre(df):
    df["genre"] = df.author_genres.apply(getGenre)
    return df

def main(show_graph=False):

    data = pd.read_csv("data/Cleaned_authors.csv")
    df = pd.DataFrame(data)


    df = ajoutGenre(df)

    df = df.drop_duplicates(subset=['author_name'])

    nbrValueCount = df["genre"].value_counts()

    listeGenrePlusPop = []
    for i in range(0,15):
        listeGenrePlusPop.append(nbrValueCount.index[i])

    dfTestHomme=df
    dfTestFemme=df

    dfTestHomme = dfTestHomme.drop(dfTestHomme[dfTestHomme['author_gender']=='female'].index)  

    dfTestFemme = dfTestFemme.drop(dfTestFemme[dfTestFemme['author_gender']=='male'].index)  





    dfHomme = pd.DataFrame(columns=['genre', 'pourcentageSexe'])

    dfFemme = pd.DataFrame(columns=['genre', 'pourcentageSexe'])




    for i in listeGenrePlusPop:
        i_value_homme = dfTestHomme["genre"].value_counts()
        i_value_femme = dfTestFemme["genre"].value_counts()
        try:
            if(i_value_femme[i]!=0):
                dfHomme.loc[len(dfHomme.index)] = [i, i_value_homme[i]/(i_value_homme[i] + i_value_femme[i])*100] 
                dfFemme.loc[len(dfFemme.index)] = [i, i_value_femme[i]/(i_value_homme[i] + i_value_femme[i])*100] 
            else:
                dfHomme.loc[len(dfHomme.index)] = [i, 100] 
                dfFemme.loc[len(dfFemme.index)] = [i, 0]
        except:
            if(i not in i_value_femme):
                dfHomme.loc[len(dfHomme.index)] = [i, 100] 
                dfFemme.loc[len(dfFemme.index)] = [i, 0]
            else:
                dfHomme.loc[len(dfHomme.index)] = [i, 0] 
                dfFemme.loc[len(dfFemme.index)] = [i, 100]

    # fig = plt.figure(figsize = (10, 5))

    # # creating the bar plot
    # plt.bar(dfHomme['genre'], dfHomme['pourcentageSexe'], color ='maroon', width = 0.4)

    # plt.xlabel("Genre Littéraire")
    # plt.ylabel("Pourcentage d'Homme/Femme")
    # plt.title("Genre littéraire en fonction du pourcentage d'homme et de femmes écrivant dans celui-ci")
    # plt.show()

    N = len(dfHomme)
    ind = np.arange(N)
    width = 0.35

    fig, ax = plt.subplots(figsize =(10, 7))
    p1 = ax.bar(ind, dfHomme['pourcentageSexe'], width)
    p2 = ax.bar(ind, dfFemme['pourcentageSexe'], width, bottom = dfHomme['pourcentageSexe'])

    ax.set_ylabel('Percentage of authors which are men or women')
    ax.set_title('The 12 most popular genre of authors divided by the percentage of each sex writing them')
    ax.set_xticks(ind)
    ax.set_xticklabels(dfHomme['genre'])
    ax.set_yticks(np.arange(0, 81, 10))
    ax.set_yticks(np.arange(0, 101, 10))
    ax.legend((p1[0], p2[0]), ('Men', 'Women'))

    plt.setp(ax.get_xticklabels(), rotation=20, ha="right", rotation_mode="anchor")
    plt.savefig("./graphs/BarChart_PopularGenreByAuthorGenre", bbox_inches="tight")
    if show_graph: plt.show()

    # https://www.geeksforgeeks.org/bar-plot-in-matplotlib/


    font = {'family' : 'normal',
            'size'   : 15}
    matplotlib.rc('font', **font)


    dfNbrHomme = pd.DataFrame(columns=['genre', 'nbr'])

    nbrValueCount = dfTestHomme["genre"].value_counts()

    listeGenrePlusPopHomme = []
    for i in range(0,15):
        listeGenrePlusPopHomme.append(nbrValueCount.index[i])

    #Nbr Homme

    for i in listeGenrePlusPopHomme:
        dfNbrHomme.loc[len(dfNbrHomme.index)] = [i, nbrValueCount[i]] 

    tot=0
    for i in dfTestHomme["genre"].value_counts().index:
        print(i)
        if (i not in listeGenrePlusPopHomme):
            tot = tot + nbrValueCount[i]

    dfNbrHomme = dfNbrHomme.sort_values("nbr", ascending=False)

    dfNbrHomme.loc[len(dfNbrHomme.index)] = ["others", tot] 


    plt.pie(dfNbrHomme['nbr'], labels=dfNbrHomme['genre'], rotatelabels=True)
    plt.rcParams['axes.titley'] = 1.0 
    plt.rcParams['axes.titlepad'] = 25
    plt.title('The 12 Main genre of Male authors')
    plt.savefig("./graphs/PieChart_MenAuthorGenreInterest", bbox_inches="tight")
    if show_graph: plt.show()











    dfNbrFemme = pd.DataFrame(columns=['genre', 'nbr'])

    nbrValueCount = dfTestFemme["genre"].value_counts()

    listeGenrePlusPopFemme = []
    for i in range(0,15):
        listeGenrePlusPopFemme.append(nbrValueCount.index[i])

    #Nbr Femme
    for i in listeGenrePlusPopFemme:
        dfNbrFemme.loc[len(dfNbrFemme.index)] = [i, nbrValueCount[i]] 
    tot=0
    for i in dfTestFemme["genre"].value_counts().index:
        print(i)
        if (i not in listeGenrePlusPopFemme):
            tot = tot + nbrValueCount[i]

    dfNbrFemme = dfNbrFemme.sort_values("nbr", ascending=False)

    dfNbrFemme.loc[len(dfNbrFemme.index)] = ["others", tot] 

    plt.pie(dfNbrFemme['nbr'], labels=dfNbrFemme['genre'], rotatelabels=True)
    plt.rcParams['axes.titley'] = 1.0 
    plt.rcParams['axes.titlepad'] = 25
    plt.title('The 12 Main genre of Female authors')
    plt.savefig("./graphs/PieChart_WomenAuthorGenreInterest", bbox_inches="tight")
    if show_graph: plt.show()


if __name__ == "__main__":
    main(show_graph=False)




