import pandas as pd


csv_file = "data/product.csv"
data = pd.read_csv(csv_file)

deduplicated_data = data.drop_duplicates(subset="productId", keep="first")

data_without_header = deduplicated_data.iloc[1:]
output_file = "data/product_new.csv"
data_without_header.to_csv(output_file, index=False, header=False, encoding="utf-8")

