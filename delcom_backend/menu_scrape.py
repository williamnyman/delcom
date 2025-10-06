import requests
from authentication_util import get_cookie_and_csrf
from uber_parse_util import parse_uber_getSearchFeedV1, parse_uber_getStoreV1,parse_uber_getStoreV1_for_items, parse_uber_getMenuItemV1 #, parse_uber_getInStoreSearchV1
from spinner_util import spinner_start, spinner_end
import time

# add food as a parameter
def scraper_uber_eats(FOOD, ADDRESS, progress_callback=None):
    # Constants: address/food, cookies/headers
    # ADDRESS = "857 Greenwich St, San Francisco. CA"
    #FOOD = "pizza"

    cookie, csrf_token = get_cookie_and_csrf(ADDRESS)
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Cookie": cookie,
        "x-csrf-token": csrf_token,
    }

    candidates = []

    # Step 1) getSearchFeedV1: get restaurants that match the food query
    URLgetSearchFeedV1 = "https://www.ubereats.com/_p/api/getSearchFeedV1"


    backup_sortAndFilters = {
        "bestOverall": [
            {
                "uuid": "f844706c-2b1b-4db2-b40a-13d43cb338da",  # Sort/filter category
                "options": [
                    {"uuid": "12ce1932-1878-4e2e-80d0-5760c095c641"}  # Filter option
                ]
            }
        ],
        "under30Min": [
            {
                'uuid': 'cc5cdb95-a6e6-4371-8d10-a07c2175e509',
                'options': [
                    {
                        'uuid': 'cc5cdb95-a6e6-4371-8d10-a07c2175e510',
                    },
                ],
            },
        ],
        "ratingOver4_5": [
            {
                'uuid': 'b19c8978-203c-4a89-a23e-e4842febe4ff',
                'options': [
                    {
                        'uuid': '2c7cf7ef-730f-431f-9072-26bc39f7c043',
                    },
                ],
            }
        ],
        "default": []
    }

    

    PAYLOADgetSearchFeedV1 = {
        # Only userQuery changes
        "userQuery": FOOD,
        "date": "",
        "startTime": 0,
        "endTime": 0,
        "sortAndFilters": [], # placeholder for sortAndFilters
        "vertical": "ALL",  
        "displayType": "SEARCH_RESULTS",
        "searchSource": "SEARCH_BAR",
        "searchType": "GLOBAL_SEARCH",
        "cacheKey": "",
        "keyName": "",
        "recaptchaToken": ""
    }

    for name, filterID in backup_sortAndFilters.items():
        print("Searching for restaurants with filter:", name)
        PAYLOADgetSearchFeedV1["sortAndFilters"] = filterID
        response = requests.post(URLgetSearchFeedV1, headers=headers, json=PAYLOADgetSearchFeedV1)
        restaurants = parse_uber_getSearchFeedV1(response.json())
        if restaurants is not None:
            break

    total_restaurants = len(restaurants)
    
    for i, restaurant in enumerate(restaurants, start = 1):
        if progress_callback:
            progress = 25 + int((i / total_restaurants) * 70)
            progress_callback(progress)
        print("NEW RESTAURANT" + "----------------------"*20 + restaurant['title'])


# Step 2) getStoreV1: get store UUIDs and section UUIDs for each restaurant
# and also get menu items now!
        URLgetStoreV1 = "https://www.ubereats.com/_p/api/getStoreV1"
        PAYLOADgetStoreV1 = {
            # Only storeUuid changes
            "storeUuid": restaurant['storeUuid'],
            "cbType": "EATER_ENDORSED",
            "diningMode": "DELIVERY",
            "time": {"asap": "true"}
        }



        response2 = requests.post(URLgetStoreV1, headers=headers, json=PAYLOADgetStoreV1)
        components = parse_uber_getStoreV1(response2.json())
        menu_items = parse_uber_getStoreV1_for_items(response2.json())

        if components is None or menu_items is None:
            print("Skipping restaurant due to failed data retrieval.")
            continue
        
        for menu_item in menu_items[:5]: #[:20]:

# Step 3) getMenuItemV1: get detailed information about each menu item
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
                'storeUuid': restaurant['storeUuid'],
                'sectionUuid': menu_item['sectionuuid'],
                'subsectionUuid': menu_item['subsectionuuid'],
                'menuItemUuid': menu_item['menuitemuuid']        
            }

            response4 = requests.post(URLgetMenuItemV1, headers=headers, json=PAYLOADgetMenuItemV1)
            menu_item_details = parse_uber_getMenuItemV1(response4.json())
            # now details includes title, price, desc, customizations, image url
            item_name = menu_item_details['title']
            item_desc = menu_item_details['description']

            customizations = menu_item_details['customizations']
            string = ""
            for customization in customizations:
                string += customization['title'] + ": "
                string += ", ".join(customization['options']) + "; "
            customizations = string.strip("; ")

            restaurant_name = restaurant['title']
            restaurant_tags = components['categories']
            rating = components['rating']
            eta = components['eta']
            price = menu_item_details['price']

            encoding = (
                "[ITEM]\n"
                f"{item_name} — {restaurant_name}\n"
                f"Desc: {item_desc}\n"
                f"Options: {customizations}\n"
                f"Restaurant tags: {restaurant_tags}\n"
                f"Meta: rating {rating}, ETA {eta} min, price ${price}"
            )

            item_url = menu_item_details['image_url']

            candidates.append((encoding, item_url))

            print("\n" + encoding + "\n")

        

    print("Total candidates found:", len(candidates))


    return candidates

