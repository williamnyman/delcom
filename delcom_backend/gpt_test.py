from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from spinner_util import spinner_start, spinner_end
import time

# Load variables from .env and get the API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# openai prompt for craving normalization
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

If the craving does not list an explicit core food infer a core food based on the rest of their craving
If the users craving is not sensible return "ERROR" in plain text. By not sensible I mean it is not related to food or is an
obivous trolling attempt. Ambiguous cravings should be infered as mentioned above. 

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

# get the users craving
# need to get it from the frontend 
def get_craving(craving):
    # Make a request
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[                       
            {"role": "system", "content": prompt},
            {"role": "user", "content": craving}        
        ],

    )

    # return the craving encoding
    craving_encoding = response.choices[0].message.content.strip()
    #print(craving_encoding)
    return craving_encoding
