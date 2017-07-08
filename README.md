# SpaceTimeEmb Updates

### 7 July, 2017
  - Binary classification using SVM: (disciplinary - 0, inter-disciplianry - 1)
    - Total users : 165,861
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
 

