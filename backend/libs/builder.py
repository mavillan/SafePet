import metric
import helpers
import config as cfg
import numpy as np
from sklearn import svm
from sklearn.neighbors import BallTree

def build_nn(data):
	tree=BallTree(data,LEAF_SIZE,metric='pyfunc',func=chi2)
	return


def build_svm(in_path1, in_path2):
	#positive and negative examples data
	p_data = data_to_hist(in_path1)
	n_data = data_to_hist(in_path2)
	p,_ = p_data.shape
	n,_ = n_data.shape

	#creating matrix data and corresponding labels
	data = np.concatenate((p_data, n_data), axis=0)
	labels = np.concatenate((np.ones(p,dtype=int), np.zeros(n,dtype=int)))

	#creating the SVM with chi2 kernel
	chi2_svm = svm.SVC(kernel=chi2)
	chi2_svm.fit(data,labels)
	return chi2_svm