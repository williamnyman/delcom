'''
authentication_util.py
Utility functions for handling authentication including cookie and CSRF token retrieval.
(just UE right now, will have functions for other services later which will all be for authentication)
'''

# imports
import requests
from playwright.sync_api import sync_playwright

def get_cookie_and_csrf(address):
    '''
    Description:
    Retrieves the cookie and CSRF token needed for authenticated requests to Uber Eats.
    The function uses Playwright to automate the browser interaction to get the 
    necessary cookies (this is because Uber Eats requires a valid session to access its API
    and a valid sessions cannot be emulated, must have a window for example).

    Args:
    address (string): user address to be filled in on Uber Eats home page

    Returns:
    cookie_str, csrf_cookie (string, string) | cookie string, CSRF token string
    '''

    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True, slow_mo=0) 
        context = browser.new_context()
        page = context.new_page()

        # Go to Uber Eats entry page (with address entry)
        page.goto("https://www.ubereats.com/")
        print("Uber Eats entry page ✓")

        # if "Enter Address Manually" popup occurs, close it
        if page.is_visible("button[title='Close']"):
            page.click("button[title='Close']")
            print("Popup closed ✓")

        # Wait for the address input to be visible (wait for popup to be closed) and fill it
        page.wait_for_selector('input#location-typeahead-home-input', state='visible')
        page.fill('input#location-typeahead-home-input', address)
        print("Address filled ✓")

        # Click the find food button, retry a few times in case the button is not immediately available (can be slow sometimes)
        #for i in range(5):
        while True:
            page.click('button[data-testid=find-food-button]')
            try:
                # The selector is waited for because then we are at the home page and we know we are in an active session and therefore can pull cookie/token
                page.wait_for_selector('input#search-suggestions-typeahead-input', timeout=2000, state='visible')
                break
            except:
                pass
        print("Uber eats home page ✓")

        # Get cookies and converts them to a string format because requests library expects a string
        cookies = context.cookies()
        cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

        # Try to find CSRF token in cookies
        csrf_cookie = next((c["value"] for c in cookies if c["name"] == "x-csrf-token"), None)

        # If not found in cookies, try from localStorage
        if not csrf_cookie:
            csrf_cookie = page.evaluate("() => localStorage.getItem('x-csrf-token')")
        print("Cookies retrieved ✓")

        browser.close()
        return cookie_str, csrf_cookie or "x"