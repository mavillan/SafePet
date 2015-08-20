#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
from sklearn import decomposition
from sklearn.utils.extmath import fast_dot

IMAGES_PATH='/home/martin/HDD/Dropbox/SafePet/dog_noses++/'
ORIGINAL_DATA_PATH='./npyData_original/'
SHAPE=(960,1280)
FEATURES=SHAPE[0]*SHAPE[1]
NEIGHBORS=2
COMPONENTS=5


'''Script to insert data from IMAGES_PATH directory to the app'''


def load_orig_data():
	tmp=list()
	names=os.listdir('./npyData_original/')
	names.sort()
	for arr in names:
		tmp.append(np.load('./npyData_original/'+arr)[0])
	return np.array(tmp)


def preProcessing(img):
	return img


if __name__=='__main__':
	if len(sys.argv)>1:
		sys.exit('Wrong input!')
	
	filenames=os.listdir(IMAGES_PATH)

	for filename in filenames:
		filename=IMAGES_PATH+filename
		img=cv.imread(filename)

		#To grayscale and to float
		gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
		gray=np.float32(gray)

		#Reshape to features space
		dog=gray.reshape(1,FEATURES)

		#Store as npy file
		if len(os.listdir('./npyData_original'))==0:
			#First dog!
			last='0'
		else:
			#Get the last dog index
			last=str(len(os.listdir('./npyData_original/')))
		np.save('./npyData_original/dog'+last,dog)

		#Load data
		data=load_orig_data()
		print data
		print data.shape

		#Here start the fun...
		pca=decomposition.PCA(n_components=COMPONENTS,copy=True,whiten=False)
		pca.fit(data)
		#Proyecting...
		reduced_data=pca.transform(data) #Proyection in principal components subspace

		#Store reduced dogs in new subspace
		np.save('./reduced_dogs',reduced_data)

		#Store principal components as npy file
		np.save('./pc_matrix',pca.components_)

	print "Correctly inserted!"
	sys.exit(0)  

