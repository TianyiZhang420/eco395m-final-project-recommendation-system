import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_products(user_des, product_info):
    """
    Recommend products based on user description and product reviews.

    Args:
        user_des (string): A string containing user's description of the product.
        product_info (pd.DataFrame): A DataFrame with product information,
                                     including "productid", "reviewtext", and "productrating" columns.

    Returns:
        pd.DataFrame: A DataFrame with the ranked product recommendations.
    """

    def get_embeddings(model, df):
        if isinstance(df, str):
            lst = [df]
        else:
            lst = df.tolist()
        return model.encode(lst)

    def final_score(similarity, rating, w1, w2, alpha, beta):
        # Penalize low similarity and low rating
        adjusted_similarity = similarity**beta
        adjusted_rating = rating**alpha

        # Set weights to similarity and rating
        final_score = w1 * adjusted_similarity + w2 * adjusted_rating
        return final_score

    # Initialize the model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Compute embeddings for user description and product reviews
    user_embeddings = get_embeddings(model, user_des)
    product_reviews_embeddings = get_embeddings(model, product_info["reviewtext"])

    # Create a dictionary mapping product IDs to their embeddings
    product_embedding_dict = {
        product_id: embedding
        for product_id, embedding in zip(
            product_info["productid"], product_reviews_embeddings
        )
    }

    # Calculate similarity scores and weighted scores
    detailed_scores = {}
    for product_id, review_emb in product_embedding_dict.items():
        similarity_score = cosine_similarity(
            user_embeddings.reshape(1, -1), review_emb.reshape(1, -1)
        )[0][0]

        # scale product rating to [0,1]
        product_rating = (
            product_info.loc[
                product_info["productid"] == product_id, "productrating"
            ].iloc[0]
            / 5
        )

        detailed_scores[product_id] = final_score(
            similarity_score, product_rating, 0.7, 0.3, 0.8, 0.8
        )

    # Rank products by scores
    ranked_products = sorted(
        detailed_scores.items(), key=lambda item: item[1], reverse=True
    )

    # Create a ranked DataFrame
    ranked_list = []
    for rank, (product_id, score) in enumerate(ranked_products, start=1):
        product_details = (
            product_info.loc[product_info["productid"] == product_id].iloc[0].to_dict()
        )
        product_details["Rank"] = rank
        product_details["Score"] = score
        ranked_list.append(product_details)

    ranked_df = pd.DataFrame(ranked_list).sort_values("Rank", ascending=True)

    return ranked_df
