from openai import OpenAI
from dotenv import load_dotenv
import os

# Load variables from .env and get the API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


prompt = """
You are an AI that converts food cravings into a structured format for comparison with food delivery menu items.

Given a craving, extract the following fields:
- Title: the best short name for what they want
- Includes: specific ingredients or components they want
- Excludes: anything they say they don’t want
- Style: words that describe the vibe, tone, or situation (e.g. hangover, greasy, comfort food, light)

Then return a single string formatted like:
{Title} — {Includes} — Excludes: {Excludes} — {Style}

Examples:

Craving: “I want something greasy and huge to kill this hangover — like a breakfast burrito or loaded fries but nothing sweet.”
Output:  
Breakfast Burrito or Loaded Fries — bacon, egg, cheese, potato — Excludes: sweet items — greasy, hangover, filling

Craving: “Feeling kind of light, maybe sushi or poke, nothing with fried stuff though”
Output:  
Sushi or Poke — raw fish, rice, vegetables — Excludes: fried items — light, clean

Craving: “pad thai”
Output:  
Pad Thai — rice noodles, peanut sauce, vegetables — Excludes: none — Thai, savory
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

print(response.choices[0].message.content)
