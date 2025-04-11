# Movie Recommendation API

This project implements a REST API using FastAPI that provides movie recommendations based on semantic similarity of plots. It uses language embeddings from the `all-MiniLM-L6-v2` model and stores the vectors in a Qdrant vector database.

## Project Structure

```
├── generate_vectors.py     # Loads data, generates embeddings, uploads to Qdrant
├── app.py                 # Main FastAPI app
├── sample_mflix.embedded_movies.json  # Movie data with full plot descriptions
└── README.md
```

---

## How to Run

### 1. Requirements

- Python 3.8+
- Docker (to run Qdrant)
- `sample_mflix.embedded_movies.json` file with a `fullplot` key

### 2. Start Qdrant locally

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**Example `requirements.txt`:**
```text
fastapi
uvicorn
qdrant-client
sentence-transformers
```

### 4. Run the API

```bash
uvicorn main:app --reload
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## Endpoints

### `GET /`

Returns the top N most similar movies based on a keyword.

**Query parameters:**

- `search`: keyword to search (e.g. `"mars"`)
- `n`: number of movies to return (default: 3)

**Example request:**
```http
GET /?search=mars&n=3
```

**Example response:**
```json
{
  "message": "The Martian\nA stranded astronaut tries to survive on Mars...\n------..."
}
```

---

## How It Works

1. Loads the `sample_mflix.embedded_movies.json` dataset.
2. Uses the `all-MiniLM-L6-v2` model to embed each movie's `fullplot`.
3. Stores each vector in Qdrant with its corresponding document as payload.
4. On query, the search term is also embedded into a vector.
5. Qdrant returns the most similar movie plots using cosine similarity.

---

## Notes

- Make sure each movie in the dataset has a non-empty `fullplot`.
- Only movies with a valid `fullplot` are indexed.
- Qdrant must be running locally at `http://localhost:6333`.

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Qdrant](https://qdrant.tech/)
- [Sentence Transformers](https://www.sbert.net/)
- [Docker](https://www.docker.com/)

