import os
import sys
import time
import histogram
import numpy as np
import cv2 as cv
import config as cfg
import cPickle as pickle
from skimage.feature import local_binary_pattern as lbp

def data_to_lbp(in_path, out_path):
	"""
	> load images from in_path, and convert each one to
	  lbp respresentation.
	> stores the results as .npy searialized array on out_path.
	"""
	try:
		filenames = os.listdir(in_path)
	except OSError, msg:
		print in_path, 'is invalid!'

	if len(filenames) == 0:
		print in_path, 'is empty!'
		return -1

	for filename in filenames:
		img = cv.imread(in_path+filename, cv.IMREAD_GRAYSCALE)
		lbp_image = lbp(img, cfg.params['P'], cfg.params['R'], cfg.params['LBP_METHOD'])
		lbp_image = lbp_image.astype(np.uint8)
		np.save(out_path+filename, lbp_image)
	return 1


def data_to_hist(in_path, out_path=None, hist_type=cfg.params['HIST_TYPE'], precomputed=False):
	"""
	> load serialized numpy arrays from in_path containing
	  lbp representation of an image (if precomputed=True),
	  or load images in in_path and compute lbp represetantion
	  first (if precomputed=False). 
	> stores an (spatial | spatial pyramid) histogram matrix on out_path
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

	#dictionary with mappings between row numbers and image name
	mappings = dict()

	#Generating empty histogram matrix, such that in
	#each there will be an histogram
	nrows = len(filenames)
	#fix that to work on other cases (pyramid - square pyramid)
	ncols = cfg.params['NPATTERNS']*cfg.params['NX']*cfg.params['NY'] 
	hist_matrix = np.empty((nrows,ncols))
	i_index = 0

	for filename in filenames:
		if precomputed:
			#if precomputed just load it
			lbp_image = np.load(in_path+filename)
		else:
			#if not, compute lbp representation
			img = cv.imread(in_path+filename, cv.IMREAD_GRAYSCALE)
			lbp_image = lbp(img, cfg.params['P'], cfg.params['R'], cfg.params['LBP_METHOD'])
			lbp_image = lbp_image.astype(np.uint8)

		#transform lbp to histogram representation
		if hist_type=='SPATIAL':
			hist_matrix[i_index,:] = histogram.spatial(lbp_image, cfg.params['NX'], cfg.params['NY'], 
				              cfg.params['NPATTERNS'], cfg.params['OVERLAPX'], cfg.params['OVERLAPY'])
		elif hist_type=='SPATIAL_PYRAMID':
			hist_matrix[i_index,:] = histogram.spatial_pyramid(lbp_image, cfg.params['LEVEL'], 
				              cfg.params['NPATTERNS'], cfg.params['OVERLAPX'], cfg.params['OVERLAPY'])
		else:
			print 'invalid hist_type!'; return -1
		#save the mapping
		fileid = filename.split('-')[0]
		mappings[i_index] = fileid
		i_index += 1

	#storing mappings
	timestamp = time.strftime("%y-%m-%d")+'::'+time.strftime("%X")
	out = cfg.params['MAPPINGS_PATH']+'mappings::'+timestamp
	tgt = file(out, 'wb')
	pickle.dump(mappings, tgt)
	tgt.close()

	if out_path!=None:
		#save the resulting matrix with timestamps
		out = out_path+'hist_matrix::'+hist_type+'::'+timestamp
		np.save(out, hist_matrix)
		return 1
	else:
		return hist_matrix