from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastai.text.all import load_learner
import os

app = FastAPI(
    title="Emotion Classification Microservice",
    description="A microservice that classifies emotions in text using a FastAI model",
    version="1.0.0"
)

# Load the FastAI model at startup
try:
    learn = load_learner('emotion_classifier.pkl')
    EMOTIONS = list(learn.dls.vocab[1])
except Exception as e:
    learn = None
    EMOTIONS = []
    print(f"Model loading failed: {e}")

class TextInput(BaseModel):
    text: str

class EmotionResponse(BaseModel):
    text: str
    predicted_emotion: str
    confidence: float

@app.get("/")
async def root():
    return {
        "message": "Emotion Classification Microservice",
        "status": "running",
        "model_loaded": learn is not None,
        "note": "Using FastAI model"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": learn is not None}

@app.post("/predict", response_model=EmotionResponse)
async def predict_emotion(input_data: TextInput):
    if learn is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    pred, pred_idx, probs = learn.predict(input_data.text)
    confidence = float(probs[learn.dls.vocab[1].o2i[pred]])
    return EmotionResponse(
        text=input_data.text,
        predicted_emotion=str(pred),
        confidence=confidence
    )

@app.get("/emotions")
async def get_available_emotions():
    return {"available_emotions": EMOTIONS}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 