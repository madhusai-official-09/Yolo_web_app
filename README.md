# YOLO Live Webcam Web App

This package contains a minimal Flask web application that accepts webcam frames from the browser,
runs YOLO detection on the server, and returns annotated frames to the browser.

## Files
- `app.py` - Flask server. POST `/detect` with JSON `{image: "data:image/jpeg;base64,..."}` to receive `{image: "data:image/jpeg;base64,..."}` back.
- `templates/index.html` - Client UI that captures webcam and sends frames.
- `static/script.js` - Client JS to capture and send frames.
- `requirements.txt` - Python dependencies.

## Setup
1. Create a virtualenv: `python -m venv venv` and activate it.
2. Install dependencies: `pip install -r requirements.txt`.
3. Place your YOLO model file in the same folder, e.g. `yolo11s.pt`. If you don't have `yolo11s.pt`, change `MODEL_PATH` in `app.py` to a model you have (for example, `yolov8n.pt`).
4. Run: `python app.py` and open `http://localhost:5000` in your browser.

## Notes
- This demo sends webcam frames over HTTP to the server; it's suitable for local testing. For production or lower-latency streaming, consider WebRTC or a websocket pipeline.
- Model loading may take time and requires GPU/CUDA support if you want real-time speed.
