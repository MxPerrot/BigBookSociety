from fastapi import FastAPI, Query
from item_based_recommendation import recommendationItemBased
import database_functions as bdd
import recommendation_utilities as ru
from typing import Annotated


modelGenres = ru.model_genre()
cursor = bdd.setUpCursor()


app = FastAPI()

#https://fastapi.tiangolo.com/tutorial/first-steps/


# parameters = q=foo&q=bar

#q1 = user, q2 = nbrecommendation, q3 = limite
@app.get("/get_book_item_based/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    return recommendationItemBased(cursor, modelGenres, int(q[0]), int(q[1]), bdd.getLivresAEvaluer(cursor, int(q[2])))

@app.get("/get_book_item_based_tendance/{parameters}")
async def root():
    return recommendationItemBased(cursor, modelGenres, 11, 5, bdd.getLivresAEvaluerTendance(cursor, 10))

@app.get("/get_book_item_based_decouverte/{parameters}")
async def root():
    return recommendationItemBased(cursor, modelGenres, 11, 5, bdd.getLivresAEvaluerDecouverte(cursor, 10))

