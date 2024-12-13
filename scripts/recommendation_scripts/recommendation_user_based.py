import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Connexion à la base de données PostgreSQL
def se_connecter_bdd():
    try:
        conn = psycopg2.connect(
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT")
        )
        print("Connexion réussie à la base de données.")
        return conn
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None

# Récupérer les genres préférés des utilisateurs
def recuperer_genres_utilisateur(conn):
    query = """
    SELECT id_utilisateur, id_genre
    FROM sae._utilisateur_genre
    """
    return pd.read_sql(query, conn)

# Récupérer les livres associés aux genres
def recuperer_livres_par_genre(conn):
    query = """
    SELECT id_livre, id_genre
    FROM sae._genre_livre
    """
    return pd.read_sql(query, conn)

# Récupérer les interactions utilisateurs-livres
def recuperer_interactions(conn):
    query = """
    SELECT id_utilisateur, id_livre
    FROM sae._livre_utilisateur
    """
    return pd.read_sql(query, conn)

# Calcul des interactions entre utilisateurs et livres en fonction des genres préférés
def calculer_interactions(df_utilisateur_genre, df_livre_utilisateur):
    interactions = []
    for _, row in df_utilisateur_genre.iterrows():
        id_utilisateur = row['id_utilisateur']
        id_genre = row['id_genre']

        # Récupérer les livres associés à ce genre
        livres_genre = df_livre_utilisateur[df_livre_utilisateur['id_genre'] == id_genre]
        
        # Ajouter une interaction pour chaque livre du genre
        for _, livre_row in livres_genre.iterrows():
            interactions.append({
                'id_utilisateur': id_utilisateur,
                'id_livre': livre_row['id_livre']
            })

    return pd.DataFrame(interactions)

# Calcul de la similarité entre utilisateurs
def calculer_similarites(df_interactions):
    pivot_df = df_interactions.pivot_table(index='id_utilisateur', columns='id_livre', aggfunc='size', fill_value=0)
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
        genres_utilisateur = interactions_df[interactions_df['id_utilisateur'] == id_utilisateur]['id_genre'].unique()
        livres_recommandes = interactions_df[interactions_df['id_genre'].isin(genres_utilisateur)]['id_livre'].unique()
        
        return livres_recommandes[:top_n]

# Exemple d'utilisation
conn = se_connecter_bdd()

if conn:
    # Récupérer les données
    df_utilisateur_genre = recuperer_genres_utilisateur(conn)
    df_livre_utilisateur = recuperer_livres_par_genre(conn)
    df_interactions = recuperer_interactions(conn)

    # Calculer les interactions et les similarités
    interactions_df = calculer_interactions(df_utilisateur_genre, df_livre_utilisateur)
    similarite_df = calculer_similarites(interactions_df)

    # Recommander des livres pour un utilisateur donné
    id_utilisateur = 1
    recommandations = recommander_livres(id_utilisateur, interactions_df, similarite_df, top_n=5)
    print(f"Recommandations pour l'utilisateur {id_utilisateur} : {recommandations}")
else:
    print("Échec de la connexion à la base de données.")
