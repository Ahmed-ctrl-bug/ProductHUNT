from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Launch the browser (set headless=False for visual debugging)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to Product Hunt
        page.goto("https://www.producthunt.com/")

        # Wait for the main container of sections to load.
        # (This XPath is based on your example; adjust if needed.)
        page.wait_for_selector("xpath=/html/body/div[1]/div[3]/main/div/div[1]/section", timeout=60000)

        # Get all section elements following the pattern:
        # /html/body/div[1]/div[3]/main/div/div[1]/section[i]
        sections = page.locator("xpath=/html/body/div[1]/div[3]/main/div/div[1]/section")
        sections_count = sections.count()
        print(f"Found {sections_count} sections.")

        # Iterate over each section
        for i in range(sections_count):
            # Construct the XPath for all <a> elements within the section:
            # /html/body/div[1]/div[3]/main/div/div[1]/section[i+1]/div/a[j]
            section_xpath = f"/html/body/div[1]/div[3]/main/div/div[1]/section[{i+1}]/div/a"
            a_elements = page.locator(f"xpath={section_xpath}")
            a_count = a_elements.count()
            print(f"Section {i+1} has {a_count} link(s).")

            # Iterate over each <a> element in the current section
            for j in range(a_count):
                try:
                    text = a_elements.nth(j).text_content(timeout=10000)
                    print(f"Section {i+1}, Link {j+1}: {text}")
                except Exception as e:
                    print(f"Error retrieving text for Section {i+1}, Link {j+1}: {e}")

        browser.close()

if __name__ == "__main__":
    main()