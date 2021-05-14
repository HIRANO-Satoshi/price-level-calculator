# luncho-python.LunchoApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**countries**](LunchoApi.md#countries) | **GET** /countries | Countries
[**luncho**](LunchoApi.md#luncho) | **GET** /luncho | Luncho
[**lunchos**](LunchoApi.md#lunchos) | **GET** /lunchos | Lunchos


# **countries**
> {str: (IMFPPPCountry,)} countries()

Countries

Returns country data for all countries.

### Example

```python
import time
import luncho-python
from luncho-python.api import luncho_api
from luncho-python.model.imfppp_country import IMFPPPCountry
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = luncho-python.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with luncho-python.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = luncho_api.LunchoApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Countries
        api_response = api_instance.countries()
        pprint(api_response)
    except luncho-python.ApiException as e:
        print("Exception when calling LunchoApi->countries: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**{str: (IMFPPPCountry,)}**](IMFPPPCountry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **luncho**
> LunchoResult luncho()

Luncho

### Example

```python
import time
import luncho-python
from luncho-python.api import luncho_api
from luncho-python.model.http_validation_error import HTTPValidationError
from luncho-python.model.luncho_result import LunchoResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = luncho-python.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with luncho-python.ApiClient() as api_client:
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
    except luncho-python.ApiException as e:
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

# **lunchos**
> [LunchoResult] lunchos(luncho_value)

Lunchos

### Example

```python
import time
import luncho-python
from luncho-python.api import luncho_api
from luncho-python.model.http_validation_error import HTTPValidationError
from luncho-python.model.luncho_result import LunchoResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = luncho-python.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with luncho-python.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = luncho_api.LunchoApi(api_client)
    luncho_value = 3.14 # float | 

    # example passing only required values which don't have defaults set
    try:
        # Lunchos
        api_response = api_instance.lunchos(luncho_value)
        pprint(api_response)
    except luncho-python.ApiException as e:
        print("Exception when calling LunchoApi->lunchos: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **luncho_value** | **float**|  |

### Return type

[**[LunchoResult]**](LunchoResult.md)

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

