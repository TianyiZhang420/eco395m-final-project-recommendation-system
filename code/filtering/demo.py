import os

from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
from get_cleaned_df import get_filtered_products
from queries import *

load_dotenv()

DATABASE_USERNAME = os.environ["DATABASE_USERNAME"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_PORT = os.environ["DATABASE_PORT"]
DATABASE_DATABASE = os.environ["DATABASE_DATABASE"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)



categories = pd.read_sql_query(query_1, engine)["categoryid"].tolist()
maxprice = pd.read_sql_query(query_2, engine)["maxprice"].tolist()[0]
minprice = pd.read_sql_query(query_2, engine)["minprice"].tolist()[0]
skintype = pd.read_sql_query(query_3, engine)["skintype"].tolist()
skintone = pd.read_sql_query(query_4, engine)["skintone"].tolist()



category = "concealer"
min_price = 5
max_price = 50
user_skintype = "combination"
user_skintone = "medium"
wanted_ingredients = "Omegas 3,vitamin"
unwanted_ingredients = "acid"


cleaned_df = get_filtered_products(
    query_5,
    category,
    min_price,
    max_price,
    engine,
    user_skintype,
    user_skintone,
    wanted_ingredients,
    unwanted_ingredients,
)
