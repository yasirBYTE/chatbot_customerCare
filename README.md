# 🤖 Electronix Customer Support Bot

An intelligent chatbot built with Python, Streamlit, and scikit-learn that simulates customer support interactions for an electronics store.

## Tech Stack

- **Python 3** — Core language
- **Streamlit** — Web UI framework
- **NLTK** — Tokenization & stopword removal
- **Scikit-learn** — TF-IDF vectorization & Logistic Regression
- **Pandas** — Analytics dashboard
- **Joblib** — Model serialization

## Features

- Clean dark-themed chat interface with chat history
- 8 supported intents: Greeting, Goodbye, Product Info, Refund, Order Status, Password Reset, Contact Support, FAQ
- NLP preprocessing pipeline (lowercasing, punctuation removal, tokenization, stopword filtering)
- TF-IDF + Logistic Regression intent classification with confidence scoring
- Low-confidence fallback (gracefully suggests contacting support)
- Quick-reply suggestion buttons
- Analytics sidebar (total conversations, top category, category breakdown)
- Auto-trains model on first run

## Run Locally

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yasirBYTE/chatbot_customerCare.git
   cd chatbot_customerCare
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   streamlit run app.py
   ```

4. **Open in browser**

   The app will launch at `http://localhost:8501`. The model trains automatically on first launch — no additional setup needed.

## Project Structure

```
chatbot_customerCare/
├── app.py              # Streamlit UI — chat interface, analytics, styling
├── chatbot.py          # Bot logic — intent prediction, response generation
├── train.py            # Training pipeline — TF-IDF + Logistic Regression
├── intents.json        # Training data — patterns & responses for 8 intents
├── requirements.txt    # Python dependencies
├── model.pkl           # Trained classifier (auto-generated)
├── vectorizer.pkl      # TF-IDF vectorizer (auto-generated)
├── model_meta.pkl      # Intent metadata (auto-generated)
└── index.html          # GitHub Pages landing page
```

## Customizing Intents

Edit `intents.json` to add or modify training examples and responses. Delete the `model.pkl`, `vectorizer.pkl`, and `model_meta.pkl` files and restart the app to retrain with your changes.

## License

MIT
