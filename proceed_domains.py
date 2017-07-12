#creates the labels for the dataset
#format author|title|booktitle|domains
#on yearly basis

import os 
import glob
import time

files = os.listdir("/media/sdg/himangi/DBLP/yearly_conf")

conf_domain_dict = {'Database':['ICDE', 'VLDB', 'SIGMOD', 'PODS', 'EDBT'], 
					'Artificial Intelligence': ['IJCAI', 'AAAI', 'ICML', 'ECML'], 
					'Data Mining': ['KDD', 'PAKDD', 'ICDM', 'PKDD', 'SDM'], 
					'Information Analysis': ['SIGIR', 'WWW', 'ECIR', 'WSDM']}

def create_file(year, author, title, booktitle, domain):
	name = year + ".txt"
	f = open(name, 'a')
	f.write(str(author + "|" + title + "|" + booktitle + "|" + domain + "\n"))
	f.close()

if __name__=='__main__':
	txt_files = filter(lambda x: x[-4:] == '.txt', files)
	txt_files = glob.glob("yearly_conf/*.txt")
	
	txt_files.sort()
	#print txt_files
	
	for file in txt_files:
		with open(file, 'r') as infile:
			for line in infile:
				token = line.strip().split("|")
				for k, v in conf_domain_dict.iteritems():
					if token[2] in v:
						for k, v in conf_domain_dict.iteritems():
							if token[2] in v:
								temp = k
								print k
								name = file[12:16] + "_labels"
								create_file(name, token[0], token[1], token[2], temp)
	
	print 'done'
	
