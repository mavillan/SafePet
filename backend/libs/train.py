#!/usr/bin/python
import sys
import os
import metric
import numpy as np
import cv2 as cv
from sklearn import svm
from sklearn.neighbors import BallTree


def chi2(X, Y):
	m,n = X.shape
	p,_ = Y.shape
	#Gram matrix
	G = np.empty((m,p))
	for i in range(m):
		for j in range(p):
			G[i,j] = metric.chi2(X[i],Y[j])
	return G

def build_nn(data):
	tree=BallTree(data,LEAF_SIZE,metric='pyfunc',func=chi2)
	return


def build_svm(data, labels):
	chi2_svm = svm.SVC(kernel=chi2)
	chi2_svm.fit(data,labels)
	return chi2_svm





