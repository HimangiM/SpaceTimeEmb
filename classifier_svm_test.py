import cPickle
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
import random
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score

arr_labels = ["disciplinary", "inter-disciplinary"]

files = os.listdir("/media/sdg/himangi/DBLP/author_rep_class_labels")

with open('svm_classifier_dump_f.pkl', 'rb') as fid:
	svm_loaded = cPickle.load(fid)


#generates labels as 0, 1
def create_labels(file):
	labels = []
	with open(file, 'r') as infile:
		for line in infile.readlines():
			token = line.strip().split("|")
			if token[1
			] == "0":
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
		rep_list.append((float(i)))
	
	return rep_list

#generated the input of a file
def create_X(file):
	X = []
	with open(file, 'r') as infile:
		for line in infile.readlines():
			token = line.strip().split("|")
			rep = create_rep_array(token[0])
			X.append(rep)
	return X


if __name__=='__main__':

	data_x = np.array(create_X('test_data_svm.txt'))
	data_y = np.array(create_labels('test_data_svm.txt'))

	l = np.array(random.sample(xrange(len(data_x)), len(data_x)))

	data_x = data_x[l]
	svm_loaded.predict(data_x)
	print svm_loaded.score(data_x, data_y)

