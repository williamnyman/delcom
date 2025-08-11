import requests
from authentication_util import get_cookie_and_csrf
from uber_parse_util import parse_uber_getSearchFeedV1, parse_uber_getStoreV1, parse_uber_getInStoreSearchV1

# Constants: address/food, cookies/headers
ADDRESS = "1042 Clay St, San Francisco. CA"
FOOD = "Salmon"

cookie, csrf_token = get_cookie_and_csrf(ADDRESS)
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Cookie": cookie,
    "x-csrf-token": csrf_token,
}

# Step 1) getSearchFeedV1: get restaurants that match the food query
URLgetSearchFeedV1 = "https://www.ubereats.com/_p/api/getSearchFeedV1"
PAYLOADgetSearchFeedV1 = {
    # Only userQuery changes
    "userQuery": FOOD,
    "date": "",
    "startTime": 0,
    "endTime": 0,
    "sortAndFilters": [
        {
            "uuid": "f844706c-2b1b-4db2-b40a-13d43cb338da",  # Sort/filter category
            "options": [
                {"uuid": "12ce1932-1878-4e2e-80d0-5760c095c641"}  # Filter option
            ]
        }
    ],
    "vertical": "ALL",  
    "displayType": "SEARCH_RESULTS",
    "searchSource": "SEARCH_BAR",
    "searchType": "GLOBAL_SEARCH",
    "cacheKey": "",
    "keyName": "",
    "recaptchaToken": ""
}

response = requests.post(URLgetSearchFeedV1, headers=headers, json=PAYLOADgetSearchFeedV1)
restaurants = parse_uber_getSearchFeedV1(response.json())

test_rest = restaurants[0]
print(test_rest)
store_code = test_rest['storeUuid']

# Step 2) getStoreV1: get store UUIDs and section UUIDs for each restaurant
URLgetStoreV1 = "https://www.ubereats.com/_p/api/getStoreV1"
PAYLOADgetStoreV1 = {
    # Only storeUuid changes
    "storeUuid": test_rest['storeUuid'],
    "cbType": "EATER_ENDORSED",
    "diningMode": "DELIVERY",
    "time": {"asap": "true"}
}

response2 = requests.post(URLgetStoreV1, headers=headers, json=PAYLOADgetStoreV1)
components = parse_uber_getStoreV1(response2.json())


# Step 3) getInStoreSearchV1: get menu items that match the food query
URLgetInStoreSearchV1 = "https://www.ubereats.com/_p/api/getInStoreSearchV1"
PAYLOADgetInStoreSearchV1 = {
    # These dont change
    'diningMode': 'DELIVERY',
    'isGrocery': False,
    'entrypointContext': 'IN_STORE_SEARCH',

    # These do change
    'sectionUUIDs': components['sectionUUIDs'],
    'storeUUIDs': components['storeUUIDs'],
    'userQuery': FOOD,
    'targetLocation': components['location'],
}

response3 = requests.post(URLgetInStoreSearchV1, headers=headers, json=PAYLOADgetInStoreSearchV1)
menu_items = parse_uber_getInStoreSearchV1(response3.json())
test_item = menu_items[0]
print(test_item)

# # Step 4) getMenuItemV1: get detailed information about each menu item
URLgetMenuItemV1 = "https://www.ubereats.com/_p/api/getMenuItemV1"
PAYLOADgetMenuItemV1 = {
    # These dont change
    'itemRequestType': 'ITEM',
    'cbType': 'EATER_ENDORSED',
    'contextReferences': [
        {
            'type': 'GROUP_ITEMS',
            'payload': {
                'type': 'groupItemsContextReferencePayload',
                'groupItemsContextReferencePayload': {},
            },
            'pageContext': 'UNKNOWN',
        },
    ],

    # These do change
    'storeUuid': store_code,
    'sectionUuid': test_item['sectionuuid'],
    'subsectionUuid': test_item['subsectionuuid'],
    'menuItemUuid': test_item['menuitemuuid']
    
}

response4 = requests.post(URLgetMenuItemV1, headers=headers, json=PAYLOADgetMenuItemV1)
menu_item_details = response4.json()

# Assuming your JSON is stored in menu_item_details (as a Python dict)

