import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# Lecture des données
data = pd.read_csv('./data/Cleaned_books.csv')

data = data.dropna(subset=['genre_and_votes', 'number_of_pages'])

data['genre_and_votes'] = data['genre_and_votes'].apply(lambda x: re.sub(r'\s*\d+\s*', '', x).strip())

data = data.assign(genres=data['genre_and_votes'].str.split(',')).explode('genres')

data['genres'] = data['genres'].str.strip()

num_categories = data['genres'].nunique()
print(f"Number of unique genres: {num_categories}")

avg_pages_per_genre = data.groupby('genres')['number_of_pages'].mean().reset_index()

avg_pages_per_genre = avg_pages_per_genre.sort_values(by='number_of_pages', ascending=False)


num_genres_to_display = 20  
top_genres = avg_pages_per_genre.head(num_genres_to_display)


# Bar chart
plt.figure(figsize=(12, 6))
plt.bar(top_genres['genres'], top_genres['number_of_pages'])
plt.xlabel('Genre')
plt.ylabel('Average Number of Pages')
plt.title('Average Number of Pages by Genre')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
