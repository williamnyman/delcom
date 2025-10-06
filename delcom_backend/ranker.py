from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from menu_scrape import scraper_uber_eats
from gpt_test import get_craving
from spinner_util import spinner_start, spinner_end
import time
import re

def parse_item_string(encoding: str):
    """
    Parses an encoded item string into structured fields.
    """

    lines = encoding[0].strip().split("\n")
    print("Parsing item string lines:", lines)
    
    # First line is [ITEM], skip it
    _, name_line, desc_line, options_line, tags_line, meta_line = lines

    # Parse item name and restaurant name
    if "—" in name_line:
        item_name, restaurant_name = map(str.strip, name_line.split("—"))
    
    else:
        item_name = name_line.strip()
        restaurant_name = ""

    print("Item name:", item_name)

    # Parse description
    item_desc = desc_line.replace("Desc:", "").strip()

    # Parse options
    customizations = options_line.replace("Options:", "").strip()

    # Parse restaurant tags
    restaurant_tags = tags_line.replace("Restaurant tags:", "").strip().split(",")

    # ---- Parse meta info (rating, ETA, price) using splitting ----
    meta_line = meta_line.replace("Meta:", "").strip()
    parts = [p.strip() for p in meta_line.split(",")]
    print("Meta parts:", parts)

    
    rating = float(parts[0][6:])   
    print(rating)      # "rating 4.6" → 4.6
    eta = int(parts[1].split()[1].split("–")[0])       
    print(eta)    # "ETA 25 min" → 25
    price = float(parts[2][7:])      # "$12.99" → 12.99
    print(price)

    

    return {
        "item_name": item_name,
        "restaurant_name": restaurant_name,
        "item_desc": item_desc,
        "customizations": customizations,
        "restaurant_tags": [tag.strip() for tag in restaurant_tags if tag.strip()],
        "meta": {
            "rating": rating,
            "eta": eta,
            "price": price
        },
        "image_url": encoding[1]
    }


def get_embedding(text: str, client) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text.strip()
    )
    return response.data[0].embedding

def extract_core_food(text):
    # Look for a line starting with "Title:" and capture everything after it
    match = re.search(r"Title:\s*(.+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None
# ------------------------------------------------------------------------------

def ranker_main(craving, address, progress_callback=None):

    print("craving received in ranker_main:", craving)
    print("address received in ranker_main:", address)
    if progress_callback: progress_callback(5)

   
    # Load variables from .env and get the API key
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    if progress_callback: progress_callback(10)


    # gets the craving ENCODING
    # need to pass whatever the user typed in the craving box
    CRAVING = get_craving(craving)
    if progress_callback: progress_callback(15)



    # need a function here to get the food name
    food_title = extract_core_food(CRAVING)


    EMB_CRAVING = get_embedding(CRAVING, client)
    if progress_callback: progress_callback(20)


    
    # need the logic here to get the first food name 
    # and then can put it in the scraper VVVV

    # bunch of pairs of (encoding string, image url)
    candidates = scraper_uber_eats(food_title, address, progress_callback)

    if progress_callback: progress_callback(95)

    best_candidate = None
    best_similarity = -1

    for candidate in candidates:
        # Get the embedding for the candidate encoding string
        candidate_embedding = get_embedding(candidate[0], client)
        
        # Calculate cosine similarity
        similarity = cosine_similarity([EMB_CRAVING], [candidate_embedding])[0][0]
        
        if similarity > best_similarity:
            best_similarity = similarity
            # still is a pair (encoding, image url)
            best_candidate = candidate
            


    print("Best candidate string:", best_candidate)
    print("Best similarity score:", best_similarity)
    
    if progress_callback: progress_callback(100)
    return parse_item_string(best_candidate)

        
# print(f"Best candidate: {best_candidate} with similarity {best_similarity}")
