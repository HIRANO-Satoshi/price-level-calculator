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
async def luncho_data(
        country_code: CountryCode, # client provided country code in ISO-3166-1-2 formant like 'JP'
) -> LunchoData:
    '''
      Returns LunchoData that is needed to convert between Luncho and local currency of the countryCode.
        If data for the country is not available either ppp or exchange_rate is 0.
      Data size is about 400 bytes.

      - **country_code**: client provided country code in ISO-3166-1-2 formant like 'JP'
      - **return**: LunchoData

    '''
    country: Optional[Country] = Countries.get(country_code, None)
    if not country:
        error(country_code, 'Invalid country code')
        # never come here

    return country

@api_router.get("/country-code", response_model=str, tags=['Luncho'])
async def country_code(
        X_Appengine_Country: Optional[str]=Header(None),  # country code if on Google App Engine
) -> str:
    '''
      Returns country code. This is available only when the server runs on Google App Engine.
      - **X_Appengine_Country**: Internal use. Ignore this.
      - **return**: str. A country code.

    '''
    print('country_code before = ' + str(X_Appengine_Country))
    return X_Appengine_Country or 'JP'

@api_router.get("/countries", response_model=Dict[CountryCode, str], tags=['Luncho'])
async def countries() -> Dict[CountryCode, str]:
    '''
      Returns a dict of supported country codes and names so that you can show
    a dropdown list of countries. Data size is about 3.5KB.
       E.g. {'JP': 'Japan', 'US': 'United States'...}.
        If data for a country is not available, either its ppp or exchange_rate is 0.

      - **return**: Dict[CountryCode, str] A dict of a country code and country name.
    '''
    return CountryCode_Names


@api_router.get("/all-luncho-data", response_model=Dict[CountryCode, LunchoData], tags=['Luncho'])
async def all_luncho_data() -> Dict[CountryCode, LunchoData]:
    '''
      Returns A dict of LunchoDatas for supported countries. Data size is about 40KB.
    - **return**: Dict[CountryCode, LunchoData] A dict of a country code and LunchoData.
    '''

    return Countries


@api_router.get("/health", tags=['Luncho'])
async def health() -> None:
    '''
      Do nothing other than telling it's OK.
    '''
    return


@api_router.get("/update_exchange_rate", include_in_schema=False)  # not in OpenAPI
async def update_exchange_rate() -> None:
    '''
      Update exchange rate data. This is an internal API.
    '''
    exchange_rate.load_exchange_rates()


# use method names in OpenAPI operationIds to generate methods with the method names
simplify_operation_ids(api_router)
