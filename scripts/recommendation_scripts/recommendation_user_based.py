import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Connexion à la base de données
connexion = psycopg2.connect(
    database=os.getenv("DATABASE_NAME"),
    user=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    port=os.getenv("PORT")
)

# Récupération des données depuis la base
curseur = connexion.cursor()
curseur.execute("SELECT id_livre, titre, description FROM sae._livre;")
livres = curseur.fetchall()

# Fermeture de la connexion à la base de données
curseur.close()
connexion.close()

# Conversion des données des livres en DataFrame
livres_df = pd.DataFrame(livres, columns=['id_livre', 'titre', 'description'])

# Création d'une matrice TF-IDF basée sur les descriptions des livres
tfidf = TfidfVectorizer(stop_words='french')
tfidf_matrix = tfidf.fit_transform(livres_df['description'].fillna(''))

# Calcul de la similarité cosinus entre les livres
similarite_livres = cosine_similarity(tfidf_matrix)

# Fonction de recommandation basée sur le contenu
def recommander_livres(id_livre, top_n=5):
    # Vérification si l'ID du livre est valide
    if id_livre not in livres_df['id_livre'].values:
        return []

    # Trouver l'index du livre dans le DataFrame
    index_livre = livres_df[livres_df['id_livre'] == id_livre].index[0]

    # Récupérer les scores de similarité pour ce livre
    scores = list(enumerate(similarite_livres[index_livre]))

    # Trier les scores par similarité décroissante
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Récupérer les IDs des livres les plus similaires (hors lui-même)
    livres_similaires = [livres_df.iloc[i]['id_livre'] for i, score in scores[1:top_n + 1]]

    # Récupérer les titres des livres similaires
    titres_recommandes = livres_df[livres_df['id_livre'].isin(livres_similaires)]['titre'].tolist()
    return titres_recommandes

# Exemple : recommander des livres similaires au livre avec ID 1
id_livre = 1
recommandations = recommander_livres(id_livre)
print(f"Recommandations pour le livre {id_livre} : {recommandations}")
