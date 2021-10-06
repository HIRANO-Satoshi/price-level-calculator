'''
  Exchange rates

  Created on 2021/05/09

  Author: HIRANO Satoshi
'''

import datetime
import json
import time
import sys
import logging
import threading
from threading import Thread
from typing import Type, Optional, List, Dict #, Tuple, Union, Any, Generator, cast
from typing_extensions import TypedDict
import requests

from src.utils import error
from src.types import Currency, CurrencyCode, C1000
import conf
if conf.Use_Fixer_For_Forex:
    import api_keys
    fixer_access_key = api_keys.Fixer_Access_Key
else:
    fixer_access_key = ''

global_variable_lock = threading.Lock()

# exchange rates based on USD
Exchange_Rates: Dict[CurrencyCode, float] = {}  # { currencyCode: rate }

# Expiration time of Exchange_Rates
expiration: float = 0.0

# time of the last load of Exchange_Rates
last_load: float = 0

# SDR/Dollar
SDR_Per_Dollar: float = 0   # filled in load_exchange_rates()  1 SDR = $1.4...

class FixerExchangeRate(TypedDict):
    success: bool    # true if API success
    timestamp: int   # 1605081845
    base: str        # always "EUR"
    date: str        #"2020-11-11",
    rates: Dict[CurrencyCode, float]   # EUR based rates, "AED": 4.337445

def convert(source: Currency, currencyCode: CurrencyCode) -> Currency:
    if source.currencyCode == currencyCode:
        return source

    source_exchange_rate: Optional[float] = Exchange_Rates.get(source.currencyCode, None)
    if source_exchange_rate is None or source_exchange_rate == 0:
        error(source.currencyCode, "Currency code mismatch")

    to_exchange_rate: Optional[float] = Exchange_Rates.get(currencyCode, None)
    if to_exchange_rate is None:
        error(currencyCode, "Currency code mismatch")

    value: float = source.value / source_exchange_rate * to_exchange_rate
    return Currency(code=currencyCode, value=int(value))


def exchange_rate_per_USD(currencyCode: CurrencyCode) -> float:
    ''' Returns exchange rate per USD for the currencyCode.
        None if the currencyCode is not available. '''

    return Exchange_Rates.get(currencyCode, 0.0)


def load_exchange_rates(use_dummy_data: bool):
    ''' Load exchange rates from fixer or dummy data file. '''

    fixer_exchange_rate: FixerExchangeRate
    new_exchange_rate: Dict[CurrencyCode, float] = {}

    if use_dummy_data:
        with open(conf.Dummy_Fixer_Exchange_File, 'r', newline='', encoding="utf_8_sig") as fixer_file:
            fixer_exchange_rate = json.load(fixer_file) # 168 currencies
    else:
        url = ''.join((conf.Exchangerate_URL, 'latest', '?access_key=', fixer_access_key)) # date can be '2021-05-25'
        #XXX fall back?

        OK: boolean = False
        err_msg: str = ''
        try:
            response = requests.get(url, headers=conf.Header_To_Fetch('en'), allow_redirects=True)
            OK = response.ok
            err_msg = str(response.status_code)
        except Exception as ex:   #pylint: disable=broad-except
            err_msg = str(ex)
        if OK:   # no retry. will load after one hour.
            fixer_exchange_rate = json.loads(response.text)
            assert fixer_exchange_rate['base'] == 'EUR'  # always EUR with free plan
            logging.info('Fetched exchange rate')
            #XXX save it
            # with open(conf.Last_Fixer_Exchange_File, 'w', newline='', encoding="utf_8_sig") as fixer_new_file:
            #     fixer_new_file.write(response.text)
        else:
            # use the last exchange rate data. if not available, use test data
            try:
                with open(conf.Last_Fixer_Exchange_File, newline='', encoding="utf_8_sig") as fixer_last_file:
                    fixer_exchange_rate = json.load(fixer_last_file)
                    logging.error('Fetching exchange rate failed for %s with %s fall down to data last got', conf.Exchangerate_URL, err_msg)
            except OSError:
                with open(conf.Dummy_Fixer_Exchange_File, newline='', encoding="utf_8_sig") as fixer_last_file:
                    fixer_exchange_rate = json.load(fixer_last_file)
                    logging.error('Fetching exchange rate failed for %s with %s. Fall down to data in %s', conf.Exchangerate_URL, err_msg, conf.Dummy_Fixer_Exchange_File)

    # build Exchange_rates which is USD based rates from fixer_exchange_rate which is EUR based
    usd: float = fixer_exchange_rate['rates']['USD']  # USD per euro
    for currecy_code, euro_value in fixer_exchange_rate['rates'].items():  #type: CurrencyCode, float
        new_exchange_rate[currecy_code] = euro_value / usd   # store in USD

    # update globals
    global Exchange_Rates, SDR_Per_Dollar, last_load, expiration

    with global_variable_lock:
        Exchange_Rates = new_exchange_rate
        SDR_Per_Dollar = Exchange_Rates['XDR']
        last_load = time.time()
        expiration = timeToUpdate() + 40  # expires 40 sec after Forex data update time

    # update PPP data
    from src import ppp_data
    ppp_data.update()


