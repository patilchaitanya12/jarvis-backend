from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    response: str
    confidence: float
    source: str #ml or llm