# openapi_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**convert_from_luncho**](DefaultApi.md#convert_from_luncho) | **GET** /convert-from-luncho/ | Convert From Luncho
[**convert_from_luncho_all**](DefaultApi.md#convert_from_luncho_all) | **GET** /convert-from-luncho-all | Convert From Luncho All
[**convert_from_luncho_dummy**](DefaultApi.md#convert_from_luncho_dummy) | **GET** /convert-from-luncho-dummy/ | Convert From Luncho Dummy
[**countries**](DefaultApi.md#countries) | **GET** /countries | Countries
[**test**](DefaultApi.md#test) | **GET** /test/ | Test


# **convert_from_luncho**
> LunchoResult convert_from_luncho()

Convert From Luncho

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
        # Convert From Luncho
        api_response = api_instance.convert_from_luncho(country_code=country_code, luncho_value=luncho_value)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->convert_from_luncho: %s\n" % e)
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

# **convert_from_luncho_all**
> [LunchoResult] convert_from_luncho_all(luncho_value)

Convert From Luncho All

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
        # Convert From Luncho All
        api_response = api_instance.convert_from_luncho_all(luncho_value)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->convert_from_luncho_all: %s\n" % e)
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

# **convert_from_luncho_dummy**
> bool, date, datetime, dict, float, int, list, str, none_type convert_from_luncho_dummy(currency_code, luncho_value)

Convert From Luncho Dummy

### Example

```python
import time
import openapi_client
from openapi_client.api import default_api
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
    currency_code = "currency_code_example" # str | 
    luncho_value = 3.14 # float | 

    # example passing only required values which don't have defaults set
    try:
        # Convert From Luncho Dummy
        api_response = api_instance.convert_from_luncho_dummy(currency_code, luncho_value)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->convert_from_luncho_dummy: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **currency_code** | **str**|  |
 **luncho_value** | **float**|  |

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

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

# **countries**
> {str: (IMFPPPCountry,)} countries()

Countries

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

