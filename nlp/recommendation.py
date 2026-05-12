import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import re

# A helper to preprocess problem strings for simple matching

nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

_stop_words = set(stopwords.words("english"))


def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    tokens = [t for t in text.split() if t not in _stop_words]
    return " ".join(tokens)


class ProblemRecommender:
    def __init__(self, csv_path: str):
        # load dataset
        self.df = pd.read_csv(csv_path)
        # preprocess problem names for easier matching
        self.df["_clean_problem"] = self.df["problem"].apply(preprocess_text)
        # prepare TF-IDF vectorizer for semantic search (replaces sentence-transformers)
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.embeddings = self.vectorizer.fit_transform(self.df["_clean_problem"].tolist())

    def filter_by_topic_difficulty(self, topics=None, difficulties=None):
        """Compatibility wrapper around the generic :meth:`filter` method.

        Keeps the original API but simply delegates to :meth:`filter` under the
        hood so that future criteria (company, tags, etc.) can be handled with
        the same code path.
        """
        return self.filter(topic=topics, difficulty=difficulties)

    def filter(self, **criteria):
        """Generic filtering helper.

        Each keyword argument corresponds to a column in the underlying dataframe.
        Values may be a single string or an iterable of strings. Comparison is
        case-insensitive and ignores empty values. Supports matching within
        comma-separated values (like 'company' or 'tags').
        """
        df = self.df
        for col, val in criteria.items():
            if not val or col not in df.columns:
                continue
            
            # Helper function to check if any of the target values match the cell
            def _matches(cell_val, target_values):
                if pd.isna(cell_val):
                    return False
                items = [i.strip().lower() for i in str(cell_val).split(',')]
                return any(t in items for t in target_values)

            target_values = [str(v).lower() for v in val if v] if isinstance(val, (list, tuple)) else [str(val).lower()]
            if not target_values:
                 continue
                 
            df = df[df[col].apply(lambda x: _matches(x, target_values))]
        return df

    def recommend_similar(self, query: str, top_k=5):
        """Use TF-IDF similarity to recommend problems given a query string.

        Returns a list of dicts (records) containing the original dataframe
        columns.  This makes it easier for templates to show additional
        metadata (url, tags, etc.) if the dataset contains those fields.
        """
        clean = preprocess_text(query)
        q_vec = self.vectorizer.transform([clean])
        sims = cosine_similarity(q_vec, self.embeddings)[0]
        idxs = sims.argsort()[::-1][:top_k]
        return self.df.iloc[idxs].to_dict(orient="records")
