#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv


IMAGES_PATH='/home/martin/HDD/Dropbox/SafePet_Data/training_set_processed/'

if __name__=='__main__':
	if len(sys.argv)!=2:
		sys.exit('Wrong input!')	
	
	img=cv.imread(IMAGES_PATH+sys.argv[1])
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

	cv.namedWindow( "Original grayscale image", cv.WINDOW_NORMAL)
	cv.imshow("Original grayscale image", gray)
	cv.waitKey(0)
	cv.destroyAllWindows()

	# Applying a 5x5 gaussian kernel to image
	gray =cv.GaussianBlur(gray,(9,9),7)

	cv.namedWindow( "Blurred grayscale image", cv.WINDOW_NORMAL)
	cv.imshow("Blurred grayscale image", gray)
	cv.waitKey(0)
	cv.destroyAllWindows()


	edged = cv.Canny(gray, 2, 20)

	(cnts, _) = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key = cv.contourArea, reverse =True)[:10]

	cv.drawContours(img, cnts, -1, (0, 255, 0), 3)
	cv.namedWindow( "Contourned dog", cv.WINDOW_NORMAL)
	cv.imshow("Contourned dog", img)
	cv.waitKey(0)
	cv.destroyAllWindows()

	