import cv2 as cv
import numpy as np

# read image
img = cv.imread('opencv-training-assets/cat.jpg')

# make two blank windows
blank1 = np.zeros(img.shape, dtype='uint8')
blank2 = np.zeros(img.shape, dtype='uint8')

# make image grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# make canny image
canny = cv.Canny(img, 125, 175)
cv.imshow('canny img', canny)

# different kinds of threshold
ret, thresh = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)
cv.imshow('thresh img', thresh)

retInv, threshInv = cv.threshold(gray, 125, 255, cv.THRESH_BINARY_INV)
cv.imshow('threshInv img', threshInv)

adaptiveThresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 5.0)
cv.imshow('adaptiveThresh img', adaptiveThresh)

# using canny to find contours
contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contours)} contours found from canny!')

cv.drawContours(blank1, contours, -1, (0, 255, 255), 1)
cv.imshow('contours drawn from canny', blank1)

# using threshold to find contours
contours, hierarchies = cv.findContours(adaptiveThresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contours)} contours found from thresh!')

cv.drawContours(blank2, contours, -1, (0, 255, 255), 1)
cv.imshow('contours drawn from thresh', blank2)

cv.waitKey(0)