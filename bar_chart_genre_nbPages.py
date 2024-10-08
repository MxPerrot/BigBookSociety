import pandas as pd
import matplotlib.pyplot as plt

def definir_genre(df):
    def getGenre(genresWithVotes): 
        if not pd.isna(genresWithVotes):
            genreWithVotes = genresWithVotes.split(',')[0]
            genre = genreWithVotes.split(' ')[0] 
            return genre
        else:
            return "None"

    df['genre'] = df.genre_and_votes.apply(getGenre)
    return df

# Lecture des données CSV
data = pd.read_csv('./data/Cleaned_books.csv')

# Définir le genre pour chaque livre
data = definir_genre(data)

# Enlever livres avec nb pages inférieur à zéro
data = data[data['number_of_pages'] > 0]

# Moyenne du nombre de pages par genre
moyennePagesGenre = data.groupby('genre')['number_of_pages'].mean().reset_index()

# Compter le nombre de livres par genre
nombreLivresParGenre = data['genre'].value_counts().reset_index()
nombreLivresParGenre.columns = ['genre', 'nombre_de_livres']

# Fusionner les deux DataFrames sur le genre
resultat = pd.merge(moyennePagesGenre, nombreLivresParGenre, on='genre')

# Trier les genres en fonction de la moyenne du nombre de pages en ordre décroissant
resultat = resultat.sort_values(by='number_of_pages', ascending=False)

# Limite l'affichage à 40 genres pour éviter un graphique trop chargé
num_genres_to_display = 400  
top_genres = resultat.head(num_genres_to_display)

# Ajout de couleurs
colors = plt.cm.get_cmap('tab20', num_genres_to_display).colors  

# Affichage des résultats dans le terminal
for index, row in resultat.iterrows():
    print(f"Genre: {row['genre']}, Moyenne de pages: {row['number_of_pages']:.2f}, Nombre de livres: {row['nombre_de_livres']}")

# Bar chart
plt.figure(figsize=(12, 6))
bars = plt.bar(top_genres['genre'], top_genres['number_of_pages'], color=colors)
plt.xlabel('Genre')
plt.ylabel('Nombre moyen de pages')
plt.title('Nombre moyen de pages par genre')
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.subplots_adjust(bottom=0.3)
plt.tight_layout()
plt.show()
