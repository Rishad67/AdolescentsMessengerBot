#!/usr/bin/python
import re
     
class Response(object):

    def __init__(self,db):
        self.db = db
        self.default_response = "দুঃখিত, আমি আপনার কথা বুঝতে পারছি না।"
        self.subject_mapping = {"ব্রন": "ব্রণ", "ব্রণ": "ব্রণ"}


    def get_response(self,dict):
        if 'text' in dict.keys():
            statements = self.db.get_statement(tag_names=['সাধারণ'])
            if statements:
                for statement in statements:
                    db_text = statement[2].replace('\n',"")
                    if(db_text == dict['text']):
                        return statement[1]

        if 'subject' not in dict.keys() or 'intent' not in dict.keys():
            return self.default_response
        
        #subject is problem name in bengali
        subject = dict['subject']

        if subject in self.subject_mapping.keys():
            subject = self.subject_mapping[subject]
            
        intent = dict['intent']

        if re.search("reason",intent):
            cause =  self.db.get_cause(subject)
            if isinstance(cause, str):
                q = cause
            else:
                q = "সাধারণত যে যে কারনে "+subject+" হয় -\n" + '\n'.join(cause)
            
            
        elif re.search('definition',intent):
            q = self.db.get_defination(subject)
            
        elif re.search("symptom",intent):
            ps = self.db.get_symptoms(subject)
            if isinstance(ps, str):
                q = ps
            else:
                q = subject+" হলে সাধারণত যে লক্ষনগুলো দেখা যায় -\n" + '\n'.join(ps)


        elif re.search("advice",intent):
            solution = self.db.get_solution(subject)
            if isinstance(solution, str):
                q = solution
            else:
                q = subject+" থেকে রক্ষা পাওয়ার জন্য তুমি যা করতে পার ->\n" + '\n'.join(solution)

        else:
            q = self.default_response

        return q

