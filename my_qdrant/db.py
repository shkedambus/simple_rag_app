from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_ollama.embeddings import OllamaEmbeddings

client = QdrantClient(url="http://localhost:6333")

collection_name = "main"
vector_size = 768 # because I use nomic-embed-text model

if not client.collection_exists(collection_name=collection_name):
    # this collection uses a dot product distance metric to compare vectors
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.DOT)
    )

embedding_model = OllamaEmbeddings(model="nomic-embed-text")

def clear_db():
    if client.collection_exists(collection_name=collection_name):
        client.delete_collection(collection_name=collection_name)

def update_db(text_chunks):
    for i, chunk in enumerate(text_chunks):
        vector = embedding_model.embed_query(chunk)
        client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(id=i, vector=vector, payload={"text": chunk})
            ]
    )

def similarity_search(question):
    query_vector = embedding_model.embed_query(question)

    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=10,
    )

    retrieved_texts = [hit.payload["text"] for hit in search_result]
    return retrieved_texts