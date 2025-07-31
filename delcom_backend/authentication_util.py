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

        # Enter address
        page.get_by_label("Enter delivery address").fill(address)
        page.keyboard.press("Enter")
        page.wait_for_timeout(3000)

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

address = "1042 Clay St, San Francisco, CA 94108-1510"
cookie_str, csrf_token = get_cookie_and_csrf(address)
print(f"Cookie: {cookie_str}")
print(f"CSRF Token: {csrf_token}")