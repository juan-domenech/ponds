# kraken.com
# https://www.kraken.com/help/api

import os
import datetime
import sys
import urllib2
import ast # String to Dictionary

DEBUG=0

def debug(message):
    if DEBUG:
        print 'DEBUG '+message

def error(message):
    print 'ERROR '+message

def system_epoch_milliseconds():
    return int(datetime.datetime.utcnow().strftime('%s%f')[:-3])


class API(object):

    def __init__(self, pair, DEBUG=0):

        self.name = 'kraken'
        self.limit_milliseconds = 1000 # Throttling limit ms

        debug(self.name+' Init')

        if pair == 'EURBTC':
            self.pair = 'XBTEUR'
        elif pair != 'BTCEUR':
            error(self.name+'init() Unknown pair '+pair)
            sys.exit(1)
        else:
            self.pair = 'XBTEUR'

        # Get credentials from Environment Variables
        self.KRAKEN_ACCESS_KEY = os.getenv('KRAKEN_ACCESS_KEY')
        self.KRAKEN_SECRET_KEY = os.getenv('KRAKEN_SECRET_KEY')

        if self.KRAKEN_ACCESS_KEY == None:
            error(self.name+' Environment variable KRAKEN_ACCESS_KEY not found. Please make sure this variable is loaded in memory.')
            sys.exit(1)
        debug(self.name+' KRAKEN_ACCESS_KEY: '+self.KRAKEN_ACCESS_KEY)

        if self.KRAKEN_SECRET_KEY == None:
            error(self.name+' Environment variable KRAKEN_SECRET_KEY not found. Please make sure this variable is loaded in memory.')
            sys.exit(1)
        debug(self.name+' KRAKEN_SECRET_KEY: '+'*'*(len(self.KRAKEN_SECRET_KEY)-3)+self.KRAKEN_SECRET_KEY[-3:])

        self.root_url = 'https://api.kraken.com/0'

        self.global_nonce = system_epoch_milliseconds()
        debug(self.name+' init global_nonce '+str(self.global_nonce))

        # Initialize system_time_epoch()
        self.system_time_epoch_nonce = self.global_nonce - self.limit_milliseconds
        self.system_time_epoch_cached = None


    # def system_time(self):
    #     return datetime.datetime.utcnow()


    def now_milliseconds(self):
        return int(datetime.datetime.utcnow().strftime('%s%f')[:-3])


    # Epoch (seconds)
    # https://www.kraken.com/help/api#get-server-time
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
            response = ast.literal_eval(urllib2.urlopen(self.root_url+'/public/Time').read())
            if response['error']:
                error('ERROR '+self.name+'.system_time_epoch(): '+response)
                sys.exit(1)
            else:
                ### {'result': {'unixtime': 1471293119, 'rfc1123': 'Mon, 15 Aug 16 20:31:59 +0000'}, 'error': []}
                debug(self.name+' system_time_epoch result: '+str(response['result']))
                self.system_time_epoch_cached = int(response['result']['unixtime'])

                debug(self.name+' system_time_epoch '+str(self.system_time_epoch_cached))

                return {'error': '', 'epoch': self.system_time_epoch_cached, 'throttled': False}


    def ticker(self):
        # https://www.kraken.com/help/api#get-ticker-info
        # {"error":[],"result":{"XXBTZEUR":{"a":["525.99900","1","1.000"],"b":["525.70000","1","1.000"],"c":["525.99900","0.04401000"],"v":["1033.95355743","1844.02477478"],"p":["526.62096","526.40549"],"t":[1652,3126],"l":["523.00000","523.00000"],"h":["528.98000","528.98000"],"o":"526.87100"}}}

        ticker = {}

        response = ast.literal_eval(urllib2.urlopen(self.root_url+'/public/Ticker?pair='+self.pair).read())
        if response['error']:
            print "ERROR "+self.name+".ticker():",response
            sys.exit(1)
        else:
            ticker['ask'] = float(response['result']['XXBTZEUR']['a'][0])
            ticker['bid'] = float(response['result']['XXBTZEUR']['b'][0])
            ticker['last'] = float(response['result']['XXBTZEUR']['c'][0])
            ticker['volume_today'] = float(response['result']['XXBTZEUR']['v'][0])
            ticker['volume_24h'] = float(response['result']['XXBTZEUR']['v'][1])
            return ticker


    # def transactions(self):







