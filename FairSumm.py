'''
Code of FairSumm fair text summarization algorithm
By: adash
'''
from nltk.stem.porter import *
import sys
reload(sys)
sys.setdefaultencoding("latin-1")
import re,os
import math
import string
from collections import defaultdict
from copy import deepcopy
import subprocess
import pandas as pd
import argparse
import zipfile


def parse_args():
	'''
	Parses the FairSumm arguments.
	'''
	parser = argparse.ArgumentParser(description="Run FairSumm.")
	parser.add_argument('--file', nargs='?', default='Claritin.txt', help= 'Enter the file name containing the input file name, fairness notion and the length of the summary. a) Claritin.txt or b) US-Election.txt or c) METOO.txt. Default is Claritin.txt')
	parser.add_argument('--evaluation', nargs = '?', type=int, default = 0, help='If 1, the code evaluates ROUGE scores for the generated summary. If 0, it does not evaluate the ROUGE scores. Default value is 0.')
	return parser.parse_args()

	
args = parse_args()
Threshold = {}
print(args)
if args.evaluation not in {0, 1}:
	print('Please enter either 0 or 1 for evaluation')
	exit(0)
	
print(type(args.evaluation))
#exit(0)
inputfile = open('./'+args.file, 'r').readlines()
inpt = inputfile[0].split('<||>')[1].strip()
length = int(inputfile[1].split('<||>')[1].strip())
num_class = int(inputfile[2].split('<||>')[1].strip())
for i in range(3, 3+num_class):
	content = inputfile[i].split('<||>')
	Threshold[content[0]] = int(content[1].strip())

if length != sum(list(Threshold.values())):
	print('Set the thresholds such that sum of tweets of each classes will add up to the length of the desired summary.')
	exit(0)
st = PorterStemmer()

if not os.path.exists("./Dataset/"+inpt):
	print('Enter the dataset name properly. You can check it by executing python FairSumm.py --help on your terminal')
	exit(0)


zf = zipfile.ZipFile('./Dataset/'+inpt+'/cosinescores.zip') 
A = pd.read_csv(zf.open('cosinescores.csv'))
#A = pd.read_csv('./Dataset/'+inpt+'/cosinescores.csv')
corpus_sim = list(A.iloc[:, 1:].sum(axis = 1))
print(sum(corpus_sim))

pattern=re.compile(r'[\d+\.]*[\d]+|[^\w]+') #pattern to detect numbers (real/integer) non alphanumeric (no underscore)

Summary = []
lamda = 0.5
inf = 21
#stopword dictionary from "stopwords.txt" file

stopWordDict = defaultdict(int)
stopWordFile = open("./Dataset/stopwords.txt","r")
for line in stopWordFile:
	stopWordDict[line.strip()]=1

sensitive_info = {}
Tweets = []
Tweetids = {}
with open('./Dataset/'+inpt+'/input.txt', 'r') as file:
	for line in file.readlines():
		sensitive_info[line.split('<||>')[2].strip()] = line.split('<||>')[1]
		Tweets.append(line.split('<||>')[2].strip())
		Tweetids[line.split('<||>')[2].strip()] = line.split('<||>')[0]

def extractDocumentCorpus():
	document_to_sentence_corpus = {}
	Filename = './Temp/temptext.txt'
	with open(Filename,'w') as file:
		for tweet in Tweets:
			file.write(tweet+'\n')
	print('Writing done')
	fileptr = open(Filename,'r')
	fileText = fileptr.read()
	fileptr.close()
	document_to_sentence_corpus['source'] = fileText
	return document_to_sentence_corpus

def generateClusterInputFile(corpus):
	ClusterInputFile = "./Temp/SentencesToCluster.txt"
	ClusterInputFile_ptr = open(ClusterInputFile,'w')
	for each_doc in corpus:
		current_doc = corpus[each_doc]
		sentences = []
		sentences = current_doc.split('\n')
		print each_doc
		for each_sentence in sentences:
			if len(each_sentence)>1:
				if each_sentence[0]==' ':
					each_sentence = each_sentence[1:]
				ClusterInputFile_ptr.write(each_sentence+'\n')

	ClusterInputFile_ptr.close()

def convertFiletoMatFormat():
	os.system("perl doc2mat/doc2mat -mystoplist=./Dataset/stopwords.txt -nlskip=1 -skipnumeric ./Temp/SentencesToCluster.txt ./Temp/ClutoInput.mat")

