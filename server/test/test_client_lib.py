'''

  pytest test_client_lib.py
  pytest test/test_client_lib.py::test_countries_luncho


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
from luncho_python.api import luncho_api, luncho
from luncho_python.model.http_validation_error import HTTPValidationError
from luncho_python.model.luncho_data import LunchoData
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = luncho_python.Configuration(
    host = "http://localhost:8000"
)

def test_countries_luncho():

    # Enter a context with an instance of the API client
    with luncho_python.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = luncho.Luncho(api_client)

        try:
            datas: Dict[CountryCode, str] = api_instance.countries_fast()
            assert len(datas) > 150

            # again should use cache
            datas = api_instance.countries_fast()
            assert len(datas) > 150
        except luncho_python.ApiException as e:
            print("Exception when calling LunchoApi->countries: %s\n" % e)

def test_countries_luncho_api():

    # Enter a context with an instance of the API client
    with luncho_python.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = luncho_api.LunchoApi(api_client)

        try:
            datas: Dict[CountryCode, str] = api_instance.countries()
            assert len(datas) > 150
        except luncho_python.ApiException as e:
            print("Exception when calling LunchoApi->countries: %s\n" % e)

def test_luncho_data_luncho():

    # Enter a context with an instance of the API client
    with luncho_python.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = luncho.Luncho(api_client)

        try:
            lunchoData: LunchoData = api_instance.luncho_data_fast('JP')
            Japan_test(lunchoData)

            # again should use cache
            import pdb; pdb.set_trace()

            lunchoData = api_instance.luncho_data_fast('JP')
            Japan_test(lunchoData)
        except luncho_python.ApiException as e:
            print("Exception when calling LunchoApi->countries: %s\n" % e)

        try:
            lunchoData: LunchoData = api_instance.luncho_data_fast('NOT EXISTS')
        except luncho_python.ApiException as e:
            print("Exception when calling LunchoApi->countries: %s\n" % e)

def test_luncho_data_luncho_api():

    # Enter a context with an instance of the API client
    with luncho_python.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = luncho_api.LunchoApi(api_client)

        try:
            lunchoData: LunchoData = api_instance.luncho_data('JP')
            Japan_test(lunchoData)
        except luncho_python.ApiException as e:
            print("Exception when calling LunchoApi->countries: %s\n" % e)

def test_luncho_datas_luncho():

    # Enter a context with an instance of the API client
    with luncho_python.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = luncho.Luncho(api_client)

        try:
            lunchoDatas: Dict[CountryCode, LunchoData] = api_instance.luncho_datas_fast()
            Japan_test(lunchoDatas['JP'])

            # again should use cache
            lunchoDatas = api_instance.luncho_datas_fast()
            Japan_test(lunchoDatas['JP'])
        except luncho_python.ApiException as e:
            print("Exception when calling LunchoApi->countries: %s\n" % e)

def test_luncho_datas_luncho_api():

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

def test_localCurrencyFromLuncho():

    # Enter a context with an instance of the API client
    with luncho_python.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = luncho.Luncho(api_client)

        try:
            #import pdb; pdb.set_trace()
            value: float = api_instance.localCurrencyFromLuncho(100.0, 'JP')
            assert value >= 500

            # again should use cache
            value = api_instance.localCurrencyFromLuncho(100.0, 'JP')
            assert value >= 500
        except luncho_python.ApiException as e:
            print("Exception when calling LunchoApi->countries: %s\n" % e)

def test_USDollarFromLuncho():

    # Enter a context with an instance of the API client
    with luncho_python.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = luncho.Luncho(api_client)

        try:
            value: float = api_instance.USDollarFromLuncho(100.0, 'JP')
            assert value >= 6.0

            # again should use cache
            value = api_instance.USDollarFromLuncho(100.0, 'JP')
            assert value >= 6.0
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
