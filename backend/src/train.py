#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
from skimage.feature import local_binary_pattern as lbp


def weight_calculate():
	return


def weighted_chi2():
	return


def histogram(src,hist,numPatterns=59):
	"""
	> src must be uniform LBP version of image.
	> hist uses uint32 because the assumption that there is 
	  no more than 4294967295 of each pattern (very realistic).
	> defautl value of number of patterns corresponds to uniform
	  version of LBP operator.
	"""
	hist=np.zeros(numPatterns).astype(np.uint32)
	rows,cols=src.shape
	for i in range(rows):
		for j in range(cols):
			pattern=src[i,j]
			hist[pattern]+=1
	return hist


def spatial_histogram(src,dst,numPatterns=59,windowSize,overlap=False):
	"""
	> 
	"""
	return  sHist


"""
DEFINING SOME IMPORTANT PARAMETERS
"""
P=8 #P (number of neighbors) parameter or LBP operator
R=2 #Raduis parameter of LBP operator
LBP_METHOD='nri_uniform' #Method of LBP operator 

TRAINING_PATH='/home/martin/HDD/Documents/SafePet_Data/training_set_processed/' #Default training path



if __name__='__main___':
	if len(sys.argv)!=1:
		sys.exit('Wrong input!')

	files=os.listdir(TRAINING_PATH)

	for filename in files:
		filename=TRAINING_PATH+filename
		img=cv.imread(filename)

		#To grayscale and to float
		gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

		#LBP kernel convolution with the gray-scale image
		#Applying LBPu2(P,R), no rotational invariant
		lbp_image=lbp(gray,P,R,method=LBP_METHOD)




