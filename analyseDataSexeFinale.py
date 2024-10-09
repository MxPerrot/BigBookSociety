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

    # Get the data from the CSV files
    data = pd.read_csv("data/Cleaned_authors.csv")
    df = pd.DataFrame(data)

    # Simplify the genres
    df = ajoutGenre(df)

    # Drop duplicate authors
    df = df.drop_duplicates(subset=['author_name'])

    # Count the number of authors for each genre
    nbrValueCount = df["genre"].value_counts()

    # Get the top 15 genres with the most authors
    listeGenrePlusPop = []
    for i in range(0,15):
        listeGenrePlusPop.append(nbrValueCount.index[i])

    # Seperate authors by gender in variable for later, actual separation done later
    dfHommeFullFrame=df
    dfFemmeFullFrame=df

    # Separate authors by gender in the dataframes
    dfHommeFullFrame = dfHommeFullFrame.drop(dfHommeFullFrame[dfHommeFullFrame['author_gender']=='male'].index)
    dfHommeFullFrame = dfHommeFullFrame.drop(dfHommeFullFrame[dfHommeFullFrame['author_gender']=='female'].index)  


    # Create dataframes for the percentage of authors by genre for each gender
    dfHomme = pd.DataFrame(columns=['genre', 'pourcentageSexe'])
    dfFemme = pd.DataFrame(columns=['genre', 'pourcentageSexe'])



    # Calculate the percentage of authors by genre for each gender
    for i in listeGenrePlusPop:
        # Get the number of authors by genre for each gender
        i_value_homme = dfHommeFullFrame["genre"].value_counts()
        i_value_femme = dfFemmeFullFrame["genre"].value_counts()
        # Try to calculate the percentages of authors by genre for each gender
        try:
            if(i_value_femme[i]!=0):
                dfHomme.loc[len(dfHomme.index)] = [i, i_value_homme[i]/(i_value_homme[i] + i_value_femme[i])*100] 
                dfFemme.loc[len(dfFemme.index)] = [i, i_value_femme[i]/(i_value_homme[i] + i_value_femme[i])*100] 
            else:
                dfHomme.loc[len(dfHomme.index)] = [i, 100] 
                dfFemme.loc[len(dfFemme.index)] = [i, 0]
        # Catch exceptions when a genre doesn't exist in one gender's data
        except:
            if(i not in i_value_femme):
                # If the genre doesn't exist in the female's data, assume 0% of the female's authors are in the genre and 100% of male are
                dfHomme.loc[len(dfHomme.index)] = [i, 100] 
                dfFemme.loc[len(dfFemme.index)] = [i, 0]
            else:
                # If the genre doesn't exist in the male's data, assume 0% of the male's authors are in the genre and 100% of female are
                dfHomme.loc[len(dfHomme.index)] = [i, 0] 
                dfFemme.loc[len(dfFemme.index)] = [i, 100]

    # Plot the bar chart
    N = len(dfHomme)
    ind = np.arange(N)
    width = 0.35

    fig, ax = plt.subplots(figsize =(10, 7))
    p1 = ax.bar(ind, dfHomme['pourcentageSexe'], width)
    p2 = ax.bar(ind, dfFemme['pourcentageSexe'], width, bottom = dfHomme['pourcentageSexe'])

    ax.set_ylabel('Percentage of authors which are men or women')
    ax.set_title('The 12 most popular genres of authors divided by the ratio of each sex writing them')
    ax.set_xticks(ind)
    ax.set_xticklabels(dfHomme['genre'])
    ax.set_yticks(np.arange(0, 81, 10))
    ax.set_yticks(np.arange(0, 101, 10))
    ax.legend((p1[0], p2[0]), ('Men', 'Women'))

    plt.setp(ax.get_xticklabels(), rotation=20, ha="right", rotation_mode="anchor")
    plt.savefig("./graphs/BarChart_PopularGenreByAuthorGenre", bbox_inches="tight")
    plt.clf()
    if show_graph: plt.show()


    # First pie chart for male authors

    # Change the font size and style for the labels later on
    font = {'family' : 'normal',
            'size'   : 15}
    matplotlib.rc('font', **font)

    # Creates a variable to store the number of male authors for each genre
    dfNbrHomme = pd.DataFrame(columns=['genre', 'nbr'])

    # Get the top 15 genres with the most male authors
    nbrValueCount = dfHommeFullFrame["genre"].value_counts()
    listeGenrePlusPopHomme = []
    for i in range(0,15):
        listeGenrePlusPopHomme.append(nbrValueCount.index[i])

    # Calculate the number of male authors for each of the popular genre
    for i in listeGenrePlusPopHomme:
        dfNbrHomme.loc[len(dfNbrHomme.index)] = [i, nbrValueCount[i]] 

    # Calculate the number of male authors for genres that are not in the top 15
    tot=0
    for i in dfHommeFullFrame["genre"].value_counts().index:
        print(i)
        if (i not in listeGenrePlusPopHomme):
            tot = tot + nbrValueCount[i]

    # Sort the dataframe by the number of male authors in descending order
    dfNbrHomme = dfNbrHomme.sort_values("nbr", ascending=False)

    # Add a new row to the dataframe for the other genres that are not in the top 15
    dfNbrHomme.loc[len(dfNbrHomme.index)] = ["others", tot] 

    # Create a pie chart for male authors
    plt.pie(dfNbrHomme['nbr'], labels=dfNbrHomme['genre'], rotatelabels=True)
    plt.rcParams['axes.titley'] = 1.0 
    plt.rcParams['axes.titlepad'] = 25
    plt.title('The 12 Main genres of Male authors')
    plt.savefig("./graphs/PieChart_MenAuthorGenreInterest", bbox_inches="tight")
    plt.clf()
    if show_graph: plt.show()









    # Second pie chart for female authors

    # Create a variable to store the number of female authors for each genre
    dfNbrFemme = pd.DataFrame(columns=['genre', 'nbr'])

    # Calculate the number of female authors for each genre
    nbrValueCount = dfFemmeFullFrame["genre"].value_counts()

    # Get the top 15 genres with the most female authors
    listeGenrePlusPopFemme = []
    for i in range(0,15):
        listeGenrePlusPopFemme.append(nbrValueCount.index[i])

    # Calculate the number of female authors for each of the popular genre
    for i in listeGenrePlusPopFemme:
        dfNbrFemme.loc[len(dfNbrFemme.index)] = [i, nbrValueCount[i]] 

    # Calculate the number of female authors for genres that are not in the top 15
    tot=0
    for i in dfFemmeFullFrame["genre"].value_counts().index:
        print(i)
        if (i not in listeGenrePlusPopFemme):
            tot = tot + nbrValueCount[i]

    # Sort the dataframe by the number of female authors in descending order
    dfNbrFemme = dfNbrFemme.sort_values("nbr", ascending=False)

    # Add a new row to the dataframe for the other genres that are not in the top 15
    dfNbrFemme.loc[len(dfNbrFemme.index)] = ["others", tot] 

    # Create a pie chart for female authors
    plt.pie(dfNbrFemme['nbr'], labels=dfNbrFemme['genre'], rotatelabels=True)
    plt.rcParams['axes.titley'] = 1.0 
    plt.rcParams['axes.titlepad'] = 25
    plt.title('The 12 Main genres of Female authors')
    plt.savefig("./graphs/PieChart_WomenAuthorGenreInterest", bbox_inches="tight")
    plt.clf()
    if show_graph: plt.show()


if __name__ == "__main__":
    main(show_graph=False)




