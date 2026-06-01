import json
import re
import nltk
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)

STOPWORDS = set(stopwords.words("english"))


def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS]
    return " ".join(tokens)


def load_intents(path: str = "intents.json") -> tuple:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts, labels = [], []
    tag_map = {}
    for intent in data["intents"]:
        tag = intent["tag"]
        if tag not in tag_map:
            tag_map[tag] = len(tag_map)
        for pattern in intent["patterns"]:
            texts.append(preprocess_text(pattern))
            labels.append(tag_map[tag])

    return texts, labels, data["intents"], tag_map


def train_model(texts: list, labels: list) -> tuple:
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
        ("clf", LogisticRegression(C=2.0, max_iter=500, solver="lbfgs")),
    ])
    pipeline.fit(texts, labels)
    return pipeline


def save_artifacts(pipeline, tag_map, intents, model_path="model.pkl", vectorizer_path="vectorizer.pkl"):
    joblib.dump(pipeline.named_steps["clf"], model_path)
    joblib.dump(pipeline.named_steps["tfidf"], vectorizer_path)
    meta = {"tag_map": tag_map, "intents": intents}
    joblib.dump(meta, "model_meta.pkl")
    print(f"Model saved to {model_path}")
    print(f"Vectorizer saved to {vectorizer_path}")
    print(f"Metadata saved to model_meta.pkl")


def main():
    print("Loading intents...")
    texts, labels, intents, tag_map = load_intents()
    print(f"Training on {len(texts)} examples across {len(tag_map)} intents.")
    pipeline = train_model(texts, labels)
    save_artifacts(pipeline, tag_map, intents)
    print("Training complete!")


if __name__ == "__main__":
    main()
