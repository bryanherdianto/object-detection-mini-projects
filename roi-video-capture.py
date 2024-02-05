import cv2 as cv

# Global variables to store ROI coordinates
roi_width, roi_height = 400, 200
roi_x, roi_y = 50, 50
drawing_roi = False
roi_offset_x, roi_offset_y = 0, 0

def color_and_draw_roi(frame):
    # Draw rectangle and set the color
    if drawing_roi is False:
        cv.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 0, 0), 2)
    else:
        cv.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 0, 255), 2)
    
    # Convert the ROI to grayscale
    roi_gray = cv.cvtColor(frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width], cv.COLOR_BGR2GRAY)
    
    # Apply the grayscale ROI back to the original frame
    frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width] = cv.cvtColor(roi_gray, cv.COLOR_GRAY2BGR)

def mouse_callback(event, x, y, flags, param):
    global roi_x, roi_y, drawing_roi, roi_offset_x, roi_offset_y

    # Start drawing if left mouse button is down
    if event == cv.EVENT_LBUTTONDOWN:
        if roi_x < x < roi_x + roi_width and roi_y < y < roi_y + roi_height:
            drawing_roi = True
            roi_offset_x = x - roi_x
            roi_offset_y = y - roi_y

    # Stop drawing if left mouse button is up
    elif event == cv.EVENT_LBUTTONUP:
        drawing_roi = False

    # Move position of the rectangle if mouse is moved
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing_roi:
            roi_x = x - roi_offset_x
            roi_y = y - roi_offset_y

# Open the video capture
cap = cv.VideoCapture(0)

# Check if the video capture is successful
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Create a window and set the mouse callback function
cv.namedWindow('Frame with ROI')
cv.setMouseCallback('Frame with ROI', mouse_callback)

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # Break the loop if the video is finished
    if not ret:
        break

    # Display ROI
    roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
    roi = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    cv.imshow('ROI', roi)
    
    # Draw the fixed-size ROI on the frame
    color_and_draw_roi(frame)
    
    # Display the frame with the interactive ROI
    cv.imshow('Frame with ROI', frame)

    # Break the loop if 'q' is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv.destroyAllWindows()