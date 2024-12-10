import pandas as pd
import matplotlib.pyplot as plt
import squarify
import seaborn as sns
from textblob import TextBlob

# Load the data
df = pd.read_csv("data/category_product_cleaned_with_header.csv")
review_df = pd.read_csv("data/review.csv")


def plot_category_distribution(df):
    """Category Distribution Treemap"""
    category_counts = df["categoryID"].value_counts()
    categories = category_counts.index.tolist()
    values = category_counts.values.tolist()

    # Generate 17 different colors
    colors = sns.color_palette("Paired", len(categories)).as_hex()

    # Create the treemap
    plt.figure(figsize=(12, 8))
    squarify.plot(
        sizes=values,
        label=[f"{cat}\n{val}" for cat, val in zip(categories, values)],
        color=colors[: len(values)],
        alpha=0.8,
        text_kwargs={"fontsize": 8, "weight": "bold", "color": "black"},
    )
    plt.axis("off")  # Remove axis
    plt.title("Number of Products in Main Categories", fontsize=16)
    plt.tight_layout()

    # Save the figure as an image
    plt.savefig("image/category_distribution.png")


def plot_rating_distribution(df):
    """Rating Distribution Barplot"""
    bins = [1, 2, 3, 4, 5]
    labels = ["1-2", "2-3", "3-4", "4-5"]
    df["rating_range"] = pd.cut(df["rating"], bins=bins, labels=labels, right=False)

    rating_counts = df["rating_range"].value_counts().sort_index()

    # Plot the bar chart
    plt.figure(figsize=(8, 5))
    sns.barplot(x=rating_counts.index, y=rating_counts.values, palette="viridis")
    plt.title("Number of Products in Rating Ranges")
    plt.xlabel("Rating Range")
    plt.ylabel("Count of Products")
    # Save the figure as an image
    plt.savefig("image/rating_distribution.png")


def plot_correlation_analysis(df):
    """Correlation Analysis Scatterplot"""
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="rating", y="reviews", color="blue")
    plt.title("Correlation between Ratings and Number of Reviews")
    plt.xlabel("Rating")
    plt.ylabel("Number of Reviews")

    # Calculate the correlation coefficient
    correlation = df["rating"].corr(df["reviews"])
    print(f"Correlation between ratings and number of reviews: {correlation:.2f}")

    # Save the figure as an image
    plt.savefig("image/correlation_analysis.png")


def plot_sentiment_analysis(review_df):
    """Sentiment Analysis Pie Chart"""

    def get_sentiment(text):
        analysis = TextBlob(text)
        score = analysis.sentiment.polarity
        if score > 0:
            return "Positive"
        elif score < 0:
            return "Negative"
        else:
            return "Neutral"

    review_cleaned = review_df.dropna(subset=["ReviewText"])
    review_cleaned["sentiment"] = review_cleaned["ReviewText"].apply(get_sentiment)
    sentiment_counts = review_cleaned["sentiment"].value_counts()

    # Plot the sentiment distribution pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(
        sentiment_counts,
        labels=sentiment_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=["#66b3ff", "#99ff99", "#ff6666"],
    )
    plt.title("Sentiment Analysis of Reviews")
    plt.axis("equal")  # Make the pie chart circular

    # Save the figure as an image
    plt.savefig("image/sentiment_analysis.png")


# Example Usage
plot_category_distribution(df)
plot_rating_distribution(df)
plot_correlation_analysis(df)
plot_sentiment_analysis(review_df)
