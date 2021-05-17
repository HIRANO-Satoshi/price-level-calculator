'''
  Types

  Created on 2021/05/12

  Author: HIRANO Satoshi
'''

from typing import List, Dict, Tuple, Union, Any, Type, Generator, Optional, ClassVar, cast
from typing_extensions import TypedDict
from pydantic import BaseModel, create_model_from_typeddict

CountryCode = str               # ISO 3166-1 2 letter code. E.g. 'JP'
CurrencyCode = str              # ISO 4217   3 letter currency code. E.g. 'AFN'
ContinentCode = str             # NA, SA, AS, OC, AF

class Country(TypedDict, total=False):
    ''' IMF PPP data for a country
           {'AFG': {            1981: 17.4...
           {'ALB': {1980: 24.4, 1981: 24.5...
    '''

    year_ppp: Optional[Dict[int, float]]  # { year: ppp }  Optional
    #ppp: float                # PPP in local currency of currency_name
    currency_code: CurrencyCode # AFN  (ISO 3 letter currency code)
    currency_name: str        # Afghani
    country_name: str           # Afghanistan

create_model_from_typeddict(Country)

continents: Dict[ContinentCode, str] = {
    'NA': 'North America',
    'SA': 'South America',
    'EU': 'Europe',
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
}

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
