from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Launch the browser in non-headless mode so you can see what's happening
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to Product Hunt
        page.goto("https://www.producthunt.com/")
        
        # Wait for the elements to load using the provided XPaths
        page.wait_for_selector("xpath=/html/body/div[1]/div[3]/main/div/div[1]/section[1]/div/a[1]", timeout=60000)
        page.wait_for_selector("xpath=/html/body/div[1]/div[3]/main/div/div[1]/section[2]/div/a[1]", timeout=60000)
        
        # Extract text content from the elements using their XPaths
        title1 = page.locator("xpath=/html/body/div[1]/div[3]/main/div/div[1]/section[1]/div/a[1]").text_content()
        title2 = page.locator("xpath=/html/body/div[1]/div[3]/main/div/div[1]/section[2]/div/a[1]").text_content()
        
        # Print the titles to the console
        print("Title 1:", title1)
        print("Title 2:", title2)
        
        browser.close()

if __name__ == "__main__":
    main()