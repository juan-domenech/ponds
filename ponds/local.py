# local.API for testing purposes

import os
import datetime
import sys

class API(object):

    def __init__(self, pair,DEBUG=0):

        def debug(message):
            if DEBUG:
                print 'DEBUG '+message

        def error(message):
            print 'ERROR '+message

        self.name = 'local'

        debug(self.name+' Init')

        if pair == 'EURBTC':
            self.pair = 'BTCEUR'
        elif pair == 'BTCEUR':
            self.pair = 'BTCEUR'
        else:
            error(self.name+' init() Unknown pair '+pair)
            sys.exit(1)

        # Get credentials from Environment Variables
        self.LOCAL_ACCESS_KEY = os.getenv('LOCAL_ACCESS_KEY')
        self.LOCAL_SECRET_KEY = os.getenv('LOCAL_SECRET_KEY')

        if self.LOCAL_ACCESS_KEY == None:
            error('ERROR '+self.name+' Environment variable LOCAL_ACCESS_KEY not found. Please make sure this variable is loaded in memory.')
            sys.exit(1)
        if self.LOCAL_SECRET_KEY == None:
            error('ERROR '+self.name+' Environment variable LOCAL_SECRET_KEY not found. Please make sure this variable is loaded in memory.')
            sys.exit(1)

        debug(self.name+' LOCAL_ACCESS_KEY: '+self.LOCAL_ACCESS_KEY)
        debug(self.name+' LOCAL_SECRET_KEY: '+'*'*(len(self.LOCAL_SECRET_KEY)-3)+self.LOCAL_SECRET_KEY[-3:])



    def system_time(self):
        return datetime.datetime.utcnow()


    # Epoch (seconds)
    def system_time_epoch(self):
        return int(datetime.datetime.utcnow().strftime('%s%f')[:-6])