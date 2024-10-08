import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
moyennePagesGenre = data.groupby('genre')['number_of_pages'].agg(['mean', 'count', 'std']).reset_index()
moyennePagesGenre.columns = ['genre', 'mean_pages', 'count', 'std_pages']

# Calcul de l'intervalle de confiance à 95%
moyennePagesGenre['conf_int'] = 1.96 * (moyennePagesGenre['std_pages'] / np.sqrt(moyennePagesGenre['count']))

# Compter le nombre de livres par genre
nombreLivresParGenre = data['genre'].value_counts().reset_index()
nombreLivresParGenre.columns = ['genre', 'nombre_de_livres']

# Fusionner les deux DataFrames sur le genre
resultat = pd.merge(moyennePagesGenre, nombreLivresParGenre, on='genre')

# Trier les genres par nombre de livres en ordre décroissant
resultat_par_nombre_livres = resultat.sort_values(by='nombre_de_livres', ascending=False)

# Limite l'affichage à 40 genres pour éviter un graphique trop chargé
num_genres_to_display = 40  
top_genres_nombre_livres = resultat_par_nombre_livres.head(num_genres_to_display)

# Ajout de couleurs
colors_nombre_livres = plt.cm.get_cmap('tab20', num_genres_to_display).colors

# Affichage des résultats dans le terminal
print("Affichage trié par nombre de livres :")
for index, row in resultat_par_nombre_livres.iterrows():
    print(f"Genre: {row['genre']}, Moyenne de pages: {row['mean_pages']:.2f}, Nombre de livres: {row['nombre_de_livres']}")

# Graphique pour le nombre moyen de pages par genre (trié par nombre de livres)
plt.figure(figsize=(12, 6))
bars = plt.bar(top_genres_nombre_livres['genre'], top_genres_nombre_livres['mean_pages'], 
                yerr=top_genres_nombre_livres['conf_int'], color=colors_nombre_livres, capsize=5)

# Annotation pour le nombre de livres sur chaque barre, légèrement au-dessus de l'intervalle de confiance
for bar, nombre, conf in zip(bars, top_genres_nombre_livres['nombre_de_livres'], top_genres_nombre_livres['conf_int']):
    pos_x = bar.get_x() + bar.get_width() / 2
    pos_y = bar.get_height() + conf + 0.5  # Positionne au-dessus de l'intervalle de confiance
    
    # Vérifiez si pos_y et pos_x sont des valeurs finies
    if np.isfinite(pos_y) and np.isfinite(pos_x):
        plt.text(pos_x, pos_y, str(nombre), ha='center', va='bottom', fontsize=10)

plt.xlabel('Genre')
plt.ylabel('Nombre moyen de pages')
plt.title('Nombre moyen de pages par genre (trié par nombre de livres)')
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.subplots_adjust(bottom=0.3)
plt.tight_layout()
plt.show()

# Trier les genres par moyenne du nombre de pages en ordre décroissant
resultat_par_moyenne_pages = resultat.sort_values(by='mean_pages', ascending=False)

# Limite l'affichage à 40 genres pour éviter un graphique trop chargé
top_genres_moyenne_pages = resultat_par_moyenne_pages.head(num_genres_to_display)

# Ajout de couleurs variées pour le second graphique
colors_moyenne_pages = plt.cm.get_cmap('tab20', num_genres_to_display).colors

# Affichage des résultats dans le terminal
print("\nAffichage trié par moyenne de pages :")
for index, row in resultat_par_moyenne_pages.iterrows():
    print(f"Genre: {row['genre']}, Moyenne de pages: {row['mean_pages']:.2f}, Nombre de livres: {row['nombre_de_livres']}")

# Graphique pour le nombre moyen de pages par genre (trié par moyenne de pages)
plt.figure(figsize=(12, 6))
bars_moyenne = plt.bar(top_genres_moyenne_pages['genre'], top_genres_moyenne_pages['mean_pages'], 
                        yerr=top_genres_moyenne_pages['conf_int'], color=colors_moyenne_pages, capsize=5)

# Annotation pour le nombre de livres sur chaque barre, légèrement au-dessus de l'intervalle de confiance
for bar, nombre, conf in zip(bars_moyenne, top_genres_moyenne_pages['nombre_de_livres'], top_genres_moyenne_pages['conf_int']):
    pos_x = bar.get_x() + bar.get_width() / 2
    pos_y = bar.get_height() + conf + 0.5  # Positionne au-dessus de l'intervalle de confiance

    # Vérifiez si pos_y et pos_x sont des valeurs finies
    if np.isfinite(pos_y) and np.isfinite(pos_x):
        plt.text(pos_x, pos_y, str(nombre), ha='center', va='bottom', fontsize=10)

plt.xlabel('Genre')
plt.ylabel('Nombre moyen de pages')
plt.title('Nombre moyen de pages par genre (trié par moyenne de pages)')
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.subplots_adjust(bottom=0.3)
plt.tight_layout()
plt.show()
