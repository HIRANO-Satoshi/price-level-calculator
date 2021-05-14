'''
  Exchange rates

  Created on 2021/05/09

  Author: HIRANO Satoshi
'''

import json
import time
import sys
import logging
from threading import Thread
from typing import Type, Optional, List, Dict #, Tuple, Union, Any, Generator, cast
from typing_extensions import TypedDict
import requests

from src.utils import error
import conf
import keys
from src.types import Currency, CurrencyCode, C1000

class FixerExchangeRate(TypedDict):
    success: bool    # true if API success
    timestamp: int   # 1605081845
    base: str        # always "EUR"
    date: str        #"2020-11-11",
    rates: Dict[CurrencyCode, float]   # "AED": 4.337445

Fixer_Exchange_Rates: FixerExchangeRate = {}

# exchange rates based on USD
Exchange_Rates: Dict[CurrencyCode, float] = {}  # { currencyCode: rate }

# Dollar/SDR
Dollar_Per_SDR: float = 0   # filled in load_exchange_rates()  1 SDR = $1.4...

# time of the last load of exchange rates
last_load: float = 0

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


def exchange_rate_per_USD(currencyCode: CurrencyCode) -> Optional[float]:
    ''' Returns exchange rate per USD for the currencyCode.
        None if the currencyCode is not available. '''

    return Exchange_Rates.get(currencyCode, None)

def load_exchange_rates():
    ''' load exchange rates and SDR from fixer. '''

    global Fixer_Exchange_Rates, Exchange_Rates, last_load

    if last_load + (20*60*1000) > time.time():  # don't load again for 20 min
        return

    url: str = ''.join(('http://data.fixer.io/api/latest?access_key=', keys.Fixer_Access_Key))

    response = requests.get(url, headers=conf.Header_To_Fetch('en'), allow_redirects=True)
    assert response.ok   #XXX Can we retry?
    logging.info('fetched exchange rate')

    Fixer_Exchange_Rates = json.loads(response.text)
    assert Fixer_Exchange_Rates['base'] == 'EUR'  # always EUR with free plan

    usd: float = Fixer_Exchange_Rates['rates']['USD']  # USD per euro
    for currecy_code, euro_value in Fixer_Exchange_Rates['rates'].items():  #type: CurrencyCode, float
        Exchange_Rates[currecy_code] = euro_value / usd   # store in USD
        if currecy_code == 'XDR':
            global Dollar_Per_SDR
            Dollar_Per_SDR = 1 / Exchange_Rates[currecy_code]
            logging.info('Dollar/SDR = ' + str(Dollar_Per_SDR))
    last_load = time.time()

def cron():
    while True:
        time.sleep(60*60)      # every one hour
        load_exchange_rates()


def init():
    # load exchange rates at startup and every one hour
    load_exchange_rates()

    # # start cron task
    thread: Thread = Thread(target=cron)
    thread.start()
