'''

  pytest test_client_lib.py

  This test does not run in Emacs. Why?

  @author HIRANO Satoshi
  @date  2021/5/18
'''

import time
import pytest
from pprint import pprint
# import importlib
# foobar = importlib.import_module("luncho-python")
import luncho_python
from luncho_python.api import luncho_api
from luncho_python.model.http_validation_error import HTTPValidationError
from luncho_python.model.luncho_data import LunchoData
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = luncho_python.Configuration(
    host = "http://localhost:8000"
)

def test_countries():

    # Enter a context with an instance of the API client
    with luncho_python.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = luncho_api.LunchoApi(api_client)

        try:
            # Countries
            datas: Dict[CountryCode, str] = api_instance.countries()
            assert len(datas) > 150
        except luncho_python.ApiException as e:
            print("Exception when calling LunchoApi->countries: %s\n" % e)

def test_luncho_data():

    # Enter a context with an instance of the API client
    with luncho_python.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = luncho_api.LunchoApi(api_client)

        try:
            # Countries
            lunchoData: LunchoData = api_instance.luncho_data('JP')
            Japan_test(lunchoData)
        except luncho_python.ApiException as e:
            print("Exception when calling LunchoApi->countries: %s\n" % e)

def test_luncho_datas():

    # Enter a context with an instance of the API client
    with luncho_python.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = luncho_api.LunchoApi(api_client)

        try:
            # Countries
            lunchoDatas: Dict[CountryCode, LunchoData] = api_instance.luncho_datas()
            Japan_test(lunchoDatas['JP'])
        except luncho_python.ApiException as e:
            print("Exception when calling LunchoApi->countries: %s\n" % e)

def Japan_test(lunchoData: LunchoData):
    assert lunchoData['country_code']   == 'JP'
    assert lunchoData['country_name']   == 'Japan'
    assert lunchoData['country_code']   == 'JP'
    assert lunchoData['continent_code'] == 'AS'
    assert lunchoData['currency_code']  == 'JPY'
    assert lunchoData['currency_name']  == 'Yen'
    assert lunchoData['exchange_rate']  > 80
    assert lunchoData['ppp']            > 80
    assert lunchoData['dollar_per_luncho'] > 0.04
    #assert lunchoData['expiration']     > time.time() + 60*60 - 2
