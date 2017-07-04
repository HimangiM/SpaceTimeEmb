# SpaceTimeEmb Updates

### 4 July, 2017
  - Generate a file manually that will have the contents as:
    author|representation|domain/labels. (domain/labels - Database, Data Mining, Artificial Intelligence, Information Analysis)
  - Perform the classification. Taking some percentage of the file (say 75%) and prediction on the rest (25%). Input will be       the representation and output will be one of the 4 classes.
  - Find out the Macro F1- score for the analysis.
  - Experiment:
    Considering the time window with respect to the user node i.e, when the user published his first paper, from thereafter         taking the window.
  
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
 

