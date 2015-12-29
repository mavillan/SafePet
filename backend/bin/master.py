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
		self.hist_matrix = np.load(cfg.params['MATRICES_PATH']+matrices[-1])


	def _process(self, path):
		"""
		Performing some operations, common for all the options
		"""
		if not os.path.isfile(path):
			#change that!
			sys.exit('File doesnt exist.')
		#grayscale image
		img = cv.imread(path, cv.IMREAD_GRAYSCALE)
		#lbp representation
		lbp_img = lbp(img, cfg.params['P'], cfg.params['R'], cfg.params['LBP_METHOD'])
		lbp_img = lbp_image.astype(np.uint8)
		#histogram representation
		hist = histogram.spatial(lbp_img, cfg.params['NX'], cfg.params['NY'], 
			   cfg.params['NPATTERNS'], cfg.params['OVERLAPX'], cfg.params['OVERLAPY'])
		return (lbp_img, hist)

	
	#Verify if the argument photo is or not
	#a valid one, i.e, corresponds to dog nose.
	def verify(self, path):
			_,hist = self._process(path)
			result = self.clf.predict([hist])
			if result[0]==0: return 'invalid'
			else: return 'valid'

	#Perform a search for the k nearest results
	#stored in the database
	def search(self, path):
			_,hist = self._process(path)
			#performing the search
			dist, ind = self.nn.query(hist, k=cfg.params['NEIGHBORS'])
			#mapping the results
			result = [self.mappings[i] for i in ind]
			return result
	
	#Insert a new dog
	def insert(self, path):
			lbp_image,hist = self._process(path)
			filename = path.strip().split('/')[-1]
			#store lbp representation
			np.save(cfg.params['TRAINING_PATH_LBP']+filename, lbp_image)

			#append hist to hist matrix and update it
			#todo: search a better way to do that: hdf5?
			self.hist_matrix = np.vstack(self.hist_matrix, hist)
			out = cfg.params['MATRICES_PATH']+'::'+time.strftime("%y-%m-%d")+'::'+time.strftime("%X")
			np.save(out, self.hist_matrix)

			#append the mapping to dict and update it
			self.mappings[self.hist_matrix.shape[0]-1] = filename
			#storing mappings in vault
			tgt = file(cfg.params['VAULT']+'mappings', 'wb')
			pickle.dump(self.mappings, tgt)
			tgt.close() 

			#rebuild NearestNeighbors object and update it
			self.nn = build_nn(self.hist_matrix)
			tgt = file(cfg.params['VAULT']+'NearestNeighbors', 'wb')
			pickle.dump(self.nn, tgt)
			tgt.close()
		 	return 1

if __name__=='__main__':
	s = zerorpc.Server(Master())
	s.bind('tcp://0.0.0.0:4242')
	s.run()