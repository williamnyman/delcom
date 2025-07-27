from openai import OpenAI
from dotenv import load_dotenv
import os

# Load variables from .env and get the API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

craving = input("Enter your food craving: ")

# Make a request
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[                           # conversation history (including instructions)
        {"role": "system", "content": 
            "You are a helpful assistant that converts food cravings into structured data."

            "A user will describe what they're craving. Based on the text, extract the following fields:"

            "title: A short name for the item the user likely wants (e.g. “Pad Thai”, “Cheeseburger”, “Breakfast Burrito”)"

            "ingredients: Any specific additions or expected components (e.g. “chicken”, “bacon”, “extra cheese”)"

            "exclusions: Any ingredients the user explicitly does not want (e.g. “no green onion”, “no mayo”)"

            "qualities: Vague or emotional desires or food properties (e.g. “salty”, “greasy”, “hangover food”)"

            "Only extract qualities if you cannot extract a title."
            
            "If any of these fields are not mentioned, leave them blank."},
        {"role": "user", "content": craving}        
    ],

)

print(response.choices[0].message.content)
