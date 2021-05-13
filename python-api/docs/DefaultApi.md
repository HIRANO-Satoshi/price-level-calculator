# openapi_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**countries**](DefaultApi.md#countries) | **GET** /countries | Countries
[**lunchos**](DefaultApi.md#lunchos) | **GET** /lunchos | Lunchos
[**test**](DefaultApi.md#test) | **GET** /test/ | Test


# **countries**
> {str: (IMFPPPCountry,)} countries()

Countries

Returns country data for all countries.

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.imfppp_country import IMFPPPCountry
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Countries
        api_response = api_instance.countries()
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->countries: %s\n" % e)
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

# **lunchos**
> [LunchoResult] lunchos(luncho_value)

Lunchos

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
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
    api_instance = default_api.DefaultApi(api_client)
    luncho_value = 3.14 # float | 

    # example passing only required values which don't have defaults set
    try:
        # Lunchos
        api_response = api_instance.lunchos(luncho_value)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->lunchos: %s\n" % e)
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

# **test**
> LunchoResult test()

Test

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
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
    api_instance = default_api.DefaultApi(api_client)
    country_code = "JPN" # str |  (optional) if omitted the server will use the default value of "JPN"
    luncho_value = 100 # float |  (optional) if omitted the server will use the default value of 100

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Test
        api_response = api_instance.test(country_code=country_code, luncho_value=luncho_value)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->test: %s\n" % e)
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

