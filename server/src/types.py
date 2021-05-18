'''
  Types

  Created on 2021/05/12

  Author: HIRANO Satoshi
'''

from typing import List, Dict, Optional
from pydantic import BaseModel

CountryCode = str               # ISO 3166-1 2 letter code. E.g. 'JP'
CurrencyCode = str              # ISO 4217   3 letter currency code. E.g. 'AFN'
ContinentCode = str             # NA, SA, AS, OC, AF

continents: Dict[ContinentCode, str] = {
    'NA': 'North America',
    'SA': 'South America',
    'EU': 'Europe',
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
}

class Info(BaseModel):
    expiration: float               # Data expiration in unix time. You need to call APIs after this time.
    dollar_per_luncho: float        # dollar/luncho rate


class LunchoData(BaseModel):
    ''' Data needed to convert between Luncho and local currency. '''

    country_code: CountryCode       # Country code
    country_name: str               # Country name
    continent_code: str             # Continent

    currency_code: CurrencyCode     # Currency code
    currency_name: str              # Currency name
    exchange_rate: Optional[float]  # Exchange rate per US Dollar

    ppp: Optional[float]            # PPP data
    dollar_per_luncho: float        # dollar/luncho rate
    #dollar_value: float
    #local_currency_value: float

class Country(LunchoData):
    ''' Internal data with yearly PPP values. '''
    year_ppp: Optional[Dict[int, float]]  # { year: ppp }  Optional

# class CountryCodeName(BaseModel):
#     ''' Country code and name. '''

#     country_code: CountryCode       # Country code
#     country_name: str               # Country name


class Currency():
    """
    NOT USED. Currency. Value is multipied by 1000.

    """


    def __init__(self, value=None, code=None, unit=None,):
        super().__init__()
        self.value = value
        self.code = code
        self.unit = unit

C1000 = 1000
