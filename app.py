from fastapi import FastAPI
from generate_vectors import MoviesVectorDataBase

db = MoviesVectorDataBase()

db.generate_vectors()

app = FastAPI()
@app.get("/")
async def recommended_movies(search:str, n:int = 3):
    message = ''
    searches = db.client.query_points(
    collection_name="movies",
    query = db.encoder.encode("mars").tolist(),
    limit=n
    ).points

    for search in searches:
        message += search.payload["title"]
        message += '\n'
        message += search.payload["fullplot"]
        message += '------'

    return {"message":message}