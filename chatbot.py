import json
import random
import re
import os
import joblib
import nltk
import numpy as np
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)

STOPWORDS = set(stopwords.words("english"))
MODEL_PATH = "model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"
META_PATH = "model_meta.pkl"
INTENTS_PATH = "intents.json"


def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS]
    return " ".join(tokens)


class CustomerSupportBot:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.tag_map = None
        self.intents = None
        self.load_or_train()

    def load_or_train(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH) and os.path.exists(META_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            meta = joblib.load(META_PATH)
            self.tag_map = meta["tag_map"]
            self.intents = meta["intents"]
        else:
            self._train()

    def _train(self):
        from train import load_intents, train_model, save_artifacts
        print("Training model from scratch...")
        texts, labels, intents, tag_map = load_intents(INTENTS_PATH)
        pipeline = train_model(texts, labels)
        save_artifacts(pipeline, tag_map, intents, MODEL_PATH, VECTORIZER_PATH)
        self.model = pipeline.named_steps["clf"]
        self.vectorizer = pipeline.named_steps["tfidf"]
        self.tag_map = tag_map
        self.intents = intents

    def _predict_intent(self, text: str) -> tuple:
        processed = preprocess_text(text)
        features = self.vectorizer.transform([processed])
        probs = self.model.predict_proba(features)[0]
        pred_idx = np.argmax(probs)
        confidence = probs[pred_idx]
        inv_tag_map = {v: k for k, v in self.tag_map.items()}
        intent_tag = inv_tag_map[pred_idx]
        return intent_tag, confidence

    def get_response(self, user_message: str) -> dict:
        intent_tag, confidence = self._predict_intent(user_message)

        if confidence < 0.4:
            return {
                "intent": "unknown",
                "confidence": round(float(confidence), 3),
                "response": (
                    "I'm sorry, I didn't quite understand that. "
                    "Could you try rephrasing your question?\n\n"
                    "If you need immediate assistance, please reach out to our support team at "
                    "support@electronix.com or call 1-800-353-2876."
                ),
            }

        for intent in self.intents:
            if intent["tag"] == intent_tag:
                response = random.choice(intent["responses"])
                break
        else:
            response = (
                "I'm not sure how to help with that. Please try rephrasing "
                "or contact our support team at support@electronix.com."
            )

        return {
            "intent": intent_tag,
            "confidence": round(float(confidence), 3),
            "response": response,
        }

    def get_suggestions(self) -> list:
        return [
            "What products do you have?",
            "Where is my order?",
            "I want a refund",
            "I forgot my password",
            "Talk to a human",
            "Do you ship internationally?",
        ]

    def get_category_name(self, intent_tag: str) -> str:
        names = {
            "greeting": "Greeting",
            "goodbye": "Goodbye",
            "product_information": "Product Information",
            "refund": "Refund",
            "order_status": "Order Status",
            "password_reset": "Password Reset",
            "contact_support": "Contact Support",
            "faq": "General FAQ",
        }
        return names.get(intent_tag, "Unknown")
