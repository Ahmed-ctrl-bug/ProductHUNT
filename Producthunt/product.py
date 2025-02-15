import sqlite3
from playwright.sync_api import sync_playwright

def scrape_all_elements():
    with sync_playwright() as p:
        # Launch the browser in headless mode (set headless=False to debug visually)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to Product Hunt
        page.goto("https://www.producthunt.com/")
        
        # Wait for the main product sections to load using an XPath selector
        page.wait_for_selector("xpath=/html/body/div[1]/div[3]/main/div/div[1]/section", timeout=60000)
        
        # Locate all section elements (each product section)
        sections_locator = page.locator("xpath=/html/body/div[1]/div[3]/main/div/div[1]/section")
        num_sections = sections_locator.count()
        print(f"Found {num_sections} sections.")
        
        # List to store scraped data as tuples: (section_number, link_index, text, href)
        data = []
        
        # Loop over each section (XPath indices start at 1)
        for i in range(1, num_sections + 1):
            # Construct the XPath for all <a> elements within section[i]
            xpath_links = f"/html/body/div[1]/div[3]/main/div/div[1]/section[{i}]/div/a"
            links_locator = page.locator(f"xpath={xpath_links}")
            num_links = links_locator.count()
            print(f"Section {i} has {num_links} link(s).")
            
            # Loop over each link element in the current section
            for j in range(1, num_links + 1):
                try:
                    # Get text content and href attribute from the element
                    element_locator = page.locator(f"xpath={xpath_links}[{j}]")
                    text = element_locator.text_content(timeout=10000)
                    href = element_locator.get_attribute("href")
                    if text:
                        text = text.strip()
                    else:
                        text = ""
                    data.append((i, j, text, href))
                    print(f"Section {i}, Link {j}: {text}, href: {href}")
                except Exception as e:
                    print(f"Error retrieving link {j} in section {i}: {e}")
        
        browser.close()
        return data

def save_data_to_db(data):
    # Path to the SQLite database file (update as needed)
    db_path = r"C:\Users\Asfand\AppData\Roaming\Python\Python311\Scripts\Producthunt\product_hunt.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the table to store product elements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section_number INTEGER,
            link_index INTEGER,
            text TEXT,
            href TEXT
        )
    ''')
    conn.commit()
    
    # Insert each record into the table
    for record in data:
        cursor.execute('''
            INSERT INTO product_elements (section_number, link_index, text, href)
            VALUES (?, ?, ?, ?)
        ''', record)
    
    conn.commit()
    conn.close()
    print("Data saved to the database successfully!")

def main():
    scraped_data = scrape_all_elements()
    if scraped_data:
        save_data_to_db(scraped_data)
    else:
        print("No data scraped.")

if __name__ == "__main__":
    main()