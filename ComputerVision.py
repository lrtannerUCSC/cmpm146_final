from inference_sdk import InferenceHTTPClient

# Initialize the Roboflow Inference Client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="STo3KO5ZeI7ewemeqMvR"
)

def detect_objects(image_path, model_id="group_work/2"):
    """Run object detection using Roboflow inference API."""
    result = CLIENT.infer(image_path, model_id=model_id)
    
    detected_items = {prediction["class"].title().replace("_", " ") for prediction in result["predictions"]}
    return detected_items

if __name__ == "__main__":
    image_path = "fridge.jpg"
    
    detected_items = detect_objects(image_path)
    
    print("Detected items:", detected_items)
