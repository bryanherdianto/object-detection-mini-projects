# import opencv which is cv2 as cv
import cv2 as cv

# rescale image
def rescale(frame, scale=0.5):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimension = (width, height)

    return cv.resize(frame, dimension, interpolation=cv.INTER_AREA)

# capture the video into a variable capture
capture = cv.VideoCapture('opencv-training-assets/dog.mp4')

# the way to play a video in opencv is by reading every frame of it and showing it every loop
while True:
    # every frame of the video is read
    isTrue, frame = capture.read()

    # rescale original frame
    rescaledFrame = rescale(frame)

    if isTrue:
        # show the frame that changes every loop
        cv.imshow('A dog', frame)

        # show the rescaled frame that changes every loop
        cv.imshow('A rescaled dog', rescaledFrame)

        # if the 'd' key is pressed, then it will break
        if cv.waitKey(0) == ord('d'):
            break
    else:
        break

# release the video file that we captured
capture.release()

# destroy the window
cv.destroyAllWindows()