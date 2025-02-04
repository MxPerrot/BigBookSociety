
from fastapi import FastAPI, Query
from item_based_recommendation import recommendationItemBased
from user_based_recommendation import recommendationUserBased
import database_functions as bdd
import recommendation_utilities as ru
from typing import Annotated

cursor = bdd.setUpCursor()
modelGenres = ru.model_genre(cursor)
app = FastAPI()

#https://fastapi.tiangolo.com/tutorial/first-steps/


#q1 = user, q2 = nbrecommendation, q3 = limite
@app.get("/get_book_item_based/")
async def get_book_item_based(q: Annotated[list[str] | None, Query()] = None):
    book_id_list = recommendationItemBased(cursor, modelGenres, int(q[0]), int(q[1]), bdd.getLivresAEvaluer(cursor, int(q[2])))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

@app.get("/get_book_item_based_tendance/")
async def get_book_item_based_tendance(q: Annotated[list[str] | None, Query()] = None):
    book_id_list = recommendationItemBased(cursor, modelGenres, int(q[0]), int(q[1]), bdd.getLivresAEvaluerTendance(cursor, int(q[2])))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

@app.get("/get_book_item_based_decouverte/")
async def get_book_item_based_decouverte(q: Annotated[list[str] | None, Query()] = None):
    book_id_list = recommendationItemBased(cursor, modelGenres, int(q[0]), int(q[1]), bdd.getLivresAEvaluerDecouverte(cursor, int(q[2])))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

#q1 = user, q2 = nbrecommendation
@app.get("/get_book_user_based/")
async def get_book_user_based(q: Annotated[list[str] | None, Query()] = None):
    book_id_list = recommendationUserBased(cursor, int(q[0]), int(q[1]))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos


@app.get("/get_decouverte/{limit}")
async def get_decouverte(limit):
    book_id_list = bdd.getLivresAEvaluerDecouverte(cursor, limit)
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

@app.get("/get_tendance/{limit}")
async def get_tendance(limit):
    book_id_list = bdd.getLivresAEvaluerTendance(cursor, limit)
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

#q1 = user, q2 = nbrecommendation
@app.get("/get_meme_auteur/")
async def get_meme_auteur(q: Annotated[list[str] | None, Query()] = None):
    book_id_list = bdd.getBookIdSameAuthor(cursor, int(q[0]),int(q[1]))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

#q1 = user
@app.get("/get_in_serie/")
async def get_in_serie(q: Annotated[list[str] | None, Query()] = None):
    book_id_list = bdd.getBookIdInSeries(cursor, int(q[0]))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos



# @app.get("/get_book_by_id/{id}")
# async def get_book_by_id(id):
#     return recommendationItemBased(cursor, modelGenres, int(q[0]), int(q[1]), bdd.getLivresAEvaluerDecouverte(cursor, int(q[2])))




# --titre
# serie
# --description
# --nom auteur
# --edition
# --nbr de pages
# --date de sortie
# eventuellement prix


def getLivresInformation(cursor,idLivres):
    idLivres = tuple(idLivres)

    cursor.execute(f"""
        SELECT _livre.id_livre, _auteur.nom, _livre.titre, _livre.nb_notes, _livre.nombre_pages, _livre.date_publication, _livre.nombre_pages, _editeur.nom_editeur, _prix.nom_prix, _serie.nom_serie
        FROM _livre

        LEFT JOIN _editeur ON _editeur.id_editeur = _livre.id_editeur

        LEFT JOIN _prix_livre ON _livre.id_livre = _prix_livre.id_livre
        LEFT JOIN _prix ON _prix_livre.id_prix = _prix.id_prix
                
        LEFT JOIN _cadre_livre ON _livre.id_livre = _cadre_livre.id_livre
        LEFT JOIN _cadre ON _cadre_livre.id_cadre = _cadre.id_cadre

        LEFT JOIN _auteur_livre ON _livre.id_livre = _auteur_livre.id_livre
        LEFT JOIN _auteur ON _auteur_livre.id_auteur = _auteur.id_auteur

        LEFT JOIN _genre_livre ON _livre.id_livre = _genre_livre.id_livre
        LEFT JOIN _genre ON _genre_livre.id_genre = _genre.id_genre

        LEFT JOIN _episode_serie ON _livre.id_livre = _episode_serie.id_livre
        LEFT JOIN _serie ON _episode_serie.id_serie = _serie.id_serie

        WHERE _livre.id_livre IN {idLivres}
    """)

    bookData = cursor.fetchall()

    if len(bookData) == 0:
        raise Exception('No book found, either there is no book with those IDs or the Database is not operating correctly\nList of book ID : '+idLivres)


    bookList = [list(book) for book in bookData]

    return bookList