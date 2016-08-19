# kraken.com
# https://www.kraken.com/help/api

import os
import datetime
import sys
import urllib2
import ast # String to Dictionary

DEBUG = 1


def debug(message):
    if DEBUG:
        print 'DEBUG '+message

def error(message):
    print 'ERROR '+message


class API(object):

    def __init__(self, pair):

        self.name = 'kraken'

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
        if self.KRAKEN_SECRET_KEY == None:
            error(self.name+' Environment variable KRAKEN_SECRET_KEY not found. Please make sure this variable is loaded in memory.')
            sys.exit(1)

        debug(self.name+'LOCAL_ACCESS_KEY: '+self.KRAKEN_ACCESS_KEY)
        debug(self.name+'LOCAL_SECRET_KEY: '+self.KRAKEN_SECRET_KEY)

        self.root_url = 'https://api.kraken.com/0'



    def system_time(self):
        return datetime.datetime.utcnow()

    def now_milliseconds(self):
        return int(datetime.datetime.utcnow().strftime('%s%f')[:-3])

    # Epoch (seconds)
    def system_time_epoch(self):
        # https://www.kraken.com/help/api#get-server-time

        response = ast.literal_eval(urllib2.urlopen(self.root_url+'/public/Time').read())
        if response['error']:
            print "ERROR "+self.name+".system_time_epoch():",response
            sys.exit(1)
        else:
            # {'result': {'unixtime': 1471293119, 'rfc1123': 'Mon, 15 Aug 16 20:31:59 +0000'}, 'error': []}
            return int(response['result']['unixtime'])


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







