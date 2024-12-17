import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Connexion à la base de données PostgreSQL avec SQLAlchemy
def se_connecter_bdd():
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DATABASE_NAME')}"
        )
        print("Connexion réussie à la base de données.")
        return engine
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None

# Récupérer les genres préférés des utilisateurs
def recuperer_genres_utilisateur(engine):
    query = """
    SELECT id_utilisateur, id_genre
    FROM sae._utilisateur_genre
    """
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        print(f"Erreur lors de la récupération des genres utilisateurs : {e}")
        return pd.DataFrame()

# Récupérer les livres associés aux genres
def recuperer_livres_par_genre(engine):
    query = """
    SELECT id_livre, id_genre
    FROM sae._genre_livre
    """
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        print(f"Erreur lors de la récupération des livres par genre : {e}")
        return pd.DataFrame()

# Récupérer les interactions utilisateurs-livres
def recuperer_interactions(engine):
    query = """
    SELECT id_utilisateur, id_livre
    FROM sae._livre_utilisateur
    """
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        print(f"Erreur lors de la récupération des interactions : {e}")
        return pd.DataFrame()

# Calcul des interactions entre utilisateurs et livres en fonction des genres préférés
def calculer_interactions(df_utilisateur_genre, df_livres_par_genre):
    # Vérification des colonnes nécessaires
    if 'id_genre' not in df_utilisateur_genre.columns or 'id_genre' not in df_livres_par_genre.columns:
        print("Les données ne contiennent pas les colonnes nécessaires (id_genre).")
        return pd.DataFrame()

    # Fusionner les genres préférés des utilisateurs avec les livres par genre
    merged_df = pd.merge(df_utilisateur_genre, df_livres_par_genre, on='id_genre', how='inner')

    # Garder uniquement les colonnes nécessaires
    interactions = merged_df[['id_utilisateur', 'id_livre']]

    return interactions

# Calcul de la similarité entre utilisateurs
def calculer_similarites(df_interactions):
    if df_interactions.empty:
        print("Aucune interaction disponible pour calculer la similarité.")
        return pd.DataFrame()

    # Créer une table pivot pour les interactions
    pivot_df = df_interactions.pivot_table(index='id_utilisateur', columns='id_livre', aggfunc='size', fill_value=0)
    
    # Calculer la similarité cosinus
    similarity_matrix = cosine_similarity(pivot_df)
    similarity_df = pd.DataFrame(similarity_matrix, index=pivot_df.index, columns=pivot_df.index)
    
    return similarity_df

# Recommandation de livres
def recommander_livres(id_utilisateur, interactions_df, similarite_df, top_n=5):
    # Vérifier si l'utilisateur a des interactions
    user_interactions = interactions_df[interactions_df['id_utilisateur'] == id_utilisateur]

    if not user_interactions.empty:
        livres_preferes = user_interactions['id_livre'].tolist()
        recommandations = []

        # Utilisateurs similaires
        similar_users = similarite_df[id_utilisateur].sort_values(ascending=False).index[1:top_n+1]

        for similar_user in similar_users:
            user_livres = interactions_df[interactions_df['id_utilisateur'] == similar_user]['id_livre']
            recommandations.extend(user_livres)

        # Filtrer les livres déjà lus
        recommandations = list(set(recommandations) - set(livres_preferes))
        
        return recommandations[:top_n]

    else:
        print(f"L'utilisateur {id_utilisateur} n'a pas d'interactions enregistrées.")
        return []

# Exemple d'utilisation
if __name__ == "__main__":
    engine = se_connecter_bdd()

    if engine:
        # Récupérer les données
        df_utilisateur_genre = recuperer_genres_utilisateur(engine)
        df_livres_par_genre = recuperer_livres_par_genre(engine)
        df_interactions = recuperer_interactions(engine)

        # Vérifier les données récupérées
        print("Genres préférés des utilisateurs :")
        print(df_utilisateur_genre.head())

        print("Livres par genre :")
        print(df_livres_par_genre.head())

        print("Interactions utilisateurs-livres :")
        print(df_interactions.head())

        # Calculer les interactions et les similarités
        interactions_df = calculer_interactions(df_utilisateur_genre, df_livres_par_genre)
        print("Interactions calculées :")
        print(interactions_df.head())

        if not interactions_df.empty:
            similarite_df = calculer_similarites(interactions_df)
            print("Matrice de similarité :")
            print(similarite_df)

            # Recommander des livres pour un utilisateur donné
            id_utilisateur = 1
            recommandations = recommander_livres(id_utilisateur, interactions_df, similarite_df, top_n=5)
            print(f"Recommandations pour l'utilisateur {id_utilisateur} : {recommandations}")
    else:
        print("Échec de la connexion à la base de données.")
