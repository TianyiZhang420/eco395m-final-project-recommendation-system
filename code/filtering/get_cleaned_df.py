import pandas as pd
from sqlalchemy import text
from sql_filter import get_products_and_reviews


def filter_reviews_by_skin(df, user_skin_type, user_skin_tone):
    """
    Filters a DataFrame of products and reviews based on user input for SkinType and SkinTone.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing product and review data.
    user_skin_type (str): The user's desired SkinType.
    user_skin_tone (str): The user's desired SkinTone.

    Returns:
    pd.DataFrame: A filtered DataFrame with reviews meeting the specified conditions.
    """
    # Add a flag to identify reviews that match the user's SkinType and SkinTone
    df["matches_user"] = (df["skintype"] == user_skin_type) & (
        df["skintone"] == user_skin_tone
    )

    # Group by product_id (or equivalent column) to check if any review matches the user's input
    product_group = df.groupby("productid")["matches_user"].any()

    # Create a dictionary of products to retain based on the group-level condition
    product_retain_map = product_group.to_dict()

    # Filter the DataFrame based on the logic
    filtered_df = df[
        (df["matches_user"])  # Keep reviews that match the user's input
        | (
            ~df["productid"].map(product_retain_map)
        )  # Keep all reviews if no match exists
    ].drop(
        columns=["matches_user"]
    )  # Drop the helper column

    return filtered_df


def filter_by_ingredients(df, wanted_ingredients, ingredient_column_name):
    """
    Filters the DataFrame to include rows where:
    1. The ingredient description contains any of the user-provided ingredients.
    2. The ingredient description is empty or NaN.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    user_ingredients (str): A comma-separated string of ingredients input by the user.
    ingredient_column (str): The column name containing ingredient descriptions.

    Returns:
    pd.DataFrame: A filtered DataFrame.
    """
    # Process user input: split into list, strip spaces, and convert to lowercase
    ingredients_list = [ing.strip().lower() for ing in wanted_ingredients.split(",")]

    # Process DataFrame: fill NaN with empty string and convert to lowercase
    df[ingredient_column_name] = df[ingredient_column_name].fillna("").str.lower()

    # Create a boolean mask for rows where the ingredient description matches any user ingredient
    matches = df[ingredient_column_name].apply(
        lambda desc: any(ingredient in desc for ingredient in ingredients_list)
    )

    # Include rows where the ingredient description is NaN or empty
    is_empty = df[ingredient_column_name] == ""

    # Combine the two conditions
    filtered_df = df[matches | is_empty]

    return filtered_df

def filter_out_ingredients(df, unwanted_ingredients, ingredient_column_name):
    """
    Filters the DataFrame to exclude rows where:
    1. The ingredient description contains any of the unwanted ingredients.
    2. The ingredient description is empty or NaN.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    unwanted_ingredients (str): A comma-separated string of ingredients the user wants to exclude.
    ingredient_column_name (str): The column name containing ingredient descriptions.

    Returns:
    pd.DataFrame: A filtered DataFrame.
    """
    # Process user input: split into list, strip spaces, and convert to lowercase
    unwanted_list = [ing.strip().lower() for ing in unwanted_ingredients.split(',')]
    
    # Process DataFrame: fill NaN with empty string and convert to lowercase
    df[ingredient_column_name] = df[ingredient_column_name].fillna('').str.lower()
    
    # Create a boolean mask for rows where the ingredient description contains any unwanted ingredient
    contains_unwanted = df[ingredient_column_name].apply(
        lambda desc: any(ingredient in desc for ingredient in unwanted_list)
    )
    
    # Include rows where the ingredient description is empty
    is_empty = df[ingredient_column_name] == ''
    
    # Combine the conditions:
    # - Exclude rows that contain any unwanted ingredients
    # - Include rows where the ingredient description is empty
    filtered_df = df[~contains_unwanted | is_empty]
    
    return filtered_df

def get_filtered_products(
    query,
    category,
    min_price,
    max_price,
    engine,
    user_skintype,
    user_skintone,
    wanted_ingredients=None,
    unwanted_ingredients=None,
):
    """
    Retrieve and filter product and review data.

    Parameters:
    - query: The query string
    - product_type: Type of product (e.g., 'concealer')
    - top_n: Number of top products to retrieve
    - reviews_limit: Number of reviews to retrieve per product
    - engine: Database engine or other necessary parameter
    - user_skintype: User's skin type (e.g., 'combination')
    - user_skintone: User's skin tone (e.g., 'medium')
    - user_ingredients: Ingredients the user wants to include (optional)

    Returns:
    - Filtered DataFrame
    """
    # Retrieve product and review data
    df = get_products_and_reviews(text(query), category, min_price, max_price, engine)

    # If the user provided ingredients, filter by ingredients
    if wanted_ingredients:
        df = filter_by_ingredients(df, wanted_ingredients, "ingredientdesc")

    # Filter reviews based on skin type and skin tone
    df = filter_reviews_by_skin(df, user_skintype, user_skintone)

    return df
