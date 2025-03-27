from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import json




class MoviesVectorDataBase:
    def __init__(self):
        with open("sample_mflix.embedded_movies.json", "r") as f:
            self.data = json.load(f)

    def generate_vectors(self):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = QdrantClient(url="http://localhost:6333")
        
        # Recupera a lista de coleções existentes
        existing_collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in existing_collections]
        
        # Cria a coleção apenas se ela não existir
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
