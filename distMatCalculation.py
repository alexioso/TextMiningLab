import sys
import numpy as np
from lxml import etree as ET

class Vector:
	def __init__(self, fileName, authorName):
		self.fileName = fileName
		self.authorName = authorName
	vector = None

def calcNormal(firstSet, secondSet, m1, m2, first, second):
	m3 = 0
	bottom = (m1 * m2)**0.5
	fin = list(firstSet.intersection(secondSet))
	for t in fin:
		m3 += first[t] * second[t]
	return 1 - m3/bottom


#run as py distMatCalculation.py plainVector.csv tfidfVector.csv

filePlain = open(sys.argv[1], "r")
fileTfidf = open(sys.argv[2], "r")

distMatPlain = np.zeros((5000, 5000))
distMatTfidf = np.zeros((5000, 5000))


plainVect = []
tfidfVect = []

plainLines = filePlain.readlines()

for line in plainLines:
	line = line.split(",")
	author = line[0]
	fileName = line[1]
	tempVect = Vector(fileName, author)
	tempDict = {}
	for i in range(2, len(line)-1):
		thisPair = line[i].split()
		tempDict[thisPair[0]] = float(thisPair[1])
	tempVect.vector = tempDict
	plainVect.append(tempVect)

filePlain.close()

tfidfLines = fileTfidf.readlines()

for line in tfidfLines:
	line = line.split(",")
	author = line[0]
	fileName = line[1]
	tempVect = Vector(fileName, author)
	tempDict = {}
	for i in range(2, len(line)-1):
		thisPair = line[i].split()
		tempDict[thisPair[0]] = float(thisPair[1])
	tempVect.vector = tempDict
	tfidfVect.append(tempVect)

fileTfidf.close()

listNums = list(range(5000))

z = 0
mSet = []
for a in tfidfVect:
	curThing = a.vector
	mVal = 0
	for a in curThing.keys():
		mVal += (curThing[a])**2
	mSet.append(mVal)

setSet = []
for a in tfidfVect:
	temp = set(a.vector.keys())
	setSet.append(temp)

for i in range(4999):
	for j in range(i + 1, 5000):
		distMatPlain[i][j] = calcNormal(setSet[i], setSet[j], mSet[i], mSet[j], tfidfVect[i].vector, tfidfVect[j].vector)
		if(z % 100000 == 0):
			print(z)
		z += 1

np.savetxt("plainDistMat.txt", distMatPlain)