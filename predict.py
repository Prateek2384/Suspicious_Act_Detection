import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder

# Constants
MODEL_PATH = "suspicious_activity_model.keras"
CLASSES = ['walking', 'vandalism', 'fighting']  # Must match folder names exactly
TARGET_FRAMES = 30  # Must match what your model expects
RESIZE_DIM = (64, 64)  # Must match model's input shape

# Initialize components
model = load_model(MODEL_PATH)
label_encoder = LabelEncoder()
label_encoder.fit(CLASSES)  # Critical for correct label mapping

def extract_frames(video_path):
    """Extract exactly TARGET_FRAMES from video, centered."""
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate start frame to center the segment
    start_frame = max(0, (total_frames - TARGET_FRAMES) // 2)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    frames = []
    for _ in range(TARGET_FRAMES):
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, RESIZE_DIM)
        frames.append(frame)
    
    cap.release()
    return np.array(frames) / 255.0 if len(frames) == TARGET_FRAMES else None

def predict_video(video_path):
    """Predict activity from video file."""
    frames = extract_frames(video_path)
    if frames is None:
        return {"error": f"Video must have >= {TARGET_FRAMES} frames"}
    
    # Add batch dimension and predict
    frames = np.expand_dims(frames, axis=0)
    pred = model.predict(frames, verbose=0)[0]
    class_idx = np.argmax(pred)
    class_label = label_encoder.inverse_transform([class_idx])[0]
    
    return {
        "activity": class_label,
        "status": "suspicious" if class_label == "vandalism" or class_label=="fighting" else "normal",
        "confidence": float(pred[class_idx])  # Add confidence score
    }

# Example usage
if __name__ == "__main__":
    # Test with a sample video from your dataset
    test_video = os.path.join("database3", "vandalism", "test", "30r.mp4")  # Example
    
    if os.path.exists(test_video):
        result = predict_video(test_video)
        print(f"Prediction: {result}")
    else:
        print(f"Test video not found at: {test_video}")