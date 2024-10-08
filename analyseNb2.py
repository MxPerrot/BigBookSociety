import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = './data/Cleaned_books.csv'
df = pd.read_csv(file_path)

def definir_genre(df):
    def getGenre(genresWithVotes): 
        if not pd.isna(genresWithVotes):
            genreWithVotes = genresWithVotes.split(',')[0]
            genre = genreWithVotes.split(' ')[0] 
            return genre
        else:
            return "None"

    df['genre'] = df['genre_and_votes'].apply(getGenre)
    return df

df = definir_genre(df)

if 'average_rating' in df.columns and 'genre' in df.columns:
    
    df_filtered = df[(df['average_rating'] >= 2) & (df['number_of_pages'] <= 1500)]
    
    genre_stats = df_filtered.groupby('genre').agg(
        average_rating=('average_rating', 'mean'),
        book_count=('average_rating', 'size')
    ).reset_index()
    
    genre_stats = genre_stats.sort_values(by='book_count', ascending=False).head(50)
    
    genre_stats = genre_stats.sort_values(by='average_rating', ascending=True)

    fig, ax1 = plt.subplots(figsize=(16, 8))

    colors = plt.cm.viridis(np.linspace(0, 1, len(genre_stats)))

    bars = ax1.bar(genre_stats['genre'], genre_stats['book_count'], color=colors, label='Number of books', alpha=0.7)
    
    plt.xticks(rotation=45, ha="right", fontsize=10)

    ax2 = ax1.twinx()  
    ax2.plot(genre_stats['genre'], genre_stats['average_rating'], marker='o', linestyle='-', color='b', label='Average rating')
    
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=10)
    
    ax1.set_title('Average rating and number of books by gender (Top 50)', fontsize=16)
    ax1.set_xlabel('Genre', fontsize=14)
    ax1.set_ylabel('Number of books', fontsize=14)
    ax2.set_ylabel('Average rating', fontsize=14)

    ax1.tick_params(axis='y', labelcolor='gray', labelsize=12)
    ax2.tick_params(axis='y', labelcolor='blue', labelsize=12)

    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

else:
    print("Les colonnes 'average_rating' et 'genre' ne sont pas présentes dans le fichier.")
