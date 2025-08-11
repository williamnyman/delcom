from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load variables from .env and get the API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text.strip()
    )
    return response.data[0].embedding


prompt = """
You are a data normalizer for a food matching app.

Given a user’s craving, extract and normalize the key details into the following structured text format for semantic embedding.

Rules:
- The Title must be ONLY the core food name that can be searched directly on a delivery platform (e.g., "cheeseburger", "pad thai", "pepperoni pizza").
- Do NOT include modifiers like toppings, ingredients, or dietary restrictions in the Title.
- Put additional required details in the Must section.
- Put ingredients or attributes to avoid in the Avoid section.
- Vibe describes the desired quality or feel (cheap, fast, healthy, gourmet, etc.).
- Diet lists dietary restrictions if any, otherwise "none".
- Notes include constraints like budget, ETA, or other relevant context.

Format:
[CRAVING] Title: <core food>
Must: <comma-separated must-have details>
Avoid: <comma-separated avoid items>
Vibe: <comma-separated vibe words>
Diet: <diet restrictions or 'none'>
Notes: <constraints and other context>
"""

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

craving = input("Enter your food craving: ")


# Make a request
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[                           # conversation history (including instructions)
        {"role": "system", "content": prompt},
        {"role": "user", "content": craving}        
    ],

)

craving_encoding = response.choices[0].message.content.strip()
print(craving_encoding)

craving_embedding = get_embedding(craving_encoding)