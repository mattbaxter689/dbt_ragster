import pandas as pd
import nltk
import re
import string
import nltk
import emoji
import ssl
from sqlalchemy.engine import Engine
from textblob import TextBlob
from num2words import num2words
from dbt_ragster.assets.reddit.constant import (
    chat_words_list,
    chat_words_map_dict,
)

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# nltk.download(
#     ["stopwords", "punkt_tab", "averaged_perceptron_tagger_eng", "corpora"]
# )
nltk.download("stopwords")
nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("corpora")
from nltk.corpus import stopwords


class TextProcessor:
    def __init__(self) -> None:
        pass

    def process_all(self, engine: Engine) -> pd.DataFrame:
        data = self.extract_text_data(engine=engine)
        data = self.remove_urls(data=data)
        data = self.convert_chat_words(data=data)
        data = self.remove_stop_and_punctuation(data=data)
        data = self.remove_emojis(data=data)
        data = self.textualize_numbers(data=data)
        data = self.lemmatize_words(data=data)

        return data[["comment_id", "body_final"]]

    def extract_text_data(self, engine: Engine) -> pd.DataFrame:

        with engine.begin() as conn:
            text_data = pd.read_sql(
                """
                select body, comment_id
                from comment_data
                """,
                conn,
            )

        return text_data

    def textualize_numbers(self, data: pd.DataFrame) -> pd.DataFrame:

        def num_to_text(text: str) -> str:
            output = []
            for word in text.split():
                if word.isdigit():
                    output.append(num2words(word))
                else:
                    output.append(word)

            return " ".join(output)

        data["new_body"] = data["new_body"].apply(lambda x: num_to_text(x))

        return data

    def remove_stop_and_punctuation(self, data: pd.DataFrame) -> pd.DataFrame:

        def remove_punctuation(text: str) -> str:
            return text.translate(str.maketrans("", "", string.punctuation))

        def remove_stops(text: str) -> str:
            stops = set(stopwords.words("english"))
            return " ".join(
                [word for word in str(text).split() if word not in stops]
            )

        data["new_body"] = (
            data["new_body"].str.lower().str.replace("`|’", "'", regex=True)
        )
        data["new_body"] = data["new_body"].apply(
            lambda x: remove_punctuation(x)
        )
        data["new_body"] = data["new_body"].apply(lambda x: remove_stops(x))

        return data

    def remove_emojis(self, data: pd.DataFrame) -> pd.DataFrame:
        def remove_emoji(text: str) -> str:
            return emoji.replace_emoji(text, "")

        data["new_body"] = data["new_body"].apply(lambda x: remove_emoji(x))

        return data

    def remove_urls(self, data: pd.DataFrame) -> pd.DataFrame:
        def remove_url(text: str) -> str:
            url_pattern = re.compile(r"https?://\S+|www\.\S+")
            return url_pattern.sub(r"", text)

        data["new_body"] = data["body"].apply(lambda x: remove_url(x))

        return data

    def convert_chat_words(self, data: pd.DataFrame) -> pd.DataFrame:
        def convert_chat(text: str) -> str:
            new_text = []
            for word in text.split():
                if word.upper() in chat_words_list:
                    new_text.append(chat_words_map_dict[word.upper()])
                else:
                    new_text.append(word)
            return " ".join(new_text)

        data["new_body"] = data["new_body"].apply(lambda x: convert_chat(x))

        return data

    def lemmatize_words(self, data: pd.DataFrame) -> pd.DataFrame:
        def lemma(text: str) -> str:
            sentence = TextBlob(text)
            tag_dict = {"J": "a", "N": "n", "V": "v", "R": "r"}
            words_tags = [
                (word, tag_dict.get(pos[0], "n"))
                for word, pos in sentence.tags
            ]
            lemma_list = [word.lemmatize(tag) for word, tag in words_tags]
            return " ".join(lemma_list)

        data["body_final"] = data["new_body"].apply(lambda x: lemma(x))

        return data
