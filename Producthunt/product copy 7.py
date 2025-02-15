from playwright.sync_api import sync_playwright
import sqlite3

def scrape_product_titles():
    """Scrapes product titles from Product Hunt and returns a list of titles."""
    with sync_playwright() as p:
        # Launch the browser (set headless=False for debugging)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to Product Hunt
        page.goto("https://www.producthunt.com/")
        
        # Wait for product sections to load (adjust timeout if needed)
        page.wait_for_selector("section[data-test^='post-item']", timeout=60000)
        
        # Locate all product sections
        product_sections = page.locator("section[data-test^='post-item']")
        count = product_sections.count()
        print(f"Found {count} product sections.")
        
        titles = []
        for i in range(count):
            try:
                # Check if there's at least one anchor with href starting with '/posts/' in this section
                anchor_locator = product_sections.nth(i).locator("a[href^='/posts/']")
                if anchor_locator.count() > 0:
                    # Retrieve the text content from the first such anchor
                    title = anchor_locator.first.text_content(timeout=15000)
                    if title:
                        cleaned_title = title.strip()
                        titles.append(cleaned_title)
                        print(f"Product section {i+1}: {cleaned_title}")
                    else:
                        print(f"Product section {i+1}: No title text found.")
                else:
                    print(f"Product section {i+1}: No anchor with href '/posts/' found.")
            except Exception as e:
                print(f"Error retrieving title for product section {i+1}: {e}")
        
        browser.close()
        return titles

def save_titles_to_db(titles):
    """Saves the list of titles into a SQLite database."""
    db_path = r"C:\Users\Asfand\AppData\Roaming\Python\Python311\Scripts\Producthunt\product_hunt.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the 'products' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')
    conn.commit()
    
    # Insert each title into the table
    for title in titles:
        cursor.execute("INSERT INTO products (title) VALUES (?)", (title,))
    
    conn.commit()
    conn.close()
    print("Data inserted into the database successfully!")

def main():
    titles = scrape_product_titles()
    if titles:
        save_titles_to_db(titles)
    else:
        print("No titles were scraped.")

if __name__ == "__main__":
    main()