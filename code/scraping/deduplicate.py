import pandas as pd


csv_file = "data/category_product.csv"
data = pd.read_csv(csv_file)

deduplicated_data = data.drop_duplicates(subset="productId", keep="first")



output_file = "data/category_product_new.csv"
deduplicated_data.to_csv(output_file, index=False, encoding="utf-8")