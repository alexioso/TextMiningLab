# TextMiningLab

knnAuthorship.py
Usage: python knnAuthorship.py <distanceMatrix.txt> <groundTruth.csv> K [documentIndices.txt]

Creating the distance matrix took 2 and 15 minutes for okapi and cosine similarity respectively so in order to avoid
recomputing the distance matrix on every call (iterative testing would have taken way too long) we designed our KNN
classifier to read the distance matrix from a file. As a result the usage of the script changes a little.
To use it first compute the distance matrices by running distMatCalculation.py. Then run knnAuthorship.py specifying
which matrix to use as a program argument. The similarity metric is implicitly indicated by the choice of distance matrix.

By default the classifier will perform all-but-one validation on each document (row of the distance matrix).
If you would like to use to classifier to a specific subset of documents, instead of giving the program a list of vectorized
documents you must give it the indices of the rows that correspond to those vectorized documents in the distance
matrix. This is done with the optional documentIndices.txt argument
The order that the documents appeared in the vectorized form inputted to distMatCalculation.py will be the same
order they appear in the distMatrix. It then uses the groundTruth.csv to map these document indices to the author.

To run the evaluation we build the distance matrix for all 5000 documents do not specify the optional argument.
This goes through each document, finds the k most similar documents, looks up the authors of each, and
prints the majority author to the output file.