def clusterSentences():
	line_count = 0
	ClusterFile = open("./Temp/SentencesToCluster.txt",'r')
	for line in ClusterFile.readlines():
		line_count+=1
	print line_count	
	os.system("./cluto/Linux-x86_64/vcluster -clmethod=bagglo -sim=cos -niter=100 -seed=45 ./Temp/ClutoInput.mat "+str(line_count/10))
	return line_count/10
	
def mapSentencetoCluster(noOfClusters):
	sentenceFile = open("./Temp/SentencesToCluster.txt",'r')
	sentences = sentenceFile.readlines()
	sentenceFile.close()

	for idx in range(len(sentences)):
	    sentences[idx] = sentences[idx].split('\n')[0]

	# Creating cluster number index.

	clusterFile = open("./Temp/ClutoInput.mat.clustering."+str(noOfClusters),'r')
	clusterIndex = clusterFile.readlines()
	clusterFile.close()

	for idx in range(len(clusterIndex)):
	    clusterIndex[idx] = clusterIndex[idx].split('\n')[0]

	

	clusterSentenceIndex = []
	for idx in range(len(clusterIndex)):
	    temp = []
	    temp.append(clusterIndex[idx])
	    temp.append(sentences[idx])

	    clusterSentenceIndex.append(temp)

	clusterSentenceIndex.sort()

	# Printing the sentences into the file.
	outputIndexFile= open('./Temp/sentence-cluster-sorted-index.txt','w')
	for idx in range(len(clusterSentenceIndex)):
		if int(clusterSentenceIndex[idx][0]) >= 0:			# Handles Unneccesary empty sentences
			line = clusterSentenceIndex[idx][1]+'<||>'+clusterSentenceIndex[idx][0]+'\n'
			outputIndexFile.write(line)
	outputIndexFile.close()

def consolidateClusters():
	clusterSentencesFile = open('./Temp/sentence-cluster-sorted-index.txt','r')
	cluster_to_sentences_dict = defaultdict(list)
	for line in clusterSentencesFile.readlines():
		lin,cluster = line.split('<||>')
		cluster = cluster.replace('\n','')
		if cluster in cluster_to_sentences_dict:
			cluster_to_sentences_dict[cluster].append(lin)
		else:
			cluster_to_sentences_dict[cluster] = [lin]
	return cluster_to_sentences_dict				


def calculateSimilarityWithSummary(summary):
	Summary_similarity = 0
	for i in summary:
		if len(i)>1:
			Summary_similarity += corpus_sim[Tweets.index(i)]

	return Summary_similarity


def getTotalSenteces():
	fp = open('Temp/sentence-cluster-sorted-index.txt','r')
	text = fp.readlines()
	return len(text)

def getDiversity(total_sentences, summary, cluster_to_sentences_dict):
	#global cluster_to_sentences_dict
	diversity_measure = 0
	for cluster in cluster_to_sentences_dict:
		current_cluster = cluster_to_sentences_dict[cluster]
		intersection_set = set(summary).intersection(set(current_cluster))
		cluster_diversity = 0
		for sentence in intersection_set:
			cluster_diversity += corpus_sim[Tweets.index(sentence)]/total_sentences

		diversity_measure += math.sqrt(cluster_diversity)
	return diversity_measure		

def fair_stats(summary):
	Final_Stat = {}
	Classes = {}
	for val in sensitive_info.values():
		if val not in Classes.keys():
			Classes[val] = 1
		else:
			Classes[val] += 1
	for key in Classes:
		Final_Stat[key] = 0		
	for sentence in summary:
		if sentence not in sensitive_info.keys():
			return False
		else:
			Final_Stat[sensitive_info[sentence]] += 1		
			
	print(Final_Stat)

# This is the segment where the current summary belongs to the matroid or not is checked (Fairness constraint)

def fairness(summary, Threshold, k):
	Classes = {}
	Current = {}
	TruthValue = True
	for val in sensitive_info.values():
		if val not in Classes.keys():
			Classes[val] = 1
		else:
			Classes[val] += 1
	
	for key in Classes:
		Current[key] = 0

	#print(Current)
	for sentence in summary:
		if sentence not in sensitive_info.keys():
			return False
		else:
			Current[sensitive_info[sentence]] += 1
	for key in Classes.keys():
		TruthValue = TruthValue and (Current[key] <= Threshold[key])
	return TruthValue

	
