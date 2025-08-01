import json
import requests
from playwright.sync_api import sync_playwright

def get_cookie_and_csrf(address):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Go to Uber Eats
        page.goto("https://www.ubereats.com/")

        if page.is_visible("button[title='Close']"):
            page.click("button[title='Close']")
            print('Popup closed.')

        page.wait_for_selector('input#location-typeahead-home-input', state='visible')
        page.fill('input#location-typeahead-home-input', address)

        for i in range(5):
            page.click('button[data-testid=find-food-button]')
            try:
                page.wait_for_selector('input#search-suggestions-typeahead-input', timeout=2000, state='visible')
                break
            except:
                pass

        # Get cookies
        cookies = context.cookies()
        cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

        # Try to find CSRF token in cookies
        csrf_cookie = next((c["value"] for c in cookies if c["name"] == "x-csrf-token"), None)

        # If not found in cookies, try from localStorage
        if not csrf_cookie:
            csrf_cookie = page.evaluate("() => localStorage.getItem('x-csrf-token')")

        browser.close()
        return cookie_str, csrf_cookie or "x"