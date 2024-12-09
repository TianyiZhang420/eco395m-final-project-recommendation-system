# eco395m-final-project-recommendation-system
## Introduction
## A. Data Scraping
## B. Recommendation System Pipline
***User Interface:*** 
We design an interactive dashboard in Python using Streamlit for users to select with their preference and get the best fit product from our recommendation system. Make sure you upload your data to Google Cloud Platform with the instance started and have your database credentials in the hidden .env file, so that Streamlit can connect to the corresponding database. Everything is being connected through the [dashboard.py](code/recommendation_system/dashboard.py) file by local modules and there is nothing else you need to run separately for queries or models. To open up the Streamlit dashboard, run the following command from the root:
```bash
streamlit run code/recommendation_system/dashboard.py 
```
Some dashboard highlights are as follows:

1. Users can select a product category, specify a desired price range, choose a skin tone and skin type, and provide a short description of their desired product. They may also optionally input wanted and unwanted ingredients.
2. All filters must be completed for users to proceed to the recommendation step. If any required filter is missing, a warning message will be displayed.
3. Based on the user's selections, SQL queries will be executed to search the database for products that meet all the specified criteria. If no matching products are found, users will be prompted to modify their selections.
4. If products meeting the initial requirements are found, their details, along with the user's description, will be sent to our embedding model for further recommendations. The model will then provide the user with the top 5 products based on recommendation scores.
5. The dashboard will display the top 5 recommended products, including their names and clickable links that direct users to the corresponding product pages on Sephora.

## C. Findings
## D. Limitations
## E. Further Plans
