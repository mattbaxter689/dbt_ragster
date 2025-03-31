import ssl
import nltk
from dbt_ragster.assets.torch_model.db_conn import engine
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dbt_ragster.assets.torch_model.dataset import TextDataset

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("vader_lexicon")


def main():
    analyzer = SentimentIntensityAnalyzer()

    def extract_score(text: str):
        score = analyzer.polarity_scores(text)
        compound = score["compound"]

        sentiment = "neutral"
        if compound >= 0.05:
            sentiment = "positive"

        elif compound <= -0.05:
            sentiment = "negative"

        return sentiment

    with engine.begin() as conn:
        text_data = pd.read_sql(
            """
            select *
            from processed_data
            """,
            conn,
        )

    text_data["sentiment"] = text_data["body_final"].apply(extract_score)
    text_data["test"] = 1
    text_data["sentiment"] = text_data["sentiment"].map(
        {"neutral": 0, "positive": 1, "negative": 2}
    )

    handler = TextDataset(text_data=text_data)


if __name__ == "__main__":
    main()
