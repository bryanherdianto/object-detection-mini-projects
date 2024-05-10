# Importing necessary libraries
from ultralytics import YOLO  # Import YOLO model from Ultralytics

# Initializing YOLO model with pre-trained weights
model = YOLO("miniPythonProjects\yoloDetection\yolov8m.pt")

# Make sure source is 0 to predict from webcam
results = model.predict(source="0", show=True)

print(results)
