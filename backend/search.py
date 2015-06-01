#!/usr/bin/python
import sys
import cv2
import numpy as np

PATH='/home/martin/HDD/Dropbox/SafePet/images/'
SHAPE=(960,1280)
FEATURES=1228800


if __name__='__main__':
	if len(sys.argv)>2:
		sys.exit('Wrong input!')

	filename=PATH+sys.argv[1]
	img=cv2.imread(filename)

	# Plot of original image
	cv2.namedWindow('main',cv2.WINDOW_NORMAL)
	cv2.imshow('main',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# To grayscale and to float
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	gray=np.float32(gray)

	# Plot of grayscale image
	cv2.namedWindow('main', cv2.WINDOW_NORMAL)
	cv2.imshow('main',gray)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# Reshape to features space
	v=gray.reshape(1,FEATURES)


