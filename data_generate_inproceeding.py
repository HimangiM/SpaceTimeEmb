#parses the xml file to generate the inproceedings dataset of author|title|booktitle
#on yearly basis

import codecs, os
import xml.etree.ElementTree as ET
import time

input_direc = "dblp.xml (2)"
paper_tag = ('article','inproceedings','proceedings','book', 'incollection','phdthesis','mastersthesis','www')

class AllEntities:
	def __getitem__(self, key):
		return key

#parse begin

#result = codecs.open('author_year', 'w', 'utf-8')
start = time.time()

def parse_dict(dict):
	for key, value in dict.iteritems():
		file_name = key+'.txt'
		f = open(file_name, 'a')
		f.write(str('author|title|booktitle\n'))
		for i in value:
			f.write(str(i))
			f.write("\n")
		f.close()


if __name__=='__main__':
	parser = ET.XMLParser()
	parser.parser.UseForeignDTD()
	parser.entity = AllEntities()

	dblp = dict()

	i = 0

	for event, inproceedings in ET.iterparse('dblp.xml (2)', events = ("start", "end"), parser = parser):
		if inproceedings.tag == "inproceedings" and event == 'end':
			for author_name in inproceedings.findall('author'):
				if author_name == None or inproceedings.find('booktitle') == None or inproceedings.find('title') == None or inproceedings.find('year') == None:
						continue
				else:
					y = inproceedings.find('year').text
					if inproceedings.find('year').text not in dblp.keys():
							dblp[y] = []

					if author_name.text != None and inproceedings.find('title').text != None and inproceedings.find('booktitle').text != None: 
						temp = u''.join((author_name.text,'|',inproceedings.find('title').text,'|',inproceedings.find('booktitle').text)).encode('utf-8').strip()
						print temp
						dblp[y].append(temp)
						
	parse_dict(dblp)
	print (time.time() - start)
			
	
