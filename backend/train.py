#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
from skimage.feature import local_binary_pattern as lbp



TRAINING_PATH='/home/martin/HDD/Documents/SafePet_Data/training_set_processed/'

# Defining some important parameters
NEIGHBORS=2
LBP_METHOD='default'



if __name__='__main___':
	if len(sys.argv)!=1:
		sys.exit('Wrong input!')

	files=os.listdir(TRAINING_PATH)

	for filename in files:
		filename=TRAINING_PATH+filename
		img=cv.imread(filename)

		#Some pre processing stage here

		#To grayscale and to float
		gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

		#LBP kernel convolution with the gray-scale image
		#Applying LBPu2(8,2)
		lbp_image=lbp(gray,8,2,method=LBP_METHOD)