def cron(use_dummy_data):
    '''Cron task thread. Update exchange rate data at 00:06 UTC everyday,
       since exchangerate.host updates at 00:05. https://exchangerate.host/#/#docs"

        In case on App Engine, cron.yaml is used and this is not used.
    '''

    while True:
        time.sleep(timeToUpdate() - time.time())
        #time.sleep(10)        # test
        load_exchange_rates(use_dummy_data)


def init(use_dummy_data):
    ''' Initialize exchange rates. '''

    # load exchange rates at startup and every one hour
    load_exchange_rates(use_dummy_data)

    if conf.Is_AppEngine:
        # we use cron.yaml on GAE
        pass
    else:
        # start cron task
        thread: Thread = Thread(target=cron, args=(use_dummy_data,))
        thread.start()

def timeToUpdate():
    ''' Returns next update time in POSIX time. '''

    if conf.Use_Fixer_For_Forex:
        # Fixer update every hour. We update 3 minute every hour. 00:03, 01:03, 02:03...
        #
        #  now = datetime.datetime(2021, 5, 21, 15, 26, 27, 291409)
        #  next_hour = datetime.datetime(2021, 5, 21, 16, 26, 27, 291409)
        #  time_until_next_hour = datetime.timedelta(seconds=2012, microseconds=708591)
        #  seconds_until_next_hour = 2012
        #  time_to_update = 1621580600 (2021-05-21 16:03)
        #
        now: datetime = datetime.datetime.now()
        next_hour: datetime  = now + datetime.timedelta(hours=1)
        time_until_next_hour: datetime.timedelta = next_hour.replace(minute=0, second=0, microsecond=0) - now
        seconds_until_next_hour: int = time_until_next_hour.seconds
        time_to_update: float = time.time() + seconds_until_next_hour + 3*60
        return time_to_update
    else:
        # exchangerate.host updates every day at 00:05 https://exchangerate.host/#/#docs"
        # we update at 00:06 everyday.
        #
        #  now = datetime.datetime(2021, 5, 21, 15, 22, 7, 226310)
        #  tomorrow = datetime.datetime(2021, 5, 22, 15, 22, 7, 226310)
        #  time_until_midnight = datetime.timedelta(seconds=31072, microseconds=773690)
        #  seconds_until_midnight = 31072
        #  time_to_update = 1621609503.573357 (2021-05-22 00:06:00)
        #
        now: datetime = datetime.datetime.now()
        tomorrow: datetime  = now + datetime.timedelta(days=1)
        time_until_midnight: datetime.timedelta = datetime.datetime.combine(tomorrow, datetime.time.min) - now
        seconds_until_midnight: int = time_until_midnight.seconds
        time_to_update = time.time() + seconds_until_midnight + 6*60
        return time_to_update

def exchange_rates_benchmark(use_dummy_data: bool):
    ''' Calculate the average exchange rates during the following period for each currency.

    - [[file:///Users/hirano/Downloads/stasapp.pdf][World Economic Outlook 2021, STATISTICAL APPENDIX]]
      - Assumptions
        - Real effective exchange rates for the advanced economies are assumed to remain constant at
          their _average levels measured during January 18, 2021–February 15, 2021_. For 2021 and 2022
          these assumptions imply average US dollar–special drawing right (SDR) conversion rates of
          1.445 and 1.458,
    '''
    pass
    #XXX
