import numpy as np
import operator
import sys


class KNN:
    def __init__(self, distMatrix, k, labels):
        self.distMatrix = distMatrix
        self.labels = labels
        self.k = k

    def classify(self, id):
        distances = []
        """Traverse down column until you hit id of document then traverse down row"""
        i = 0
        j = id
        # Go down row
        while i < id:
            distances.append((self.distMatrix[i][j], i))
            i += 1
        assert(i==j)
        j += 1
        # Go down column
        while j < len(self.distMatrix[i]):
            distances.append((self.distMatrix[i][j], j))
            j += 1

        distances = sorted(distances, key=lambda distance: -1 * distance[0])

        votes = {}
        for x in range(self.k):
            author = self.labels[distances[x][1]]
            if author in votes:
                votes[author] += 1
            else:
                votes[author] = 1

        return max(votes.items(), key=operator.itemgetter(1))[0]


def main():

    indicesPath = None
    if len(sys.argv) == 5:
        indicesPath = sys.argv[4]
    elif len(sys.argv) != 4:
        print("Usage: python knnAuthorship.py <distanceMatrix.txt> <groundTruth.csv> K [documentIndices.txt] ")
        sys.exit(1)

    distMatrixPath = sys.argv[1]
    groundTruthPath = sys.argv[2]
    k = int(sys.argv[3])

    distMatrix = np.loadtxt(distMatrixPath, dtype=float, delimiter=' ')
    labels = {}
    with open(groundTruthPath, 'r') as labelFile:
        for id, line in enumerate(labelFile.readlines()):
            labels[id] = line.split(',')[1].strip()

    knn = KNN(distMatrix, k, labels)

    with open('knn-output.txt', 'w') as outputFile:
        if indicesPath != None:
            with open(indicesPath, 'r') as indicesFile:
                for line in indicesFile.readlines():
                    row = int(line.strip())
                    print(knn.classify(row), file=outputFile)
        else:
            for i in range(len(distMatrix)):
                print(knn.classify(i), file=outputFile)

if __name__ == '__main__':
    main()
