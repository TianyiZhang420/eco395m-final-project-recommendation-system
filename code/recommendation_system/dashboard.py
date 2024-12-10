import pandas as pd
import streamlit as st
from database import engine
from queries import *
from get_cleaned_df import get_filtered_products
from recommendation_score_computation import recommend_products


# Background Image
st.image("image/sephora.jpg", use_container_width=True)

# Dashboard Title
st.title("💄Sephora Product Finder")

# List of product category
product_category = pd.read_sql_query(query_1, engine)["categoryid"].tolist()

# Filter to select a product type
selected_product_category = st.selectbox(
    "Select a product product_category:",
    options=["Select an option"] + product_category,
)

# Slider for price range
org_min_price = pd.read_sql_query(query_2, engine)["minprice"].tolist()[0]
org_max_price = pd.read_sql_query(query_2, engine)["maxprice"].tolist()[0]
min_price, max_price = st.slider(
    "Select desired price range ($):",
    min_value=org_min_price,
    max_value=org_max_price,
    value=(org_min_price, org_max_price),
)

# List of Skin Tone and Skin Type
skin_tone = pd.read_sql_query(query_4, engine)["skintone"].tolist()
skin_type = pd.read_sql_query(query_3, engine)["skintype"].tolist()

# Filter to select a skin tone and a skin type
user_skintone = st.selectbox(
    "Select your skin tone:", options=["Select an option"] + skin_tone
)
user_skintype = st.selectbox(
    "Select your skin type:", options=["Select an option"] + skin_type
)

# Textbox for product description
product_description = st.text_input("Describe the product you are looking for:")

# Optional textbox for wanted and unwanted product ingredients
wanted_ingredients = st.text_input(
    "What are some ingredients you want in the product? If multiple ones, separate by commas; Otherwise, leave it blank:"
)
unwanted_ingredients = st.text_input(
    "What are some ingredients you do not want in the product? If multiple ones, separate by commas; Otherwise, leave it blank:"
)

# Display the output
if (
    selected_product_category == "Select an option"
    or user_skintone == "Select an option"
    or user_skintype == "Select an option"
    or product_description == ""
):
    st.warning("Please fill in all information to see the results.")
else:
    result_df = get_filtered_products(
        query_5,
        selected_product_category,
        min_price,
        max_price,
        engine,
        user_skintype,
        user_skintone,
        wanted_ingredients,
        unwanted_ingredients,
    )
    if result_df.empty:
        st.write("No matched product. Please modify your inputs and try again.")
    else:
        ranked_df = recommend_products(product_description, result_df)
        st.markdown(f"### The top 5 {selected_product_category} for you:")
        for index, row in ranked_df.head(5).iterrows():
            st.markdown(
                f"- **{row['displayname']}**: [View Product]({row['fullsiteproducturl']})"
            )
        st.markdown("Thank you for using our App!")
