# openapi_client.LunchoApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**luncho**](LunchoApi.md#luncho) | **GET** /luncho | Luncho


# **luncho**
> LunchoResult luncho()

Luncho

### Example

```python
import time
import openapi_client
from openapi_client.api import luncho_api
from openapi_client.model.luncho_result import LunchoResult
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = luncho_api.LunchoApi(api_client)
    country_code = "JPN" # str |  (optional) if omitted the server will use the default value of "JPN"
    luncho_value = 100 # float |  (optional) if omitted the server will use the default value of 100

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Luncho
        api_response = api_instance.luncho(country_code=country_code, luncho_value=luncho_value)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling LunchoApi->luncho: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **country_code** | **str**|  | [optional] if omitted the server will use the default value of "JPN"
 **luncho_value** | **float**|  | [optional] if omitted the server will use the default value of 100

### Return type

[**LunchoResult**](LunchoResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

