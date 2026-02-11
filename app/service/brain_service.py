from app.brain import get_response, predict_intent

confidence_threshold = 0.8

@staticmethod
def process_message(message: str):
    tag, confidence = predict_intent(message)
    
    if confidence >= confidence_threshold:
        response = get_response(message)
        return response, confidence, "ml"
    
    response = get_response(message)
    return response, confidence, "llm"