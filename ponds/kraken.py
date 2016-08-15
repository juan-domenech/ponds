# kraken.com
# https://www.kraken.com/help/api

import os
import datetime
import sys
import urllib2
import ast

DEBUG = 1

class API(object):

    def __init__(self):

        # Get credentials from Environment Variables
        self.KRAKEN_ACCESS_KEY = os.getenv('KRAKEN_ACCESS_KEY')
        self.KRAKEN_SECRET_KEY = os.getenv('KRAKEN_SECRET_KEY')

        if self.KRAKEN_ACCESS_KEY == None:
            print "ERROR Environment variable KRAKEN_ACCESS_KEY not found. Please make sure this variable is loaded in memory."
            sys.exit(1)
        if self.KRAKEN_SECRET_KEY == None:
            print "ERROR Environment variable KRAKEN_SECRET_KEY not found. Please make sure this variable is loaded in memory."
            sys.exit(1)

        if DEBUG:
            print 'LOCAL_ACCESS_KEY:',self.KRAKEN_ACCESS_KEY
            print 'LOCAL_SECRET_KEY:',self.KRAKEN_SECRET_KEY

        self.root_url = 'https://api.kraken.com/0'



    def system_time(self):
        return datetime.datetime.utcnow()


    # Epoch (seconds)
    def system_time_epoch(self):
        # https://www.kraken.com/help/api#get-server-time

        response = ast.literal_eval(urllib2.urlopen(self.root_url+'/public/Time').read())
        if response['error']:
            print "ERROR system_time_epoch():",response
            sys.exit(1)
        else:
            # {'result': {'unixtime': 1471293119, 'rfc1123': 'Mon, 15 Aug 16 20:31:59 +0000'}, 'error': []}
            return int(response['result']['unixtime'])





