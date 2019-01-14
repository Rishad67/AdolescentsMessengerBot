#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class RuleBasedStemmer(object):

	rule = []

	def __init__(self):

		with open('Process/stemmingRule.txt','r',encoding='utf-8') as f:
			lines = f.readlines()
			i=0
			while i<len(lines):
				if '{' in lines[i]:
					i = i+1
					r=[]
					while '}' not in lines[i]:
						
						line = re.sub(r' |#.*',"",lines[i]).strip()
						i = i+1
						if len(line)<1:
							continue
						line = line.split("->")
						if len(line)<2:
							line.append("")
						r.append(line)
						
					self.rule.append(r)
				else:
					i = i+1


	def stem(self,word):
		for r in self.rule:
			for element in r:
				matcher = element[0]+"$"
				if re.search(matcher,word):
					word = re.sub(matcher,element[1],word)
					break

		return word


class MapBasedStemmer(object):
	dict = {}

	def __init__(self):

		with open('Process/stemmingMap.txt', 'r', encoding='utf-8') as f:
			lines = f.readlines()
			for line in lines:
				line = line.replace("\n","")
				line = line.split("<-")
				self.dict[line[1].strip()] = line[0]


	def stem(self, word):
		word = word.strip()
		if word in self.dict.keys():
			return self.dict[word]

		return word
