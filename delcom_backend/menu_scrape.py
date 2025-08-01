import requests
from authentication_util import get_cookie_and_csrf
from uber_parse_util import parse_uber_getSearchFeedV1, parse_uber_getStoreV1

ADDRESS = "Hyde St & Lombard St, San Francisco. CA"
FOOD = "Burrito"

cookie, csrf_token = get_cookie_and_csrf(ADDRESS)

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Cookie": cookie,
    "x-csrf-token": csrf_token,
}

URLgetSearchFeedV1 = "https://www.ubereats.com/_p/api/getSearchFeedV1"

PAYLOADgetSearchFeedV1 = {
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

# response.json() is a dictionary!!
restaurants = parse_uber_getSearchFeedV1(response.json())

test_rest = restaurants[0]
print(test_rest)

URLgetStoreV1 = "https://www.ubereats.com/_p/api/getStoreV1"

# eventually will be for more restaurants, but for now just testing with the first one

PAYLOADgetStoreV1 = {
    "cbType": "EATER_ENDORSED",
    "diningMode": "DELIVERY",
    "storeUuid": test_rest['storeUuid'],
    "time": {"asap": "true"}
}
print("Payload loaded ✓")

response2 = requests.post(URLgetStoreV1, headers=headers, json=PAYLOADgetStoreV1)
#print(response2.json())

print("Response 2 received ✓")

components = parse_uber_getStoreV1(response2.json())



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
print(response3.json())