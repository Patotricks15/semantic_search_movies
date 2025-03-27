from fastapi import FastAPI
from generate_vectors import MoviesVectorDataBase

db = MoviesVectorDataBase()

db.generate_vectors()

app = FastAPI()
@app.get("/")
async def recommended_movies(search:str, n:int = 3):
    """
    Return a list of the top n movies whose plots are most similar to the word "mars".

    Args:
        search (str): The word to search for.
        n (int, optional): The number of movies to return. Defaults to 3.

    Returns:
        dict: A dictionary with a single key, "message", containing a string
        where each line is a movie title followed by its plot, separated by a newline.
    """
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