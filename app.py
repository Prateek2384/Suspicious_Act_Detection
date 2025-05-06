from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from predict import predict_video
import tempfile
import os
from datetime import datetime

app = Flask(__name__)

# Configuration
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def handle_prediction():
    # Check if file exists in request
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    video = request.files['file']
    
    # Validate filename and extension
    if video.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    if not allowed_file(video.filename):
        return jsonify({"error": f"Allowed formats: {ALLOWED_EXTENSIONS}"}), 400
    
    # Secure filename and create temp path
    filename = secure_filename(video.filename)
    temp_path = os.path.join(tempfile.gettempdir(), filename)
    
    try:
        # Save and validate file size
        video.save(temp_path)
        if os.path.getsize(temp_path) > MAX_FILE_SIZE:
            return jsonify({"error": f"File exceeds {MAX_FILE_SIZE//(1024*1024)}MB limit"}), 400
        
        # Process video
        result = predict_video(temp_path)
        result["timestamp"] = datetime.utcnow().isoformat() + "Z"
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)