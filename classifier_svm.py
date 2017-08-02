#implements a svm 
#ignores the node if not present
#time window of 5 taken normally, not wrt user
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
import random
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
import cPickle

arr_labels = ["disciplinary", "inter-disciplinary"]

files = os.listdir("/media/sdg/himangi/DBLP/author_rep_class_labels")

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
			r = rep
			#print rep
			X.append(r)

	return X

# def create_folds(size, num_folds):
# 	perm = np.random.permutation(size)
# 	#perm = np.int32(perm)
# 	folds = []
# 	fold_size = int(size/num_folds)
# 	for f in range(num_folds):
# 		test = perm[fold_size*f:fold_size*f+fold_size] 
# 		train = [item for item in perm if item not in test]
# 		folds.append([train,test])

# 	return folds

def create_folds(size, num_folds):
	perm1 = np.random.permutation(size/2)					#disci
	perm2 = [item for item in range(size) if item not in perm1]	#inter-disci
	folds = []
	fold_size = int(size/num_folds)
	for f in range(num_folds):
		test1 = perm1[(fold_size*f)/2:(fold_size*f + fold_size)/2]
		test2 = perm2[(fold_size*f)/2:(fold_size*f + fold_size)/2]
		test =  np.concatenate((test1, test2), axis=0)
		train1 = [item for item in perm1 if item not in test1]
		train2 = [item for item in perm2 if item not in test2]
		train =  np.concatenate((train1, train2), axis=0)

		folds.append([train, test])

	return folds		



if __name__=='__main__':
	
	txt_files = filter(lambda x: x[-4:] == '.txt', files)
	txt_files = glob.glob("author_rep_class_labels/*.txt")
	
	txt_files.sort()	

	# data_x = []
	# data_y = []

	# for i in txt_files:
	# 	data_x += create_X(i)
	# 	data_y += create_labels(i)
	
	# data_x = np.array(data_x)
	# data_y = np.array(data_y)

	l = np.array(random.sample(xrange(50591),8040))
	
	print l

	
	f_d = open("disciplinary.txt", 'r')
	f_id = open("inter_disciplinary.txt", 'r')

	data_x_disci = np.array(create_X("disciplinary.txt"))			#all disci rep data points				
	l_train = int(0.7*8040)

	data_x_disci_new = data_x_disci[l]								#final randomly selected 8040 points
	data_x_disci_train = data_x_disci_new[0:l_train+20]				#final randomly selected 8040 points
	data_x_disci_test = data_x_disci_new[l_train+20:]

	data_y_disci = np.array(create_labels("disciplinary.txt"))		#all disci labels data points
	data_y_disci_new = data_y_disci[l]								#final labels of the random points
	data_y_disci_train = data_y_disci_new[0:l_train+20]								#final labels of the random points
	data_y_disci_test = data_y_disci_new[l_train+20:]

	print len(data_x_disci_train)

	data_x_inter = np.array(create_X("inter_disciplinary.txt"))			#final all inter rep data points
	train = int(0.7*len(data_x_inter))
	data_x_inter_train = data_x_inter[0:train]
	data_x_inter_test = data_x_inter[train:]

	data_y_inter = np.array(create_labels("inter_disciplinary.txt"))	#finalall inter label points	
	data_y_inter_train = data_y_inter[0:train]
	data_y_inter_test = data_y_inter[train:]
	
	print data_x_inter_train.shape[0]

	# print data_x_disci_test[0]
	# print str(" ".join(repr(float(i)) for i in data_x_disci_test[0]))
	# f_td = open('test_data_svm.txt', 'a')
	# i = 0
	# while(i < len(data_x_disci_test)):
	# 	# print str(" ".join(repr(float(i)) for i in data_x_disci_test[0]))
	# 	f_td.write(str(" ".join(repr(float(i)) for i in data_x_disci_test[i])) + "|" + str(data_y_disci_test[i]) + "\n")	
	#  	i += 1


	# i = 0
	# while(i < len(data_x_inter_test)):
	# 	f_td.write(str(" ".join(repr(float(i)) for i in data_x_inter_test[i])) + "|" + str(data_y_inter_test[i]) + "\n")	
	# 	i += 1


	skf = StratifiedKFold(n_splits = 10)
	data_x = np.concatenate((data_x_disci_train, data_x_inter_train), axis=0)
	data_y = np.concatenate((data_y_disci_train, data_y_inter_train), axis=0)

	p = np.array(random.sample(xrange(len(data_x)), len(data_x)))

	data_x = data_x[p]
	data_y = data_y[p]
	
	skf.get_n_splits(data_x, data_y)

	l_clf = []
	l_macro = []

	for train_idx, test_idx in skf.split(data_x, data_y):
		x_train, x_test = data_x[train_idx], data_x[test_idx]
		y_train, y_test = data_y[train_idx], data_y[test_idx]
		
		clf = svm.SVC()

		clf.fit(x_train, y_train)
		y_pred = clf.predict(x_test)
		
		print 'classifier score'
		print clf.score(x_test, y_test)
		l_clf.append(clf.score(x_test, y_test))
		
	# 	# print 'micro f1 score'
	# 	# print f1_score(y_test, y_pred, average = 'micro')
	# 	# print 'macro f1 score'
	# 	# print f1_score(y_test, y_pred, average = 'macro')
	# 	# l_macro.append(f1_score(y_test, y_pred, average = 'macro'))
	
	sum = 0
	for i in l_clf:
		sum = sum + i

	print (sum/10.0)

	with open('svm_classifier_dump_f.pkl', 'wb') as fid:
		cPickle.dump(clf, fid)

	print 'done'    

	f_d.close()
	# f_td.close()
	f_id.close()

	# # load it again
	# with open('my_dumped_classifier.pkl', 'rb') as fid:
	#     gnb_loaded = cPickle.load(fid)

	# sum2 = 0
	# for i in l_macro:
	# 	sum2 = sum2 + i
	
	# print (sum2/10.0)
	
	# folds = create_folds(data_x.shape[0], 10)
	# #print folds

	



