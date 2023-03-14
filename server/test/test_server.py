'''
  Python test cases for Luncho server and client library.

  @author: HIRANO Satoshi
  @date: 2021-5-15
'''

from __future__ import annotations
import os
import time
from typing import cast
import pytest
from fastapi.testclient import TestClient

import conf
import main
from src.ppp_data import Countries, CountryCode_Names
from src.types import CountryCode, LunchoData

main.init(use_dummy_data=True)   # use dummy data from files
client = TestClient(main.app)

@pytest.fixture(scope="function", autouse=True)
def setup_method() -> None:
    pass

def test_server_api() -> None:
    response = client.get("/v1/countries")
    assert response.status_code == 200
    datas: dict[CountryCode, str] = response.json()
    assert datas['JP'] == 'Japan'
    assert len(datas) > 150

    response = client.get("/v1/luncho-data?country_code=JP")
    assert response.status_code == 200
    lunchoData: LunchoData = cast(LunchoData, response.json())
    Japan_test(lunchoData)

    response = client.get("/v1/all-luncho-data")
    assert response.status_code == 200
    lunchoDatas: dict[CountryCode, LunchoData] = cast(dict[CountryCode, LunchoData], response.json())
    Japan_test(lunchoDatas['JP'])

    response = client.get("/v1/luncho-data?dummydata=JP")
    assert response.status_code == 422

def test_server_api_error() -> None:
    ''' Test for Forex fetch error. '''

    #XXX if os.path.exists(conf.Last_Fixer_Exchange_File):
    #    os.remove(conf.Last_Fixer_Exchange_File)

    # do without Last_Fixer_Exchange_File
    conf.Exchangerate_URL = 'https://not_exsist_not_exist.com'
    main.init(use_dummy_data=False)
    #XXX assert not os.path.exists(conf.Last_Fixer_Exchange_File)

    # do normally to make Last_Fixer_Exchange_File
    conf.Exchangerate_URL = conf.Free_Exchangerate_URL
    main.init(use_dummy_data=False)
    assert os.path.exists(conf.Last_Fixer_Exchange_File)

    # do with Last_Fixer_Exchange_File
    conf.Exchangerate_URL = 'https://not_exsist_not_exist.com'
    main.init(use_dummy_data=False)

def Japan_test(lunchoData: LunchoData) -> None:
    assert lunchoData['country_code']   == 'JP'
    assert lunchoData['country_name']   == 'Japan'
    assert lunchoData['country_code']   == 'JP'
    assert lunchoData['continent_code'] == 'AS'
    assert lunchoData['currency_code']  == 'JPY'
    assert lunchoData['currency_name']  == 'Yen'
    assert lunchoData['exchange_rate']  == 105.40404976166664
    assert lunchoData['ppp']            == 100.265 #98.662
    assert lunchoData['dollar_per_luncho'] == 0.07139819441152714
    assert lunchoData['expiration']     > time.time() + 60*60 - 2
