import sys
import numpy as np
from knnAuthorship import KNN

def main():

    if len(sys.argv) != 3:
        print("Usage: python classifierEvaluation.py <predictions.txt> <groundTruth.csv>")

    predictionsPath = sys.argv[1]
    groundTruthPath = sys.argv[2]

    labels = {}
    with open(groundTruthPath, 'r') as labelsFile:
        for id, line in enumerate(labelsFile.readlines()):
            labels[id] = line.split(',')[1].strip()

    confusion = np.zeros(50,50)
    with open(predictionsPath, 'w') as predictionsFile:
        predictionsFile.



if __name__ == '__main__':
    main()
