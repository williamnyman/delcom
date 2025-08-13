from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from menu_scrape import scraper_uber_eats
from gpt_test import get_craving

# Load variables from .env and get the API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text.strip()
    )
    return response.data[0].embedding

CRAVING = get_craving() # craving pulled from gpt_test.py

EMB_CRAVING = get_embedding(CRAVING)

candidates = scraper_uber_eats()
best_candidate = None
best_similarity = -1

combos = []

for candidate in candidates:
    # Get the embedding for the candidate
    candidate_embedding = get_embedding(candidate)
    
    # Calculate cosine similarity
    similarity = cosine_similarity([EMB_CRAVING], [candidate_embedding])[0][0]
    
    if similarity > best_similarity:
        best_similarity = similarity
        best_candidate = candidate

    
print(f"Best candidate: {best_candidate} with similarity {best_similarity}")
