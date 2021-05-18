'''
  Python test cases for Luncho server and client library.

  @author: HIRANO Satoshi
  @date: 2021-5-15
'''

import os
import logging
import time
from typing import List, Dict, Tuple, Callable, Union, Any, Set, ClassVar, Type, Optional, cast
import pytest
from fastapi.testclient import TestClient

import conf
import main
from src.ppp_data import Countries, CountryCode_Names
from src.types import Currency, CurrencyCode, C1000, CountryCode, LunchoData, Country

main.init(use_dummy_data=True)   # use dummy data from files
client = TestClient(main.app)

@pytest.fixture(scope="function", autouse=True)
def setup_method():
    pass

def test_server_api():
    response = client.get("/v1/countries")
    assert response.status_code == 200
    datas: Dict[CountryCode, str] = response.json()
    assert datas['JP'] == 'Japan'
    assert len(datas) > 150

    response = client.get("/v1/luncho-data?country_code=JP")
    assert response.status_code == 200
    lunchoData: LunchoData = cast(LunchoData, response.json())
    Japan_test(lunchoData)

    response = client.get("/v1/luncho-datas")
    assert response.status_code == 200
    lunchoDatas: Dict[CountryCode, LunchoData] = cast(Dict[CountryCode, LunchoData], response.json())
    Japan_test(lunchoDatas['JP'])

    response = client.get("/v1/luncho-data?dummydata=JP")
    assert response.status_code == 422

def Japan_test(lunchoData: LunchoData):
    assert lunchoData['country_code']   == 'JP'
    assert lunchoData['country_name']   == 'Japan'
    assert lunchoData['country_code']   == 'JP'
    assert lunchoData['continent_code'] == 'AS'
    assert lunchoData['currency_code']  == 'JPY'
    assert lunchoData['currency_name']  == 'Yen'
    assert lunchoData['exchange_rate']  == 105.40404976166664
    assert lunchoData['ppp']            == 98.662
    assert lunchoData['dollar_per_luncho'] == 0.07139819441152714
    assert lunchoData['expiration']     > time.time() + 60*60 - 2
