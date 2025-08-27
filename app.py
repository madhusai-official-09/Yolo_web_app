from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import io
from ultralytics import YOLO
from PIL import Image
import threading

app = Flask(__name__)

# Load model once (change the model path/name if you have a different file)
MODEL_PATH = "yolov8n.pt"  # place your model in the same folder or change this path
try:
    model = YOLO(MODEL_PATH)
    print(f"Loaded model: {MODEL_PATH}")
except Exception as e:
    print(f"Warning: Failed to load model '{MODEL_PATH}'. Make sure the file exists. Error: {e}")
    model = None

lock = threading.Lock()

def decode_base64_image(data_url):
    # data_url like "data:image/jpeg;base64,/9j/4AAQ..."
    header, encoded = data_url.split(",", 1)
    data = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(data)).convert("RGB")
    arr = np.array(image)[:, :, ::-1].copy()  # RGB->BGR
    return arr

def encode_image_to_dataurl(img_bgr):
    # Input BGR numpy array -> return data URL (jpeg)
    ret, buf = cv2.imencode('.jpg', img_bgr)
    if not ret:
        return None
    b64 = base64.b64encode(buf).decode('utf-8')
    return "data:image/jpeg;base64," + b64

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    global model
    if model is None:
        return jsonify({"error": "Model not loaded on server. Place model file and restart."}), 500
    data = request.json.get('image', None)
    if not data:
        return jsonify({"error": "No image received"}), 400
    try:
        frame = decode_base64_image(data)
    except Exception as e:
        return jsonify({"error": f"Failed to decode image: {e}"}), 400
    # Run detection under lock to avoid model concurrency issues
    with lock:
        try:
            results = model.predict(source=frame, stream=False, show=False)
            annotated = results[0].plot()  # BGR image
        except Exception as e:
            return jsonify({"error": f"Model prediction failed: {e}"}), 500
    data_url = encode_image_to_dataurl(annotated)
    if data_url is None:
        return jsonify({"error": "Failed to encode output image"}), 500
    return jsonify({"image": data_url})

if __name__ == '__main__':
    # For development only. Use gunicorn for production.
    app.run(host='0.0.0.0', port=5000, debug=True)
