import os
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
import json

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MOCK_DOCS = [
    {"content": "A group of flamingos is called a 'flamboyance'.", "name": "Fun Fact 1"},
    {"content": "Octopuses have three hearts.", "name": "Fun Fact 2"},
    {"content": "Butterflies taste with their feet.", "name": "Fun Fact 3"},
    {"content": "A snail can sleep for three years.", "name": "Fun Fact 4"},
    {"content": "Elephants are the only animals that can't jump.", "name": "Fun Fact 5"},
    {"content": "A rhinoceros' horn is made of hair.", "name": "Fun Fact 6"},
    {"content": "Slugs have four noses.", "name": "Fun Fact 7"},
    {"content": "A cow gives nearly 200,000 glasses of milk in a lifetime.", "name": "Fun Fact 8"},
    {"content": "Bats are the only mammals that can fly.", "name": "Fun Fact 9"},
    {"content": "Koalas sleep up to 22 hours a day.", "name": "Fun Fact 10"}
]

def init_database():
    conn = sqlite3.connect('documents.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    return conn

def upload_documents(docs: List[Dict[str, str]]) -> List[List[float]]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        dimensions=256,
        input=[doc["content"] for doc in docs]
    )
    
    print(response.data)
    print(len(response.data))
    
    conn = init_database()
    cursor = conn.cursor()
    
    for i, item in enumerate(response.data):
        cursor.execute('''
            INSERT INTO documents (name, content, embedding)
            VALUES (?, ?, ?)
        ''', (docs[i]["name"], docs[i]["content"], json.dumps(item.embedding)))
    
    conn.commit()
    conn.close()
    
    return [item.embedding for item in response.data]

if __name__ == "__main__":
    embeddings = upload_documents(MOCK_DOCS)
    print(f"Uploaded {len(embeddings)} documents with embeddings")