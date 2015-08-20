#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
from skimage.feature import local_binary_pattern
from sklearn.preprocessing import normalize
from scipy.stats import itemfreq


IMAGES_PATH='/home/martin/HDD/Dropbox/SafePet_Data/training_set_processed/'

#parameters for lbp function
radius=3
no_points=8
METHOD='uniform'


if __name__=='__main__':
	if len(sys.argv)!=2:
		sys.exit('Wrong input!')	
	
	img=cv.imread(IMAGES_PATH+sys.argv[1])
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

	lbp = local_binary_pattern(gray, no_points, radius, method=METHOD)
	x = itemfreq(lbp.ravel())
	hist = x[:, 1]/np.sum(x[:, 1])

	# I really think this new approach could work


