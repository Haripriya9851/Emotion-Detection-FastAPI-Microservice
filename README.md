# Emotion Classification Microservice

This document describes a microservice for emotion classification in text.

## Service Description

The service exposes a web API that accepts a sentence as input and returns the predicted emotion with a confidence score.

### Input

The service expects a JSON object with a single key, `text`, containing the sentence to be classified.

**Example Input:**
```json
{
  "text": "I am so happy today!"
}
```

### Output

The service returns a JSON object with the original text, the predicted emotion, and the confidence score of the prediction.

**Example Output:**
```json
{
  "text": "I am so happy today!",
  "predicted_emotion": "happiness",
  "confidence": 0.85
}
```

## Available Emotions

You can get a list of all available emotions by sending a GET request to the `/emotions` endpoint.

## Service URL

The service is deployed and available at the following URL:

[Your Deployed Service URL](https://your-service-url.up.railway.app)

*(Please replace the above URL with the one provided by Railway after deployment.)*

## How to Invoke the Service

You can use any HTTP client, like `curl` or Python's `requests` library, to invoke the service.

### Using `curl`
```bash
curl -X POST "https://your-service-url.up.railway.app/predict" \
-H "Content-Type: application/json" \
-d '{"text": "This is a test sentence."}'
```

### Using Python
```python
import requests

url = "https://your-service-url.up.railway.app/predict"
data = {"text": "This is another test sentence."}

response = requests.post(url, json=data)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")
```

# Test