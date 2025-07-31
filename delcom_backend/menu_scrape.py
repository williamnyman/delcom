import requests
from authentication_util import get_cookie_and_csrf

ADDRESS = "980 NW Hillside Park Dr, Bend, OR"

cookie, csrf_token = get_cookie_and_csrf(ADDRESS)

url = "https://www.ubereats.com/_p/api/getSearchFeedV1"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Cookie": cookie,
    "x-csrf-token": csrf_token,
}


payload = {
    "userQuery": "Cheeseburger",
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

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text[:500])

print(response.status_code)
print(response.json())
