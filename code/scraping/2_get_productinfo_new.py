import http.client
import json
import pandas as pd
import csv
import os
from dotenv import load_dotenv
load_dotenv()

# API request headers
API_HOST = "sephora14.p.rapidapi.com"
headers = {
    'x-rapidapi-key': os.getenv("API_KEY"),
    'x-rapidapi-host': "sephora14.p.rapidapi.com"
}

# Read category list from CSV
df = pd.read_csv('../../data/pick_category.csv') 
categories = df['categoryID'].unique().tolist()

def fetch_products(category_id, page):
    """
    Fetch products from the API by category and page.

    Parameters:
    category_id (str): The ID of the category to fetch products from.
    page (int): The page number for pagination.

    Returns:
    dict: A dictionary containing the JSON response from the API, 
          typically including baisc product data and pagination details.
    """
    conn = http.client.HTTPSConnection(API_HOST)
    url = f"/searchByCategory?categoryID={category_id}&page={page}&sortBy=NEW"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return json.loads(data)

def save_to_csv(all_products, output_file):
    """
    Save product data to a CSV file.

    Parameters:
    all_products (list of dict): A list of dictionaries containing product data.
        Each dictionary should include the keys: 
        "categoryID", "brandName", "displayName", "heroImage", "productId", "rating", "reviews".
    output_file (str): The path to the output CSV file.

    Returns:
    None: This function writes data directly to the specified CSV file.
    """
    keys = ["categoryID", "brandName", "displayName", "heroImage", "productId", "rating", "reviews"]
    with open(output_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_products)

def scrape_all_products():
    """
    Scrape product information for all categories and save it to a CSV file.

    This function iterates through all categories, fetching up to 75 products per category 
    using the `fetch_products` function. It extracts relevant product details, handles missing 
    data gracefully, and saves the compiled data to a CSV file.

    Parameters:
    None

    Returns:
    None: This function writes the scraped product data to a CSV file and prints a summary of the operation.
    """
    all_products = []
    output_file = "../../data/category_product.csv"
    
    for category in categories:
        page = 1
        product_fetched = 0  # Initialize the product counter for each category
        
        # while product_fetched < 75:  # Limit to 75 products per category
        try:
            response = fetch_products(category, page)
            products = response.get("products", [])
            
            if len(products) == 0:  
                break

            # Extract product information
            for product in products:
                if product_fetched >= 75:  
                    break
                
                # Handle missing fields like rating or reviews (default to 0 if missing)
                product_info = {
                    "categoryID": category,
                    "brandName": product.get("brandName", "Unknown"),
                    "displayName": product.get("displayName", "Unknown"),
                    "heroImage": product.get("heroImage", "Unknown"),
                    "productId": product.get("productId", "Unknown"),
                    "rating": product.get("rating", 0),  # Default to 0 if missing
                    "reviews": product.get("reviews", 0),  # Default to 0 if missing
                }
                all_products.append(product_info)
                product_fetched += 1  

            page += 1  # Move to the next page


        except Exception as e:
            print(f"Error fetching page {page} for category {category}: {e}")
            break

    # Save the fetched data to CSV
    save_to_csv(all_products, output_file)
    print(f"Successfully saved {len(all_products)} products to {output_file}")

# Execute the scraping process
scrape_all_products()





