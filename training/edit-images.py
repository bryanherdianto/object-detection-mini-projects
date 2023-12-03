import cv2 as cv
import numpy as np

# DRAWING -----------------------------------------------------------------------------------------------
# initialize a blank window that has the color black
blank = np.zeros((500, 500, 3), dtype='uint8')

# paint the image a certain colour
# the zeroth element refers to the height, while the first is the width
# the color is BGR
blank[200:300, 300:400] = 0, 0, 255

# double slash (//) means floor division
# draw a rectangle
cv.rectangle(blank, (0, 0), (blank.shape[1]//2, blank.shape[0]//2), (0, 255, 0), thickness=-1)

# thickness --> -1 means that the shape is filled
# draw a circle
cv.circle(blank, (blank.shape[1]//2, blank.shape[0]//2), 40, (0, 0, 255), thickness=-1)

# draw a line
cv.line(blank, (100, 250), (300, 400), (255, 255, 255), thickness=1)

# write a text
cv.putText(blank, 'Hello World!', (0, 225), cv.FONT_HERSHEY_DUPLEX, 1.0, (12, 255, 255), 2)
cv.imshow('Final Result of Drawing', blank)
# -------------------------------------------------------------------------------------------------------

# STYLING -----------------------------------------------------------------------------------------------
img = cv.imread('opencv-training-assets/cat.jpg')

# converting to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('grayscale cat', gray)

# blur the image 
blur = cv.GaussianBlur(img, (7, 7), cv.BORDER_DEFAULT)
cv.imshow('blurred cat', blur)

# highlight edges of image
canny = cv.Canny(blur, 125, 175)
cv.imshow('canny edges cat', canny)

# dilating the image --> make the edges bolder
dilated = cv.dilate(canny, (15, 15), iterations=3)
cv.imshow('dilated cat', dilated)

# eroding the edges of the image
eroded = cv.erode(dilated, (7, 7), iterations=3)
cv.imshow('eroded cat', eroded)

# cropping --> [height, width]
cropped = img[50:200, 200:400]
cv.imshow('cropped cat', cropped)
# -------------------------------------------------------------------------------------------------------

# TRANSFORMATION ----------------------------------------------------------------------------------------
img_1 = cv.imread('opencv-training-assets/cat.jpg')

# translation
def translate(img, x, y):
    transMat = np.float32([[1, 0, x], [0, 1, y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)

translated = translate(img_1, 50, 50)
cv.imshow('translated cat', translated)

# rotation
def rotate(img, angle, rotPoint=None):
    height, width = img.shape[:2]
    dimensions = (width, height)

    if rotPoint is None:
        rotPoint = (width//2, height//2)
    
    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)

    return cv.warpAffine(img, rotMat, dimensions)

rotated = rotate(img_1, -90, (40, 70))
cv.imshow('rotated cat', rotated)

# reflection
flip = cv.flip(img_1, -1)
cv.imshow('flipped cat', flip)
# -------------------------------------------------------------------------------------------------------

cv.waitKey(0)