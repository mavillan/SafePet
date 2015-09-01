#!/usr/bin/python

"""
MASTER CONFIGURATION FILE
"""

### Parameters for the LBP operator
_P = 8 #P neighbors 
_R = 2 #Raduis parameter
_LBP_METHOD = 'nri_uniform'
_NPATTERNS = 59 #number of patterns of lbp method

### Parameters for histogram() module funcions
_HIST_TYPE = 'SPATIAL' #could be SPATIAL or SPATIAL_PYRAMID
_NX = 20 #number of images divisions on x (rows) direction
_NX = 20 #number of images divisions on y (cols) direction
_OVERLAPX = 2 #overlap on x (rows) direction
_OVERLAPY = 2 #overlap on y (cols) direction  
_LEVEL = 3 #number of levels on spatial pyramid


### Important paths
_TRAINING_PATH = '/home/martin/HDD/Mega/SafePet/SafePetData/training_set_processed/'
_TEST_PATH = '/home/martin/HDD/Mega/SafePet/SafePetData/test_set_processed/'
_TRAINING_PATH_LBP = '/home/martin/HDD/Documents/SafePet_Data/lbp_images/'
_TEST_PATH_LBP = ''
_SP_HIST_PATH = '/home/martin/HDD/Documents/SafePet_Data/sp_hist/'
_SP_PYRD_PATH = ''

### Parameters of nearest neighbor search
_LEAF_SIZE = 30 #leaf size of ball_tree structure
_NEIGHBORS = 2  #neighbors to show on NN search

### params dictionary
params = {
	'P' : _P,
	'R' : _R,
	'LBP_METHOD' : _LBP_METHOD,
	'NPATTERNS' : _NPATTERNS,

	'HIST_TYPE' : _HIST_TYPE,
	'NX' : _NX,
	'NX' : _NY,
	'OVERLAPX' : _OVERLAPX,
	'OVERLAPY' : _OVERLAPY,
	'LEVEL' : _LEVEL,

	'TRAINING_PATH' : _TRAINING_PATH,
	'TEST_PATH' : _TEST_PATH,
	'TRAINING_PATH_LBP' : _TRAINING_PATH_LBP,
	'TEST_PATH_LBP' : _TEST_PATH_LBP,
	'SP_HIST_PATH' : _SP_HIST_PATH,
	'SP_PYRD_PATH' : _SP_PYRD_PATH

	'LEAF_SIZE' : _LEAF_SIZE,
	'NEIGHBORS' : _NEIGHBORS,
}



