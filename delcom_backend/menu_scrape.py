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
print(menu_item_details)


# ok got to the point where we have pulled the menu item details