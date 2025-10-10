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

# once we get the best candidate from the ranker we parse it to send as
# results to the frontend
# def parse_item_string(encoding: str):
#     # once we get the best candidate from the ranker we parse it to send as
#     # results to the frontend

#     # takes the encoding and splits it up into a bunch of lines
#     # if this continues to give me issues then i will just restructure the parsing to be hard coded
#     lines = encoding[0].strip().split("\n")
#     for line in lines:
#         print(line)


#     # First line is [ITEM], skip it
#     _, name_line, desc_line, options_line, tags_line, meta_line = lines

#     # Parse item name and restaurant name
#     if "—" in name_line:
#         item_name, restaurant_name = map(str.strip, name_line.split("—"))
    
#     else:
#         item_name = name_line.strip()
#         restaurant_name = ""

#     print("Item name:", item_name)

#     # Parse description
#     item_desc = desc_line.replace("Desc:", "").strip()

#     # Parse options
#     customizations = options_line.replace("Options:", "").strip()

#     # Parse restaurant tags
#     restaurant_tags = tags_line.replace("Restaurant tags:", "").strip().split(",")

#     # ---- Parse meta info (rating, ETA, price) using splitting ----
#     meta_line = meta_line.replace("Meta:", "").strip()
#     parts = [p.strip() for p in meta_line.split(",")]
#     print("Meta parts:", parts)

#     # clean up meta data
#     rating = float(parts[0][6:])   
#     print(rating)      # "rating 4.6" → 4.6
#     eta = int(parts[1].split()[1].split("–")[0])       
#     print(eta)    # "ETA 25 min" → 25
#     price = float(parts[2][7:])      # "$12.99" → 12.99
#     print(price)

    
#     # construct and return dict/json of candidate
#     return {
#         "item_name": item_name,
#         "restaurant_name": restaurant_name,
#         "item_desc": item_desc,
#         "customizations": customizations,
#         "restaurant_tags": [tag.strip() for tag in restaurant_tags if tag.strip()],
#         "meta": {
#             "rating": rating,
#             "eta": eta,
#             "price": price
#         },
#         "image_url": encoding[1]
#     }

def parse_item_string(encoding: tuple):
    """
    Parses an encoding string of the form:
    [ITEM]
    item_name — restaurant_name
    Desc: ...
    Options: ...
    Restaurant tags: ...
    Meta: rating X, ETA Y min, price $Z
    """

    text = encoding[0]
    url_info = encoding[1]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        print(line)

    # --- Parse name/restaurant ---
    item_name, restaurant_name = "", ""
    for line in lines:
        if line.startswith("[ITEM]"):
            continue
        if "—" in line:
            item_name, restaurant_name = map(str.strip, line.split("—", 1))
            break
        else:
            item_name = line.strip()
            restaurant_name = ""
            break

    print("Item name:", item_name)

    # --- Parse description ---
    item_desc = ""
    for line in lines:
        if line.startswith("Desc:"):
            item_desc = line.replace("Desc:", "").strip()

    # --- Parse options ---
    customizations = ""
    for line in lines:
        if line.startswith("Options:"):
            customizations = line.replace("Options:", "").strip()

    # --- Parse tags ---
    restaurant_tags = []
    for line in lines:
        if line.startswith("Restaurant tags:"):
            raw = line.replace("Restaurant tags:", "").strip()
            restaurant_tags = [tag.strip() for tag in raw.split(",") if tag.strip()]

    # --- Parse meta ---
    rating = eta = price = None
    for line in lines:
        if line.startswith("Meta:"):
            meta = line.replace("Meta:", "").strip()
            parts = [p.strip() for p in meta.split(",")]

            # Expect parts like: "rating 4.6", "ETA 25 min", "price $12.99"
            try:
                rating = float(parts[0][6:]) if len(parts) > 0 else None
                eta = int(parts[1].split()[1].split("–")[0]) if len(parts) > 1 else None
                price = float(parts[2][7:]) if len(parts) > 2 else None
            except Exception as e:
                print("Meta parsing failed:", e, "parts:", parts)

    print("Meta -> rating:", rating, "eta:", eta, "price:", price)

    # --- Build result dict ---
    return {
        "item_name": item_name,
        "restaurant_name": restaurant_name,
        "item_desc": item_desc,
        "customizations": customizations,
        "restaurant_tags": restaurant_tags,
        "meta": {
            "rating": rating,
            "eta": eta,
            "price": price
        },
        "url_info": url_info
        # "image_url": url_info['image_url'],
        # "action_url": url_info['action_url'],
        # "store_uuid": url_info['store_uuid'],
        # "section_uuid": url_info['section_uuid'],
        # "subsection_uuid": url_info['subsection_uuid'],
        # "item_uuid": url_info['item_uuid']
    }


# craving at start and each candidate are passed through this to get the embedding vector
def get_embedding(text: str, client) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text.strip()
    )
    return response.data[0].embedding

# get the core food from the encoding to know what to search for
def extract_core_food(text):
    # Look for a line starting with "Title:" and capture everything after it
    match = re.search(r"Title:\s*(.+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None
# ------------------------------------------------------------------------------

# quite literally the function that does everything, this is
# the result that is passed to the frontend
def ranker_main(craving, address, progress_callback=None):
    print("craving received in ranker_main:", craving)
    print("address received in ranker_main:", address)
    if progress_callback: 
        progress_callback(5)

    # Load variables from .env and get the API key
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    if progress_callback: 
        progress_callback(10)

    # Encode craving
    CRAVING = get_craving(craving)

    if 'ERROR' in CRAVING:
        # need to go back to home screen with an error message
        return {"error" : "please enter a valid address and a sensible craving"}


    if progress_callback: 
        progress_callback(15)

    food_title = extract_core_food(CRAVING)

    # embed the craving into a vector
    EMB_CRAVING = get_embedding(CRAVING, client)
    if progress_callback: 
        progress_callback(20)

    # Get candidates from scraper
    candidates = scraper_uber_eats(food_title, address, progress_callback)

    if candidates == -1:
        return {"error" : "please enter a valid address and a sensible craving"}


    if progress_callback: 
        progress_callback(95)

    # Compute similarity for all candidates
    scored_candidates = []
    for candidate in candidates:
        candidate_embedding = get_embedding(candidate[0], client)
        similarity = cosine_similarity([EMB_CRAVING], [candidate_embedding])[0][0]
        scored_candidates.append((candidate, similarity))

    # Sort by similarity (descending) and take top 4
    top_candidates = sorted(scored_candidates, key=lambda x: x[1], reverse=True)[:4]

    # print("Top 4 candidates:")
    # for cand, score in top_candidates:
    #     print(f"Candidate: {cand}, Score: {score}")

    if progress_callback: 
        progress_callback(100)

    # Return the parsed versions
    
    return [parse_item_string(cand) for cand, _ in top_candidates]


        
# print(f"Best candidate: {best_candidate} with similarity {best_similarity}")
