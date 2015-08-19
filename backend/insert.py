#!/usr/bin/python
import sys
import os
import numpy as np
import cv2 as cv
from skimage.feature import local_binary_pattern


IMAGES_PATH='/home/martin/HDD/Dropbox/SafePet/dog_noses++/'
ORIGINAL_DATA_PATH='./npyData_original/'
SHAPE=(960,1280)
FEATURES=SHAPE[0]*SHAPE[1]
NEIGHBORS=2
COMPONENTS=5


