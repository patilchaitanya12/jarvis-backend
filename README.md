# 🧠 JARVIS Backend

AI Chatbot Backend built with FastAPI + TensorFlow + LLM fallback.

---

## 🚀 Tech Stack

- FastAPI
- TensorFlow (Intent Classification)
- NumPy
- HuggingFace API (LLM fallback)
- uv (Astral Python package manager)
- Docker
- CORS middleware

---

## 🧠 Architecture Flow

User Message
    ↓
Intent Classification Model (TensorFlow)
    ↓
If confidence > threshold → Rule-based response
Else → LLM Fallback (HuggingFace)
    ↓
Structured JSON Response

---

## 📂 Project Structure

app/
 ├── main.py
 ├── brain.py
 ├── routers/
 │    └── chat.py
 ├── schemas/
 │    └── chat.py
 ├── service/
 │    └── brain_service.py
 └── intents.json

models/
 ├── chat_model.h5
 ├── tokenizer.pkl
 └── label_encoder.pkl

Dockerfile
pyproject.toml
uv.lock

---

## ⚙️ Environment Variables

Create `.env`:

HUGGINGFACE_API_KEY=your_key_here
CONFIDENCE_THRESHOLD=0.75

---

## 🏃 Run Locally

Using uv:

uv sync
uv run uvicorn app.main:app --reload

Backend runs on:

http://localhost:8000

Swagger Docs:

http://localhost:8000/docs

---

## 🐳 Run With Docker

docker build -t jarvis-backend .
docker run -p 8000:8000 jarvis-backend

---

## 📡 API Endpoint

POST /chat/

Request:
{
  "message": "Who made you?"
}

Response:
{
  "response": "I was made by Chaitanya.",
  "confidence": 1.0,
  "source": "rule"
}

---

## 🔥 Key Features

- Custom trained NLP intent classifier
- Confidence-based response routing
- LLM fallback mechanism
- Modular architecture
- Dockerized
- Production-ready API design

---

## 🎯 Future Improvements

- Redis caching
- CI/CD pipeline
- Logging & monitoring
- Model retraining pipeline
- Rate limiting

---

Built by Chaitanya Patil 🚀