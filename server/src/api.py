'''
  Luncho API

  @author HIRANO Satoshi
  @date  2021/05/13
'''

import json
import copy
import datetime
import logging
from typing import List, Dict, Tuple, Union, Any, Type, Generator, Optional, ClassVar, cast

from fastapi.openapi.utils import get_openapi

from main import app
from src import exchange_rate
from src.ppp_data import IMF_PPP_All
from src.types import Currency, CurrencyCode, C1000, Country, CountryCode, LunchoResult, IMF_PPP_Country

SDR_Per_Luncho = 5.0/100.0   # 100 Luncho is 5 SDR.
Doller_Per_SDR = 1.424900 # 1 SDR = $1.424900


@app.get("/test/", response_model=LunchoResult)
async def test(country_code: CountryCode = 'JPN', luncho_value: float = 100) -> List[str]:
    return ['a']

@app.get("/convert-from-luncho/", response_model=LunchoResult)
async def convert_from_luncho(country_code: CountryCode = 'JPN', luncho_value: float = 100) -> LunchoResult:

    if not country_code:
        country_code = 'JPN'


    dollar_per_luncho: float = 0
    local_currency_value: float = 0
    dollar_value: float = 0
    exchange_rate_per_USD: Optional[float] = 0
    currency_code: Optional[CurrencyCode] = None

    IMF_PPP_this_country = IMF_PPP_All[country_code]
    currency_code = IMF_PPP_this_country['currency_code']
    year: int = datetime.datetime.today().year
    ppp: float = IMF_PPP_this_country['year_ppp'].get(year, None)  # country's ppp of this year
    if ppp:
        exchange_rate_per_USD = exchange_rate.exchange_rate_per_USD(currency_code)
        if exchange_rate_per_USD is not None:
            #breakpoint()
            dollar_per_luncho = Doller_Per_SDR * SDR_Per_Luncho
            local_currency_value = dollar_per_luncho * ppp * luncho_value
            dollar_value = local_currency_value / exchange_rate_per_USD
        else:
            print('Exchange rate not found: ' + IMF_PPP_this_country['country_name'] + ' ' + IMF_PPP_this_country['currency_name'] + '(' + currency_code + ')')
    else:
        print('PPP not found: ' + IMF_PPP_this_country['country_name'] + ' ' + IMF_PPP_this_country['currency_name'] + '(' + currency_code + ')')


    return {"dollar_value": dollar_value,
            'local_currency_value': local_currency_value,
            'currency_code': currency_code,
            'country_code': country_code,
            'country_name': IMF_PPP_this_country['country_name'],
            'currency_name': IMF_PPP_this_country['currency_name'],
            'ppp': ppp,
            'dollar_per_luncho': dollar_per_luncho,
            'exchange_rate': exchange_rate_per_USD
    }

def gen_openapi_schema() -> Dict:
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/convert-from-luncho-all")
async def convert_from_luncho_all(luncho_value: float) -> List[IMF_PPP_Country]:

    lunchos = []
    for country_code in IMF_PPP_All:  #type: CountryCode
        lunchos.append(await convert_from_luncho(country_code, luncho_value))
    return lunchos


@app.get("/countries")
async def countries() -> Dict[CountryCode, IMF_PPP_Country]:
    IMF_PPP_All_copy: Dict[CountryCode, IMF_PPP_Country] = copy.deepcopy(IMF_PPP_All)

    for country_code in IMF_PPP_All_copy:  #type: CountryCode
        del IMF_PPP_All_copy[country_code]['year_ppp']
    return IMF_PPP_All_copy



@app.get("/convert-from-luncho-dummy/")
async def convert_from_luncho_dummy(currency_code: CurrencyCode, luncho_value: float) -> Dict[str, float]:
    ppp = 1.0
    if currency_code == 'USD':
        ppp = 4.81
    elif currency_code == 'JPY':
        ppp = 530
    elif currency_code == 'EURO':
        ppp = 4.40
    elif currency_code == 'CNY':
        ppp = 33.92

    return {"currency_value": luncho_value * ppp}
