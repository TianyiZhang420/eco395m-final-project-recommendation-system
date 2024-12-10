import http.client
import json
import csv
import time
import os
from dotenv import load_dotenv

load_dotenv()

# API request headers
conn = http.client.HTTPSConnection("sephora14.p.rapidapi.com")
headers = {
    "x-rapidapi-key": os.getenv("API_KEY"),
    "x-rapidapi-host": "sephora14.p.rapidapi.com",
}


def read_product_ids(csv_file):
    """
    Reads product IDs from a CSV file.

    Parameters:
    csv_file (str): Path to the CSV file containing product IDs.

    Returns:
    list: A list of product IDs extracted from the CSV file.
    """
    product_ids = []
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            product_ids.append(row["productId"])
    return product_ids


def extract_context_values(context_data):
    """
    Extract specific context field values from a product review.

    The function extracts values for the fields 'skinTone', 'eyeColor', 'skinType',
    and 'hairColor' from a nested dictionary. If the fields are not present
    or are missing the 'Value' subfield, default to an empty string.

    Parameters:
    context_data (dict): A dictionary containing the 'ContextDataValues' field from a product review.

    Returns:
    dict: A dictionary containing the extracted values for the specified context fields.
          Keys will always be present, with empty string as the default value if missing.
    """
    result = {
        "skinTone": "",
        "eyeColor": "",
        "skinType": "",
        "IncentivizedReview": "",
        "hairColor": "",
    }

    if isinstance(context_data, dict):
        for key in result.keys():
            if key in context_data:
                value_data = context_data[key]
                if isinstance(value_data, dict) and "Value" in value_data:
                    result[key] = value_data["Value"]

    return result


def fetch_reviews_for_product(product_id, limit=50):
    """
    Fetch reviews for a specific product from the API.

    Retrieves up to 'limit' reviews for a given product, including fields such as
    rating, review text, and context-specific values (e.g., skin tone, eye color).

    Parameters:
    product_id (str): The unique identifier of the product for which reviews are being fetched.
    limit (int, optional): The maximum number of reviews to fetch (default is 50).

    Returns:
    list of dict: A list of dictionaries where each dictionary represents a review, containing
                  fields like 'Rating', 'ReviewText', 'Title', and extracted context data values.
    """
    offset = 0
    all_reviews = []

    url = f"/productReviews?productID={product_id}&page=1"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()

    response_data = data.decode("utf-8")
    json_data = json.loads(response_data)

    if isinstance(json_data, list):
        results = json_data
    else:
        results = json_data.get("Results", [])

    if not results:
        print(f"All {product_id} 's reviews have been scraped!")
        return []

    for review in results[:limit]:
        context_values = extract_context_values(review.get("ContextDataValues", {}))
        all_reviews.append(
            {
                "ProductId": product_id,
                "OriginalProductName": review.get("OriginalProductName", ""),
                "Rating": review.get("Rating", ""),
                "Helpfulness": review.get("Helpfulness", ""),
                "ReviewText": review.get("ReviewText", ""),
                "Title": review.get("Title", ""),
                "skinTone": context_values.get("skinTone", ""),
                "eyeColor": context_values.get("eyeColor", ""),
                "skinType": context_values.get("skinType", ""),
                "hairColor": context_values.get("hairColor", ""),
            }
        )

    print(f"Get {len(all_reviews)} reviews")
    return all_reviews


def save_reviews_to_csv(reviews, output_file="../../data/review.csv"):
    """
    Save review data to a CSV file.

    Writes a list of reviews to a CSV file with headers, ensuring that all data
    fields are correctly formatted and saved.

    Parameters:
    reviews (list of dict): A list of dictionaries containing review data.
    output_file (str, optional): Path to the output CSV file

    Returns:
    None: The function writes data directly to a file and prints a confirmation message.
    """
    csv_headers = [
        "ProductId",
        "OriginalProductName",
        "Rating",
        "ReviewText",
        "Title",
        "Helpfulness",
        "skinTone",
        "eyeColor",
        "skinType",
        "hairColor",
    ]

    with open(output_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        if headers:
            writer.writeheader()

        for review in reviews:
            writer.writerow(review)

    print(f"Data has been saved to {output_file}, saved {len(reviews)} reviews.")


def main():
    """
    Main function to orchestrate the review scraping process.

    - Reads product IDs from a CSV file.
    - Fetches reviews for each product ID, limiting to a set number of reviews per product.
    - Periodically saves the fetched reviews to a CSV file for reliability.
    - Handles API rate limits by introducing delays between requests.

    Parameters:
    None

    Returns:
    None: The function executes the full pipeline and writes the resulting reviews to a CSV file.
    """
    product_ids = read_product_ids("../../data/category_product.csv")
    all_reviews = []

    for idx, product_id in enumerate(product_ids):
        print(f"Getting {product_id} 's reviews...")
        product_reviews = fetch_reviews_for_product(product_id)
        all_reviews.extend(product_reviews)
        print(f"Fetched {len(product_reviews)} reviews for product {product_id}")

        if (idx + 1) % 20 == 0:
            save_reviews_to_csv(all_reviews, output_file="../../data/review.csv")

        time.sleep(1)

    if all_reviews:
        save_reviews_to_csv(all_reviews)


if __name__ == "__main__":
    main()
