import pandas as pd

def get_unique_values(query, engine):
    """
    Fetch unique values from the database.

    Parameters:
    query (str): SQL query string to retrieve the data.
    db_connection_string (str): Database connection string.

    Returns:
    list: A list of unique values.
    """
    
    # Execute query and load results into a DataFrame
    df = pd.read_sql_query(query, engine)
    
    # Extract unique values and return as a list
    unique_values = df.iloc[:, 0].dropna().unique().tolist()  # Assumes the skinType or skinTone is the first column
    return unique_values


def get_products_and_reviews(query, category, min_price, max_price, engine):
    """
    Fetch products and their reviews based on category and price range.

    Parameters:
    category (str): The product category to filter.
    min_price (float): The minimum price.
    max_price (float): The maximum price.
    db_connection_string (str): Database connection string.

    Returns:
    pd.DataFrame: A DataFrame containing the filtered products and reviews.
    """
    
    # Execute the query with parameters
    params = {"category": category, "min_price": min_price, "max_price": max_price}
    result = pd.read_sql_query(query, engine, params=params)
    
    return result
