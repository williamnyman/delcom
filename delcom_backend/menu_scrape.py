from playwright.sync_api import sync_playwright

food = 'Cheeseburger'
address = '1042 Clay St San Francisco, CA' 

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False, slow_mo=0)
    page = browser.new_page()
    page.goto("https://ubereats.com")

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

    page.fill('input#search-suggestions-typeahead-input', food)

    page.keyboard.press('Enter')
    page.wait_for_selector('[data-testid="search-feed-tab-sort-filter-container"] li:text("Restaurants")', state='visible')
    page.locator('[data-testid="search-feed-tab-sort-filter-container"] li', has_text="Restaurants").click()

    page.locator('button:has-text("Best overall")').click(force=True)

    input("Press Enter to close the browser...")