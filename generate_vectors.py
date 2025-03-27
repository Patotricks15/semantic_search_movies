from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import json




class MoviesVectorDataBase:
    def __init__(self):
        """
        Initialize the class with a json file containing movies data.

        The data is supposed to be in a file named "sample_mflix.embedded_movies.json".
        The data is loaded in a class variable named "data".
        """
        with open("sample_mflix.embedded_movies.json", "r") as f:
            self.data = json.load(f)

    def generate_vectors(self):
        """
        Generate sentence embeddings for the movies data and upload them to the Qdrant collection "movies".

        If the collection "movies" does not exist, it is created with a vector config of size equal to the embedding dimension of the sentence transformer model, and COSINE distance.

        The points are uploaded with the id as the index of the document in the data list, the vector as the sentence embedding of the document's fullplot, and the payload as the document itself.
        """
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = QdrantClient(url="http://localhost:6333")
        
        existing_collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in existing_collections]
        
        if "movies" not in collection_names:
            self.client.create_collection(
                collection_name="movies",
                vectors_config=models.VectorParams(
                    size=self.encoder.get_sentence_embedding_dimension(),
                    distance=models.Distance.COSINE
                ),
            )

            self.client.upload_points(
                collection_name="movies",
                points=[
                    models.PointStruct(
                        id=idx, 
                        vector=self.encoder.encode(doc['fullplot']).tolist(), 
                        payload=doc
                    ) 
                    for idx, doc in enumerate(self.data) 
                    if doc.get('fullplot') is not None
                ]
            )
