from lxml import etree as ET
import sys
import math
import numpy as np

# py clusterEvaluation.py answerXML.xml tfidVector.csv

def recurse(node, tempList):
	for child in node:
		if(child.tag == "leaf"):
			tempList.append(child)
		else:
			recurse(child, tempList)


tree = ET.parse(sys.argv[1])
root = tree.getroot()
readFile = open(sys.argv[2], "r")

lines = readFile.readlines()
fileToAuth = {}

i = 0
authToNum = {}
for line in lines:
	line = line.split(",")
	fileToAuth[line[1]] = line[0]

i = 0
for line in lines:
	line = line.split(",")
	if line[0] not in authToNum:
		authToNum[line[0]] = i
		i += 1

clusters = []
clusters.append((root.attrib["height"], root))

while(len(clusters) < 50):
	sortedThings = sorted(clusters, key=lambda tup:tup[0], reverse=True)
	bestIndex = -1
	for i in range(len(sortedThings)):
		children = []
		for child in sortedThings[i][1]:
			if(child.tag != "leaf"):
				children.append(child)
		numList = []
		for a in children:
			tempThing = []
			recurse(a, tempThing)
			numList.append(len(tempThing))
		flag = True
		for a in numList:
			if a < 30:
				flag = False
		if flag:
			bestIndex = i
			break
	temp = sortedThings.pop(i)
	for child in temp[1]:
		if(child.tag != "leaf"):
			sortedThings.append((child.attrib["height"], child))
	clusters = sortedThings

realCluster = []
for node in clusters:
	tempList = []
	recurse(node[1], tempList)
	realCluster.append(tempList)

#expected is row, actual is column
matrix = np.zeros((50, 50))
right = 0
wrong = 0
purity = 0
pureCluster = {}
clustCount = {}
print(authToNum)
for a in authToNum.keys():
	pureCluster[a] = 0
	clustCount[a] = 0

it = 0
for thisClust in realCluster:
	hm = {}
	tot = 0
	for leaf in thisClust:
		tot += 1
		if fileToAuth[leaf.attrib["data"]] not in hm:
			hm[fileToAuth[leaf.attrib["data"]]] = 1
		else:
			hm[fileToAuth[leaf.attrib["data"]]] += 1
	tupList = []
	for k in hm.keys():
		tupList.append((k, hm[k]))
	tupList = sorted(tupList, key=lambda tup:tup[1], reverse = True)
	print("Cluster: ",it)
	it += 1
	pureness = tupList[0][1] / tot
	purity += pureness
	print("Purity: ",pureness)
	print("Label: "+tupList[0][0])
	for leaf in thisClust:
		if tupList[0][0] == fileToAuth[leaf.attrib["data"]]:
			right += 1
		else:
			wrong += 1
		matrix[authToNum[tupList[0][0]]][authToNum[fileToAuth[leaf.attrib["data"]]]] += 1
	print("")
	pureCluster[tupList[0][0]] += pureness
	clustCount[tupList[0][0]] += 1 

for i in authToNum.keys():
	if clustCount[i] != 0:
		pureCluster[i] /= clustCount[i]
numTup = []
for i in clustCount.keys():
	numTup.append((i, pureCluster[i]))

numTup = sorted(numTup, key=lambda tup:tup[1], reverse = True)
print("Authors sorted by purity of clusters assigned to them")
for thing in numTup:
	print("Author: ",thing[0]," Purity of Clusters: ",thing[1])
print("")

for i in authToNum.keys():
	prec = 0
	rec = 0
	acc = matrix[authToNum[i]][authToNum[i]]
	for j in range(len(matrix)):
		prec += matrix[authToNum[i]][j]
		rec += matrix[j][authToNum[i]]
	if prec != 0:
		prec = acc/prec
	if rec != 0:
		rec = acc/rec
	print("Author: ", i," Precision: ", prec," Recall: ",rec)


print("")
print("Overall purity of clusters: ", purity/50)
print("Overall accuracy: ", right/(wrong+right))



