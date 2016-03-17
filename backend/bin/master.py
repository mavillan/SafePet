#!/usr/bin/python
import sys
import os
import time
import zerorpc
import builder
import histogram
import numpy as np
import cv2 as cv
import config as cfg
import cPickle as pickle
from skimage.feature import local_binary_pattern as lbp


class Master():
	def __init__(self):
		#loading nn object and storing it as attribute
		nn_list = os.listdir(cfg.params['NN_PATH'])
		nn_list.sort()
		tgt = open(cfg.params['NN_PATH']+nn_list[-1], 'rb')
		self.nn = pickle.load(tgt)
		tgt.close()

		#loading svm object and storing it as attribute
		svm_list = os.listdir(cfg.params['SVM_PATH'])
		svm_list.sort()
		tgt = open(cfg.params['SVM_PATH']+svm_list[-1], 'rb')
		self.clf = pickle.load(tgt)
		tgt.close()

		#loading mappings dictionary and storing it as attribute
		mappings_list = os.listdir(cfg.params['MAPPINGS_PATH'])
		mappings_list.sort()
		tgt = open(cfg.params['MAPPINGS_PATH']+mappings_list[-1], 'rb')
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
		lbp_img = lbp_img.astype(np.uint8)
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
			dist, ind = self.nn.query([hist], k=cfg.params['NEIGHBORS'])
			#mapping the results
			result = []
			for i in ind[0]:
				fileid = self.mappings[i]
				#dont put the same id many times
				if fileid in result: continue
				result.append(fileid)
			return result
	
	#Insert a new dog
	def insert(self, path):
			lbp_img,hist = self._process(path)
			filename = path.strip().split('/')[-1]

			#verify it's a valid one
			valid = self.clf.predict([hist])[0]
			if not valid: return 0

			#store lbp representation
			np.save(cfg.params['TRAINING_PATH_LBP']+filename, lbp_img)

			#append hist to hist matrix and update it
			#todo: search a better way to do that: hdf5?
			self.hist_matrix = np.vstack((self.hist_matrix, hist))
			timestamp = time.strftime("%y-%m-%d")+'::'+time.strftime("%X")
			out = cfg.params['MATRICES_PATH']+'hist_matrix::'+cfg.params['HIST_TYPE']+'::'+timestamp
			np.save(out, self.hist_matrix)

			#append the mapping to dict and update it
			fileid = filename.split('-')[0]
			self.mappings[self.hist_matrix.shape[0]-1] = fileid
			#storing mappings
			out = cfg.params['MAPPINGS_PATH']+'mappings::'+timestamp
			tgt = file(out, 'wb')
			pickle.dump(self.mappings, tgt)
			tgt.close() 

			#rebuild NearestNeighbors object and update it
			self.nn = builder.build_nn(self.hist_matrix, store=False)
			out = cfg.params['NN_PATH']+'nearestneighbors::'+timestamp
			tgt = file(out, 'wb')
			pickle.dump(self.nn, tgt)
			tgt.close()
		 	return 1

	def delete(self, id):
			#iterate through mappings
			deleted = list()
			for ind, mapp_id in self.mappings.items():
				if mapp_id != id: continue
				#delete the mapping
				del self.mappings[ind]
				deleted.append(ind)
				#delete the corresponding matrix entry
				self.hist_matrix = np.delete(self.hist_matrix, ind, axis=0)

			#fix order in mappings indexes
			sec_ind = 0
			for ind in self.mappings.keys():
				if ind != sec_ind:
					self.mappings[sec_ind] = self.mappings.pop(ind)
				sec_ind += 1

			#storing updated mappins and hist_matrix
			timestamp = time.strftime("%y-%m-%d")+'::'+time.strftime("%X")
			out = cfg.params['MATRICES_PATH']+'hist_matrix::'+cfg.params['HIST_TYPE']+'::'+timestamp
			np.save(out, self.hist_matrix)

			out = cfg.params['MAPPINGS_PATH']+'mappings::'+timestamp
			tgt = file(out, 'wb')
			pickle.dump(self.mappings, tgt)
			tgt.close()

			#rebuild NearestNeighbors object and update it
			self.nn = builder.build_nn(self.hist_matrix, store=False)
			out = cfg.params['NN_PATH']+'nearestneighbors::'+timestamp
			tgt = file(out, 'wb')
			pickle.dump(self.nn, tgt)
			tgt.close()
		 	return 1

	def synchronize(self, ids):
		"""
		This funcion is called when differences are found in
		both backends. It takes all ids correctly registered,
		and update the structures (mappings, hist_matrix, nn) 
		so both backends are correctly synchronized.
		"""
		#ids stored actually on this backend
		current_ids = self.mappings.values()

		for tmp in current_ids:
			if tmp in ids: continue
			#if not present in the other backend
			self.delete(tmp)
		return 1

if __name__=='__main__':
	s = zerorpc.Server(Master())
	s.bind('tcp://0.0.0.0:4242')
	s.run()