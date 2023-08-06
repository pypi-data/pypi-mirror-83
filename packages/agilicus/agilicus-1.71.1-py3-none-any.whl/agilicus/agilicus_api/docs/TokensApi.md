# agilicus_api.TokensApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_introspect_token**](TokensApi.md#create_introspect_token) | **POST** /v1/tokens/introspect | Introspect a token
[**create_reissued_token**](TokensApi.md#create_reissued_token) | **POST** /v1/tokens/reissue | Issue a new token from another
[**create_revoke_token_task**](TokensApi.md#create_revoke_token_task) | **POST** /v1/tokens/revoke | Revoke a token
[**create_token**](TokensApi.md#create_token) | **POST** /v1/tokens | Create a token
[**create_token_validation**](TokensApi.md#create_token_validation) | **POST** /v1/tokens/validations | Validate a token request
[**list_tokens**](TokensApi.md#list_tokens) | **GET** /v1/tokens | Query tokens


# **create_introspect_token**
> Token create_introspect_token(token_introspect)

Introspect a token

Introspect a token

### Example

```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with agilicus_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.TokensApi(api_client)
    token_introspect = agilicus_api.TokenIntrospect() # TokenIntrospect | Token to introspect

    try:
        # Introspect a token
        api_response = api_instance.create_introspect_token(token_introspect)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_introspect_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_introspect** | [**TokenIntrospect**](TokenIntrospect.md)| Token to introspect | 

### Return type

[**Token**](Token.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Traffic token |  -  |
**410** | Token has been revoked |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_reissued_token**
> RawToken create_reissued_token(token_reissue_request)

Issue a new token from another

Issues a new token with the same or reduced scope to the one presented. Use this to retrieve a token for accessing a different organisation than the one you're currently operating on. Note that the presented token remains valid if it already was. If it is not valid, or the you do not have permissions in the requested organisation, the request will fail. The token will expire at the same time as the presented token. 

### Example

```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with agilicus_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.TokensApi(api_client)
    token_reissue_request = agilicus_api.TokenReissueRequest() # TokenReissueRequest | The token request

    try:
        # Issue a new token from another
        api_response = api_instance.create_reissued_token(token_reissue_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_reissued_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_reissue_request** | [**TokenReissueRequest**](TokenReissueRequest.md)| The token request | 

### Return type

[**RawToken**](RawToken.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The token was succesfully issued. It is contained in the response.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_revoke_token_task**
> create_revoke_token_task(token_revoke)

Revoke a token

Revoke a token

### Example

```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with agilicus_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.TokensApi(api_client)
    token_revoke = agilicus_api.TokenRevoke() # TokenRevoke | Token to revoke

    try:
        # Revoke a token
        api_instance.create_revoke_token_task(token_revoke)
    except ApiException as e:
        print("Exception when calling TokensApi->create_revoke_token_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_revoke** | [**TokenRevoke**](TokenRevoke.md)| Token to revoke | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | token has been revoked |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_token**
> RawToken create_token(create_token_request)

Create a token

Create a token

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.TokensApi(api_client)
    create_token_request = agilicus_api.CreateTokenRequest() # CreateTokenRequest | Rule to sign

    try:
        # Create a token
        api_response = api_instance.create_token(create_token_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_token_request** | [**CreateTokenRequest**](CreateTokenRequest.md)| Rule to sign | 

### Return type

[**RawToken**](RawToken.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully signed assertion |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_token_validation**
> CreateTokenRequest create_token_validation(create_token_request)

Validate a token request

Validate a token request prior to creating a token. This verifies the user has permission to access the scopes requested

### Example

```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with agilicus_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.TokensApi(api_client)
    create_token_request = agilicus_api.CreateTokenRequest() # CreateTokenRequest | Token to validate

    try:
        # Validate a token request
        api_response = api_instance.create_token_validation(create_token_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_token_validation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_token_request** | [**CreateTokenRequest**](CreateTokenRequest.md)| Token to validate | 

### Return type

[**CreateTokenRequest**](CreateTokenRequest.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully validated token request. The user has permission to access specified scopes |  -  |
**403** | Token request is invalid |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_tokens**
> ListTokensResponse list_tokens(limit=limit, sub=sub, exp_from=exp_from, exp_to=exp_to, iat_from=iat_from, iat_to=iat_to, jti=jti, org=org, revoked=revoked)

Query tokens

Query tokens

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.TokensApi(api_client)
    limit = 100 # int | limit the number of rows in the response (optional) (default to 100)
sub = 'sub_example' # str | search criteria sub (optional)
exp_from = 'exp_from_example' # str | search criteria expired from using dateparser (optional)
exp_to = 'exp_to_example' # str | search criteria expired to using dateparser (optional)
iat_from = 'iat_from_example' # str | search criteria issued from using dateparser (optional)
iat_to = 'iat_to_example' # str | search criteria issued to using dateparser (optional)
jti = 'jti_example' # str | search criteria using jti (optional)
org = 'org_example' # str | search criteria using org (optional)
revoked = True # bool | search criteria for revoked tokens (optional)

    try:
        # Query tokens
        api_response = api_instance.list_tokens(limit=limit, sub=sub, exp_from=exp_from, exp_to=exp_to, iat_from=iat_from, iat_to=iat_to, jti=jti, org=org, revoked=revoked)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->list_tokens: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 100]
 **sub** | **str**| search criteria sub | [optional] 
 **exp_from** | **str**| search criteria expired from using dateparser | [optional] 
 **exp_to** | **str**| search criteria expired to using dateparser | [optional] 
 **iat_from** | **str**| search criteria issued from using dateparser | [optional] 
 **iat_to** | **str**| search criteria issued to using dateparser | [optional] 
 **jti** | **str**| search criteria using jti | [optional] 
 **org** | **str**| search criteria using org | [optional] 
 **revoked** | **bool**| search criteria for revoked tokens | [optional] 

### Return type

[**ListTokensResponse**](ListTokensResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return traffic tokens list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

