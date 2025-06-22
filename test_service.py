import requests
import json

# Test the microservice
def test_service():
    base_url = "http://localhost:8000"
    
    # Test health check
    print("Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test root endpoint
    print("\nTesting root endpoint...")
    try:
        response = requests.get(base_url)
        print(f"Root endpoint: {response.json()}")
    except Exception as e:
        print(f"Root endpoint failed: {e}")
    
    # Test available emotions
    print("\nTesting available emotions...")
    try:
        response = requests.get(f"{base_url}/emotions")
        print(f"Available emotions: {response.json()}")
    except Exception as e:
        print(f"Available emotions failed: {e}")
    
    # Test prediction
    print("\nTesting prediction...")
    test_texts = [
        "I am so pumped up!",
        "This boils my blood!",
        "I feel disappointed about this news.",
        "I love that this movie ended soon!"
    ]
    
    for text in test_texts:
        try:
            data = {"text": text}
            response = requests.post(f"{base_url}/predict", json=data)
            if response.status_code == 200:
                result = response.json()
                print(f"Text: '{text}' -> Emotion: {result['predicted_emotion']} (confidence: {result['confidence']:.3f})")
            else:
                print(f"Prediction failed for '{text}': {response.text}")
        except Exception as e:
            print(f"Prediction failed for '{text}': {e}")

if __name__ == "__main__":
    test_service() 