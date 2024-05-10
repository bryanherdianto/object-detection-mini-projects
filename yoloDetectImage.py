# Importing necessary libraries
from ultralytics import YOLO  # Import YOLO model from Ultralytics
from tkinter import filedialog  # Import filedialog from tkinter for file selection

# Initializing YOLO model with pre-trained weights
model = YOLO("miniPythonProjects\yoloDetection\yolov8m.pt")

# Prompting user to select an image file using a file dialog
image = filedialog.askopenfilename()

# Performing object detection on the selected image
results = model.predict(image)

# Printing the number of detected objects
print("There are " + str(len(results[0].boxes)) + " object(s)\n")

# Extracting and printing information about each detected object
result = results[0]
for box in result.boxes:
    class_id = result.names[box.cls[0].item()]
    coordinates = box.xyxy[0].tolist()
    coordinates = [round(x) for x in coordinates]
    prob = round(box.conf[0].item(), 2)
    print("Object type:", class_id)
    print("Coordinates:", coordinates)
    print("Probability:", prob)
    print("")
