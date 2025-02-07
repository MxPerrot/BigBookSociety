import database_functions as bdd
import item_based_recommendation as ib
import user_based_recommendation as ub
import recommendation_utilities as ru
from time import process_time

NOMBRE_LIVRES_TESTES = 1000
UTILISATEUR_A_RECOMMANDER = 131

# Met en place le curseur de la connexion à la base de données
cursor = bdd.setUpCursor()


# Entrainement du modèle des genres
st = process_time()
modelGenres = ru.model_genre(cursor)
end = process_time()
res = end - st
print(f"Entrainement du model des genres : {res}")


st = process_time()
livresItemBased = ib.recommendationItemBased(cursor, modelGenres, UTILISATEUR_A_RECOMMANDER, 2, bdd.getLivresAEvaluer(cursor, NOMBRE_LIVRES_TESTES))
end = process_time()
res = end - st
print(f"Item Based : {res}")
st = process_time()
livresUserBased = ub.recommendationUserBased(cursor, UTILISATEUR_A_RECOMMANDER, 2)
end = process_time()
res = end - st
print(f"User Based : {res}")
st = process_time()
livresDecouverteItemBased = ib.recommendationItemBased(cursor, modelGenres, UTILISATEUR_A_RECOMMANDER, 2, bdd.getLivresAEvaluerDecouverte(cursor, NOMBRE_LIVRES_TESTES))
end = process_time()
res = end - st
print(f"Decouverte Item Based : {res}")
st = process_time()
livresTendances = list(bdd.getLivresAEvaluerTendance(cursor, 2)['id_livre'].unique())
end = process_time()
res = end - st
print(f"Tendances : {res}")
st = process_time()
livresTendancesItemBased = ib.recommendationItemBased(cursor, modelGenres, UTILISATEUR_A_RECOMMANDER, 2, bdd.getLivresAEvaluerTendance(cursor, NOMBRE_LIVRES_TESTES))
end = process_time()
res = end - st
print(f"Tendances + hybride item based : {res}")
st = process_time()
livresDecouverte = list(bdd.getLivresAEvaluerDecouverte(cursor, 2)['id_livre'].unique())
end = process_time()
res = end - st
print(f"Decouverte : {res}")
st = process_time()
livresDecouverteItemBased = ib.recommendationItemBased(cursor, modelGenres, UTILISATEUR_A_RECOMMANDER, 2, bdd.getLivresAEvaluerDecouverte(cursor, NOMBRE_LIVRES_TESTES))
end = process_time()
res = end - st
print(f"Decouverte + hybride item based : {res}")
st = process_time()
livresMemeAuteur = bdd.getBookIdSameAuthor(cursor, UTILISATEUR_A_RECOMMANDER, 2) # TODO: FIXME
end = process_time()
res = end - st
print(f"Même auteur : {res}")
st = process_time()
livresMemeSerie = bdd.getBookIdInSeries(cursor, UTILISATEUR_A_RECOMMANDER)
end = process_time()
res = end - st
print(f"Même série : {res}")

liste_libelle = ["livresItemBased", "livresUserBased", "livresTendances","livresTendancesItemBased", "livresDecouverte", "livresDecouverteItemBased", "livresMemeAuteur", "livresMemeSerie"]
y=0
for i in [livresItemBased, livresUserBased, livresTendances, livresTendancesItemBased, livresDecouverte, livresDecouverteItemBased,  livresMemeAuteur, livresMemeSerie]: # TODO livresMemeAuteur, MANQUANT CAR BUGGE
    print("\n-----------------\n")
    print(liste_libelle[y])
    y=y+1
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