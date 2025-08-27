# Original script uploaded by the user (kept for reference)
import cv2
from ultralytics import YOLO

print(f"OpenCV version: {cv2.__version__}")
model = YOLO("yolo11s.pt")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()
print("Webcam opened successfully. Press 'q' to quit the detection window.")
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        results = model.predict(source=frame, show=False, stream=False)
        annotated_frame = results[0].plot()
        cv2.imshow("YOLO11 Real-time Detection", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam released and windows closed.")
