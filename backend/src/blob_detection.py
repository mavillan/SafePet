#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv

PATH='/home/martin/HDD/Mega/SafePet/SafePetData/training_set_processed/'

# Read image
img = cv.imread(PATH+"dog0000.jpg", cv.IMREAD_GRAYSCALE)

# Blur it
im = cv.GaussianBlur(img,(13,13),10)


# Setup SimpleBlobDetector parameters.
params = cv.SimpleBlobDetector_Params()
 
# Change thresholds
params.minThreshold = 10;
params.maxThreshold = 200;
 
# Filter by Area.
params.filterByArea = True
params.minArea = 1500 # 60% of image
 
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1
 
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87
 
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01
 
# Create a detector with the parameters
detector = cv.SimpleBlobDetector(params)

# Detect blobs.
keypoints = detector.detect(im)

# Draw detected blobs as red circles.
# cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv.namedWindow( "Keypoints", cv.WINDOW_NORMAL)
cv.imshow("Keypoints", im_with_keypoints)
cv.waitKey(0)
cv.destroyAllWindows()
