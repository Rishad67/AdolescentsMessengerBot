#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from stemmer import MapBasedStemmer as Stemmer



class PreProcessor(object):

    def __init__(self,db):
        self.stopwords = self.get_stopwords()
        self.db = db
        self.stemmer = Stemmer()

    def removeCommonPrefix(self,word):
        prefix = ['(?P<id>.+)জাতীয়$', '(?P<id>.+)জনক$', '(?P<id>.+)গুলো$', '(?P<id>.+)গুলা$', '(?P<id>.+)সমূহ$',
                  '(?P<id>.+)গুলোকে$', '(?P<id>.+)গুলাকে$', '(?P<id>.+)সমূহকে$', '(?P<id>.+)গুলোর$', '(?P<id>.+)গুলার$',
                  '(?P<id>.+)সমূহের$']

        for r in prefix:
            if re.search(r, word):
                word = re.sub(r, "\g<id>", word)

        return word

    def checkWord(self,word):
        replace = [['ড়', 'ড়'], ['ঢ়', 'ঢ়'], ['ব়', 'র'], ['য়', 'য়'], ['ঁ', ''], ['ঃ', ''], ['ণ', 'ন'], ['ূ', 'ু'],
                   ['(?P<id>.)ো', '\g<id>ো']]
        for r in replace:
            if re.search(r[0], word):
                word = re.sub(r[0], r[1], word)
        return word

    def get_stopwords(self):
        with open('Process/stopwords.txt','r',encoding='utf-8') as f:
            stopwords = set(f.read().replace('\ufeff','').split('\n'))
        return stopwords



    def split_text(self,text):
        #split the text to word_list
        # Remove consecutive spaces,linebreaks and tabs
        word_list = re.sub(r"[.?;!।,\s'\"]+"," ",text).split()
        return word_list

    def synonym_map(self,word_list):
        for i in range(len(word_list)):
            word_list[i] = self.db.get_synonyme(word_list[i])
        return word_list

    def get_keywords(self,word_list):
        # remove stopwords and stem all the words in the word_list
        new_word_list = [ self.stemmer.stem(self.checkWord(self.removeCommonPrefix(word))) for word in word_list if word not in self.stopwords]
        if len(new_word_list) != 0:
            word_list = new_word_list
        return word_list


    def process_response(self,user_text):

        word_list = self.split_text(user_text)
        word_list = self.get_keywords(word_list)
        word_list = self.synonym_map(word_list)

        return word_list
