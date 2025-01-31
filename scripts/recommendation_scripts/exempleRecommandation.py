import database_functions as bdd
import item_based_recommendation as ib
import user_based_recommendation as ub
import recommendation_utilities as ru

NOMBRE_LIVRES_TESTES = 1000
UTILISATEUR_A_RECOMMANDER = 131

# Met en place le curseur de la connexion à la base de données
cursor = bdd.setUpCursor()
# Entrainement du modèle des genres
modelGenres = ru.model_genre(cursor)

livresItemBased = ib.recommendationItemBased(cursor, modelGenres, UTILISATEUR_A_RECOMMANDER, 2, bdd.getLivresAEvaluer(cursor, NOMBRE_LIVRES_TESTES))
livresUserBased = ub.recommendationUserBased(cursor, UTILISATEUR_A_RECOMMANDER, 2)
livresTendances = list(bdd.getLivresAEvaluerTendance(cursor, 2)['id_livre'].unique())
livresTendancesItemBased = ib.recommendationItemBased(cursor, modelGenres, UTILISATEUR_A_RECOMMANDER, 2, bdd.getLivresAEvaluerTendance(cursor, NOMBRE_LIVRES_TESTES))
livresDecouverte = list(bdd.getLivresAEvaluerDecouverte(cursor, 2)['id_livre'].unique())
livresDecouverteItemBased = ib.recommendationItemBased(cursor, modelGenres, UTILISATEUR_A_RECOMMANDER, 2, bdd.getLivresAEvaluerDecouverte(cursor, NOMBRE_LIVRES_TESTES))
livresMemeAuteur = bdd.getBookIdSameAuthor(cursor, UTILISATEUR_A_RECOMMANDER, 2)
livresMemeSerie = bdd.getBookIdInSeries(cursor, UTILISATEUR_A_RECOMMANDER)

for i in [livresItemBased, livresUserBased, livresTendances, livresTendancesItemBased, livresDecouverte, livresDecouverteItemBased, livresMemeAuteur, livresMemeSerie]:
    print("\n-----------------\n")
    # DEBUG : Recupère les infos des livres recommandés pour verifier leur cohérence
    cursor.execute(f"""
        SELECT DISTINCT _livre.titre, _auteur.nom
        FROM _livre

        LEFT JOIN _auteur_livre ON _livre.id_livre = _auteur_livre.id_livre
        LEFT JOIN _auteur ON _auteur_livre.id_auteur = _auteur.id_auteur

        LEFT JOIN _genre_livre ON _livre.id_livre = _genre_livre.id_livre
        LEFT JOIN _genre ON _genre_livre.id_genre = _genre.id_genre

        WHERE _livre.id_livre IN {tuple(i)};
    """)

    livresRecommandes = cursor.fetchall()
    for book in livresRecommandes:
        print("\n", book[0], book[1])