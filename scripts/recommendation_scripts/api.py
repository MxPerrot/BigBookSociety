
from fastapi import FastAPI, Query, HTTPException
from item_based_recommendation import recommendationItemBased
from user_based_recommendation import recommendationUserBased
import database_functions as bdd
import recommendation_utilities as ru
from typing import Annotated
import json 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cursor = bdd.setUpCursor()

modelGenres = ru.model_genre(cursor)

#https://fastapi.tiangolo.com/tutorial/first-steps/


#q1 = user, q2 = nbrecommendation, q3 = limite

#/get_book_item_based/?q=40&q=10&q=10


@app.get("/get_book_item_based/")
async def get_book_item_based(user: int, nbrecommendation: int,limit: int):
    book_id_list = recommendationItemBased(cursor, modelGenres, int(user), int(nbrecommendation), bdd.getLivresAEvaluer(cursor, int(limit)))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

@app.get("/get_book_item_based_tendance/")
async def get_book_item_based_tendance(user: int, nbrecommendation: int,limit: int):
    book_id_list = recommendationItemBased(cursor, modelGenres, int(user), int(nbrecommendation), bdd.getLivresAEvaluerTendance(cursor, int(limit)))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

@app.get("/get_book_item_based_decouverte/")
async def get_book_item_based_decouverte(user: int, nbrecommendation: int,limit: int):
    book_id_list = recommendationItemBased(cursor, modelGenres, int(user), int(nbrecommendation), bdd.getLivresAEvaluerDecouverte(cursor, int(limit)))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

#q1 = user, q2 = nbrecommendation
@app.get("/get_book_user_based/")
async def get_book_user_based(user: int, nbrecommendation: int):
    book_id_list = recommendationUserBased(cursor, int(user), int(nbrecommendation))
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
async def get_meme_auteur(user: int = 0, nbrecommendation: int = 10):
    book_id_list = bdd.getBookIdSameAuthor(cursor, int(user),int(nbrecommendation))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

#q1 = user
@app.get("/get_in_serie/{user}")
async def get_in_serie(user):
    book_id_list = bdd.getBookIdInSeries(cursor, int(user))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

@app.get("/get_next_books/{id}")
async def get_next_books(id):

    cursor.execute(f"""
        SELECT _episode_serie.id_serie
        FROM _episode_serie
        WHERE _episode_serie.id_livre = {id};
    """)

    serieData = cursor.fetchall()

    cursor.execute(f"""
        SELECT _episode_serie.id_livre
        FROM _episode_serie
        WHERE _episode_serie.id_serie = {serieData[0][0]};
    """)

    bookData = cursor.fetchall()
    books_infos = getLivresInformation(cursor,bookData)

    return books_infos

@app.get("/get_genres/")
async def get_genres():
    genre_list = bdd.getGenres(cursor)
    return json.dumps(genre_list)

@app.get("/get_authors/")
async def get_authors():
    author_list = bdd.getAuthors(cursor)
    return json.dumps(author_list)

@app.get("/search_books/")
async def search_books(title:str=None, authors:tuple=None, genres:tuple=None, minNote:int=None, maxNote:int=None):
    book_id_list = bdd.rechercheLivre(cursor, title, authors, genres, minNote, maxNote) 
    if len(book_id_list) < 1:
        return json.dumps([])
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

