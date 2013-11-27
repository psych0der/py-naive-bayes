'''
Naive bayes classifier written in python 
'''
from __future__ import division
import math,sys
import operator
from preprocess.preprocessor import preprocess
import json



class NaiveBayesClassifier(object):
	def __init__(self,filename=None):
		
		try:
			with open('training_data.json') as fl:
				self.training_data = json.load(fl)
		except IOError:
   			self.training_data = {} # dictionary to store all information related to training data
			self.training_data['labels'] = {}
			self.training_data['total_data_set'] = 0

		if filename is not None:
			try:
				with open(filename) as fl:
					lines = fl.readlines()
				
					for index,data in enumerate(lines):
						lines[index] = data.replace("\n","").split('##')

					for line in lines:
						self.train(line[0],line[1])
			
			except IOError:
   				print 'unable to open the file '+filename



		
	def train(self,text,label):
		data = preprocess(text)
		self.training_data['total_data_set']+=1
		
		if label in self.training_data['labels']:
			self.training_data['labels'][label]['docs']+=1
			
		else :
			self.training_data['labels'][label] = {}
			self.training_data['labels'][label]['docs'] = 1
			self.training_data['labels'][label]['keywords'] = {}
			self.training_data['labels'][label]['total_keywords'] = 0
			

		for word in data :
			self.training_data['labels'][label]['total_keywords']+=1
			if word in self.training_data['labels'][label]:
				self.training_data['labels'][label]['keywords'][word]+=1				
			else:
				self.training_data['labels'][label]['keywords'][word]=1

		self.save()



	def classify(self,text):
		
		if self.training_data['total_data_set'] ==0:
			print 'Training data empty: Please train the system before executing classify'
			sys.exit(0)

		data = preprocess(text)
		label_weights = {}
		for label in self.training_data['labels']:

			prior = math.log10(1+(self.training_data['labels'][label]['docs'])/(self.training_data['total_data_set']))
			term_weight = 0
			for word in data:
				if word in self.training_data['labels'][label]['keywords']:
					n = self.training_data['labels'][label]['keywords'][word]
				else :
					n = 0
				
				term_weight+= math.log10((n+1)/(self.training_data['labels'][label]['docs']+ len(data)))

			label_weights[label] = prior + term_weight

		
		return max(label_weights.iteritems(), key=operator.itemgetter(1))[0]

	def save(self):
		with open('training_data.json',"w") as fl:
			json.dump(self.training_data,fl)


clss = NaiveBayesClassifier()#
'''clss.train('AAP releases manifestos for 28 Assembly constituencies','politics')
clss.train('FIRs filed against UP sugar mill owners','law')
clss.train('BJP will win in four states due to anti-Congress wave: Arun Jaitley','politics')
clss.train('AAP trashes BJP charge of playing religious card','politics')'''
print clss.classify('BJP has become a party by Modi, for Modi, of Modi: Congress')



