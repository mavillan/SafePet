#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from skimage.feature import local_binary_pattern as lbp
from scipy.stats import itemfreq 


def weight_calculate():
	return


def weighted_chi2():
	return


def _histogram(src,numPatterns=59):
	"""
	> src must be uniform LBP version of image.
	> defautl value of number of patterns corresponds to uniform
	  version of LBP operator.
	"""
	rows,cols=src.shape
	hist=itemfreq(src)[:,1]
	normalized_hist=hist/np.float(rows*cols)
	return normalized_hist


def spatial_histogram(src,numPatterns=59,nx,ny,overlapX=0,overlapY=0):
	"""
	> the window size couldn't be fixed. Example, if there are 2 noses 
	  pictures of the same dog, the first 800x800 and the second 400x400,
	  then the spatial information will not match.
	> more or less realistic assumption, the noses pictures will keep ratio.
	> nx and ny stands for the number of divisions in horizontal and vertical
	  axis, respectively.
	"""
	height,width=src.shape

	#widowsSize=(dx,dy)
	dx=np.int(np.floor((width+2.*overlapX)/nx))
	dy=np.int(np.floor((height+2.*overlapY)/ny))
	#remainders=(rx,ry)
	x_rem=width-nx*dx+2*overlapX
	y_rem=height-ny*dy+2*overlapY
	#right and left tops for regions with +1 pixel
	if rx%2==0:
		rx_top=rx/2-1
		lx_top=nx-rx/2
	else:
		rx_top=rx/2
		lx_top=nx-rx/2

	#upper and lower tops for regions with +1 pixel
	if ry%2==0:
		uy_top=ry/2-1
		ly_top=ny-ry/2
	else:
		uy_top=ry/2-1
		ly_top=ny-ry/2

	sp_histo=np.empty((nx*ny,numPatterns))
		
	#i_start_index and j_start_index are index where to start
	#in the next iteration.
	i_start_index=0
	for i in range(nx):
		j_start_index=0
		for j in range(ny):
			#verify it a pixel must be added
			if i<=rx_top | i>=lx_top:
				x_windows_size=dx+1
			if j<=uy_top | j>=ly_top:
				y_windows_size=dy+1

			hist=_histogram(src[i_start_index:i_start_index+x_windows_size,j_start_index+y_windows_size],numPatterns)

	return  sp_hist


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
		lbp_image=lbp_image.astype(np.uint8)




