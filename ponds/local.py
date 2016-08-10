# local.API for testing purposes

import os
import datetime

DEBUG = 1

class API(object):

    def __init__(self):

        # Get credentials from Environment Variables
        self.LOCAL_ACCESS_KEY = os.getenv('LOCAL_ACCESS_KEY')
        self.LOCAL_SECRET_KEY = os.getenv('LOCAL_SECRET_KEY')

        if DEBUG:
            print 'LOCAL_ACCESS_KEY:',self.LOCAL_ACCESS_KEY
            print 'LOCAL_SECRET_KEY:',self.LOCAL_SECRET_KEY


    def system_time(self):

        return datetime.datetime.utcnow()

