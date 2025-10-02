'''
uber_parse_util.py
Utility functions for handling JSON parsing for Uber Eats API responses.
Including parsing the getSearchFeedV1, getStoreV1 and ...
'''

from spinner_util import spinner_start, spinner_end
import time

def parse_uber_getSearchFeedV1(data):
    """
    Description:
    Parses a JSON file (as a dict) and extracts restaurant names and UUIDs

    Args:
    data (dict): JSON from getSearchFeedV1 API response as a dict

    Returns:
    restaurants (list of dicts) | Each dict contains 'title' and 'storeUuid' of a restaurant
    """

    if data.get("data", {}).get("feedItems", [{}])[0].get("uuid") == "no-results-found-for-search-refresh":
        return None

    # create empty list to hold restaurant data
    restaurants = []

    # Extracting restaurant names and UUIDs from the JSON data
    feedItems = data.get("data", {}).get("feedItems", [])
    for item in feedItems[:10]:
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
    components (dict) | Contains important components for in-store search: location, sectionUUIDs, storeUUIDs
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

    components.update({"categories": data.get("data", {}).get("categories", [])})    

    components.update({"rating" : data.get("data", {}).get("rating", {}).get("ratingValue")})
    components.update({"eta" : data.get("data", {}).get("etaRange", {}).get("text")})
    
    return components 

def parse_uber_getStoreV1_for_items(data):
    # need this as a return
    # 'sectionUuid': menu_item['sectionuuid'],
    # 'subsectionUuid': menu_item['subsectionuuid'],
    # 'menuItemUuid': menu_item['menuitemuuid']

    menu_items = []

    for section_id, section_content in data["catalogSectionsMap"].items():
        for block in section_content:
            catalog_items = block.get("payload", {}).get("standardItemsPayload", {}).get("catalogItems", [])
            for item in catalog_items:
                section_uuid = item.get("sectionUuid")
                subsection_uuid = item.get("subsectionUuid")
                menuitem_uuid = item.get("uuid")
                menu_items.append({
                    "sectionUuid": section_uuid,
                    "subsectionUuid": subsection_uuid,
                    "menuItemUuid": menuitem_uuid
                })



    # menu_items = []
    # item_ids = {
    #     "storeuuid": "",
    #     "sectionuuid": "",
    #     "subsectionuuid": "",
    #     "menuitemuuid": ""
    # }

    # data1 = data['data']
    # data2 = data1['catalogSectionsMap']


    # item_ids

    return menu_items

def parse_uber_getInStoreSearchV1(data):
    """
    Description:
    Parses a JSON file (as a dict) and extracts components needed for getMenuItemV1 API call

    Args:
    data (dict): JSON from getInStoreSearchV1 API response as a dict

    Returns:
    items (list of dicts) | Each dict contains storeUUID, sectionUUID, menuItemUUID, subsectionUUID of a menu item
    """
    items_list = []

    data = data["data"]["catalogSectionsMap"]

    for section_key, section_list in data.items():
        for section in section_list:
            #section_uuid = section.get("catalogSectionUUID")
            
            catalog_items = (
                section.get("payload", {})
                    .get("standardItemsPayload", {})
                    .get("catalogItems", [])
            )
            
            for item in catalog_items:
                menu_item_uuid = item.get("uuid")
                section_uuid = item.get("sectionUuid")
                subsection_uuid = item.get("subsectionUuid")
                menu_item_title = item.get("title")
                
                items_list.append({
                    "title": menu_item_title,
                    "sectionuuid": section_uuid,
                    "subsectionuuid": subsection_uuid,
                    "menuitemuuid": menu_item_uuid,
                })

    return items_list

def parse_uber_getMenuItemV1(data):
    """
    Parses a getMenuItemV1 API JSON dict and extracts:
      - item title (string)
      - price (float, dollars)
      - description (string)
      - customizations (list of customization titles and their options)

    Args:
        data (dict): Uber Eats getMenuItemV1 API response as dict

    Returns:
        dict: {
            "title": str,
            "price": float,
            "description": str,
            "customizations": list[dict]
        }
    """
    item = data.get("data", {})

    # Basic fields
    title = item.get("title", "")
    description = item.get("itemDescription", "")
    price = round(item.get("price", 0)/100,2)
    

    # Extract customizations
    customizations = []
    for cust in item.get("customizationsList", []):
        cust_title = cust.get("title", "")
        options = [opt.get("title", "") for opt in cust.get("options", [])]
        customizations.append({
            "title": cust_title,
            "options": options
        })

    return {
        "title": title,
        "price": price,
        "description": description,
        "customizations": customizations
    }

    
