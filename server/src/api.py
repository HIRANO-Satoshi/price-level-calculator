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

from fastapi import Header, APIRouter
from fastapi.openapi.utils import get_openapi
from fastapi_utils.openapi import simplify_operation_ids

from conf import SDR_Per_Luncho
from src import exchange_rate
from src.utils import error
from src.ppp_data import Countries, CountryCode_Names
from src.types import Currency, CurrencyCode, C1000, CountryCode, LunchoData, Country

api_router = APIRouter()

@api_router.get("/luncho-data", response_model=LunchoData, tags=['Luncho'])
async def lunchoData(

        country_code: Optional[CountryCode] = None, # client provided country code in ISO-3166-1-2 formant like 'JP'
) -> LunchoData:

        # # ISO-3166-1-2 'client_region' by Google Cloud load balancer (Optional)
        # client_region: Optional[CountryCode] = Header(None),

        # # ISO 3166-1-2 'CloudFront-Viewer-Country' by AWS CloudFront HTTP headers  (Optional)
        # cloudfront_viewer_country: Optional[CountryCode] = Header(None)
    '''
      Returns LunchoData that is needed to convert between Luncho and local currency of the countryCode.
      Data size is about 400 bytes.
    '''

    #country_code: Optional[CountryCode] = country_code or client_region or cloudFront_viewer_country or None

    country: Optional[Country] = Countries.get(country_code, None)
    if not country:
        error(country_code, 'Invalid country code')
        # never come here

    # fill time dependent properties, though its a global data,
    # because all requests share the same data.
    country['ppp'] = country['year_ppp'].get(datetime.datetime.today().year, None)  # country's ppp of this year
    country['exchange_rate'] = exchange_rate.exchange_rate_per_USD(country['currency_code'])
    country['dollar_per_luncho'] = exchange_rate.Dollar_Per_SDR * SDR_Per_Luncho

    return country


@api_router.get("/countries", response_model=Dict[CountryCode, str], tags=['Luncho'])
async def countries() -> Dict[CountryCode, str]:
    '''
      Returns a dict of supported country codes and names so that you can show
    a dropdown list of countries. Data size is about 3.5KB.
       E.g. {'JP': 'Japan', 'US': 'United States'...}.
    '''
    return CountryCode_Names


@api_router.get("/luncho-datas", response_model=Dict[CountryCode, LunchoData], tags=['Luncho'])
async def lunchoDatas() -> Dict[CountryCode, LunchoData]:
    '''
      Returns A list of LunchoDatas for all supported countries. Data size is about 40KB.
    '''

    lunchoDatas: Dict[LunchoData] = {}
    for country_code in Countries:  #type: CountryCode
        lunchoDatas[country_code] = await lunchoData(country_code)
    return lunchoDatas



def gen_openapi_schema() -> Dict:
    ''' Callback for generating OpenAPI schema. '''

    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Client library for Luncho API. ",
        version="0.0.1",
        description="Use luncho.ts and luncho.py rather than LunchoAPI.ts and others.",
        routes=app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# use method names in OpenAPI operationIds to generate methods with the method names
simplify_operation_ids(api_router)
