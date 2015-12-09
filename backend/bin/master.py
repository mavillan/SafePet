#!/usr/bin/python
import sys
import os
import time
import argparse
import histogram
import numpy as np
import cv2 as cv
import config as cfg
import cPickle as pickle
from skimage.feature import local_binary_pattern as lbp



if __name__=='__main__':
	"""
	Parsing the arguments
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verify', action='store_true')
	parser.add_argument('-s', '--search', action='store_true')
	parser.add_argument('-i', '--insert', action='store_true')
	parser.add_argument('path', type=str)
	args = parser.parse_args()

	path = args.path
	if not os.path.isfile(path):
		sys.exit('File doesnt exist.')

	"""
	Performing some operations, common for all
	the options
	"""
	#greyscale image
	img = cv.imread(path, cv.IMREAD_GRAYSCALE)
	#lbp representation
	lbp_img = lbp(img, cfg.params['P'], cfg.params['R'], cfg.params['LBP_METHOD'])
	lbp_img = lbp_image.astype(np.uint8)
	#histogram representation
	hist = histogram.spatial(lbp_img, cfg.params['NX'], cfg.params['NY'], 
		   cfg.params['NPATTERNS'], cfg.params['OVERLAPX'], cfg.params['OVERLAPY'])

	"""
	Verify if the argument photo is or not
	a valid one, ie, corresponds to dog nose.
	"""
	if args.verify:
		#loading svm object
		tgt = open(cfg.params['VAULT']+'SVM', 'rb')
		clf = pickle.load(tgt)
		tgt.close()
		#predict
		result = clf.predict([hist])
		if result[0]==0: return 'invalid'
		else: return 'valid'

	"""
	Perform a search for the k nearest results
	stored in the database
	"""
	elif args.search:
		#loading nn object
	 	tgt = open(cfg.params['VAULT']+'NearestNeighbors', 'rb')
	 	nn = pickle.load(tgt)
	 	tgt.close()
	 	#loading mappings dictionary
	 	tgt = open(cfg.params['VAULT']+'mappings', 'rb')
	 	mappings = pickle.load(tgt)
	 	tgt.close()
	 	#performing the search
	 	dist, ind = nn.query(hist, k=cfg.params['NEIGHBORS'])
	 	#mapping the results
	 	result = [mappings[i] for i in ind]
	 	return result
	
	# elif args.insert:
	# 	#loading hist matrix

	# 	#loading mapings

	# 	#store lbp representation

	# 	#append hist to hist matrix and update it

	# 	#append the mapping to dict and update it

	# 	#rebuild NearestNeighbors object and update it

	# 	return

	# else:
	# 	sys.exit('Give me some instruction.')
	