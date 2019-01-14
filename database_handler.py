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

    def get_problem(self,problem):

        cur = self.con.cursor()
        cur.execute("SELECT * FROM problems where problem=?",(problem,))
     
        problem_ = cur.fetchone()
        if problem_:
            return problem_
        else:
            return None

    def get_cause(self,problem):
        key = self.get_problem(problem)
        if key:
            k = key[0]
        
            cur = self.con.cursor()
            cur.execute("SELECT cause_id FROM cause_problem where problems_id=?",(k,))
            cause_id = cur.fetchall()
            if not cause_id:
                return problem+" এর কারন সম্পর্কে আমার কাছে কোন তথ্য নাই ।"
            cause = []
            for c in cause_id :
                cur.execute("SELECT cause FROM cause where id=?",(c[0],))
                cause.append( cur.fetchone()[0] )
            
            return cause
        else:
            return problem+" সম্পর্কে আমার কাছে কোন তথ্য নাই ।"
            

    def get_solution(self,problem):
        key = self.get_problem(problem)
        if key:
            k = key[0]
            cur = self.con.cursor()
            cur.execute("SELECT solution_id FROM solution_problem where problems_id=?",(k,))
            solution_id = cur.fetchall()
            if not solution_id:
                return problem+" বিষয়ে পরামর্শ দেওয়ার মত আমার কাছে পর্যাপ্ত তথ্য নাই ।"
            solution = []
            for s in solution_id:
                cur.execute("SELECT solution FROM solution where id=?",(s[0],))
                solution.append( cur.fetchone()[0] )

            return solution
        else:
            return problem+" সম্পর্কে আমার কাছে কোন তথ্য নাই ।"
    

    def get_defination(self,problem):
        problem_ = self.get_problem(problem)
        if problem_:
            return problem_[3]
        else:
            return problem+" সম্পর্কে আমার কাছে কোন তথ্য নাই ।"


    def get_symptoms(self,problem):
        key = self.get_problem(problem)
        if key:
            k = key[0]
            cur = self.con.cursor()
            cur.execute("SELECT symptom_id FROM problem_symptoms where problem_id=?",(k,))
            symptom_id = cur.fetchall()
            if not symptom_id:
                return problem+" এর লক্ষণগুলো আমার এখনও জানা নাই ।"
            symptoms = []
            for s in symptom_id:
                cur.execute("SELECT symptom FROM symptoms where id=?",(s[0],))
                symptoms.append( cur.fetchone()[0] )

            return symptoms
        else:
            return problem+" সম্পর্কে আমার কাছে কোন তথ্য নাই ।"
    def get_tag_id(self,tags):
        cur = self.con.cursor()
        query = "SELECT id FROM tag where tag in "+str(tuple(tags))
        query = query.replace(",)",")")
        cur.execute( query )
     
        tag_id = cur.fetchall()
        if tag_id:
            return [t[0] for t in tag_id]
        else:
            return None
        
    def get_statement(self,**kwargs):
        cur = self.con.cursor()
        if 'tags' in kwargs.keys():
            tag_id = self.get_tag_id(kwargs['tags'])
            query = "SELECT statement_id FROM statement_tags where tag_id in " + str(tuple(tag_id))
            query = query.replace(",)",")")
            cur.execute( query )
     
            rows = cur.fetchall()
            if rows:
                statement_id = [r[0] for r in rows]
                query = "SELECT code,response FROM statement where id in " + str(tuple(statement_id)) 
                query = query.replace(",)",")")
                cur.execute( query )
                rows = cur.fetchall()
                return rows
        else:
            cur.execute("SELECT code,response FROM statement")
            rows = cur.fetchall()
            return rows

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
