rep = "./spacetimerep_files/space_time_99.spacetimerep"
labels_disci = "./synthetic_data_labels/train_data_labels/train_disp/train-disp-label-95-99.txt"
labels_inter = "./synthetic_data_labels/train_data_labels/train_interdisp/train-inter-disp-label-95-99.txt"
trainfile = open("./train_data/train_data_99.txt", "w")



if __name__=='__main__':

	disci = []
	inter = []
	with open(labels_disci, "r") as infile:
		for line in infile.readlines():
			line = line.strip("\n")
			disci.append(line)


	with open(labels_inter, "r") as infile:
		for line in infile.readlines():
			line = line.strip("\n")
			inter.append(line)


	with open(rep, "r") as infile:
		infile.readline()
		for line in infile.readlines():
			rep_arr = ""
			token = line.strip().split(" ")
	
			for i in range(1, len(token)-1):
				rep_arr += token[i]
				rep_arr += " "
				
			rep_arr += token[len(token)-1]			
				
			time = token[0].split("_")
			if time[1] == "99": 
				if token[0] in disci:
					label = "0"
					print token[0], label
					trainfile.write(str(token[0] + "|"))
					trainfile.write(str(rep_arr.strip()))
					trainfile.write(str("|" + label + "\n"))
				elif token[0] in inter:
					label = "1"
					print token[0], label
					trainfile.write(str(token[0] + "|"))
					trainfile.write(str(rep_arr.strip()))
					trainfile.write(str("|" + label + "\n"))
			else:
				continue	
			
	trainfile.close()

		
