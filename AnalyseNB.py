import pandas as pd
import matplotlib.pyplot as plt

file_path = './data/Cleaned_books.csv'
df = pd.read_csv(file_path)

if 'average_rating' in df.columns and 'number_of_pages' in df.columns and 'rating_count' in df.columns:
    
    df_filtered = df[(df['number_of_pages'] <= 1500) & (df['average_rating'] >= 2)]

    plt.figure(figsize=(10, 6))
    
    sizes = df_filtered['rating_count'] / df_filtered['rating_count'].max() * 200  # Ajuster les tailles pour ne pas être trop gros
    colors = df_filtered['average_rating']  # Utilisation d'une échelle de couleur basée sur la note moyenne

    scatter = plt.scatter(df_filtered['average_rating'], df_filtered['number_of_pages'], 
                          s=sizes, alpha=0.6, linewidth=0.5, c=colors, cmap='coolwarm', edgecolor='black')

    plt.grid(True, which='both', linestyle='--', linewidth=0.3)

    plt.title('Nuage de points: Note moyenne vs Nombre de pages (Taille: Nombre de notes)', fontsize=14)
    plt.xlabel('Note moyenne (average_rating)', fontsize=12)
    plt.ylabel('Nombre de pages (number_of_pages)', fontsize=12)

    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    plt.xlim(2, df_filtered['average_rating'].max() + 0.5)
    plt.ylim(df_filtered['number_of_pages'].min() - 50, df_filtered['number_of_pages'].max() + 50)

    plt.colorbar(scatter, label='Note moyenne')

    plt.tight_layout()

    plt.show()

else:
    print("Les colonnes 'average_rating', 'number_of_pages' et 'rating_count' ne sont pas présentes dans le fichier.")
