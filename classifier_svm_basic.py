import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm

arr_labels = ["disciplinary", "inter-disciplinary"]

files = os.listdir("/media/sdg/himangi/DBLP/author_rep_class_labels")

#generates labels as 0, 1
def create_labels(file):
	labels = []
	with open(file, 'r') as infile:
		for line in infile.readlines():
			token = line.strip().split("|")
			if token[2] == "disciplinary":
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
			r = rep
			#print rep
			X.append(r)

	return X

def create_folds(size, num_folds):
	perm = np.random.permutation(size)
	#perm = np.int32(perm)
	folds = []
	fold_size = int(size/num_folds)
	for f in range(num_folds):
		test = perm[fold_size*f:fold_size*f+fold_size] 
		train = [item for item in perm if item not in test]
		folds.append([train,test])

	return folds


if __name__=='__main__':
	
	txt_files = filter(lambda x: x[-4:] == '.txt', files)
	txt_files = glob.glob("author_rep_class_labels/*.txt")
	
	txt_files.sort()	

	data_x = []
	data_y = []

	for i in txt_files:
		data_x += create_X(i)
		data_y += create_labels(i)
	
	data_x = np.array(data_x)
	data_y = np.array(data_y)
	
	folds = create_folds(data_x.shape[0], 5)
	#print folds

	for fold in folds:
		train_idx,test_idx = fold
		x_train = data_x[train_idx,:]
		y_train = data_y[train_idx]

		x_test = data_x[test_idx,:]
		y_test = data_y[test_idx]

		clf = svm.SVC()
		clf.fit(x_train, y_train)

		clf.predict(x_test)
		print clf.score(x_test, y_test)
