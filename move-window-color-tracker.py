import cv2 as cv
import numpy as np

# Function to handle trackbar changes for hue low value
def onTrack1(val):
    global hueLow
    hueLow = val
    print("Hue Low", hueLow)

# Function to handle trackbar changes for hue high value
def onTrack2(val):
    global hueHigh
    hueHigh = val
    print("Hue High", hueHigh)

# Function to handle trackbar changes for saturation low value
def onTrack3(val):
    global satLow
    satLow = val
    print("Sat Low", satLow)

# Function to handle trackbar changes for saturation high value
def onTrack4(val):
    global satHigh
    satHigh = val
    print("Sat High", satHigh)

# Function to handle trackbar changes for value low value
def onTrack5(val):
    global valLow
    valLow = val
    print("Val Low", valLow)

# Function to handle trackbar changes for value high value
def onTrack6(val):
    global valHigh
    valHigh = val
    print("Val High", valHigh)

# Setting width and height for camera resolution
width = 640
height = 360

# Initial values for HSV thresholds
hueLow = 100
hueHigh = 170
satLow = 10
satHigh = 250
valLow = 10
valHigh = 250

# Open webcam
cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, height)

# Creating trackbars window
cv.namedWindow("trackbars")

# Creating trackbars to adjust HSV thresholds
cv.createTrackbar('Hue Low', 'trackbars', hueLow, 179, onTrack1)
cv.createTrackbar('Hue High', 'trackbars', hueHigh, 179, onTrack2)
cv.createTrackbar('Sat Low', 'trackbars', satLow, 255, onTrack3)
cv.createTrackbar('Sat High', 'trackbars', satHigh, 255, onTrack4)
cv.createTrackbar('Val Low', 'trackbars', valLow, 255, onTrack5)
cv.createTrackbar('Val High', 'trackbars', valHigh, 255, onTrack6)

# Creating window for camera feed
cv.namedWindow('camera')

# Main loop for capturing and processing frames
while True:
    # Read frame from webcam
    ret, frame = cam.read()

    # Break loop if frame cannot be retrieved
    if not ret:
        break

    # Convert frame from BGR to HSV color space
    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Define lower and upper bounds of the HSV color range
    lowerBound = np.array([hueLow, satLow, valLow])
    upperBound = np.array([hueHigh, satHigh, valHigh])

    # Create a mask using the defined color range
    mask = cv.inRange(frameHSV, lowerBound, upperBound)

    # Apply the mask to the original frame
    maskedFrame = cv.bitwise_and(frame, frame, mask=mask)

    # Find contours in the mask
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Iterate through each contour
    for contour in contours:
        # Calculate area of contour
        area = cv.contourArea(contour)
        # If contour area is above a certain threshold, draw contour and bounding rectangle
        if area > 10_000:
            cv.drawContours(frame, [contour], 0, (255, 0, 0), 3)
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv.moveWindow("camera", x, y)

    # Display the mask, masked frame, and original frame
    cv.imshow("mask", mask)
    cv.imshow("maskedFrame", maskedFrame)
    cv.imshow("camera", frame)

    # Exit loop if 'q' key is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cam.release()
cv.destroyAllWindows()
