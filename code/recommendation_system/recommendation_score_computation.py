import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# user's info
user_df = pd.read_csv("user_data.csv")
# Test with the first data
user1 = user_df.iloc[0]

# Review data after matching with user input and filtering

review_df_1 = pd.read_csv("output.csv")
review_df_1 = review_df_1.drop_duplicates()


# Compute embeddings
def get_embeddings(model, df):
    if isinstance(df, str):
        lst = [df]
    else:
        lst = df.tolist()
    return model.encode(lst)


# Compute the cosine similarity of the first sample user data with all the selected products' reviews


def final_score(similarity, rating):
    return similarity * rating


def calculate_individual_similarities(user_info, product_info):
    detailed_scores = {}
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # get embeddings of user description and reviews of products
    requirements_embeddings = get_embeddings(model, user_info["description"])
    review_embeddings = get_embeddings(model, product_info["reviewtext"])

    product_embedding_dict = {
        product_id: embedding
        for product_id, embedding in zip(product_info["productid"], review_embeddings)
    }

    # computing similarity scores
    for product_id, review_embs in product_embedding_dict.items():

        scores = cosine_similarity(
            requirements_embeddings.reshape(1, -1), review_embs.reshape(1, -1)
        )
        scaled_product_rating = product_info.loc[
            product_info["productid"] == product_id, "productrating"
        ].iloc[0]

        detailed_scores[product_id] = final_score(scores[0][0], scaled_product_rating)

    # Ranking and select top5
    ranked_dict = dict(
        sorted(detailed_scores.items(), key=lambda item: item[1], reverse=True)
    )
    ranked_list = []
    for rank, (key, value) in enumerate(ranked_dict.items(), start=1):
        # Fetch product details from review_df_1
        product_details = (
            product_info.loc[product_info["productid"] == key].iloc[0].to_dict()
        )
        product_details["Rank"] = rank
        product_details["Score"] = value
        ranked_list.append(product_details)

    # Convert the list of product details to a DataFrame
    ranked_df = pd.DataFrame(ranked_list)

    # Sort the DataFrame by rank (if necessary, though it's already sorted by enumerate)
    ranked_df = ranked_df.sort_values("Rank", ascending=True)

    return ranked_df


# Display the ranked DataFrame
ranked_df = calculate_individual_similarities(user1, review_df_1)

print(ranked_df.head())
