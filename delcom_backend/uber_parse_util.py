import json


def parse_uber_getSearchFeedV1(data):
    """
    Description:
    Parses a JSON file (as a dict) and extracts restaurant names and UUIDs

    Args:
    data (dict): JSON from getSearchFeedV1 API response as a dict

    Returns:
    restaurants | list of dicts: Each dict contains 'title' and 'storeUuid' of a restaurant
    """

    restaurants = []

    feedItems = data.get("data", {}).get("feedItems", [])
    for item in feedItems:
        store_name = item.get("store", {}).get("title", {}).get("text", "")
        store_uuid = item.get("store", {}).get("storeUuid", "")

        restaurants.append({
            "title": store_name
            "storeUuid": store_uuid
        })

    return restaurants



