import sys
import numpy as np
from collections import defaultdict

from knnAuthorship import KNN

def main():

    if len(sys.argv) != 3:
        print("Usage: python classifierEvaluation.py <predictions.txt> <groundTruth.csv>")
        sys.exit(1)

    predictionsPath = sys.argv[1]
    groundTruthPath = sys.argv[2]

    actual = []
    authors = set()
    with open(groundTruthPath, 'r') as labelsFile:
        for line in labelsFile.readlines():
            actual.append(line.split(',')[1].strip())
            authors.add(line.split(',')[1].strip())

    assert(len(authors) == 50)
    authors = list(authors)

    predicted = []
    confusion = np.zeros((len(authors), len(authors)))
    with open(predictionsPath, 'r') as predictionsFile:
        for line in predictionsFile.readlines():
            predicted.append(line.strip())

    hits = defaultdict(int)
    strikes = defaultdict(int)
    misses = defaultdict(int)

    for i in range(len(predicted)):
        if predicted[i] == actual[i]:
            hits[predicted[i]] += 1
        else:
            strikes[predicted[i]] += 1
            misses[actual[i]] += 1

        p = authors.index(predicted[i])
        a = authors.index(actual[i])
        confusion[p][a] += 1

    print('Confusion matrix')
    for c in confusion:
        for x in c:
            print("{}".format(x), end=' ')
        print()

    correct = 0
    incorrect = 0
    for key in hits.keys():
        print(key)
        print('     Hits:', hits[key])
        print('     Strikes:', strikes[key])
        print('     Misses:', misses[key])
        precision = hits[key]/float(hits[key]+strikes[key])
        recall = hits[key]/float(hits[key]+misses[key])
        print('     Precision:', precision)
        print('     Recall:', recall)
        print('     F-1:', (2 * precision*recall)/(precision+recall))
        correct += hits[key]
        incorrect += misses[key]

    print()
    print('Correct:', correct)
    print('Incorrect:', incorrect)
    print('Accuracy:', correct/float(incorrect+correct))


if __name__ == '__main__':
    main()
