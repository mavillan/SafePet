#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
from sklearn import decomposition

IMAGES_PATH='/home/martin/HDD/Dropbox/SafePet/dog_noses/'
SHAPE=(960,1280)
FEATURES=1228800


def load_orig_data():
	tmp=list()
	for arr in os.listdir('./npyData_original/'):
		tmp.append(np.load('./npyData_original/'+arr)[0])
	return np.array(tmp)


def preProcessing(img):
	return img


if __name__=='__main__':
	if len(sys.argv)>2:
		sys.exit('Wrong input!')
	elif len(sys.argv)==1:
		sys.exit('No image input!')

	filename=IMAGES_PATH+sys.argv[1]
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
		last=os.listdir('./npyData_original/')
		last=str(int(last)+1)
	np.save('./npyData_original/dog'+last,dog)

	#Load data
	data=load_orig_data()
	print data
	print data.shape

	#Here start the fun...
	pca=decomposition.PCA(n_components=5)
	pca.fit(data)
	reduced_dog=pca.transform(dog) #Proyection in principal components subspace

	#Store reduced dog as npy file
	np.save('./npyData_reduced/reduced_dog'+last,reduced_dog)

	#Store principal components as npy file
	np.save('./pc_matrix',pca.components_)

	print "Correctly inserted!"
	sys.exit(0)  

