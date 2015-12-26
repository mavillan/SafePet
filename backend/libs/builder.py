import metric
import config as cfg
import numpy as np
import cPickle as pickle
from sklearn import svm
from sklearn.externals import joblib
from sklearn.neighbors import BallTree
from helpers import data_to_hist


def build_nn(data, out_path=None):
	nn = BallTree(data, cfg.params['LEAF_SIZE'], metric='pyfunc', func=metric.chi2)
	if out_path is not None:
		tgt = file(cfg.params['VAULT']+'NearestNeighbors', 'wb')
		pickle.dump(nn, tgt)
		tgt.close()
		return 1
	else: return nn

def build_svm(in_path1, in_path2, out_path=None):
	#positive and negative examples data respectively
	p_data = data_to_hist(in_path1)
	n_data = data_to_hist(in_path2)
	p,_ = p_data.shape
	n,_ = n_data.shape

	#creating matrix data and corresponding labels
	data = np.concatenate((p_data, n_data), axis=0)
	labels = np.concatenate((np.ones(p,dtype=int), np.zeros(n,dtype=int)))

	#creating the SVM with chi2 kernel
	#to do: cross validation
	clf = svm.NuSVC(kernel=metric.Chi2, nu=0.1)
	clf.fit(data,labels)

	if out_path is not None:
		tgt = file(cfg.params['VAULT']+'SVM', 'wb')
		pickle.dump(clf, tgt)
		tgt.close()
		return 1
	else: return clf