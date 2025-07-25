import os
import sqlite3
import json
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        dimensions=256,
        input=texts
    )
    return [item.embedding for item in response.data]

def cosine_distance(a: List[float], b: List[float]) -> float:
    return 1 - cosine_similarity([a], [b])[0][0]

def retrieve_documents(query: str, limit: int = 3) -> List[Dict]:
    embeddings = generate_embeddings([query])
    query_embedding = embeddings[0]
    
    conn = sqlite3.connect('documents.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, content, embedding FROM documents')
    rows = cursor.fetchall()
    conn.close()
    
    documents_with_similarity = []
    for row in rows:
        doc_id, name, content, embedding_json = row
        doc_embedding = json.loads(embedding_json)
        
        similarity = 1 - cosine_distance(query_embedding, doc_embedding)
        
        documents_with_similarity.append({
            'id': doc_id,
            'name': name,
            'content': content,
            'similarity': similarity
        })
    
    documents_with_similarity.sort(key=lambda x: x['similarity'], reverse=True)
    
    results = documents_with_similarity[:limit]
    print(results)
    
    return results

if __name__ == "__main__":
    docs = retrieve_documents("Tell me about rhinos")
    print(f"Retrieved {len(docs)} documents")