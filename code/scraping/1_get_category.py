import http.client
import json
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# API connection setup
conn = http.client.HTTPSConnection("sephora14.p.rapidapi.com")

headers = {
    "x-rapidapi-key": os.getenv("API_KEY"),
    "x-rapidapi-host": "sephora14.p.rapidapi.com",
}

# Make the API request
conn.request("GET", "/categories", headers=headers)
res = conn.getresponse()
data = res.read()

# Decode and parse the response
decoded_data = data.decode("utf-8")
parsed_data = json.loads(decoded_data)  # Assuming the API returns JSON
print(parsed_data)
# Specify the output file path
output_file_path = "../../data/category.csv"

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Write data to a CSV file
try:
    with open(output_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write header row
        csv_writer.writerow(["categoryLabel", "categoryID"])

        # Write category data
        for category in parsed_data:
            csv_writer.writerow(
                [category.get("categoryLabel"), category.get("categoryID")]
            )

    print(f"Data saved to {output_file_path}")

except Exception as e:
    print(f"An error occurred while writing to CSV: {e}")
