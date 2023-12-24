import cv2 as cv
import numpy as np

img = cv.imread('opencv-training-assets/cat.jpg')

blank = np.zeros(img.shape[:2], dtype='uint8')

# make a circle mask
circle = cv.circle(blank.copy(), (img.shape[1]//2 + 90, img.shape[0]//2), 150, 255, -1)

masked = cv.bitwise_and(img, img, mask=circle)
cv.imshow('Cat Face Image', masked)

# make a rectangle mask
rect = cv.rectangle(blank.copy(), (0,0), (img.shape[1], img.shape[0]//2), 255, -1)

masked_double = cv.bitwise_and(masked, masked, mask=rect)
cv.imshow('Double Masked Cat Image', masked_double)

cv.waitKey(0)