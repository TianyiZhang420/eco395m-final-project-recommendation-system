import http.client
import json
import pandas as pd
import time
from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv()

"""
In order to To minimize the number of API calls, I've added some test code in the comments that you can use to try to run and prevent running a lot of data at once and causing the API to exceed its limits.
"""

API_HOST = "sephora14.p.rapidapi.com"
headers = {
    "x-rapidapi-key": os.getenv("API_KEY"),
    "x-rapidapi-host": "sephora14.p.rapidapi.com",
}

df = pd.read_csv("../../data/category_product.csv")
# df = pd.read_csv('../../data/category_product_test.csv') #use this line to test
df = df.drop_duplicates(
    subset="productId", keep="first"
)  # drop duplicated data and keep the first productId
df.to_csv("../../data/category_product.csv", index=False, encoding="utf-8")
# df.to_csv('../../data/category_product_test.csv', index=False, encoding='utf-8') #use this line to test

products = df["productId"].unique().tolist()
# products = df['productId'].unique().tolist()[:1]  #use this line to test，only scrape the first category


def fetch_details(product_id, page):
    """
    Fetch detailed information for a specific product from the API.

    Parameters:
    product_id (str): The unique identifier of the product.
    page (int): The page number for pagination.

    Returns:
    dict: A dictionary containing detailed information about the product,
          including its ingredient, listprice, longDescription, lovesCount, fullSiteProductUrl and quickLookDescription.
    """
    conn = http.client.HTTPSConnection(API_HOST)
    url = f"/product?productID={product_id}&page={page}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return json.loads(data)


def scrape_all_details():
    """
    Scrape detailed information for all products.

    Iterates through a list of product IDs and fetches their details using the `fetch_details` function.
    Extracts and processes specific information such as descriptions, pricing, and URLs, and returns
    a list of product details.

    Parameters:
    None

    Returns:
    list of dict: A list of dictionaries where each dictionary contains detailed information.
    """
    all_details = []

    for product_id in tqdm(products, desc="Scraping products", unit="product"):
        page = 1
        try:
            response = fetch_details(product_id, page)

            brand = response.get("brand", {})
            currentSku = response.get("currentSku", {})
            product_detail = {
                "productId": product_id,
                "longDescription": brand.get("longDescription", ""),
                "brandID": brand.get("brandID", ""),
                "ingredientDesc": currentSku.get("ingredientDesc", ""),
                "listPrice": currentSku.get("listPrice", ""),
                "quickLookDescription": response.get("quickLookDescription", ""),
                "lovesCount": response.get("lovesCount", 0),
                "fullSiteProductUrl": response.get("fullSiteProductUrl", ""),
            }
            all_details.append(product_detail)
            page += 1
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching page {page} for product {product_id}: {e}")
            break
    return all_details


def update_csv_with_details(all_details, input_file, output_file):
    """
    Update an existing CSV file with new product details.

    Reads an existing CSV file, merges it with the new product details, and writes the updated data to a new CSV file.
    Do data cleaning to delete "$" in listPrice and lines with no listPrice and loveCount

    Parameters:
    all_details (list of dict): A list of dictionaries containing new product details.
    input_file (str): Path to the input CSV file containing existing product data.
    output_file (str): Path to the output CSV file where updated data will be saved.

    Returns:
    None: This function writes updated data directly to the specified output file and prints a confirmation message.
    """
    existing_data = pd.read_csv(input_file)
    new_data = pd.DataFrame(all_details)

    if new_data.empty:
        print("No new data to update.")
        return

    updated_data = pd.merge(
        existing_data, new_data, on="productId", how="left", suffixes=("", "_new")
    )

    updated_data = updated_data[updated_data["listPrice"].notna()]
    updated_data = updated_data[updated_data["lovesCount"].notna()]

    updated_data["listPrice"] = updated_data["listPrice"].replace(
        {"\$": "", ",": ""}, regex=True
    )
    updated_data["listPrice"] = updated_data["listPrice"].astype(float)

    updated_data.to_csv(output_file, index=False, encoding="utf-8", header=False)
    print(f"Successfully updated the data and saved to {output_file}")


def main():
    """
    Main function to run the scraping and updating process.

    Reads an input CSV file containing product data, scrapes detailed information for each product,
    and updates the input file with the newly scraped details. Saves the updated data to a new output file.

    Parameters:
    None

    Returns:
    None: This function executes the full pipeline and prints progress and completion messages.
    """
    input_file = "../../data/category_product.csv"
    # input_file = '../../data/category_product_test.csv' #use this to test
    output_file = "../../data/category_product_cleaned.csv"
    # output_file = '../../data/category_product_cleaned_test.csv'  #use this to test
    print("Starting to scrape product details...")
    all_details = scrape_all_details()
    print(f"Scraped details for {len(all_details)} entries. Updating CSV...")
    update_csv_with_details(all_details, input_file, output_file)


if __name__ == "__main__":
    main()
