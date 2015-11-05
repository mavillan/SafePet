#!/usr/bin/python
import sys
import os
import metric
import histogram
import numpy as np
import cv2 as cv
import config as cfg
from sklearn import svm
from sklearn.neighbors import BallTree
from skimage.feature import local_binary_pattern as lbp


def chi2(X, Y):
	m,n = X.shape
	p,_ = Y.shape
	#Gram matrix
	G = np.empty((m,p))
	for i in range(m):
		for j in range(p):
			G[i,j] = metric.chi2(X[i],Y[j])
	return G

def data_to_hist(in_path, out_path=None, hist_type=cfg.params['HIST_TYPE']):
	"""
	> load serialized numpy arrays from in_path containing
	  images
	> returns (stores) an histogram representation matrix (on out_path)
	"""
	try:
		filenames = os.listdir(in_path)
		filenames.sort()
	except OSError, msg:
		print in_path, 'is invalid!'
		return -1

	if len(filenames)==0:
		print in_path, 'is empty!'
		return -1

	#Generating empty histogram matrix, such that in
	#each row there will be an histogram
	nrows = len(filenames)
	#fix this for other cases (pyramid - square pyramid)
	ncols = cfg.params['NPATTERNS']*cfg.params['NX']*cfg.params['NY'] 
	hist_matrix = np.empty((nrows,ncols))
	i_index = 0

	for filename in filenames:
		img = cv.imread(in_path+filename, cv.IMREAD_GRAYSCALE)
		lbp_image = lbp(img, cfg.params['P'], cfg.params['R'], cfg.params['LBP_METHOD'])
		lbp_image = lbp_image.astype(np.uint8)

		#transform lbp to histogram representation
		if hist_type=='SPATIAL':
			hist_matrix[i_index,:] = histogram.spatial(lbp_image, cfg.params['NX'], cfg.params['NY'], 
				              cfg.params['NPATTERNS'], cfg.params['OVERLAPX'], cfg.params['OVERLAPY'])
			i_index+=1
		elif hist_type=='SPATIAL_PYRAMID':
			hist_matrix[i_index,:] = histogram.spatial_pyramid(lbp_image, cfg.params['LEVEL'], 
				              cfg.params['NPATTERNS'], cfg.params['OVERLAPX'], cfg.params['OVERLAPY'])
			i_index+=1
		else:
			print 'invalid hist_type!'
			return -1

	if out_path!=None:
		#save the resulting matrix with timestamps
		out = out_path+'hist_matrix::'+hist_type+'::'+time.strftime("%y-%m-%d")+'::'+time.strftime("%X")
		np.save(out, hist_matrix)
		return 1
	return hist_matrix


def build_nn(data):
	tree=BallTree(data,LEAF_SIZE,metric='pyfunc',func=chi2)
	return


def build_svm(in_path1, in_path2):
	#positive and negative examples data
	p_data = data_to_hist(in_path1)
	n_data = data_to_hist(in_path2)
	p,_ = p_data.shape
	n,_ = n_data.shape

	#creating matrix data and corresponding labels
	data = np.concatenate((p_data, n_data), axis=0)
	labels = np.concatenate((np.ones(p,dtype=int), np.zeros(n,dtype=int)))

	#creating the SVM with chi2 kernel
	chi2_svm = svm.SVC(kernel=chi2)
	chi2_svm.fit(data,labels)
	return chi2_svm





