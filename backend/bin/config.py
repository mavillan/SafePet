#!/usr/bin/python
import os
import sys

"""
MASTER CONFIGURATION FILE
"""

### Parameters for the LBP operator
_P = 8 #P neighbors 
_R = 2 #Radius parameter
_LBP_METHOD = 'nri_uniform'
_NPATTERNS = 59 #number of patterns of lbp method

### Parameters for histogram() module funcions
_HIST_TYPE = 'SPATIAL' #could be SPATIAL or SPATIAL_PYRAMID
_NX = 10 #number of images divisions on x (rows) direction
_NY = 10 #number of images divisions on y (cols) direction
_OVERLAPX = 2 #overlap on x (rows) direction
_OVERLAPY = 2 #overlap on y (cols) direction  
_LEVEL = 3 #number of levels on spatial pyramid


### Important paths (paths must be ended by '/', except _ROOT)
_ROOT = '/home/martin/HDD/Mega/SafePet/SafePetData'
_TRAINING_PATH = _ROOT+'/internet_data/'
_TRAINING_PATH_LBP = _ROOT+'/training_set_lbp/'
_TEST_PATH = _ROOT+'/test_set/'
_TEST_PATH_LBP = _ROOT+'/test_set_lbp/'
_MATRICES_PATH = _ROOT+'/matrices/'

# Verification of existence
if not os.path.isdir(_TRAINING_PATH):
	sys.exit(_TRAINING_PATH+' is not a valid directory!')

if not os.path.isdir(_TRAINING_PATH_LBP):
	sys.exit(_TRAINING_PATH_LBP+' is not a valid directory!')		

if not os.path.isdir(_TEST_PATH):
	sys.exit(_TEST_PATH+' is not a valid directory!')

if not os.path.isdir(_TEST_PATH_LBP):
	sys.exit(_TEST_PATH_LBP+' is not a valid directory!')

if not os.path.isdir(_MATRICES_PATH):
	sys.exit(_MATRICES_PATH+' is not a valid directory!')


### Parameters of nearest neighbor search
_LEAF_SIZE = 30 #leaf size of ball_tree structure
_NEIGHBORS = 2  #neighbors to show on NN search



### create params dictionary
params = {
	'P' : _P,
	'R' : _R,
	'LBP_METHOD' : _LBP_METHOD,
	'NPATTERNS' : _NPATTERNS,

	'HIST_TYPE' : _HIST_TYPE,
	'NX' : _NX,
	'NY' : _NY,
	'OVERLAPX' : _OVERLAPX,
	'OVERLAPY' : _OVERLAPY,
	'LEVEL' : _LEVEL,

	'TRAINING_PATH' : _TRAINING_PATH,
	'TRAINING_PATH_LBP' : _TRAINING_PATH_LBP,
	'TEST_PATH' : _TEST_PATH,
	'TEST_PATH_LBP' : _TEST_PATH_LBP,
	'MATRICES_PATH' : _MATRICES_PATH,

	'LEAF_SIZE' : _LEAF_SIZE,
	'NEIGHBORS' : _NEIGHBORS,
}
