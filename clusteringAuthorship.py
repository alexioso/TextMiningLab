import sys
import numpy as np
from lxml import etree as ET
import math

class Vector:
	def __init__(self, fileName, authorName):
		self.fileName = fileName
		self.authorName = authorName
	vector = None

class Leaf:
	def __init__(self, height, data):
		self.height = height
		self.data = data

class Node:
	def __init__(self, height):
		self.height = height
		self.l1 = None
		self.l2 = None
		self.n1 = None
		self.n2 = None

class Tree:
	def __init__(self, height):
		self.height = height
		self.l1 = None
		self.l2 = None
		self.n1 = None
		self.n2 = None

def difFast(listNums, tes2d):
	minDist = 9999999999
	ans = 0
	minIN = -1
	minJN = -1
	for i in range(0, len(listNums) - 1):
		for j in range(i + 1, len(listNums)):
			ans = tes2d[i][j]
			if(ans < minDist):
				minIN = i
				minJN = j
				minDist = ans
	return minIN, minJN, minDist

def recurseTree(curNode, myXML, existNode, nodeList, k):
	if(curNode.l1 != None):
		leaf = ET.Element("leaf")
		leaf.set("height", "0")
		leaf.set("data", str(curNode.l1.data)) 
		myXML.append(leaf)
	else:
		node = ET.Element("node")
		node.set("height", "{:.4f}".format(curNode.n1.height))
		myXML.append(node)
		recurseTree(curNode.n1, node, None, nodeList, k)
	if(curNode.l2 != None):
		leaf = ET.Element("leaf")
		leaf.set("height", "0")
		leaf.set("data", str(curNode.l2.data)) 
		myXML.append(leaf)
	else:
		node = ET.Element("node")
		node.set("height", "{:.4f}".format(curNode.n2.height))
		myXML.append(node)
		recurseTree(curNode.n2, node, None, nodeList, k)

#run as py clusteringAuthorship.py plainVector.csv tfidfVector.csv

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

#edited


a = np.loadtxt("plainDistMat.txt", dtype = np.float16)

for t in range(0, len(a) - 1):
	for u in range(t + 1, len(a)):
		a[t][u] = 1 - a[t][u]


listNums = list(range(len(a)))

distMatPlain = None
distMatTfidf = None

minI = -1
minJ = -1
minDist = -1
edited = {}
finTree = Tree(-1)

minI, minJ, minDist = difFast(listNums, a)

totalLen = len(a)
lol = 0
for t in range(0, totalLen - 1):
	print(lol)
	lol += 1
	bigger = max(minI, minJ)
	smaller = min(minI, minJ)
	biggerIndex = listNums[bigger]
	smallerIndex = listNums[smaller]
	del listNums[bigger]

	#used for end dendogram
	if(len(listNums) > 1):
		tempNode = Node(minDist)
		if smallerIndex in edited:
			tempNode.n1 = edited[smallerIndex]
		else:
			tempL1 = Leaf(0, tfidfVect[smallerIndex].fileName)
			tempNode.l1 = tempL1
		if biggerIndex in edited:
			tempNode.n2 = edited[biggerIndex]
		else:
			tempL2 = Leaf(0, tfidfVect[biggerIndex].fileName)
			tempNode.l2 = tempL2
		edited[smallerIndex] = tempNode
	else:
		finTree.height = minDist
		if smallerIndex in edited:
			finTree.n1 = edited[smallerIndex]
		else:
			tempL1 = Leaf(0, tfidfVect[smallerIndex].fileName)
			finTree.l1 = tempL1
		if biggerIndex in edited:
			finTree.n2 = edited[biggerIndex]
		else:
			tempL2 = Leaf(0, tfidfVect[biggerIndex].fileName)
			finTree.l2 = tempL2

	
	#dependent on distance formula
	#using complete link for this implementation
	biggerIndex = bigger
	smallerIndex = smaller
	i = 0
	while i != smallerIndex:
		curMax = max(a[i][smallerIndex], a[i][biggerIndex])
		a[i][smallerIndex] = curMax
		i += 1
	i += 1 
	while i < len(listNums):
		num1 = a[smallerIndex][i]
		num2 = -1
		if biggerIndex > i:
			num2 = a[i][biggerIndex]
		else:
			num2 = a[biggerIndex][i]
		curMax = max(num1, num2)
		a[smallerIndex][i] = curMax
		i += 1

	#remove old rows and columns from matrix
	a = np.delete(a, biggerIndex, 0)
	a = np.delete(a, biggerIndex, 1)

	#calculate new minimum distance
	if(len(listNums) > 1):
		minI, minJ, minDist = difFast(listNums, a)

nodeList = []
nodeExist = 0
root = ET.Element("tree")
root.set("height", str(finTree.height))
k = 20
if(finTree.l1 != None):
	leaf1 = ET.Element("leaf")
	leaf1.set("height", "0")
	leaf1.set("data", str(finTree.l1.data))
	root.append(leaf1)
else:
	node = ET.Element("node")
	node.set("height", "{:.4f}".format(finTree.n1.height))
	root.append(node)
	recurseTree(finTree.n1, node, None, nodeList, k)
if(finTree.l2 != None):
	leaf2 = ET.Element("leaf")
	leaf2.set("height", "0")
	leaf2.set("data", str(finTree.l2.data))
	root.append(leaf2)
else:
	node = ET.Element("node")
	node.set("height", "{:.4f}".format(finTree.n2.height))
	root.append(node)
	recurseTree(finTree.n2, node, None, nodeList, k)
answerString = ET.tostring(root, pretty_print = True).decode()
f = open("answerXML.xml", "w")
f.write(answerString)
f.close()






