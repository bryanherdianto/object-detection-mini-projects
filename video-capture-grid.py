# import the opencv library 
import cv2 as cv

# get rows and cols from user input
rows = int(input("How many rows? "))
cols = int(input("How many cols? "))

# set position of window
x = 0
y = 0

# define a video capture object 
vid = cv.VideoCapture(0)

# get the width and height from vid object
width = int(vid.get(3))
height = int(vid.get(4))

# define a resize variable to control how big/small window
resize = 5

# modified width and height variable
newWidth = width // resize
newHeight = height // resize

# list of colors for the window
colors = ['bgr', 'rgb', 'gray']

while True:

    for row in range(rows):

        # set startIndex to row value for color change
        startIndex = row

        for col in range(cols):

            # capture the video frame by frame 
            ret, frame = vid.read()

            # convert color
            color = colors[startIndex % len(colors)]
            if color == 'rgb':
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            elif color == 'gray':
                frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            # resize window
            frame = cv.resize(frame, dsize=(newWidth, newHeight))

            # display the resulting frame 
            cv.imshow(str(row) + str(col), frame)

            # set coordinates for window
            cv.moveWindow(str(row) + str(col), x, y)

            # update coordinate x
            x += newWidth

            # increment startIndex for color change
            startIndex += 1

        # reset coordinate x
        x = 0

        # update coordinate y
        y += (newHeight + 30)
	
    # reset coordinate y
    y = 0

	# the 'q' button is set as the quitting button
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# after the loop release the vid object 
vid.release()

# destroy all the windows 
cv.destroyAllWindows()