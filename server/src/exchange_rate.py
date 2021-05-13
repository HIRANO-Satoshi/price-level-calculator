'''
  Exchange rates

  Created on 2021/05/09

  Author: HIRANO Satoshi
'''

import json
from typing import Type, Optional, List, Dict #, Tuple, Union, Any, Generator, cast
from typing_extensions import TypedDict
import requests

from src.utils import error
from src import conf
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

# load exchange rates from fixer
def load_exchange_rates():
    global Fixer_Exchange_Rates, Exchange_Rates
    url: str = 'http://data.fixer.io/api/latest?access_key=12f3a3071f20a9972e381d1a8e03b818'

    response = requests.get(url, headers=conf.Header_To_Fetch('en'), allow_redirects=True)
    assert response.ok   #XXX Can we retry?

    Fixer_Exchange_Rates = json.loads(response.text)
    assert Fixer_Exchange_Rates['base'] == 'EUR'  # always EUR with free plan

    usd: float = Fixer_Exchange_Rates['rates']['USD']  # USD per euro
    for currecy_code, euro_value in Fixer_Exchange_Rates['rates'].items():  #type: CurrencyCode, float
        Exchange_Rates[currecy_code] = euro_value / usd   # store in USD

def cron_task():
    # 1000/month with free plan
    #XXX
    load_exchange_rates()

# load exchange rates at startup
load_exchange_rates()
