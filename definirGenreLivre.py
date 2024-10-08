import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/Cleaned_books.csv")
df = pd.DataFrame(data)

def getGenre(genresWithVotes): 
    #print(f"GenresBefore: {rawGenres}")
    if not pd.isna(genresWithVotes):
        genreWithVotes = genresWithVotes.split(',')[0]
        #print(f"Genres: {genres[0]}") 
        genre = genreWithVotes.split(' ')[0]
        #print(f"Genres: {genre[0]}") 
        return genre
    else:
        return "None"


df['genre'] = df.genre_and_votes.apply(getGenre)
# print(df['genre'].value_counts().to_string())


df['genre1'] = df['genre']
frequencies = df['genre1'].value_counts()

condition = frequencies<=800
mask_obs = frequencies[condition].index
mask_dict = dict.fromkeys(mask_obs, 'Other')
df2 = df['genre1'].replace(mask_dict)
df2 = df2[df2.str.contains("None") == False]

df2.value_counts().plot.pie(rotatelabels=True)
plt.show()

plt.clf()
df['genre2'] = df['genre']
frequencies = df['genre2'].value_counts()

condition1 = 800 <= frequencies
mask_obs1 = frequencies[condition1].index
mask_dict1 = dict.fromkeys(mask_obs1, 'Bigger')

condition2 = frequencies <= 180
mask_obs2 = frequencies[condition2].index
mask_dict2 = dict.fromkeys(mask_obs2, 'Other')

df2 = df['genre2'].replace(mask_dict1)
df2 = df2.replace(mask_dict2)
df2 = df2[df2.str.contains("Bigger") == False]

df2.value_counts().plot.pie(rotatelabels=True)
plt.show()