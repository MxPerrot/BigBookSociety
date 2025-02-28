
from fastapi import FastAPI, Query, HTTPException, Depends
from item_based_recommendation import recommendationItemBased
from user_based_recommendation import recommendationUserBased
import database_functions as bdd
import recommendation_utilities as ru
from typing import Annotated
import json 
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
import psycopg2.extras
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection = bdd.setUpConnection()
cursor = bdd.setUpCursor(connection)

modelGenres = ru.model_genre(cursor)

#https://fastapi.tiangolo.com/tutorial/first-steps/
    








def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


@app.post("/register")
def register_user(username: str, email: str, password: str, sexe: str):
    hashed_pw = hash_password(password)
    # conn = get_db_connection()
    # cur = conn.cursor()
    try:
        cursor.execute("INSERT INTO _utilisateur(nom_utilisateur, mail_utilisateur, mot_de_passe_hashed, sexe) VALUES (%s, %s, %s, %s) RETURNING id_utilisateur", (username, email, hashed_pw, sexe))
        user_id = cursor.fetchone()[0]
        connection.commit()
        # cursor.commit()
        return {"message": "User created successfully", "user_id": user_id}
    except psycopg2.IntegrityError:
        # cursor.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    # finally:
        # cur.close()
        # conn.close()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"] # Returns username if token is valid
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # conn = get_db_connection()
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT nom_utilisateur, mot_de_passe_hashed FROM _utilisateur WHERE nom_utilisateur = %s", (form_data.username,))
    user = cursor.fetchone()
    # cursor.close()
    # conn.close()
    print(user)
    if not user or not verify_password(form_data.password, user[1]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user[0])
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)

    # conn = get_db_connection()
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT id_utilisateur, nom_utilisateur, mail_utilisateur FROM _utilisateur WHERE nom_utilisateur = %s", (username,))
    user = cursor.fetchone()
    # cur.close()
    # conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"id": current_user[0], "username": current_user[1], "email": current_user[2]}




@app.get("/get_book_item_based/")
async def get_book_item_based(current_user: dict = Depends(get_current_user), nbrecommendation:int=10, limit:int=1000):
    book_id_list = recommendationItemBased(cursor, modelGenres, int(current_user[0]), int(nbrecommendation), bdd.getLivresAEvaluer(cursor, int(limit)))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos


@app.get("/get_book_item_based_tendance/")
async def get_book_item_based_tendance(user:int, nbrecommendation:int=10, limit:int=1000):
    book_id_list = recommendationItemBased(cursor, modelGenres, int(user), int(nbrecommendation), bdd.getLivresAEvaluerTendance(cursor, int(limit)))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos


@app.get("/get_book_item_based_decouverte/")
async def get_book_item_based_decouverte(user:int, nbrecommendation:int=10, limit:int=1000):
    book_id_list = recommendationItemBased(cursor, modelGenres, int(user), int(nbrecommendation), bdd.getLivresAEvaluerDecouverte(cursor, int(limit)))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos


@app.get("/get_book_user_based/")
async def get_book_user_based(user:int, nbrecommendation:int=10):
    book_id_list = recommendationUserBased(cursor, int(user), int(nbrecommendation))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos


@app.get("/get_tendance/{limit}")
async def get_tendance(limit:int):
    book_id_list = bdd.getIdLivresTendance(cursor, limit)
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos


@app.get("/get_meme_auteur/")
async def get_meme_auteur(user:int, nbrecommendation:int=10):
    book_id_list = bdd.getBookIdSameAuthor(cursor, int(user),int(nbrecommendation))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos


@app.get("/get_in_serie/{user}")
async def get_in_serie(user:int):
    book_id_list = bdd.getBookIdInSeries(cursor, int(user))
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

@app.get("/get_next_books/{id}")
async def get_next_books(id:int):

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
async def search_books(pageNum:int=1, paginTaille:int=20, title:str=None, authors:Annotated[list[int]|None,Query()]=None, genres:Annotated[list[int]|None,Query()]=None, minNote:int=None, maxNote:int=None):
    book_id_list = bdd.rechercheLivre(cursor, pageNum, paginTaille, title, authors, genres, minNote, maxNote) 
    if len(book_id_list) < 1:
        return json.dumps([])
    books_infos = getLivresInformation(cursor,book_id_list)
    return books_infos

@app.get("/search_author/{nom}")
async def search_author(nom:str):
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
    
    return author_json


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

        return book_json
    return 0

#print(getLivresInformation(cursor, [1,350]))
