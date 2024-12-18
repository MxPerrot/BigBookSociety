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

# ----------------------------------
#  Fonctions de vectorisation 
# ----------------------------------
def vectorizeBookLength(nb_pages):
    if pd.isnull(nb_pages):
        indTaille = 0
    else:
        if nb_pages > 1000:
            indTaille = 6
        elif nb_pages > 500:
            indTaille = 5
        elif nb_pages > 200:
            indTaille = 4
        elif nb_pages > 100:
            indTaille = 3
        elif nb_pages > 50:
            indTaille = 2
        else:
            indTaille = 1
    return indTaille

def vectorizeReviewNb(nb_note):
    if pd.isnull(nb_note):
        indPop = 0
    else:
        if nb_note > 1000000:
            indPop = 9
        elif nb_note > 500000:
            indPop = 8
        elif nb_note > 250000:
            indPop = 7
        elif nb_note > 100000:
            indPop = 6
        elif nb_note > 50000:
            indPop = 5
        elif nb_note > 10000:
            indPop = 4
        elif nb_note > 5000:
            indPop = 3
        elif nb_note > 1000:
            indPop = 2
        else:
            indPop = 1
    return indPop

# Vectorisation des données
def vectoriser_donnees(df):
    df['taille_livre'] = df['nombre_pages'].apply(vectorizeBookLength)
    df['popularite'] = df['nb_notes'].apply(vectorizeReviewNb)
    return df

# Calcul de la similarité entre utilisateurs
def calculer_similarites(df):
    if df.empty:
        print("Aucune donnée pour calculer la similarité.")
        return pd.DataFrame()

    # Créer une table pivot pour les interactions
    pivot_df = df.pivot_table(index='id_utilisateur', columns='id_livre', aggfunc='size', fill_value=0)
    
    # Calculer la similarité cosinus
    similarity_matrix = cosine_similarity(pivot_df)
    similarity_df = pd.DataFrame(similarity_matrix, index=pivot_df.index, columns=pivot_df.index)
    
    return similarity_df

# Recommandation de livres
def recommander_livres(id_utilisateur, interactions_df, similarite_df, top_n=5):
    # Vérifier si l'utilisateur est dans la matrice de similarité
    if id_utilisateur not in similarite_df.index:  # Modification
        print(f"L'utilisateur {id_utilisateur} n'existe pas dans la matrice de similarité.")
        return []

    # Vérifier si l'utilisateur a des interactions
    user_interactions = interactions_df[interactions_df['id_utilisateur'] == id_utilisateur]

    if not user_interactions.empty:
        livres_preferes = user_interactions['id_livre'].tolist()
        recommandations = []

        # Utilisateurs similaires
        similar_users = similarite_df.loc[id_utilisateur].sort_values(ascending=False).index[1:top_n+1]

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
        query = """
            SELECT DISTINCT _utilisateur.id_utilisateur, _livre.id_livre, _livre.titre, _livre.nb_notes, _livre.nombre_pages
            FROM sae._utilisateur
            LEFT JOIN sae._livre_utilisateur ON _livre_utilisateur.id_utilisateur = _utilisateur.id_utilisateur
            LEFT JOIN sae._livre ON _livre.id_livre = _livre_utilisateur.id_livre
        """
        donnees = pd.read_sql(query, engine)

        # Vectoriser les données
        donnees_vectorisees = vectoriser_donnees(donnees)

        # Calculer les similarités
        similarite_df = calculer_similarites(donnees_vectorisees)

        if not similarite_df.empty:
            # Recommander des livres
            id_utilisateur = 2  # Exemple d'utilisateur
            recommandations = recommander_livres(id_utilisateur, donnees, similarite_df, top_n=5)
            print(f"Recommandations pour l'utilisateur {id_utilisateur} : {recommandations}")
        else:
            print("Aucune similarité calculée.")
    else:
        print("Échec de la connexion à la base de données.")