customizations = menu_item_details.get("data", {}).get("customizationsList", [])

result = []
for customization in customizations:
    customization_title = customization.get("title", "")
    option_titles = [option.get("title", "") for option in customization.get("options", [])]
    result.append({
        "customization_title": customization_title,
        "options": option_titles
    })

# Example: print nicely
for c in result:
    print(f"Customization: {c['customization_title']}")
    for opt in c["options"]:
        print(f"  - {opt}")


# I NEED TO GO THRU ALL OF THIS CODE AND MAKE SURE IT IS ALL WORKING
# FIX REST. TAGS
# --- existing code above ---

response4 = requests.post(URLgetMenuItemV1, headers=headers, json=PAYLOADgetMenuItemV1)
menu_item_details = response4.json()

# -------- Build encoding --------
def _pick(*vals, default=None):
    for v in vals:
        if isinstance(v, dict):
            # if dicts are passed directly, skip (use explicit lookups below)
            continue
        if v not in (None, "", [], {}):
            return v
    return default

data = (menu_item_details or {}).get("data", {})

# 1) Item + restaurant names
item_name = _pick(test_item.get("title"), test_item.get("name"), default="Unknown Item")
restaurant_name = _pick(test_rest.get("name"), test_rest.get("title"), test_rest.get("storeName"), default="Unknown Restaurant")

# 2) Description
item_desc = _pick(data.get("itemDescription"), test_item.get("description"), default="")

# 3) Ingredients (use any field Uber provides; otherwise leave blank)
ingredients_list = _pick(
    data.get("ingredientsList"),
    data.get("ingredients"),
    data.get("defaultIngredients"),
    default=[]
)
if isinstance(ingredients_list, str):
    ingredients_list = [ingredients_list]
ingredients = ", ".join([str(x).strip() for x in ingredients_list]) if ingredients_list else ""

# 4) Options (flatten customizations)
customizations = data.get("customizationsList", []) or []
options_blocks = []
for cust in customizations:
    title = (cust or {}).get("title") or ""
    opts = [o.get("title", "") for o in (cust or {}).get("options", []) if o.get("title")]
    if title and opts:
        options_blocks.append(f"{title}: " + " | ".join(opts))
    elif opts:
        options_blocks.append(" | ".join(opts))
customizations_flat = "; ".join(options_blocks)

# 5) Restaurant tags
tags = test_rest.get("tags") or test_rest.get("categories") or []
if isinstance(tags, dict):  # sometimes comes nested
    tags = list(tags.values())
restaurant_tags = ", ".join([str(t) for t in tags]) if tags else ""

# 6) Meta: rating, ETA, price
# rating can appear in a few shapes
rating = _pick(
    test_rest.get("rating"),
    (test_rest.get("storeRating") or {}).get("value") if isinstance(test_rest.get("storeRating"), dict) else None,
    (test_rest.get("rating") or {}).get("value") if isinstance(test_rest.get("rating"), dict) else None,
    test_rest.get("avgRating"),
    default=""
)

# ETA min
eta_obj = test_rest.get("etaRange") or {}
eta_min = _pick(eta_obj.get("min"), test_rest.get("eta_min"), default="")

# Base price (cents) from detailed item if possible, else from search hit
base_price_cents = _pick(data.get("price"), test_item.get("price"), default=0) or 0
try:
    price_dollars = f"{(int(base_price_cents) / 100):.2f}"
except Exception:
    price_dollars = ""

# 7) Final encoding
encoding = (
    "[ITEM]\n"
    f"{item_name} — {restaurant_name}\n"
    f"Desc: {item_desc}\n"
    f"Ingredients: {ingredients}\n"
    f"Options: {customizations_flat}\n"
    f"Restaurant tags: {restaurant_tags}\n"
    f"Meta: rating {rating}, ETA {eta_min} min, price ${price_dollars}"
)

print("\n" + encoding + "\n")


# need to start constructing the following format:
# [ITEM]
# {item.name} — {restaurant.name}
# Desc: {item.description}
# Ingredients: {ingredients}
# Options: {customizations_flat}
# Restaurant tags: {restaurant.tags}
# Meta: rating {rating}, ETA {eta_min} min, price ${base_price_cents/100}





# ok got to the point where we have pulled the menu item details