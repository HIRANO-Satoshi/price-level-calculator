'''
  Python test cases for Luncho server and client library.

  @author: HIRANO Satoshi
  @date: 2021-5-15
'''

import os
import logging
from typing import List, Dict, Tuple, Callable, Union, Any, Set, ClassVar, Type, Optional, cast
import pytest
from fastapi.testclient import TestClient

import conf
import main

main.init()
client = TestClient(main.app)

@pytest.fixture(scope="function", autouse=True)
def setup_method():
    pass

def test_api():
    response = client.get("/v1/countries")
    assert response.status_code == 200
    assert len(response.json()) > 150

    response = client.get("/v1/luncho-data")
    assert response.status_code == 200
    assert len(response.json()) > 150
