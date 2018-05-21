#textVectoriuzer.py

import pandas as pd
import sys
import os
from collections import Counter



def main():
	
	root_dir = sys.argv[1]

	test = [dI for dI in os.listdir(root_dir + "/C50test") if os.path.isdir(os.path.join(root_dir+"/C50test",dI))]
	train = [dI for dI in os.listdir(root_dir + "/C50test") if os.path.isdir(os.path.join(root_dir+"/C50train",dI))]

	documents = []
	labels = []
	print("Reading test data...")
	for name in test:
		dir_name = root_dir + "/C50test/" + name
		files = os.listdir(dir_name)

		for file in files:
			file_name = dir_name + "/" + file
			with open(file_name, 'r') as myfile:
				document = myfile.read().replace('\n', '')
				documents.append(document.lower().replace("[^A-Za-z\s]", "").split()) 
				labels.append(name)

	print("Reading train data...")
	for name in train:

		dir_name = root_dir + "/C50train/" + name
		files = os.listdir(dir_name)

		for file in files:
			file_name = dir_name + "/" + file
			with open(file_name, 'r') as myfile:
				document = myfile.read().replace('\n', '')
				documents.append(document) 
				labels.append(name)

	
	texts = pd.DataFrame({"text":documents, "label":labels},index = range(len(documents)))

	bag_of_words = texts.loc[:,"text"].apply(Counter)

	print(bag_of_words.head())
	
	




if __name__ == "__main__":
	main()