'''
  Luncho API

  @author HIRANO Satoshi
  @date  2021/05/13
'''

import json
import copy
import datetime
import logging
import pdb
from typing import List, Dict, Tuple, Union, Any, Type, Generator, Optional, ClassVar, cast

from fastapi import Header
from fastapi.openapi.utils import get_openapi
from fastapi_utils.openapi import simplify_operation_ids

from main import app
from src import exchange_rate
from src.utils import error
from src.ppp_data import Countries
from src.types import Currency, CurrencyCode, C1000, CountryCode, LunchoData, Country

SDR_Per_Luncho = 5.0/100.0   # 100 Luncho is 5 SDR.

@app.get("/luncho-data", response_model=LunchoData, tags=['Luncho'])
async def lunchoData(
        # client provided country code in ISO-3166-1-2 formant like 'JP'
        country_code: Optional[CountryCode] = None,

        # ISO-3166-1-2 'client_region' by Google Cloud load balancer (Optional)
        client_region: Optional[CountryCode] = Header(None),

        # ISO 3166-1-2 'CloudFront-Viewer-Country' by AWS CloudFront HTTP headers  (Optional)
        cloudfront_viewer_country: Optional[CountryCode] = Header(None)

        # # IP address via load balancer
        # x_forwarded_for: Optional[str] = Header(None),

        # # IP addres
        # remote_addr: Optional[str] = Header(None)
) -> LunchoData:
    '''
      Returns LunchoData that is needed to convert between Luncho and local currency of the countryCode.
      If the countryCode is not specified, estimate it from IP address.

    '''

    #pdb.set_trace()
    currency_code: Optional[CurrencyCode] = None
    dollar_per_luncho: float = 0
    exchange_rate_per_USD: Optional[float] = 0
    dollar_per_luncho = exchange_rate.Dollar_Per_SDR * SDR_Per_Luncho
    year: int = datetime.datetime.today().year
    #local_currency_value: float = 0
    #dollar_value: float = 0

    country_code = country_code or client_region or cloudFront_viewer_country or None

    country = Countries.get(country_code, None)
    if not country:
        error(country_code, 'Invalid country code')

    currency_code = country['currency_code']
    ppp: float = country['year_ppp'].get(year, None)  # country's ppp of this year
    if ppp:
        exchange_rate_per_USD = exchange_rate.exchange_rate_per_USD(currency_code)
        if exchange_rate_per_USD is not None:
            pass
            #local_currency_value = dollar_per_luncho * ppp * luncho_value
            #dollar_value = local_currency_value / exchange_rate_per_USD
        else:
            print('Exchange rate not found: ' + country['country_name'] + ' ' + country['currency_name'] + '(' + currency_code + ')')
    else:
        print('PPP not found: ' + country['country_name'] + ' ' + country['currency_name'] + '(' + currency_code + ')')


    return {
        'country_code': country_code,
        'country_name': country['country_name'],
        'continent_code': country['continent_code'],
        'currency_code': currency_code,
        'currency_name': country['currency_name'],
        'exchange_rate': exchange_rate_per_USD,
        'ppp': ppp,
        'dollar_per_luncho': dollar_per_luncho,
        #'local_currency_value': local_currency_value
        #"dollar_value": dollar_value,
    }


@app.get("/luncho-datas", response_model=List[LunchoData], tags=['Luncho'])
async def lunchoDatas() -> List[LunchoData]:
    '''
      Returns A list of LunchoDatas for all supported countries.
    '''

    lunchoDatas: List[LunchoData] = []
    for country_code in Countries:  #type: CountryCode
        lunchoDatas.append(await lunchoData(country_code))
    return lunchoDatas


@app.get("/country-codes", response_model=List[CountryCode], tags=['Luncho'])
async def countryCodes() -> List[CountryCode]:
    '''
      Returns a list of supported country codes.
    '''
    return [country_code for coutry_data in Countries]


# @app.get("/country-PPPs", response_model=Dict[CountryCode, Country], tags=['Luncho'])
# async def countryPPPs() -> Dict[CountryCode, Country]:
#     '''
#       Returns country data for all countries.
#     '''
#     Countries_copy: Dict[CountryCode, Country] = copy.deepcopy(Countries)

#     for country_code in Countries_copy:  #type: CountryCode
#         del Countries_copy[country_code]['year_ppp']
#     return Countries_copy



# @app.get("/countryCode", response_model=CountryCode, tags=['Luncho'])
# async def countryCode() -> CountryCode:
#     ''' Returns country code for the current IP address. '''



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


# use method names in OpenAPI operationIds to generate methods with the method names
simplify_operation_ids(app)