@app.get("/search_author/{nom}")
async def search_author(nom):
    authorInfo = bdd.rechercheAuteur(cursor, nom)

    if len(authorInfo) == 0:
        return json.dumps([])
    author_json = []
    for author in authorInfo:

        noteMoy = author[4]
        if noteMoy != None:
            noteMoy = float(noteMoy)

        author_json.append({
                "id_auteur": author[0],
                "nom": author[1],
                "origine": author[2],
                "sexe": author[3],
                "note_moyenne": noteMoy,
                "genre_ecrit": author[5]
            })
    
    return json.dumps(author_json)

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
    idLivres = bdd.turnIterableIntoSqlList(idLivres)

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
        WHERE _livre.id_livre IN ({idLivres});
    """)

    bookData = cursor.fetchall()

    if len(bookData) == 0:
        return json.dumps([])
    
    cursor.execute(f"""
        SELECT _genre_livre.id_livre, _genre.libelle_genre, _genre_livre.nb_votes
        FROM _genre_livre
        INNER JOIN _genre ON _genre_livre.id_genre = _genre.id_genre
        WHERE _genre_livre.id_livre IN ({idLivres});
    """)

    genreData = cursor.fetchall()

    cursor.execute(f"""
        SELECT _auteur_livre.id_livre, _auteur.nom
        FROM _auteur_livre
        INNER JOIN _auteur ON _auteur_livre.id_auteur = _auteur.id_auteur
        WHERE _auteur_livre.id_livre IN ({idLivres});
    """)

    authorData = cursor.fetchall()

    cursor.execute(f"""
        SELECT _episode_serie.id_livre, _serie.nom_serie, _episode_serie.numero_episode
        FROM _episode_serie
        INNER JOIN _serie ON _episode_serie.id_serie = _serie.id_serie
        WHERE _episode_serie.id_livre IN ({idLivres});
    """)

    seriesData = cursor.fetchall()

    cursor.execute(f"""
        SELECT _cadre_livre.id_livre, _pays.nom, _cadre.localisation, _cadre.annee
        FROM _cadre_livre
        LEFT JOIN _cadre ON _cadre_livre.id_cadre = _cadre.id_cadre
        LEFT JOIN _pays ON _cadre.id_pays = _pays.id_pays
        WHERE _cadre_livre.id_livre IN ({idLivres});
    """)

    settingData = cursor.fetchall()

    cursor.execute(f"""
        SELECT _prix_livre.id_livre, _prix.nom_prix, _prix.annee_prix
        FROM _prix_livre
        LEFT JOIN _prix ON _prix_livre.id_prix = _prix.id_prix
        WHERE _prix_livre.id_livre IN ({idLivres});
    """)

    priceData = cursor.fetchall()


    bookList = [list(book) for book in bookData]
    genreList = [list(genre) for genre in genreData]
    authorList = [list(author) for author in authorData]
    seriesList = [list(series) for series in seriesData]
    settingList = [list(setting) for setting in settingData]
    priceList = [list(price) for price in priceData]

    if len(bookList) != 0:
        book_json = []

        for i in range(len(bookList)):
            bookId = bookList[i][0]
            #FIXME Prevoir le cas où l'une de ces données manque / est Null ou NoneType
            noteMoy = bookList[i][4]
            if noteMoy != None:
                noteMoy = float(noteMoy)
            datePubli = bookList[i][11]
            if datePubli != None:
                datePubli = str(datePubli)
            book_json.append({
                "id_livre": bookId, 
                "titre": bookList[i][1],
                "nb_notes": bookList[i][2], 
                "nb_critiques": bookList[i][3],
                "note_moyenne": noteMoy,
                "nb_note_1_etoile": bookList[i][5],
                "nb_note_2_etoile": bookList[i][6],
                "nb_note_3_etoile": bookList[i][7],
                "nb_note_4_etoile": bookList[i][8],
                "nb_note_5_etoile": bookList[i][9],
                "nombre_pages": bookList[i][10], 
                "date_publication": datePubli, 
                "titre_original": bookList[i][12],
                "isbn": bookList[i][13],
                "isbn13": bookList[i][14],
                "description": bookList[i][15],
            })

            if len(bookList[i]) >= 16:
                book_json[i]["nom_editeur"] = bookList[i][16]

            if len(genreList) != 0:
                book_json[i]["libelle_genre"] = [genre[1] for genre in genreList if genre[0] == bookId]
                book_json[i]["nb_votes"] = [genre[2] for genre in genreList if genre[0] == bookId]

            if len(authorList) != 0:
                book_json[i]["nom_auteur"] = [author[1] for author in authorList if author[0] == bookId]

            if len(seriesList) != 0:
                book_json[i]["nom_serie"] = [series[1] for series in seriesList if series[0] == bookId]
                book_json[i]["numero_episode"] = [series[2] for series in seriesList if series[0] == bookId]

            if len(settingList) != 0:
                book_json[i]["nom"] = [setting[1] for setting in settingList if setting[0] == bookId]
                book_json[i]["localisation"] = [setting[2] for setting in settingList if setting[0] == bookId]
                book_json[i]["annee"] = [setting[3] for setting in settingList if setting[0] == bookId]

            if len(priceList) != 0:
                book_json[i]["nom_prix"] = [price[1] for price in priceList if price[0] == bookId]
                book_json[i]["annee_prix"] = [price[2] for price in priceList if price[0] == bookId]

        return json.dumps(book_json)
    return 0

#print(getLivresInformation(cursor, [1,350]))