def extractSummary(cluster_to_sentences_dict):
	global lamda
	global Summary
	global inf
	total_sentences = getTotalSenteces()

	current_sentence = ""
	current_score = 0
	max_sentence = ""
	max_score = 0
	covereage = 0
	max_cluster=-1
	check_cluster=-1
	curent_cov=-1
	current_div=-1
	max_cov=-1
	max_div=-1
	max_sumsin=-1
	max_corsim =-1
	d = max (corpus_sim)
	delta = 100
	L = (delta * d )/len(corpus_sim)
	#Greedy implementation of sub-modular optimization of Algorithm 1.
	for cluster in cluster_to_sentences_dict:
		current_cluster = cluster_to_sentences_dict[cluster]
		for each_sentence in current_cluster :
			if (each_sentence not in Summary):

				############################## Compute covereage ##############################
				current_summary = deepcopy(Summary)
				min_increase = d/(1+delta**(len(current_summary)+1))
				if min_increase <= L:
					min_increase = 0
				current_summary.append(each_sentence)
				if fairness(current_summary, Threshold, 50 ):

					covereage = min(calculateSimilarityWithSummary(current_summary), (0.1/total_sentences) * sum(corpus_sim))

					############################### Compute Diversity #############################

					diversity = getDiversity(total_sentences,current_summary, cluster_to_sentences_dict)

					############################### Greedily Check ################################

					current_score = (lamda*covereage) + (lamda*diversity)
					current_sentence = each_sentence
					check_cluster =cluster
					if current_score - max_score >= min_increase:
						max_score = current_score
						max_sentence= current_sentence
						max_cluster=check_cluster
						max_cov=covereage
						max_div=diversity

	Summary.append(max_sentence)
	print(len(Summary))
#

def main():
 
	if not os.path.exists("./Temp"):
		os.makedirs("./Temp")
	# cluster the input sentences for diversity evaluations	
	document_to_sentence_corpus = extractDocumentCorpus()
	generateClusterInputFile(document_to_sentence_corpus)
	convertFiletoMatFormat()
	noOfClusters = clusterSentences()
	print "No of clusters " 
	print noOfClusters
	mapSentencetoCluster(noOfClusters)
	cluster_to_sentences_dict = consolidateClusters()
	
	# Start summarizing procedure
	print('Starting to create the summary')
	for i in xrange(length):
		extractSummary(cluster_to_sentences_dict)
	
	#Store the summary output		
	if not os.path.exists("./Summaries"):
		os.makedirs("./Summaries")
	filename = "./Summaries/"+inpt+".txt"
	outfile = open(filename,'w')
			
	print Summary
	for i in Summary:
		outfile.write(i+'\n')
	outfile.close()
	
	#Show the fairness statistics of the summary
	fair_stats(Summary)
	
	#Rouge evaluation
	if args.evaluation==1:
		output = subprocess.check_output("java -cp C_Rouge/C_ROUGE.jar executiverouge.C_ROUGE "+ filename +" ./Dataset/"+inpt+"/Test_Summaries"+"/ 1 B R",shell=True)
		output = float(output)
		output1 = subprocess.check_output("java -cp C_Rouge/C_ROUGE.jar executiverouge.C_ROUGE "+ filename +" ./Dataset/"+inpt+"/Test_Summaries"+"/ 1 B F",shell=True)
		output1 = float(output1)
		output2 = subprocess.check_output("java -cp C_Rouge/C_ROUGE.jar executiverouge.C_ROUGE "+ filename +" ./Dataset/"+inpt+"/Test_Summaries"+"/ 2 B R",shell=True)
		output2 = float(output2)
		output3 = subprocess.check_output("java -cp C_Rouge/C_ROUGE.jar executiverouge.C_ROUGE "+ filename +" ./Dataset/"+inpt+"/Test_Summaries"+"/ 2 B F",shell=True)
		output3 = float(output3)
		main_output_file = open("Final_Output.txt",'a')
		main_output_file.write(inpt+'_'+"\t"+str(output)+"\t"+str(output1)+"\t"+str(output2)+"\t"+str(output3)+"\n")
		print "\t"+str(output)+"\t"+str(output1)
		main_output_file.close()

if __name__ == '__main__':	
	main()
