#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from skimage.feature import local_binary_pattern as lbp


def data_to_lbp():
	"""
	> load images from TRAINING_PATH, and convert each one to
	  lbp respresentation
	> stores the results as .npy searialized array on LBP_PATH
	"""
	filenames=os.listdir(TRAINING_PATH)
	filenames.sort()
	if len(filenames)==0:
		sys.exit("TRAINING_PATH directory has no data!")
	for filename in filenames:
		target=TRAINING_PATH+filename #target name
		img=cv.imread(target)
		#To grayscale and to float
		gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
		#LBP kernel convolution with the gray-scale image
		#Applying LBPu2(P,R), no rotational invariant
		lbp_image=lbp(gray,P,R,method=LBP_METHOD)
		lbp_image=lbp_image.astype(np.uint8)
		np.save(LBP_PATH+filename[:-4],lbp_image)
	return 1


def data_to_sp_hist(nx,ny,numPatterns=59,overlapX=2,overlapY=2):
	"""
	> load images from LBP_PATH, and convert each one to
	  spatial histogram respresentation
	> stores the result as .npy searialized array on SP_HIST_PATH
	"""
	filenames=os.listdir(LBP_PATH)
	filenames.sort()
	if len(filenames)==0:
		sys.exit("LBP_PATH directory has no data!")
	#Generating empty target matrix
	rows=len(filenames)
	cols=59*nx*ny
	row_index=0
	overall_sp_hist=np.empty((rows,cols))
	for filename in filenames:
		target=LBP_PATH+filename #target name
		lbp_image=np.load(target)
		overall_sp_hist[row_index,:]=spatial_histogram(lbp_image,nx,ny)
		row_index+=1
	np.save(SP_HIST_PATH+"overall_sp_hist",overall_sp_hist)
	return 1


def _weight_calculate():
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
	hist=np.bincount(src.ravel(),minlength=numPatterns)
	normalized_hist=hist/np.float(rows*cols)
	return normalized_hist


def spatial_histogram(src,nx,ny,numPatterns=59,overlapX=2,overlapY=2):
	"""
	> the window size couldn't be fixed. Example, if there are 2 noses 
	  pictures of the same dog, the first 800x800 and the second 400x400,
	  then the spatial information will not match.
	> more or less realistic assumption, the noses pictures will keep ratio.
	> x and y will mean for vertical and horizontal directions respectively,
	  (x->rows direction and y->columns direction)
	> nx and ny stands for the number of divisions in vertical and horizontal	
	  axis, respectively.
	"""
	#some constrains to overlap parameter
	if (type(overlapX) is not int) or (overlapX<0) or (overlapX>10):
		print "Wrong overlapX parameter"
		return -1
	if (type(overlapY) is not int) or (overlapY<0) or (overlapY>10):
		print "Wrong overlapY parameter"
		return -1
	height,width=src.shape
	#widows size: (wsx,wsy)
	wsx=np.int(np.floor((height+2.*overlapX)/nx))
	wsy=np.int(np.floor((width+2.*overlapY)/ny))
	#remainders=(xrem,yrem), ie, number of pixels that 
	#can't be covered with such windows sizes
	xrem=height-nx*wsx+2*overlapX
	yrem=width-ny*wsy+2*overlapY
	"""
	> Each image subdivision will be named region. there are in
	  total nx*ny regions.
	> Each region has two index Rxy=R[x,y].
	> All regions R[0:rx0,:] and R[rx1:,:] will have a windows 
	  size with one more pixel on x direction. 
	> All regions R[:,0:ry0] and R[:,ry1:] will have a windows
	  size with one more pixel on y direction.
	"""
	if xrem%2==0:
		rx0=xrem/2-1
		rx1=nx-xrem/2
	else:
		rx0=xrem/2
		rx1=nx-xrem/2
	if yrem%2==0:
		ry0=yrem/2-1
		ry1=ny-yrem/2
	else:
		ry0=yrem/2
		ry1=ny-yrem/2
	#spatial histogram will contain in each of his rows
	#an LBP histogram of a region.
	sp_hist=np.empty((nx*ny,numPatterns))
	#hist_index, counter for histograms above. 
	#hist_index=0:nx*ny
	hist_index=0
	#i_index and j_index are indexes of src matrix corresponding
	#to each region in the corresponding iteration.
	i_index=0
	#iteration through regions
	for rx_index in range(nx):
		#verify if a pixel must be added to the windows size on x direction
		Wsx=wsx
		if rx_index<=rx0 | rx_index>=rx1:
			Wsx+=1
		j_index=0
		for ry_index in range(ny):
			#verify if a pixel must be added to the windows size on y direction
			Wsy=wsy
			if ry_index<=ry0 | ry_index>=ry1:
				Wsy+=1
			sp_hist[hist_index,:]=_histogram(src[i_index:i_index+Wsx, j_index:j_index+Wsy],numPatterns)
			hist_index+=1
			j_index+=Wsy-overlapY
		i_index+=Wsx-overlapX
	#concatenation of histrograms in each row
	return sp_hist.ravel()


"""
DEFINING SOME IMPORTANT PARAMETERS
"""
###parameters of lbp() function
P=8 #P (number of neighbors) parameter or LBP operator
R=2 #Raduis parameter of LBP operator
LBP_METHOD='nri_uniform' #Method of LBP operator

###parameters of spatial_histogram() function
Nx=25 #number of images divisions on x (rows) direction
Ny=25 #number of images divisions on y (cols) direction
OVERLAPx=2 #overlap on x (rows) direction
OVERLAPy=2 #overlap on y (cols) direction  

###important paths
TRAINING_PATH='/home/martin/HDD/Documents/SafePet_Data/training_set_processed/' #Default training path
LBP_PATH='/home/martin/HDD/Documents/SafePet_Data/lbp_images/'
SP_HIST_PATH='/home/martin/HDD/Documents/SafePet_Data/sp_hist/'



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
		sp_hist=spatial_histogram(lbp_image,Nx,Ny,OVERLAPx,OVERLAPy)




