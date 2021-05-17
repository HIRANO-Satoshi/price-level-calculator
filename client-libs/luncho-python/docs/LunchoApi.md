# luncho-python.LunchoApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**country_codes**](LunchoApi.md#country_codes) | **GET** /country-codes | Countrycodes
[**luncho_data**](LunchoApi.md#luncho_data) | **GET** /luncho-data | Lunchodata
[**luncho_datas**](LunchoApi.md#luncho_datas) | **GET** /luncho-datas | Lunchodatas


# **country_codes**
> [str] country_codes()

Countrycodes

Returns a list of supported country codes.

### Example

```python
import time
import luncho-python
from luncho-python.api import luncho_api
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
        # Countrycodes
        api_response = api_instance.country_codes()
        pprint(api_response)
    except luncho-python.ApiException as e:
        print("Exception when calling LunchoApi->country_codes: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**[str]**

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
> LunchoData luncho_data()

Lunchodata

Returns LunchoData that is needed to convert between Luncho and local currency of the countryCode. If the countryCode is not specified, estimate it from IP address.

### Example

```python
import time
import luncho-python
from luncho-python.api import luncho_api
from luncho-python.model.http_validation_error import HTTPValidationError
from luncho-python.model.luncho_data import LunchoData
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
    country_code = "country_code_example" # str |  (optional)
    client_region = "client-region_example" # str |  (optional)
    cloudfront_viewer_country = "cloudfront-viewer-country_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Lunchodata
        api_response = api_instance.luncho_data(country_code=country_code, client_region=client_region, cloudfront_viewer_country=cloudfront_viewer_country)
        pprint(api_response)
    except luncho-python.ApiException as e:
        print("Exception when calling LunchoApi->luncho_data: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **country_code** | **str**|  | [optional]
 **client_region** | **str**|  | [optional]
 **cloudfront_viewer_country** | **str**|  | [optional]

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

# **luncho_datas**
> [LunchoData] luncho_datas()

Lunchodatas

Returns A list of LunchoDatas for all supported countries.

### Example

```python
import time
import luncho-python
from luncho-python.api import luncho_api
from luncho-python.model.luncho_data import LunchoData
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
        # Lunchodatas
        api_response = api_instance.luncho_datas()
        pprint(api_response)
    except luncho-python.ApiException as e:
        print("Exception when calling LunchoApi->luncho_datas: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[LunchoData]**](LunchoData.md)

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

