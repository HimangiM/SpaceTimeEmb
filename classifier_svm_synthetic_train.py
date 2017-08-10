import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
import random
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
import cPickle

files = os.listdir("./train_data")

#generates labels as 0, 1
def create_labels(file):
	labels = []
	with open(file, 'r') as infile:
		for line in infile.readlines():
			token = line.strip().split("|")
			if token[2] == "0":
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
	
	#print rep_list
	return rep_list

#generated the input of a file
def create_X(file):
	X = []
	with open(file, 'r') as infile:
		for line in infile.readlines():
			token = line.strip().split("|")
			rep = create_rep_array(token[1])
			#print rep
			X.append(rep)

	return X

if __name__=='__main__':
	
	txt_files = filter(lambda x: x[-4:] == '.txt', files)
	txt_files = glob.glob("train_data/*.txt")
	
	txt_files.sort()

	data_x = []
	data_y = []
	for i in txt_files:
		data_x += create_X(i)
		data_y += create_labels(i)

	print len(data_y)
	data_x = np.array(data_x)
	data_y = np.array(data_y)


	skf = StratifiedKFold(n_splits = 10)
	skf.get_n_splits(data_x, data_y)

	l_clf = []
	
	for train_idx, test_idx in skf.split(data_x, data_y):
		x_train, x_test = data_x[train_idx], data_x[test_idx]
		y_train, y_test = data_y[train_idx], data_y[test_idx]
		
		clf = svm.SVC()

		clf.fit(x_train, y_train)

		y_pred = clf.predict(x_test)
		
		print 'classifier score'
		print clf.score(x_test, y_test)
		l_clf.append(clf.score(x_test, y_test))
			
	sum = 0
	for i in l_clf:
		sum = sum + i

	print (sum/10.0)

	with open('svm_dump_synthetic.pkl', 'wb') as fid:
		cPickle.dump(clf, fid)

	print 'done'    


