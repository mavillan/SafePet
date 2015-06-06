#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
from sklearn import decomposition
from sklearn.neighbors import NearestNeighbors

#Global
IMAGES_PATH='/home/martin/HDD/Dropbox/SafePet/dog_noses++/'
TEST_PATH='/home/martin/HDD/Dropbox/SafePet/dog_test/'
REDUCED_DATA_PATH='./npyData_reduced/'
ORIGINAL_DATA_PATH='./npyData_original/'
SHAPE=(960,1280)
FEATURES=SHAPE[0]*SHAPE[1]
NEIGHBORS=2
COMPONENTS=5


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
	if os.path.isfile('./reduced_dogs.npy'):
		reduced_data=np.load('./reduced_dogs.npy')
	if os.path.isfile('./pc_matrix.npy'):
		pc=np.load('./pc_matrix.npy')
	if data.size!=0:
		mean=np.mean(data,axis=0)

	#Compute KNN with training data
	if os.path.isfile('./reduced_dogs.npy'):
		nbrs=NearestNeighbors(n_neighbors=NEIGHBORS,algorithm='ball_tree')
		nbrs.fit(reduced_data)

	exit=False
	insert=False
	while not exit:
		command=raw_input("> ")
		argv=command.strip().split()

		if len(argv)>2:
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
			data=np.vstack((data,dog))

			#Here start the fun...
			pca=decomposition.PCA(n_components=COMPONENTS,copy=True,whiten=False)
			pca.fit(data)

			#Proyecting...
			reduced_data=pca.transform(data) #Proyection in principal components subspace
			print "Correctly inserted!"

			#Update knn object with new data
			nbrs.fit(reduced_data)
			insert=True

		
		#SEARCH	
		elif argv[0]=='search':
			if os.path.isfile(TEST_PATH+argv[1]):
				filename=TEST_PATH+argv[1]	
			elif os.path.isfile(os.getcwd()+'/'+argv[1]):
				filename=os.getcwd()+'/'+argv[1]
			elif os.path.isfile(argv[1]):
				filename=argv[1]
			else:
				print 'Image not found!'
				continue

			img=cv.imread(filename)

			#Show original image
			cv.namedWindow('main',cv.WINDOW_NORMAL)
			cv.imshow('main',img)
			cv.waitKey(0)
			cv.destroyAllWindows()

			#To grayscale and to float
			gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
			gray=np.float32(gray)

			#Reshape to features space
			dog=gray.reshape(1,FEATURES)

			#Shift
			dog-=mean

			#Proyection in principal components subspace
			rdog=np.dot(dog,pc.transpose())

			#KNN (2 nearest neighbors)
			distances,indices=nbrs.kneighbors(rdog,return_distance=True)


			#Show the match
			count=0
			print 'Results: '
			for res in indices[0]:
				print "Neighbor {0}: dog{1}, (distance={2})".format(str(count),str(res),str(distances[0,count]))
				img=cv.imread(IMAGES_PATH+'dog'+str(res)+'.jpg')
				cv.namedWindow('main', cv.WINDOW_NORMAL)
				cv.imshow('main',img)
				cv.waitKey(0)
				cv.destroyAllWindows()
				count+=1

		#EXIT
		elif argv[0]=='exit':
			exit=True
			continue

		#WRONG
		else:
			print 'Wrong input!'
			continue

	#Store actual state if something was insert
	if insert:
		#Store reduced dogs in new subspace
		np.save('./reduced_dogs',reduced_data)
		
		#Store principal components as npy file
		np.save('./pc_matrix',pca.components_)

	print "Session finished!"
	sys.exit(0)  
	