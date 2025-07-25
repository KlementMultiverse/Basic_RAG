import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List

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
    
    print(response.data)
    print(len(response.data))
    
    return [item.embedding for item in response.data]

if __name__ == "__main__":
    embeddings = generate_embeddings(["Hello, world!", "Goodbye, world!", "My name is Mckay"])
    print(f"Generated {len(embeddings)} embeddings")