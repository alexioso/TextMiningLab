#textVectoriuzer.py

import pandas as pd
import sys
import os
from collections import Counter
import porter as pstem
import re
import copy
import math

#use py textVectorizer.py root [TRUE (this is for porter)] [stopwords (or NULL)]

def main():
	#stores count of each words appearing in a file at least once
	#does not double count word appearance in a signle file
	
	ps = pstem.PorterStemmer()

	fileG = open("groundtruth.csv", "w")
	porter = False
	stopWord = None
	root_dir = sys.argv[1]
	if(sys.argv[2] == "TRUE"):
		porter = True
	if(sys.argv[3] != "NULL"):
		stopWord = sys.argv[3]

	if(stopWord != None):
		fileH = open(stopWord, "r")
		stopWord = []
		line = fileH.readlines()
		stopWord = [lines.rstrip('\n') for lines in line]
		fileH.close()

	test = [dI for dI in os.listdir(root_dir + "/C50test") if os.path.isdir(os.path.join(root_dir+"/C50test",dI))]
	train = [dI for dI in os.listdir(root_dir + "/C50test") if os.path.isdir(os.path.join(root_dir+"/C50train",dI))]

	totalDict = {}
	allVectors = []
	print("Reading test data...")
	for name in test:
		dir_name = root_dir + "/C50test/" + name
		files = os.listdir(dir_name)
		for file in files:
			fileG.write(file +","+name+"\n")
			file_name = dir_name + "/" + file
			with open(file_name, 'r') as myfile:
				document = myfile.read().replace('\n', ' ')
				document = document.replace('.', ' ').replace(",", " ").replace("\"", "").replace("-", " ")
				document = document.replace("-", "").replace("(", "").replace(")", "").replace("$", "")
				document = document.replace("?", "").replace("!", "").replace("#", "").replace("/", " ")
				document = re.sub('\d', '', document)
				document = document.lower().split()
				hitWords = []
				thisDict = {}
				for word in document:
					if(stopWord != None and word in stopWord):
						continue
					word = word.replace("'", "")
					if(word == ""):
						continue
					if(porter == True):
						word = ps.stem(word, 0, len(word) - 1)
					if(word not in hitWords):
						if word in totalDict:
							totalDict[word] += 1
						else:
							totalDict[word] = 1
						hitWords.append(word)
					if word not in thisDict:
						thisDict[word] = 1
					else:
						thisDict[word] += 1
				temp = Vector(file, name)
				temp.vector = thisDict
				allVectors.append(temp)

	print("Reading train data...")
	for name in train:
		dir_name = root_dir + "/C50train/" + name
		files = os.listdir(dir_name)
		for file in files:
			fileG.write(file +","+name+"\n")
			file_name = dir_name + "/" + file
			with open(file_name, 'r') as myfile:
				document = myfile.read().replace('\n', ' ')
				document = document.replace('.', ' ').replace(",", " ").replace("\"", "").replace("-", " ")
				document = document.replace("-", "").replace("(", "").replace(")", "").replace("$", "")
				document = document.replace("?", "").replace("!", "").replace("#", "").replace("/", " ")
				document = re.sub('\d', '', document)
				document = document.lower().split()
				hitWords = []
				thisDict = {}
				for word in document:
					if(stopWord != None and word in stopWord):
						continue
					word = word.replace("'", "")
					if(word == ""):
						continue
					if(porter == True):
						word = ps.stem(word, 0, len(word) - 1)
					if(word not in hitWords):
						if word in totalDict:
							totalDict[word] += 1
						else:
							totalDict[word] = 1
						hitWords.append(word)
					if word not in thisDict:
						thisDict[word] = 1
					else:
						thisDict[word] += 1
				temp = Vector(file, name)
				temp.vector = thisDict
				allVectors.append(temp)

	print(len(allVectors))
	fileNoNorm = open("plainVector.csv", "w")
	for vect in allVectors:
		fileNoNorm.write(vect.authorName+","+vect.fileName+",")
		vectDict = vect.vector
		for elem in vectDict:
			fileNoNorm.write(elem+" "+str(vectDict[elem])+",")
		fileNoNorm.write("\n")
	fileNoNorm.close()

	tfidfVect = copy.deepcopy(allVectors)
	for thing in tfidfVect:
		curDict = thing.vector
		maximum = max(curDict.values())
		for k in curDict:
			curDict[k] /= maximum
			curDict[k] = curDict[k] * math.log(5000/totalDict[k], 2)

	fileNoNorm = open("tfidfVector.csv", "w")
	for vect in tfidfVect:
		fileNoNorm.write(vect.authorName+","+vect.fileName+",")
		vectDict = vect.vector
		for elem in vectDict:
			fileNoNorm.write(elem+" "+str(vectDict[elem])+",")
		fileNoNorm.write("\n")
	fileNoNorm.close()

	fileG.close()
	
	
class Vector:
	def __init__(self, fileName, authorName):
		self.fileName = fileName
		self.authorName = authorName
	vector = None



if __name__ == "__main__":
	main()