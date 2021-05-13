'''
  Types

  Created on 2021/05/12

  Author: HIRANO Satoshi
'''

from typing import List, Dict, Tuple, Union, Any, Type, Generator, Optional, ClassVar, cast
from typing_extensions import TypedDict
from pydantic import BaseModel, create_model_from_typeddict

C1000 = 1000
CountryCode = str
CurrencyCode = str

class Country(TypedDict):
    ppp: float                # PPP in local currency of currency_name
    currency_code: CurrencyCode # AFN  (ISO 3 letter currency code)
    currency_name: str        # Afghani
    country_name: str           # Afghanistan


class Currency():
    """
    Currency. Value is multipied by 1000.

    """


    def __init__(self, value=None, code=None, unit=None,):
        super().__init__()
        self.value = value
        self.code = code
        self.unit = unit

class IMF_PPP_Country_Base(TypedDict, total=False):
    ''' IMF PPP data
           {'AFG': {            1981: 17.4...
           {'ALB': {1980: 24.4, 1981: 24.5...
    '''

    year_ppp: Dict[int, float]  # { year: ppp }  Optional
    ppp: float                # PPP in local currency of currency_name
    currency_code: CurrencyCode # AFN  (ISO 3 letter currency code)
    currency_name: str        # Afghani
    country_name: str           # Afghanistan

IMF_PPP_Country = create_model_from_typeddict(IMF_PPP_Country_Base)

class LunchoResult(BaseModel):
    dollar_value: float
    local_currency_value: float
    currency_code: CurrencyCode
    country_code: CountryCode
    country_name: str
    currency_name: str
    ppp: float
    dollar_per_luncho: float
    exchange_rate: float
