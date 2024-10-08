import pandas as pd
import matplotlib.pyplot as plt

# Lecture CSV
data = pd.read_csv('./data/Cleaned_books.csv')

# Calcul de la moyenne des pages par genre
moyennePagesGenre = data.groupby('genre_and_votes')['number_of_pages'].mean().reset_index()

# Trie les genres par moyenne du nombre de pages en ordre décroissant
moyennePagesGenre = moyennePagesGenre.sort_values(by='number_of_pages', ascending=False)

# On limite l'affichage à 20 genres pour ne pas surcharger le graphique
num_genres_to_display = 20  
top_genres = moyennePagesGenre.head(num_genres_to_display)

colors = plt.cm.get_cmap('tab20', num_genres_to_display).colors  

# Affichage des genres et de leur moyenne de pages dans le terminal
for index, row in moyennePagesGenre.iterrows():
    print(f"Genre: {row['genre_and_votes']}, Moyenne de pages: {row['number_of_pages']:.2f}")

# Création du graphique en barres avec les couleurs
plt.figure(figsize=(12, 6))
plt.bar(top_genres['genre_and_votes'], top_genres['number_of_pages'], color=colors)
plt.xlabel('Genre')
plt.ylabel('Nombre moyen de pages')
plt.title('Nombre moyen de pages par genre')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
