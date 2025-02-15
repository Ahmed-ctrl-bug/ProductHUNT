import sqlite3
import json

# Database path
db_path = r"C:\Users\Asfand\AppData\Roaming\Python\Python311\Scripts\Producthunt\product_hunt.db"

# Function to insert data into the database
def insert_data(data):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insert data into the table
    for product in data:
        cursor.execute('''
            INSERT INTO products (name, description)
            VALUES (?, ?)
        ''', (product["name"], product["description"]))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Data inserted successfully!")
    
# Function to load scraped data from product.py
def load_scraped_data():
    # Load the data scraped by product.py (Assuming it is saved in product_data.json)
    file_path = "product_data.json"  # Make sure product.py writes data here
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    try:
        scraped_data = load_scraped_data()
        if scraped_data:
            insert_data(scraped_data)
        else:
            print("No data to insert.")
    except FileNotFoundError:
        print("Error: 'product_data.json' file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")