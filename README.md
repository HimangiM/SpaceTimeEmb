# SpaceTimeEmb Updates

### 12 July, 2017
   - Neural Network 
      - Tuning the parameters (according to DeepWalk paper)
         - representation size : 128
         - walk length : 80
         - number of walks per node : 10
         - time window : 10
         - context size/vocabulary window size: 10
     - Result: 73% (one hidden layer)

### 11 July, 2017
   -Neural Network (TensorFlow)
      - Dataset - 8040 random disciplinary points, 7360 inter discipinary (15400 data points)
      - Result : 66% (approximately same for one and two hidden layers, nodes in a hidden layer, tuning the learning rate) 

### 10 July, 2017 (uniform dataset)
   - Binary classification using SVM: (disciplinary - 0, inter-disciplinary - 1)
      - Dataset - 8040 random disciplinary points, 7360 inter discipinary (15400 data points)
      - Result : 52%

### 7 July, 2017 (skewed dataset)
  - Binary classification using SVM: (disciplinary - 0, inter-disciplinary - 1)
      - Total users : 57,954
      - Five-fold cross validation
      - Result : 88.8576%
      - Assumptions :
         - Time window of 5 taken from 1969, 1971, 1973, 74, 75 and so on. Experiment of taking the time window with respect to the user to be done.
         - Ignoring the node if not present at some time point, creating a virtual node in place of it to be done.
                 
### 4 July, 2017  
   - Generate a file manually that will have the contents as:
    representation|domain/labels. (domain/labels - disciplinary, inter-disciplinary)
 
### 3 July, 2017
   - On the generated graphs, run the SpaceTimeEmb algorithm taking a time window of 5 to get the representation of every node. 
  
### 2 July, 2017  
### DBLP Dataset

   - Dataset:
      - 45 graphs : [1969, 1971, 1973, 1975, 1976, 1977....2017] 
      - Links between the author based on their papers (if A has a paper with B, a link exists between A and B)
      - Format of the file :
         author|title|booktitle/conference|domain/label
      - Data of ‘inproceedings’ is utilised.
      - Labels were defined with reference to the paper : ```https://pdfs.semanticscholar.org/2fb3/6ecf864f40e84f2e50a5152107e16a03fb21.pdf```
 
   - Classifier:
     4 classes - Database, Data Mining, Artificial Intelligence, Information Analysis
 

