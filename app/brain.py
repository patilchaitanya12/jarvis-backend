# app/brain.py
import json
import pickle
import random
import numpy as np
import os
import requests
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ---------------- CONFIG ----------------
MAX_LEN = 20
CONFIDENCE_THRESHOLD = 0.85

HF_MODEL = "google/flan-t5-base"
HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else None

# ---------------- LOAD ARTIFACTS (ONCE) ----------------
BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "intents.json")) as f:
    INTENTS = json.load(f)

MODEL = load_model(os.path.join(BASE_DIR, "..", "models", "chat_model.h5"))

with open(os.path.join(BASE_DIR, "..", "models", "tokenizer.pkl"), "rb") as f:
    TOKENIZER = pickle.load(f)

with open(os.path.join(BASE_DIR, "..", "models", "label_encoder.pkl"), "rb") as f:
    LABEL_ENCODER = pickle.load(f)

# ---------------- RULE-BASED LOGIC ----------------
def rule_override(text: str) -> str | None:
    text = text.lower()

    if "who made" in text or "who created" in text:
        return "I was made by Chaitanya."

    if "time" in text or "date" in text or "day" in text:
        now = datetime.now()
        return f"It is {now.strftime('%I:%M %p')} on {now.strftime('%A, %d %B %Y')}."

    return None

# ---------------- INTENT PREDICTION ----------------
def predict_intent(text: str) -> tuple[str, float]:
    sequence = TOKENIZER.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=MAX_LEN, truncating="post")

    probabilities = MODEL.predict(padded, verbose=0)[0]
    confidence = float(np.max(probabilities))
    tag = LABEL_ENCODER.inverse_transform([np.argmax(probabilities)])[0]

    return tag, confidence

# ---------------- HUGGING FACE FALLBACK ----------------
def query_llm(prompt: str) -> str:
    if not HF_HEADERS:
        return "I'm not sure how to respond to that."

    payload = {
        "inputs": f"You are JARVIS, a helpful assistant.\nUser: {prompt}",
        "parameters": {
            "max_new_tokens": 120,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(
            HF_API_URL,
            headers=HF_HEADERS,
            json=payload,
            timeout=15
        )
        if response.status_code == 200:
            return response.json()[0]["generated_text"].split("User:")[-1].strip()
    except Exception:
        pass

    return "I'm not sure how to respond to that."

# ---------------- MAIN BRAIN FUNCTION ----------------
def get_response(user_input: str) -> tuple[str, float, str]:
    """
    Returns:
    - response text
    - confidence score
    - source: 'rule', 'ml', or 'llm'
    """

    #Rule-based logic (highest priority)
    override = rule_override(user_input)
    if override:
        return override, 1.0, "rule"

    # ML intent prediction
    tag, confidence = predict_intent(user_input)

    if confidence >= CONFIDENCE_THRESHOLD:
        for intent in INTENTS["intents"]:
            if intent["tag"] == tag:
                return random.choice(intent["responses"]), confidence, "ml"

    # LLM fallback
    llm_response = query_llm(user_input)
    return llm_response, confidence, "llm"
