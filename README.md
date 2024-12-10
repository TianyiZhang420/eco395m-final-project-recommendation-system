# eco395m-final-project-recommendation-system
## Introduction
## A. Data Scraping
## B. Recommendation System Pipline
### Filtering:
We develop a module that filters products based on user inputs for category and price range by executing SQL queries on our `product_info` database, performing an inner join with the `product_reviews` database on `productid`. This process generates an initial dataframe that includes product information along with each product's corresponding reviews and the reviewers' information. Because users may also specify wanted ingredients and unwanteded ingredients, we filter products that include the wanted ingredients and exclude the unwanted ingredients. To make the subsequent embedding comparison process more efficient, we select the reviews based on the user's input for skin type and skin tone. If a product has reviewers whose skin type and skin tone match the user's inputs, only those matching reviews are retained in the dataframe. If no such matches are found, all reviews for that product are kept as data for further analysis. Through the above steps, we obtain a cleaned dataframe that serves as the data for the next stage of analysis.

### Modeling:
Here, we utilizes natural language processing (NLP) techniques and machine learning models to compute semantic similarities between user descriptions and product reviews, while also considering product ratings to enhance recommendations.

***1. Semantic Matching:***
#### Usage:
  - Input Requirements:
    1. User Description (`user_des`): A string describing the product the user is looking for.
    2. Product Information (`product_info`): A pandas DataFrame with product information.
  - Output:
    1. Ranked Product Dataframe (`ranked_df`): A DataFrame with the ranked product recommendations.

**Model Used:** The system uses the `all-MiniLM-L6-v2` model from the `SentenceTransformer` library, a lightweight pre-trained model optimized for semantic tasks.

**Process:** The user's input is converted into a semantic vector. Each product review is similarly transformed into a semantic vector. The similarity between the user input vector and each product review vector is calculated using cosine similarity. Higher similarity scores indicate a closer match between the user's needs and the product reviews.

***2. Weighted Scoring:***
  
  The recommendation system combines semantic similarity and product ratings to calculate a final score for each product. This score is used to rank products and generate a prioritized list of recommendations.

**Scoring Logic:** The recommendation score is calculated using the formula:

$$ \text{Score} = w_1 \cdot (\text{Similarity Score})^\beta + w_2 \cdot (\text{Rating})^\alpha$$

  where:

  - Rating: Normalized product rating (scaled to a 0–1 range).
  - Weights ($w_1, w_2$): Control the importance of similarity and rating in the final score.
  - Exponents ($\alpha, \beta$): Penalize lower similarity scores or ratings more heavily, emphasizing higher values.

**Default Parameters:**
  - $w_1 = 0.7, w_2 = 0.3$: Prioritizes semantic similarity over product ratings.
  - $\alpha = 0.8, \beta = 0.8$: Adjust the influence of ratings and similarity scores.

***3. Ranked Output:***

Provides a sorted list of product recommendations with detailed information.The system computes a final score for each product based on semantic similarity and rating. Products are sorted in descending order by their scores. A ranked DataFrame is created, starting with the highest-ranked product.

### User Interface:
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

### Explorative Data Analysis(EDA)

This module provides visual and statistical insights into the dataset, focusing on product categories, ratings, reviews, and sentiment analysis. The EDA helps uncover patterns, relationships, and distributions in the data to better understand the dataset.

***Category Distribution***

<div align="center">
<img src="https://github.com/TianyiZhang420/eco395m-final-project-recommendation-system/blob/main/image/category_distribution.png" alt="Image Description" style="width:50%;height:auto;">
</div>

 - **Dominance of Facial Makeup and Skincare**: Foundation makeup and mascara categories dominate in terms of product availability, indicating higher market focus.
 - **Limited Representation of Certain Categories**: Blush and sunscreen have significantly fewer products, which may indicate gaps in these markets.
 - **Even Distribution in Some Areas**: Certain categories, like luminizers and face masks, show a balanced presence.


***Correlation Analysis of ratings and the number of reviews***

<div align="center">
<img src="https://github.com/TianyiZhang420/eco395m-final-project-recommendation-system/blob/main/image/correlation_analysis.png" alt="Image Description" style="width:50%;height:auto;">
</div>

- **Correlation Coefficient**: The coefficient is -0.02, indicating a near-zero and slightly negative relationship. This suggests that ratings and the number of reviews are almost independent of each other.
- **Outliers**: Some products with mid-range ratings (e.g., ~4.0) have an exceptionally high number of reviews (>20,000), which may influence the overall distribution.


***Rating Distribution***


<div align="center">
<img src="https://github.com/TianyiZhang420/eco395m-final-project-recommendation-system/blob/main/image/rating_distribution.png" alt="Image Description" style="width:50%;height:auto;">
</div>

- **Dominance of Highly Rated Products**: The majority of products are rated between 4–5, with over 600 products falling into this category, highlighting a trend of high customer satisfaction.
- **Moderately Rated Products**: A smaller but notable portion of products has ratings in the 3–4 range, indicating decent but less impressive customer satisfaction.
- **Scarcity of Low Ratings**: Very few products fall in the 2–3 and 1–2 ranges, showing a rare occurrence of dissatisfaction.oducts with ratings in the ranges 2–3 and 1–2 are extremely few, indicating that most products are rated relatively highly.

***Sentiment Analysis***

<div align="center">
<img src="https://github.com/TianyiZhang420/eco395m-final-project-recommendation-system/blob/main/image/sentiment_analysis.png" alt="Image Description" style="width:50%;height:auto;">
</div>

- **Overwhelmingly Positive Sentiment**: Most reviews (88.2%) are positive, reflecting strong approval and satisfaction from users.
- **Moderate Neutral Sentiment**: A smaller percentage of reviews (9.8%) are neutral, suggesting an indifferent or average user experience.
- **Low Negative Sentiment**: Only 2% of reviews are negative, indicating minimal dissatisfaction among users.

## D. Limitations

* Our recommendation system does not take the official product descriptions into account, which may contain information about the product's features and uses. If we incorporate the analysis of official descriptions into our recommendation system, the recommendations may better align with user needs.
* Our dashboard only displays selected product names and links to the websites, which might not be visually engaging from an UI/UX perspective.
* Our recommendation system is linked to static database, such that new data has to be manually entered into google cloud platform in order to keep product information up to date. 

## E. Further Plans
* Include the official product descriptions in the analyzed data, generate embeddings, and calculate their similarity to the user's input as part of the recommendation score.
* Redesign output interface by adding elements includng but not limited to images, ratings, or other visual cues.
* Integrate real-time data automatically from external sources like Sephora’s API to provide updated product details on a regular basis. 
