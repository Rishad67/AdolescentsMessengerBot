#!/usr/bin/python
from database_handler import databaseHandler
from get_response import Response

class ChatBot(object):

    def __init__(self):
        self.db = databaseHandler()
        self.responder = Response(self.db)

    def get_response(self,dict):
        return self.responder.get_response(dict)


#sample
    
'''bot = ChatBot()
#r = bot.get_response({'intent':'reason'})
#r = bot.get_response({'subject':'যৌনরোগ','intent':'reason'})
#r = bot.get_response({'subject':'ব্রণ','intent':'reason'})
#r = bot.get_response({'subject':'মাসিক','intent':'advice'})
#r = bot.get_response({'subject':'ক্ষুধাহীনতা','intent':'symptom'})
#r = bot.get_response({'subject':'গনরিয়া','intent':'definition'})
#r = bot.get_response({'subject':'গনরিয়া','intent':'defination','text':'তোমার এখন কি অবস্থা ?'})
r = bot.get_response({'subject':'গনরিয়া','intent':'defination','text':'আপনার কাজ কী?'})
print(r)'''
