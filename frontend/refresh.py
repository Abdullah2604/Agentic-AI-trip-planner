import sqlite3
import requests
from datetime import datetime

# Fetch data (replace with the actual data source)
def fetch_attractions():
    url = 'https://api.visitdubai.com/attractions'  # Replace with actual data source
    response = requests.get(url)
    attractions = response.json()  # Assuming the response is in JSON format
    return attractions

# Normalize data (category/tags, price range, etc.)
def normalize_data(attractions):
    for attraction in attractions:
        # Normalize category/tags
        attraction['category'] = attraction['category'].strip().lower()
        attraction['tags'] = ','.join(attraction['tags']).lower()

        # Normalize price range (for example, categorize it as 'Low', 'Medium', 'High')
        if attraction['price_range'] <= 50:
            attraction['price_range'] = 'Low'
        elif 51 <= attraction['price_range'] <= 150:
            attraction['price_range'] = 'Medium'
        else:
            attraction['price_range'] = 'High'
    
    return attractions

# Update attractions in the database
def update_attractions(db_path, attractions):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for attraction in attractions:
        cursor.execute('''
            INSERT OR REPLACE INTO attractions (id, name, location, category, price_range, tags, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            attraction['id'], 
            attraction['name'], 
            attraction['location'], 
            attraction['category'], 
            attraction['price_range'], 
            attraction['tags'], 
            attraction['description']
        ))

    conn.commit()
    conn.close()

# Refresh data (fetch and update)
def refresh_data():
    db_path = 'db.sqlite'
    attractions = fetch_attractions()  # Fetch the data
    normalized_attractions = normalize_data(attractions)  # Normalize the data
    update_attractions(db_path, normalized_attractions)  # Update the database with fresh data
    print(f"Data refreshed at {datetime.now()}")

# Run the refresh task (once every 12 hours or at startup)
if __name__ == "__main__":
    refresh_data()
