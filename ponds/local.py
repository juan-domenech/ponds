# local.API for testing purposes

import os
import datetime
import sys

DEBUG = 1

def debug(message):
    if DEBUG:
        print 'DEBUG '+message

def error(message):
    print 'ERROR '+message

def system_epoch_milliseconds():
    return int(datetime.datetime.utcnow().strftime('%s%f')[:-3])


class API(object):

    def __init__(self, pair,DEBUG=0):

        self.name = 'local'
        self.limit_milliseconds = 1000 # Throttling limit ms

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
        debug(self.name+' LOCAL_ACCESS_KEY: '+self.LOCAL_ACCESS_KEY)

        if self.LOCAL_SECRET_KEY == None:
            error('ERROR '+self.name+' Environment variable LOCAL_SECRET_KEY not found. Please make sure this variable is loaded in memory.')
            sys.exit(1)
        debug(self.name+' LOCAL_SECRET_KEY: '+'*'*(len(self.LOCAL_SECRET_KEY)-3)+self.LOCAL_SECRET_KEY[-3:])

        self.global_nonce = system_epoch_milliseconds()
        debug(self.name+' init global_nonce '+str(self.global_nonce))

        # Initialize system_time_epoch()
        self.system_time_epoch_nonce = self.global_nonce - self.limit_milliseconds
        self.system_time_epoch_cached = None



    # def system_time(self):
    #     return datetime.datetime.utcnow()


    # Epoch (seconds)
    def system_time_epoch(self):

        debug(self.name+' system_time_epoch self.system_time_epoch_nonce '+str(self.system_time_epoch_nonce ))

        # Get current system time epoch milliseconds
        system_epoch_milliseconds_variable = system_epoch_milliseconds()

        # If less than 1000 ms have passed
        if ( system_epoch_milliseconds_variable - self.system_time_epoch_nonce ) < self.limit_milliseconds:
            # Throttle and return cached value
            debug(self.name+' system_time_epoch throttling '+str(system_epoch_milliseconds_variable - self.system_time_epoch_nonce )+' '+str(self.limit_milliseconds))
            return {'error': '', 'epoch': self.system_time_epoch_cached, 'throttled': True}

        else:
            # We are good. Return a fresh value.
            # Current time to nonce to use it on the next execution
            self.system_time_epoch_nonce = system_epoch_milliseconds_variable

            # Get fresh value and return it
            self.system_time_epoch_cached = int(datetime.datetime.utcnow().strftime('%s%f')[:-6])
            debug(self.name+' system_time_epoch '+str(self.system_time_epoch_cached))

            return {'error':'', 'epoch': self.system_time_epoch_cached, 'throttled': False}

