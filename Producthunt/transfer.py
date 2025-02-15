import sqlite3

# Sample scraped data – update this list with your actual data.
scraped_data = [
    ("1. DeskMinder", "/posts/deskminder"),
    ("Create quick desktop reminders with just one click", "/posts/deskminder"),
    ("2. Entie - Couple Assistant", "/posts/entie-couple-assistant"),
    ("Personalized romantic relationship assistant for couples", "/posts/entie-couple-assistant"),
    ("3. Subtrace", "/posts/subtrace"),
    ("Resolve production issues faster", "/posts/subtrace"),
    ("4. Nia", "/posts/nia"),
    ("AI code agent that actually understands your codebase", "/posts/nia"),
    ("5. Sefirah", "/posts/sefirah"),
    ("An opensource way of connecting your Android and Windows", "/posts/sefirah"),
    ("6. Kann for Android", "/posts/kann-for-android"),
    ("Learn Japanese vocabulary you care about!", "/posts/kann-for-android"),
    ("7. Lovify", "/posts/lovify"),
    ("Enhance your Lovable.dev experience", "/posts/lovify")
]

def transfer_data_to_products():
    # Define the path to your SQLite database
    db_path = r"C:\Users\Asfand\AppData\Roaming\Python\Python311\Scripts\Producthunt\product_hunt.db"
    
    # Connect to the database (this will create the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop the existing table if it exists
    cursor.execute("DROP TABLE IF EXISTS products")
    
    # Create the new products table with the desired columns
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            href TEXT
        )
    ''')
    conn.commit()
    
    # Insert the scraped data into the products table
    cursor.executemany("INSERT INTO products (title, href) VALUES (?, ?)", scraped_data)
    
    conn.commit()
    conn.close()
    print("Data transferred into table 'products' successfully!")

if __name__ == "__main__":
    transfer_data_to_products()