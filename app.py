from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(
    title="Emotion Classification Microservice",
    description="A microservice that classifies emotions in text using ULMFiT model",
    version="1.0.0"
)

# Mock emotions for demonstration
EMOTIONS = ["happiness", "sadness", "anger", "fear", "love", "surprise", "disgust", "neutral"]

class TextInput(BaseModel):
    text: str

class EmotionResponse(BaseModel):
    text: str
    predicted_emotion: str
    confidence: float

def mock_predict_emotion(text: str) -> tuple[str, float]:
    """Mock emotion prediction function"""
    # Simple keyword-based prediction for demonstration
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['happy', 'joy', 'excited', 'great', 'wonderful']):
        return "happiness", 0.85
    elif any(word in text_lower for word in ['sad', 'depressed', 'miserable', 'unhappy']):
        return "sadness", 0.80
    elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'hate']):
        return "anger", 0.75
    elif any(word in text_lower for word in ['afraid', 'scared', 'terrified', 'fear']):
        return "fear", 0.70
    elif any(word in text_lower for word in ['love', 'adore', 'passion', 'romantic']):
        return "love", 0.90
    elif any(word in text_lower for word in ['surprised', 'amazed', 'shocked', 'wow']):
        return "surprise", 0.65
    elif any(word in text_lower for word in ['disgust', 'gross', 'nasty', 'revolting']):
        return "disgust", 0.60
    else:
        return "neutral", 0.50

@app.get("/")
async def root():
    return {
        "message": "Emotion Classification Microservice",
        "status": "running",
        "model_loaded": True,
        "note": "Using mock prediction for demonstration"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=EmotionResponse)
async def predict_emotion(input_data: TextInput):
    try:
        # Make prediction using mock function
        predicted_emotion, confidence = mock_predict_emotion(input_data.text)
        
        return EmotionResponse(
            text=input_data.text,
            predicted_emotion=predicted_emotion,
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/emotions")
async def get_available_emotions():
    return {"available_emotions": EMOTIONS}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 