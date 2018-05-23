import sys
import numpy as np
from lxml import etree as ET

class Vector:
	def __init__(self, fileName, authorName):
		self.fileName = fileName
		self.authorName = authorName
	vector = None

def tfidfDist(first, second):
	print("LOL")

#run as py clusteringAuthorship.py plainVector.csv tfidfVector.csv

filePlain = open(sys.argv[1], "r")
fileTfidf = open(sys.argv[2], "r")

distMat = np.zeros((5000, 5000))

plainVect = []

plainLines = filePlain.readlines()

for line in plainLines:
	line = line.split(",")
	author = line[0]
	fileName = line[1]
	tempVect = Vector(fileName, author)
	tempDict = {}
	for i in range(2, len(line)-1):
		thisPair = line[i].split()
		tempDict[thisPair[0]] = thisPair[1]
	tempVect.vector = tempDict
	plainVect.append(tempVect)

print(len(plainVect))
