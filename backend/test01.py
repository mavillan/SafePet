""" Test with Harris corner detector """

import cv2
import numpy as np

PATH='/home/martin/HDD/Dropbox/SafePet/images/'

filename = PATH+'9_nariz.jpg'
img = cv2.imread(filename)

cv2.namedWindow('main', cv2.WINDOW_NORMAL)
cv2.imshow('main',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cv2.namedWindow('main', cv2.WINDOW_NORMAL)
cv2.imshow('main',gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)

cv2.namedWindow('main', cv2.WINDOW_NORMAL)
cv2.imshow('main',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]

cv2.namedWindow('main', cv2.WINDOW_NORMAL)
cv2.imshow('main',dst)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
