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
_NY = 10 #number of images div	isions on y (cols) direction
_OVERLAPX = 2 #overlap on x (rows) direction
_OVERLAPY = 2 #overlap on y (cols) direction  
_LEVEL = 3 #number of levels on spatial pyramid

### Parameters of nearest neighbor search
_LEAF_SIZE = 20 #leaf size of ball_tree structure
_NEIGHBORS = 3  #neighbors to show on NN search	


### Important paths (paths must be ended by '/', except _ROOT)
_ROOT = '/home/martin/MEGA/SafePet/SafePetData'
_TRAINING_PATH = _ROOT+'/train/'
_TRAINING_PATH_LBP = _ROOT+'/train_lbp/'
_TEST_PATH = _ROOT+'/test/'
_TEST_PATH_LBP = _ROOT+'/test_lbp/'
_MATRICES_PATH = _ROOT+'/pickled/matrices/'
_MAPPINGS_PATH = _ROOT+'/pickled/mappings/'
_NN_PATH = _ROOT+'/pickled/nearestneighbors/'
_SVM_PATH = _ROOT+'/pickled/svm/'
_SVM_POSITIVE = _ROOT+'/svm_train/positive/'
_SVM_NEGATIVE = _ROOT+'/svm_train/negative/'
_SVM_TEST = _ROOT+'/svm_test/'


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

if not os.path.isdir(_MAPPINGS_PATH):
	sys.exit(_MAPPINGS_PATH+' is not a valid directory!')

if not os.path.isdir(_NN_PATH):
	sys.exit(_NN_PATH+' is not a valid directory!')

if not os.path.isdir(_SVM_PATH):
	sys.exit(_SVM_PATH+' is not a valid directory!')

if not os.path.isdir(_SVM_POSITIVE):
	sys.exit(_SVM_POSITIVE+' is not a valid directory!')

if not os.path.isdir(_SVM_NEGATIVE):
	sys.exit(_SVM_NEGATIVE+' is not a valid directory!')

if not os.path.isdir(_SVM_TEST):
	sys.exit(_SVM_TEST+' is not a valid directory!')


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
	'MAPPINGS_PATH' : _MAPPINGS_PATH,
	'NN_PATH' : _NN_PATH,
	'SVM_PATH': _SVM_PATH,

	'LEAF_SIZE' : _LEAF_SIZE,
	'NEIGHBORS' : _NEIGHBORS,

	'SVM_NEGATIVE' : _SVM_NEGATIVE,
	'SVM_POSITIVE' : _SVM_POSITIVE,
	'SVM_TEST' : _SVM_TEST
}
