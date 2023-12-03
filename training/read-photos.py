# import opencv which is cv2 as cv
import cv2 as cv

# rescale image
def rescale(frame, scale=0.5):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimension = (width, height)

    return cv.resize(frame, dimension, interpolation=cv.INTER_AREA)

# read an image and store it to the variable img
img = cv.imread('opencv-training-assets/cat.jpg')

# rescale original image
rescaledImage = rescale(img)

# show the img on a window
cv.imshow('A cat', img)

# show the img on a window
cv.imshow('A rescaled cat', rescaledImage)

# window will close if a key is pressed, else it will open forever
cv.waitKey(0)