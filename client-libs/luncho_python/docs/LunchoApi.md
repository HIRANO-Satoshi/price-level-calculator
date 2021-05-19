# luncho_python.LunchoApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**all_luncho_data**](LunchoApi.md#all_luncho_data) | **GET** /v1/all-luncho-data | All Luncho Data
[**countries**](LunchoApi.md#countries) | **GET** /v1/countries | Countries
[**health**](LunchoApi.md#health) | **GET** /v1/health | Health
[**luncho_data**](LunchoApi.md#luncho_data) | **GET** /v1/luncho-data | Luncho Data


# **all_luncho_data**
> {str: (LunchoData,)} all_luncho_data()

All Luncho Data

Returns A dict of LunchoDatas for all supported countries. Data size is about 40KB.

### Example

```python
import time
import luncho_python
from luncho_python.api import luncho_api
from luncho_python.model.luncho_data import LunchoData
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = luncho_python.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with luncho_python.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = luncho_api.LunchoApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # All Luncho Data
        api_response = api_instance.all_luncho_data()
        pprint(api_response)
    except luncho_python.ApiException as e:
        print("Exception when calling LunchoApi->all_luncho_data: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**{str: (LunchoData,)}**](LunchoData.md)

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

# **countries**
> {str: (str,)} countries()

Countries

  Returns a dict of supported country codes and names so that you can show a dropdown list of countries. Data size is about 3.5KB.    E.g. {'JP': 'Japan', 'US': 'United States'...}.     If data for a country is not available, either its ppp or exchange_rate is 0.

### Example

```python
import time
import luncho_python
from luncho_python.api import luncho_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = luncho_python.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with luncho_python.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = luncho_api.LunchoApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Countries
        api_response = api_instance.countries()
        pprint(api_response)
    except luncho_python.ApiException as e:
        print("Exception when calling LunchoApi->countries: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**{str: (str,)}**

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

# **health**
> bool, date, datetime, dict, float, int, list, str, none_type health()

Health

Do nothing other than telling it's OK.

### Example

```python
import time
import luncho_python
from luncho_python.api import luncho_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = luncho_python.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with luncho_python.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = luncho_api.LunchoApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Health
        api_response = api_instance.health()
        pprint(api_response)
    except luncho_python.ApiException as e:
        print("Exception when calling LunchoApi->health: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **luncho_data**
> LunchoData luncho_data(country_code)

Luncho Data

Returns LunchoData that is needed to convert between Luncho and local currency of the countryCode.   If data for the country is not available either ppp or exchange_rate is 0. Data size is about 400 bytes.

### Example

```python
import time
import luncho_python
from luncho_python.api import luncho_api
from luncho_python.model.http_validation_error import HTTPValidationError
from luncho_python.model.luncho_data import LunchoData
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = luncho_python.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with luncho_python.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = luncho_api.LunchoApi(api_client)
    country_code = "country_code_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Luncho Data
        api_response = api_instance.luncho_data(country_code)
        pprint(api_response)
    except luncho_python.ApiException as e:
        print("Exception when calling LunchoApi->luncho_data: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **country_code** | **str**|  |

### Return type

[**LunchoData**](LunchoData.md)

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

