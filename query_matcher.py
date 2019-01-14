#!/usr/bin/python
from difflib import SequenceMatcher
from processing import PreProcessor


class QueryMatcher(object):

    def __init__(self,db):
        self.db = db
        self.preProcess = PreProcessor(self.db)

    def compare(self,word1, word2):
        # Return 0 if either statement has a falsy text value
        if not word1 or not word2:
            return 0
        similarity_percent = round(SequenceMatcher(None, word1, word2).ratio(), 2)
        return similarity_percent

    def match_text(self,text1, text2):
        matched = 0
        for word in text1:
            similarity = 0
            index = 0
            for j in range(len(text2)):
                s = self.compare(word, text2[j])
                if s > similarity:
                    similarity = s
                    index = j
            if similarity > 0.8:
                matched += similarity
                del text2[index]

        return 2 * matched / (len(text1) + len(text2) + matched)

    def get_response(self,**kwargs):
        if "text" not in kwargs.keys():
            return None

        word_list = self.preProcess.process_response(kwargs['text'])
        if 'tags' in kwargs.keys():
            tags = kwargs['tags']
        else:
            tags = ['সাধারণ']
        statement_list = self.db.get_statement(tags=tags)

        if not statement_list:
            log.writeInfo("Memory is Empty ...", name="Response.py")

        closest_match = {'text': None, 'confidence': 0}

        text_matched = ""
        # Find the closest matching known statement
        for statement in statement_list:
            s = statement[0].split("*")
            confidence = self.match_text(word_list, s.copy())

            if confidence > closest_match['confidence']:
                closest_match['confidence'] = confidence
                closest_match['text'] = statement[1]
                text_matched = s
                if closest_match['confidence'] > 0.9:
                    break

        if closest_match['confidence'] > 0.5:
            return closest_match['text']
        else:
            return None  
