'''
uber_parse_util.py
Utility functions for handling JSON parsing for Uber Eats API responses.
Including parsing the getSearchFeedV1, getStoreV1 and ...
'''

def parse_uber_getSearchFeedV1(data):
    """
    Description:
    Parses a JSON file (as a dict) and extracts restaurant names and UUIDs

    Args:
    data (dict): JSON from getSearchFeedV1 API response as a dict

    Returns:
    restaurants (list of dicts) | Each dict contains 'title' and 'storeUuid' of a restaurant
    """
    # create empty list to hold restaurant data
    restaurants = []

    # Extracting restaurant names and UUIDs from the JSON data
    feedItems = data.get("data", {}).get("feedItems", [])
    for item in feedItems:
        store_name = item.get("store", {}).get("title", {}).get("text", "")
        store_uuid = item.get("store", {}).get("storeUuid", "")

        restaurants.append({
            "title": store_name,
            "storeUuid": store_uuid
        })

    return restaurants


def parse_uber_getStoreV1(data):
    """
    Description:
    Parses a JSON file (as a dict) and extracts Section UUIDS, Store UUIDs, target location

    Args:
    data (dict): JSON from getStoreV1 API response as a dict

    Returns:
    restaurants (list of dicts) | Each dict contains 'title' and 'storeUuid' of a restaurant
    """
    # create empty list to hold restaurant data
    components = {}

    # Target location to be used in in-store search is the exact same as the one used in gotten from getStoreV1
    components.update({"location": data["data"]["location"]})

    sectionUUIDs = []
    for section in data.get("data", {}).get("sections", []):
        sectionUUIDs.append(section.get("uuid", ""))
    components.update({"sectionUUIDs": sectionUUIDs})

    components.update({"storeUUIDs": [data["data"]["uuid"]]})    
    
    # already have query
    
    

    return components 



