import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment",
        framework="pt"   # 🔥 FIX
    )

sentiment_analyzer = load_model()

LABEL_MAP = {
    "LABEL_0": "Negative 😡",
    "LABEL_1": "Neutral 😐",
    "LABEL_2": "Positive 😊"
}

st.set_page_config(page_title="Sentiment Analysis App", page_icon="🧠")
st.title("🧠 Sentiment Analysis")
st.write("Analyze the sentiment of any post or comment using AI.")

text = st.text_area(
    "Enter a post or comment:",
    height=150
)

if st.button("Analyze Sentiment"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        result = sentiment_analyzer(text[:512])[0]  # safe length
        sentiment = LABEL_MAP[result["label"]]
        confidence = result["score"]

        st.success(f"Sentiment: {sentiment}")
        st.write(f"Confidence: {confidence:.2f}")
