import cPickle
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
import random
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score

files = os.listdir("./test_data")

with open('svm_dump_synthetic.pkl', 'rb') as fid:
	svm_loaded = cPickle.load(fid)


#generates labels as 0, 1
def create_labels(file):
	labels = []
	with open(file, 'r') as infile:
		for line in infile.readlines():
			token = line.strip().split("|")
			if token[1] == "0":
				labels.append(0)
			else:
				labels.append(1)

	return labels

#generated array format of representation for input
def create_rep_array(line):
	rep_list = []
	token = line.strip().split(" ")
	counter = 0
	for i in token:
		i = i.strip() 
		rep_list.append(float(i))
	
	return rep_list

#generated the input of a file
def create_X(file):
	X = []
	with open(file, 'r') as infile:
		for line in infile.readlines():
			token = line.strip().split("|")
			rep = create_rep_array(token[1])
			X.append(rep)
	return X

if __name__=='__main__':
	
	txt_files = filter(lambda x: x[-4:] == '.txt', files)
	txt_files = glob.glob("test_data/*.txt")
	
	txt_files.sort()

	data_x = []
	data_y = []

	for i in txt_files:
		data_x += create_X(i)
	 	data_y += create_labels(i)

	print len(data_y)
	data_x = np.array(data_x)
	data_y = np.array(data_y)

	# print data_x[1]
	svm_loaded.predict(data_x)
	print svm_loaded.score(data_x, data_y)

