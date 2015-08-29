#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from skimage.feature import local_binary_pattern as lbp
from sklearn.neighbors import BallTree


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


	

def build_nn(data):
	tree=BallTree(data,LEAF_SIZE,metric='pyfunc',func=chi2)
	return



if __name__=='__main___':
	if len(sys.argv)!=1:
		sys.exit('Wrong input!')

	# files=os.listdir(TRAINING_PATH)

	# for filename in files:
	# 	filename=TRAINING_PATH+filename
	# 	img=cv.imread(filename)

	# 	#To grayscale and to float
	# 	gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

	# 	#LBP kernel convolution with the gray-scale image
	# 	#Applying LBPu2(P,R), no rotational invariant
	# 	lbp_image=lbp(gray,P,R,method=LBP_METHOD)
	# 	lbp_image=lbp_image.astype(np.uint8)
	# 	sp_hist=spatial_histogram(lbp_image,Nx,Ny)




