import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/Cleaned_books.csv")
df = pd.DataFrame(data)

#print(df["genre_and_votes"])

df["genre_and_votes"]

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
print(df['genre'])