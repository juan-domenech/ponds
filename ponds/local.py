# local.API for testing purposes

import os
import datetime
import sys

DEBUG = 1

class API(object):

    def __init__(self):

        # Get credentials from Environment Variables
        self.LOCAL_ACCESS_KEY = os.getenv('LOCAL_ACCESS_KEY')
        self.LOCAL_SECRET_KEY = os.getenv('LOCAL_SECRET_KEY')

        if self.LOCAL_ACCESS_KEY == None:
            print "ERROR Environment variable LOCAL_ACCESS_KEY not found. Please make sure this variable is loaded in memory."
            sys.exit(1)
        if self.LOCAL_SECRET_KEY == None:
            print "ERROR Environment variable LOCAL_SECRET_KEY not found. Please make sure this variable is loaded in memory."
            sys.exit(1)

        if DEBUG:
            print 'LOCAL_ACCESS_KEY:',self.LOCAL_ACCESS_KEY
            print 'LOCAL_SECRET_KEY:',self.LOCAL_SECRET_KEY


    def system_time(self):
        return datetime.datetime.utcnow()


    # Epoch (seconds)
    def system_time_epoch(self):
        return int(datetime.datetime.utcnow().strftime('%s%f')[:-6])