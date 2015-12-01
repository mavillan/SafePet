#!/usr/bin/python
import sys
import os
import time
import histogram
import metric
import numpy as np
import cv2 as cv
import config as cfg
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from sklearn.neighbors import BallTree	
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

	return 1

def data_to_hist(in_path, out_path=None, hist_type=cfg.params['HIST_TYPE']):
	"""
	> load serialized numpy arrays from in_path containing
	  lbp representation of an image. 
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

	#Generating empty histogram matrix, such that in
	#each there will be an histogram
	nrows = len(filenames)
	#arreglar esto para otros casos (pyramid - square pyramid)
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




if __name__=='__main__':
	# if len(sys.argv)>2:
	# 	sys.exit('Wrong input!')
	# elif len(sys.argv)==1:
	# 	sys.exit('No image input!')

	#some other hardcode here
	matrices = os.listdir(cfg.params['MATRICES_PATH'])
	matrices.sort()
	tgt_name = matrices[-1]
	data = np.load(cfg.params['MATRICES_PATH']+tgt_name)
	tree = BallTree(data, cfg.params['LEAF_SIZE'], metric='pyfunc', func=metric.chi2)
	

	exit = False
	while not exit:
		cmd = raw_input('>>> ')
		cmd = cmd.strip().split()

		if len(cmd) == 0:
			continue

		elif cmd[0] == 'build':
			if cmd[1] == 'lbp':
				#create lbp representation for each image in training set
				data_to_lbp(cfg.params['TRAINING_PATH'], cfg.params['TRAINING_PATH_LBP'])

			elif cmd[1] == 'hist':
				#create matrix with each histograms in a respective row
				data_to_hist(cfg.params['TRAINING_PATH_LBP'], cfg.params['MATRICES_PATH'])

			elif cmd[1] == 'nn':
				#build nn search objedt
				matrices = os.listdir(cfg.params['MATRICES_PATH'])
				matrices.sort()
				tgt_name = matrices[-1]
				data = np.load(cfg.params['MATRICES_PATH']+tgt_name)
				tree = BallTree(data, cfg.params['LEAF_SIZE'], metric='pyfunc', func=metric.chi2)
			else:
				print 'Wrong build command!'

		elif cmd[0] == 'query':
			if cmd[1] == 'all':
				pass

			elif os.path.isfile(cfg.params['TEST_PATH']+cmd[1]):
				img = cv.imread(cfg.params['TEST_PATH']+cmd[1], cv.IMREAD_GRAYSCALE)
				lbp_image = lbp(img, cfg.params['P'], cfg.params['R'], cfg.params['LBP_METHOD'])
				lbp_image = lbp_image.astype(np.uint8)
				query_hist = histogram.spatial(lbp_image, cfg.params['NX'], cfg.params['NY'],
				             cfg.params['NPATTERNS'], cfg.params['OVERLAPX'], cfg.params['OVERLAPY'])
				dist, ind = tree.query(query_hist, cfg.params['NEIGHBORS'])
				print "Indexes:",ind
				print "Distances:",dist

				root = '/home/martin/HDD/Mega/SafePet/SafePetData/'
				#load query image
				q_img = mpimg.imread(cfg.params['TEST_PATH']+cmd[1])
				q_img_complete = mpimg.imread(root+'test_set_unprocessed/'+cmd[1])

				#some hardcode for presentation
				training_names = os.listdir(cfg.params['TRAINING_PATH'])
				training_names.sort()

				training_names_complete = os.listdir(root+'internet_data_unprocessed/')
				training_names_complete.sort()

				#load results images
				ind1 = ind[0,0]
				dist1 = dist[0,0]
				r_img1 = mpimg.imread(cfg.params['TRAINING_PATH']+training_names[ind1], cv.IMREAD_COLOR)
				r_img1_complete = mpimg.imread(root+'internet_data_unprocessed/'+training_names_complete[ind1])

				ind2 = ind[0,1] 
				dist2 = dist[0,1]
				r_img2 = mpimg.imread(cfg.params['TRAINING_PATH']+training_names[ind2], cv.IMREAD_COLOR)
				r_img2_complete = mpimg.imread(root+'internet_data_unprocessed/'+training_names_complete[ind2])

				#visualization
				fig = plt.figure(figsize=(10,10))

				fig.add_subplot(2,3,1)
				plt.axis('off')
				plt.title('Query image processed')
				plt.imshow(q_img)

				fig.add_subplot(2,3,4)
				plt.axis('off')
				plt.title('Query image unprocessed')
				plt.imshow(q_img_complete)

				fig.add_subplot(2,3,2)
				plt.axis('off')
				plt.title('First result processed')
				plt.imshow(r_img1)

				fig.add_subplot(2,3,5)
				plt.axis('off')
				plt.title('First result unprocessed')
				plt.imshow(r_img1_complete)

				fig.add_subplot(2,3,3)
				plt.axis('off')
				plt.title('Second result processed')
				plt.imshow(r_img2)

				fig.add_subplot(2,3,6)
				plt.axis('off')
				plt.title('Second result unprocessed')
				plt.imshow(r_img2_complete)

				plt.show()

			else:
				print 'Wrong query command!'
		
		elif cmd[0] == 'exit':
			exit = True

		else:
			print 'Wrong input!'
	sys.exit(0)