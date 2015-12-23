#!/usr/bin/python
import sys
import os
import time
import zerorpc
import histogram
import numpy as np
import cv2 as cv
import config as cfg
import cPickle as pickle
from skimage.feature import local_binary_pattern as lbp


class Master():
	def __init__(self):
		#loading nn object and storing it as attribute
		tgt = open(cfg.params['VAULT']+'NearestNeighbors', 'rb')
		self.nn = pickle.load(tgt)
		tgt.close()

		#loading svm object and storing it as attribute
		tgt = open(cfg.params['VAULT']+'SVM', 'rb')
		self.clf = pickle.load(tgt)
		tgt.close()

		#loading mappings dictionary and storing it as attribute
		tgt = open(cfg.params['VAULT']+'mappings', 'rb')
		self.mappings = pickle.load(tgt)
		tgt.close()

		#loading hist matrix and storing it as attribute
		matrices = os.listdir(cfg.params['MATRICES_PATH'])
		matrices.sort()
		selfhist_matrix = np.load(matrices[-1])


	def _process(self, img):
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

	path = args.path
	filename = path.strip().split('/')[-1]
	if not os.path.isfile(path):
		sys.exit('File doesnt exist.')



	
	#Verify if the argument photo is or not
	#a valid one, i.e, corresponds to dog nose.
	def verify(self, path):
			result = clf.predict([hist])
			if result[0]==0: ret('invalid')
			else: ret('valid')

	#Perform a search for the k nearest results
	#stored in the database
	def search(self, path):
			#performing the search
			dist, ind = nn.query(hist, k=cfg.params['NEIGHBORS'])
			#mapping the results
			result = [mappings[i] for i in ind]
			ret(result)
		
	def insert(self, path):
			#store lbp representation
			np.save(cfg.params['TRAINING_PATH_LBP']+filename, lbp_image)

			#append hist to hist matrix and update it
			#todo: search a better way to do that
			hist_matrix = np.vstack(hist_matrix, hist)
			out = cfg.params['MATRICES_PATH']+'::'+time.strftime("%y-%m-%d")+'::'+time.strftime("%X")
			np.save(out, hist_matrix)

			#append the mapping to dict and update it
			mappings[hist_matrix.shape[0]-1] = filename
			#storing mappings in vault
			tgt = file(cfg.params['VAULT']+'mappings', 'wb')
			pickle.dump(mappings, tgt)
			tgt.close() 

			#rebuild NearestNeighbors object and update it
			build_nn(hist_matrix, cfg.params['VAULT'])
		 	ret(1)

if __name__=='__main__':
	s = zerorpc.Server(Master())
	s.bind('tcp://0.0.0.0:4242')
	s.run()