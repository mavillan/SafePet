#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv


IMAGES_PATH='/home/martin/HDD/Dropbox/SafePet/dog_noses/'

if __name__=='__main__':
	if len(sys.argv)!=2:
		sys.exit('Wrong input!')	
	
	img=cv.imread(IMAGES_PATH+sys.argv[1])
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	gray = cv.bilateralFilter(gray, 7, 17, 17)
	edged = cv.Canny(gray, 100, 200)
	(cnts, _) = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	#cnts = sorted(cnts, key = cv.contourArea, reverse = True)[:10]
	cv.drawContours(img, cnts, -1, (0, 255, 0), 3)
	cv.namedWindow( "Contourned dog", cv.WINDOW_NORMAL)
	cv.imshow("Contourned dog", img)
	cv.waitKey(0)
	