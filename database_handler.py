#!/usr/bin/python
import sqlite3
from sqlite3 import Error

class databaseHandler(object):

    def __init__(self):
        self.con = self.create_connection("db.sqlite3")
        self.current_problem = None
        
    def create_connection(self,db_file):

        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
     
        return None

    def get_problem(self,problem_name):

        cur = self.con.cursor()
        cur.execute("SELECT * FROM problems where problem=?",(problem_name,))
     
        problem = cur.fetchone()
        if problem:
            return problem
        else:
            return None

    def get_cause(self,problem_name):
        problem = self.get_problem(problem_name)
        if problem:
            problem_id = problem[0]
        
            cur = self.con.cursor()
            cur.execute("SELECT cause_id FROM cause_problem where problems_id=?",(problem_id,))
            cause_ids = cur.fetchall()
            if not cause_ids:
                return problem_name+" এর কারন সম্পর্কে আমার কাছে কোন তথ্য নাই ।"
            cause = []
            for cause_id in cause_ids :
                cur.execute("SELECT cause FROM cause where id=?",(cause_id[0],))
                cause.append( cur.fetchone()[0] )
            
            return cause
        else:
            return problem_name+" সম্পর্কে আমার কাছে কোন তথ্য নাই ।"
            

    def get_solution(self,problem_name):
        problem = self.get_problem(problem_name)
        if problem:
            problem_id = problem[0]
            cur = self.con.cursor()
            cur.execute("SELECT solution_id FROM solution_problem where problems_id=?",(problem_id,))
            solution_ids = cur.fetchall()
            if not solution_ids:
                return problem_name+" বিষয়ে পরামর্শ দেওয়ার মত আমার কাছে পর্যাপ্ত তথ্য নাই ।"
            solution = []
            for solution_id in solution_ids:
                cur.execute("SELECT solution FROM solution where id=?",(solution_id[0],))
                solution.append( cur.fetchone()[0] )

            return solution
        else:
            return problem_name+" সম্পর্কে আমার কাছে কোন তথ্য নাই ।"
    

    def get_defination(self,problem_name):
        problem = self.get_problem(problem_name)
        if problem:
            return problem[3]
        else:
            return problem_name+" সম্পর্কে আমার কাছে কোন তথ্য নাই ।"


    def get_symptoms(self,problem_name):
        problem = self.get_problem(problem_name)
        if problem:
            problem_id = problem[0]
            cur = self.con.cursor()
            cur.execute("SELECT symptom_id FROM problem_symptoms where problem_id=?",(problem_id,))
            symptom_ids = cur.fetchall()
            if not symptom_ids:
                return problem_name+" এর লক্ষণগুলো আমার এখনও জানা নাই ।"
            symptoms = []
            for symptom_id in symptom_ids:
                cur.execute("SELECT symptom FROM symptoms where id=?",(symptom_id[0],))
                symptoms.append( cur.fetchone()[0] )

            return symptoms
        else:
            return problem_name + " সম্পর্কে আমার কাছে কোন তথ্য নাই ।"

        
    def get_tag_ids(self,tag_names):
        cur = self.con.cursor()
        query = "SELECT id FROM tag where tag in "+str(tuple(tag_names))
        query = query.replace(",)",")")
        cur.execute( query )
     
        tag_ids = cur.fetchall()
        if tag_ids:
            return [t[0] for t in tag_ids]
        else:
            return None
        
    def get_statement(self,**kwargs):
        cur = self.con.cursor()
        if 'tag_names' in kwargs.keys():
            tag_ids = self.get_tag_ids(kwargs['tag_names'])
            query = "SELECT statement_id FROM statement_tags where tag_id in " + str(tuple(tag_ids))
            query = query.replace(",)",")")
            cur.execute( query )
     
            statement_ids = cur.fetchall()
            if statement_ids:
                statement_ids = [s[0] for s in statement_ids]
                query = "SELECT code,response,text FROM statement where id in " + str(tuple(statement_ids)) 
                query = query.replace(",)",")")
                cur.execute( query )
                statements = cur.fetchall()
                return statements
        else:
            cur.execute("SELECT code,response,text FROM statement")
            statements = cur.fetchall()
            return statements

    def get_synonyme(self,word):
        cur = self.con.cursor()
        cur.execute("SELECT synonym_id FROM vocabulary where word = ?",(word,))
        synonyme_id = cur.fetchone()
        if synonyme_id is None:
            return word
        if synonyme_id[0] is None:
            return word
        cur.execute("SELECT word FROM vocabulary where id = ?",(synonyme_id[0],))
        synonyme = cur.fetchone()[0]
        return synonyme

