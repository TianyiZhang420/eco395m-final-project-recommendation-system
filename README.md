# eco395m-final-project-recommendation-system
## Introduction
## A. Data Scraping
## B. Recommendation System Pipline
***Filtering:***
We develop a module that filters products based on user inputs for category and price range by executing SQL queries on our `product_info` database, performing an inner join with the `product_reviews` database on `productid`. This process generates an initial dataframe that includes product information along with each product's corresponding reviews and the reviewers' information. Because users may also specify wanted ingredients and unwanteded ingredients, we filter products that include the wanted ingredients and exclude the unwanted ingredients. To make the subsequent embedding comparison process more efficient, we select the reviews based on the user's input for skin type and skin tone. If a product has reviewers whose skin type and skin tone match the user's inputs, only those matching reviews are retained in the dataframe. If no such matches are found, all reviews for that product are kept as data for further analysis. Through the above steps, we obtain a cleaned dataframe that serves as the data for the next stage of analysis.

***User Interface:*** 
We design an interactive dashboard in Python using Streamlit for users to select with their preference and get the best fit product from our recommendation system. Make sure you upload your data to Google Cloud Platform with the instance started and have your database credentials in the hidden .env file. Everything is being connected through the [dashboard.py](code/recommendation_system/dashboard.py) file by local modules and there is nothing else you need to run separately for queries or models. To open up the Streamlit dashboard, run the following command from the root:
```bash
streamlit run code/recommendation_system/dashboard.py 
```
Some dashboard highlights are as follows:

1. Users can select a product category, specify a desired price range, choose a skin tone and skin type, and provide a short description of their desired product. They may also optionally input wanted and unwanted ingredients.
2. All filters must be completed for users to proceed to the recommendation step. If any required filter is missing, a warning message will be displayed.
3. Based on the user's selections, SQL queries will be executed to search the database for products that meet all the specified criteria. If no matching products are found, users will be prompted to modify their selections.
4. If products meeting the initial requirements are found, their details, along with the user's description, will be sent to our embedding model for further recommendations. 
5. The dashboard will display the top 5 recommended products, including their names and clickable links that direct users to the corresponding product pages on Sephora.

## C. Findings
## D. Limitations

* Our recommendation system does not take the official product descriptions into account, which may contain information about the product's features and uses. If we incorporate the analysis of official descriptions into our recommendation system, the recommendations may better align with user needs.
* Our dashboard only displays selected product names and links to the websites, which might not be visually engaging from an UI/UX perspective.
* Our recommendation system is linked to static database, such that new data has to be manually entered into google cloud platform in order to keep product information up to date. 

## E. Further Plans
* Include the official product descriptions in the analyzed data, generate embeddings, and calculate their similarity to the user's input as part of the recommendation score.
* Redesign output interface by adding elements includng but not limited to images, ratings, or other visual cues.
* Integrate real-time data automatically from external sources like Sephora’s API to provide updated product details on a regular basis. 
