import time
import pytest
import luncho_python
from pprint import pprint
from luncho_python.api import luncho_api
from luncho_python.model.http_validation_error import HTTPValidationError
from luncho_python.model.luncho_data import LunchoData
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = luncho_python.Configuration(
    host = "http://localhost:8000"
)

def test_api():

    # Enter a context with an instance of the API client
    with luncho_python.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = luncho_api.LunchoApi(api_client)

        try:
            # Countries
            api_response = api_instance.countries()
            pprint(api_response)
        except luncho_python.ApiException as e:
            print("Exception when calling LunchoApi->countries: %s\n" % e)
