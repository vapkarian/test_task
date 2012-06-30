from django.db import connection
import os.path
import datetime

class QueriesGetter(object):
    def __init__(self):
        MIDDLEWARE_PATH = os.path.abspath(os.path.dirname(__file__))
        now = str(datetime.datetime.now()).replace(':','-')
        self.filename = os.path.join(MIDDLEWARE_PATH,'logs','session '+now+\
                                     '.log').replace('\\','/')
    def process_response(self,request,response):
        queries = connection.queries
        with open(self.filename,'w') as log:
            for q in queries:
                log.writelines(q['sql']+'\n'+'\n')
        return response
