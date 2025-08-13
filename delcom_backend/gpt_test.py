from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load variables from .env and get the API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")





prompt = """
You are a data normalizer for a food matching app.

Given a user's craving, extract and normalize the key details into the following structured text format for semantic embedding.

Rules:
- The Title must be ONLY the core food term that could be searched directly on a delivery platform (e.g., "cheeseburger", "pad thai", "pepperoni pizza").
- Do NOT include toppings, ingredients, dietary restrictions, or other modifiers in the Title.
- Describe desired flavors, ingredients, or other relevant notes in the Desc section (plain text).
- In the Options section, include additions and removals as:
  - add <comma-separated list of additions>
  - remove <comma-separated list of removals>
  If nothing to add or remove, leave that part empty.
- Restaurant tags: list any preferred cuisines or restaurant types or vibes (comma-separated), otherwise leave empty.
- Meta: include constraints like max price, max ETA, min rating

Format:
[CRAVING]
Title: <core food>
Desc: <desired flavors/ingredients/notes in plain text>
Options: add <items>; remove <items>
Restaurant tags: <preferred cuisines/tags>
Meta: max price $<num>, max ETA <min> min, min rating <num>
"""

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def get_craving():
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
    return craving_encoding
