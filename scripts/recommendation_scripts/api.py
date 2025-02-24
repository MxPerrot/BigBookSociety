
from fastapi import FastAPI, Query
from item_based_recommendation import recommendationItemBased
from user_based_recommendation import recommendationUserBased
import database_functions as bdd
import recommendation_utilities as ru
from typing import Annotated
import json 

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
        SELECT 
            _livre.id_livre, 
            _livre.titre,
            _livre.nb_notes, 
            _livre.nb_critiques,
            _livre.note_moyenne,
            _livre.nb_note_1_etoile,
            _livre.nb_note_2_etoile,
            _livre.nb_note_3_etoile,
            _livre.nb_note_4_etoile,
            _livre.nb_note_5_etoile,
            _livre.nombre_pages, 
            _livre.date_publication, 
            _livre.titre_original,
            _livre.isbn,
            _livre.isbn13,
            _livre.description,
            _editeur.nom_editeur
        
        FROM _livre
        LEFT JOIN _editeur ON _editeur.id_editeur = _livre.id_editeur
        WHERE _livre.id_livre IN (1);
    """)

    bookData = cursor.fetchall()

    cursor.execute(f"""
        SELECT _genre.libelle_genre, _genre_livre.nb_votes
        FROM _genre_livre
        INNER JOIN _genre ON _genre_livre.id_genre = _genre.id_genre
        WHERE _genre_livre.id_livre IN (1);
    """)

    genreData = cursor.fetchall()

    cursor.execute(f"""
        SELECT _auteur.nom
        FROM _auteur_livre
        INNER JOIN _auteur ON _auteur_livre.id_auteur = _auteur.id_auteur
        WHERE _auteur_livre.id_livre IN (1);
    """)

    authorData = cursor.fetchall()

    cursor.execute(f"""
        SELECT _serie.nom_serie, _episode_serie.numero_episode
        FROM _episode_serie
        INNER JOIN _serie ON _episode_serie.id_serie = _serie.id_serie
        WHERE _episode_serie.id_livre IN (1);
    """)

    seriesData = cursor.fetchall()

    cursor.execute(f"""
        SELECT _pays.nom, _cadre.localisation, _cadre.annee
        FROM _cadre_livre
        LEFT JOIN _cadre ON _cadre_livre.id_cadre = _cadre.id_cadre
        LEFT JOIN _pays ON _cadre.id_pays = _pays.id_pays
        WHERE _cadre_livre.id_livre IN (1);
    """)

    settingData = cursor.fetchall()

    cursor.execute(f"""
        SELECT _prix.nom_prix, _prix.annee_prix
        FROM _prix_livre
        LEFT JOIN _prix ON _prix_livre.id_prix = _prix.id_prix
        WHERE _prix_livre.id_livre IN (1);
    """)

    priceData = cursor.fetchall()

    if len(bookData) == 0:
        raise Exception('No book found, either there is no book with those IDs or the Database is not operating correctly\nList of book ID : '+idLivres)

    bookList = [list(book) for book in bookData]
    genreList = [list(genre) for genre in genreData]
    authorList = [list(author) for author in authorData]
    seriesList = [list(series) for series in seriesData]
    settingList = [list(setting) for setting in settingData]
    priceList = [list(price) for price in priceData]

    if len(bookList) != 0:
        book_json = []

        for i in range(len(bookList)):
            book_json.append({
                "id_livre": bookList[i][0], 
                "titre": bookList[i][1],
                "nb_notes": bookList[i][2], 
                "nb_critiques": bookList[i][3],
                "note_moyenne": float(bookList[i][4]),
                "nb_note_1_etoile": bookList[i][5],
                "nb_note_2_etoile": bookList[i][6],
                "nb_note_3_etoile": bookList[i][7],
                "nb_note_4_etoile": bookList[i][8],
                "nb_note_5_etoile": bookList[i][9],
                "nombre_pages": bookList[i][10], 
                "date_publication": str(bookList[i][11]), 
                "titre_original": bookList[i][12],
                "isbn": bookList[i][13],
                "isbn13": bookList[i][14],
                "description": bookList[i][15],
            })

            if len(bookList[0]) >= 16:
                book_json[i]["nom_editeur"] = bookList[i][16]

            if len(genreList) >= 2:
                book_json[i]["libelle_genre"] = genreList[i][0]
                book_json[i]["nb_votes"] = genreList[i][1]

            if len(authorList) >= 1:
                book_json[i]["nom_auteur"] = authorList[i][0]

            if len(seriesList) >= 2:
                book_json[i]["nom_serie"] = seriesList[i][0]
                book_json[i]["numero_episode"] = seriesList[i][1]

            if len(settingList) != 0:
                book_json[i]["nom"] = settingList[i][0]
                book_json[i]["localisation"] = settingList[i][1]
                book_json[i]["annee"] = settingList[i][2]

            if len(priceList) != 0:
                book_json[i]["nom_prix"] = priceList[i][0]
                book_json[i]["annee_prix"] = priceList[i][1]

        return json.dumps(book_json)
    return 0

print(getLivresInformation(cursor, [1]))