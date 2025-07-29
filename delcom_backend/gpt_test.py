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
You are an AI that converts food cravings into a structured format for comparison with food delivery menu items.

Given a craving, extract the following fields:
- Title: the best short name for what they want
- Includes: specific ingredients or components they want
- Excludes: any speficic ingredients they say they don’t want
- Style: words that describe the vibe, tone, or situation (e.g. hangover, greasy, comfort food, light)

Then return a single string formatted like:
{Title} — {Includes} — Excludes: {Excludes} — {Style}

If the craving does not explicitly mention a food and only mentions a cuisine or type of food, use "Not specified" as the title

If they dont mention any specific toppings or ingredients use "Not specified" for Includes

If they do not mention any specific ingredients to exclude, use "Not specified" for Excludes

Examples:

Craving: “I want something greasy and huge to kill this hangover — like a breakfast burrito or loaded fries but nothing sweet.”
Output:  
Breakfast Burrito or Loaded Fries — Not specified — Excludes: Not Specified — greasy, hangover, filling

Craving: “Feeling kind of light, maybe sushi or poke, nothing with fried stuff though”
Output:  
Sushi or Poke — Not specified — Excludes: Not specified — light, clean

Craving: “pad thai”
Output:  
Pad Thai — Not specified — Excludes: Not specified — Thai, savory

Craving: “I want a cheeseburger that has lettuce on it and make sure there are not tomatoes”
Output:  
Cheeseburger — Lettuce — Excludes: Tomatos — classic, comfort food

Craving: “I want chicken pad thai”
Output:  
Pad Thai — Chicken — Excludes: Not specified — Thai, savory
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