#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from skimage.feature import local_binary_pattern as lbp
from sklearn.neighbors import BallTree
	

def build_nn(data):
	tree=BallTree(data,LEAF_SIZE,metric='pyfunc',func=chi2)
	return








