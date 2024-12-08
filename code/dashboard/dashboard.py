import numpy as np
import pandas as pd
import streamlit as st


# Dashboard Title
st.title("💄Sephora Product Finder")

# List of product type
product_type = ["These", "are", "test", "words"]

# Filter to select a product type
selected_type = st.selectbox("Select a product type:", options=["Select an option"] + product_type)

#Slider for price range
org_min_price = 10
org_max_price = 500
min_price, max_price = st.slider(
    "Select desired price range ($):",
    min_value=org_min_price,
    max_value=org_max_price,
    value=(org_min_price, org_max_price)
)

# Textbox for product description
product_description = st.text_input("Describe the product you are looking for:")

st.write(f"The best fit {selected_type} for you is   . Here is the [link](https://www.openai.com) to the product. Thank you for using our App!")
