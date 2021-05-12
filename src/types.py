'''
  Types

  Created on 2021/05/12

  Author: HIRANO Satoshi
'''

from mypy_extensions import TypedDict
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
