#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
from sklearn import decomposition
from sklearn.neighbors import NearestNeighbors

#Global
IMAGES_PATH='/home/martin/HDD/Dropbox/SafePet/dog_noses/'
QUERY_PATH='/home/martin/HDD/Dropbox/SafePet/query_noses/'
REDUCED_DATA_PATH='./npyData_reduced/'
ORIGINAL_DATA_PATH='./npyData_original/'
SHAPE=(960,1280)
FEATURES=1228800
NEIGHBORS=2


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
	# if len(sys.argv)>2:
	# 	sys.exit('Wrong input!')
	# elif len(sys.argv)==1:
	# 	sys.exit('No image input!')

	#Load data
	data=load_orig_data()
	reduced_data=np.load('./reduced_dogs.npy')
	pc=np.load('./pc_matrix.npy')
	mean=np.mean(data,axis=0)

	#Compute KNN with training data
	nbrs=NearestNeighbors(n_neighbors=NEIGHBORS,algorithm='ball_tree')
	nbrs.fit(reduced_data)

	exit=False
	while not exit:
		command=raw_input("> ")
		argv=command.strip().split()

		if len(argv)!=2:
			print 'Wrong input!'
			continue

		#INSERT
		elif argv[0]=='insert':
			if os.path.isfile(IMAGES_PATH+argv[1]):
				filename=IMAGES_PATH+argv[1]
			else:
				print 'Image not found!'
				continue

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

			#Add it to data matrix
			data=np.vstack(data,dog)

			#Here start the fun...
			pca=decomposition.PCA(n_components=5,copy=True,whiten=False)
			pca.fit(data)

			#Proyecting...
			reduced_data=pca.transform(data) #Proyection in principal components subspace
			print "Correctly inserted!"

			#Update knn object with new data
			nbrs.fit(reduced_data)

		
		#SEARCH	
		elif argv[0]=='search':
			if os.path.isfile(QUERY_PATH+argv[1]):
				filename=QUERY_PATH+argv[1]	
			elif os.path.isfile(os.getcwd()+'/'+argv[1]):
				filename=os.getcwd()+'/'+argv[1]
			elif os.path.isfile(argv[1]):
				filename=argv[1]
			else:
				print 'Image not found!'
				continue

			img=cv.imread(filename)

			#Show original image
			cv2.namedWindow('main',cv2.WINDOW_NORMAL)
			cv2.imshow('main',img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

			#To grayscale and to float
			gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
			gray=np.float32(gray)

			#Show grayscale image
			cv2.namedWindow('main', cv2.WINDOW_NORMAL)
			cv2.imshow('main',gray)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

			#Reshape to features space
			dog=gray.reshape(1,FEATURES)

			#Shift
			dog-=mean

			#Proyection in principal components subspace
			rdog=np.dot(dog,pc.transpose())

			#KNN (2 nearest neighbors)
			neigh=nbrs.kneighbors(rdog,return_distance=False)

			#Show the match
			count=1
			print 'Results: '
			for res in neigh:
				print "Neighbor {0}: dog{1}".format(str(count),str(neigh))
				cv2.namedWindow('main', cv2.WINDOW_NORMAL)
				cv2.imshow('main',IMAGES_PATH+'dog'+str(res))
				cv2.waitKey(0)
				cv2.destroyAllWindows()
				count+=1

		#EXIT
		elif argv[0]=='exit':
			exit=True
			continue

		#WRONG
		else:
			print 'Wrong input!'
			continue

	#Store actual state

	#Store reduced dogs in new subspace
	np.save('./reduced_dogs',reduced_data)

	#Store principal components as npy file
	np.save('./pc_matrix',pca.components_)

	print "Session finished!"
	sys.exit(0)  
	