import numpy as np
import pandas as pd
import streamlit as st


# Background Image
st.image("sephora.jpg", use_column_width=True)

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

# List of Skin Tone and Skin Type
skin_tone = ["These", "are", "test", "words"]
skin_type = ["These", "are", "test", "words"]

# Filter to select a skin tone and a skin type
selected_skin_tone = st.selectbox("Select your skin tone:", options=["Select an option"] + skin_tone)
selected_skin_type = st.selectbox("Select your skin type:", options=["Select an option"] + skin_type)

# Textbox for product description
product_description = st.text_input("Describe the product you are looking for:")

# Optional textbox for wanted and unwanted product ingredients
wanted_ingredients = st.text_input("What are some ingredients you want in the product? If multiple ones, separate by commas; Otherwise, leave it blank:")
unwanted_ingredients = st.text_input("What are some ingredients you do not want in the product? If multiple ones, separate by commas; Otherwise, leave it blank:")

# Display the output
if selected_type == "Select an option" or selected_skin_tone == "Select an option" or selected_skin_type == "Select an option" or product_description == '':
    st.warning("Please fill in all information to see the results.")
else:
    #result_df from filtering function
    if result_df.empty:
        st.write("No matched product. Please modify your inputs and try again.")
    else:
        #result product from recommendation model
        st.write(f"The best fit {selected_type} for you is   . Here is the [link](https://www.openai.com) to the product. Thank you for using our App!")
    