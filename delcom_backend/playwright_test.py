from playwright.sync_api import sync_playwright

food = 'pizza'
address = '857 greenwich St San Francisco, CA' 

with sync_playwright() as p:

    browser = p.chromium.launch(slow_mo=0)
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


    page.wait_for_selector("button:has-text('View store')", state='visible')
    page.locator("button:has-text('View store')").first.click(force=True)

    # Wait for the input whose placeholder contains "Search in"
    input_locator = page.locator('input[placeholder*="Search in"]')

    # Fill the input with the variable food
    input_locator.fill(food)

    # click on the first menu item
    page.locator('li[data-testid*="store-item"]').first.click()
        
    # I DONT KNOW WHAT SYSTEM TO USE TO COMPARE THE REQUEST TO THE MENU ITEM

    input("Press Enter to close the browser...")