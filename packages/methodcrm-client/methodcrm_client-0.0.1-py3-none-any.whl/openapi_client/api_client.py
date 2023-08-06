# coding: utf-8
"""
    Method REST API

    # Getting Started  Method's REST API gives the ability to create, update, retrieve and delete data from a Method account. It's a simple yet powerful way for programmers to integrate their applications with Method. It has predictable resource URLs and returns HTTP response codes. It also accepts and returns JSON in the HTTP body. You can use your favorite HTTP/REST library for your programming language to use our API.    In case if you would like to test the Method API before beginning your integration we have made some Postman collections available.  - [Postman Collection for OAuth2 Authentication.](../assets/method-identity-server.postman_collection.json)  - [Postman Collection for Method REST API.](../assets/method-restapi.postman_collection.json)    ## Step 1: Choose the Authentication Method  Choose the authentication method based on the application type.      | Application Type | Description | Authentication Method |  |----------|----------|----------|  | **Java Script** | Applications that run exclusively on a browser and are independent of a web server. | [OAuth2: Implicit Flow.](#section/Authentication/OAuth2:-Implicit-Flow-(Coming-Soon)) |  | **Server-Side (or \"web\")** | Applications that are clients running on a dedicated HTTP server. | [OAuth2: Authorization Code Flow.](#section/Authentication/OAuth2:-Authorization-Code-Flow) |  | **Mobile** | Applications that are installed on smart phones and tablets | [OAuth2: Authorization Code Flow.](#section/Authentication/OAuth2:-Authorization-Code-Flow) |  | **Background** | Applications that perform back-end jobs, have no user context or no-manual intervention. | [OAuth2: Client Credentials Flow](#section/Authentication/OAuth2:-Client-Credentials-Flow) or [API Key](#section/Authentication/API-Key). We recommend using OAuth2 - Client Credentials Flow for better security. |    ## Step 2: Setup Authentication  Based on the chosen authentication method, register OAuth2 client for your application, or create an API Key for your account.    We are working on automating the process of OAuth2 client registration.    ### Register OAuth2 client  To register Oauth2 client, send the following information to [api@method.me](mailto:api@method.me) with subject `REST API | OAuth2 Client Request`  - Redirect Url. : Not required for [OAuth2: Client Credentials Flow](#section/Authentication/OAuth2:-Client-Credentials-Flow)  - Application Type.  - Method Account Name.     ### Create API Key  Creation of an API Key can be done directly through your Method Account from the API Integration page  1. **[Log in](https://signin.method.me \"Method\")** to the Method Account you wish to generate an API key for    2. Click the upper-right **blue circle icon** and then select **Integrations**        ![Integrations Preference Menu](../assets/PrefsIntegrations.png \"Integrations Preferences\")    3. Click on **API** from the Integrations list    4. Click on **New** next to the section titled **API keys**    5. Enter a name for your API Key, and click on **Generate API Key**        ![New APIKey Wizard](../assets/newAPIKey.png \"New API Key\")  > 📌 __**Note**__ The Name you enter for your API Key is for display purposes only - To help you distinguish multiple API Keys from one another. It is not used in the Authentication process.         6. An API Key should now be visible for you on the screen. Make sure you Copy this key and keep it safe! **This is the only time it will ever be displayed to you**        ![Generated APIKey](../assets/GeneratedAPIKey.jpg \"Generated API Key\")        ## Step 3: Request OAuth2 Access Token  Request OAuth2 Access Token. See steps to request an access token for the appropriate flow.  - [OAuth2: Authorization Code Flow](#section/Authentication/OAuth2:-Authorization-Code-Flow)  - [OAuth2: Implicit Flow](#section/Authentication/OAuth2:-Implicit-Flow-(Coming-Soon))  - [OAuth2: Client Credentials Flow](#section/Authentication/OAuth2:-Client-Credentials-Flow)    ## Step 4: Make Authenticated Requests  Include OAuth2 Access Token or API Key in the header.    ### OAuth2  Include OAuth2 Access Token in HTTP `Authorization` header as `Bearer <access_token>`.  Example:    ```http  GET /api/v1/tables/Contacts/5 HTTP/1.1  Host: https://rest.method.me  Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7  ```    ### API Key  Include API Key in HTTP `Authorization` header as `APIKey <apikey>`.  Example:      ```http  GET /api/v1/tables/Contacts HTTP/1.1  Host: https://rest.method.me  Authorization: APIKey eyJhbGciOiJSUzI1NiIsImtpZCI  ```    # Authentication  The Method API uses the OAuth2.0 protocol for authentication.   It is an industry-standard protocol specification that enables third-party applications (clients) to gain delegated access to protected resources in Method via API.    **Why should we use OAuth2?**  - Clients are not required to support password authentication or store user credentials.  - Clients gain delegated access, i.e., access only to resources authenticated by the user.  - Users can revoke the client's delegated access anytime.  - OAuth2.0 access tokens expire after a set time. If the client faces a security breach, user data will be compromised only until the access token is valid.    **Terminologies**    The following are some terms you need to know before you start using the Method APIs.  - **Protected resources**: The Method resources, such as Contacts, Activities, Invoice, etc.  - **Resource server**: Method server that hosts protected resources. In this case, it will be Method REST API server.  - **Resource owner**: Any end-user of your account, who can grant access to the protected resources.  - **Client**: An application that sends requests to the resource server to access the protected resources on behalf of the end-user.  - **Client ID**: The consumer key generated from the connected application.  - **Client Secret**: The consumer secret generated from the connected application.  - **Authentication server**: Authorization server provides the necessary credentials (such as Access and Refresh tokens) to the client. In this case, it will be the Method Identity Server.  - **Authentication code**: The authorization server creates a temporary token and sends it to the client via the browser. The client will send this code to the authorization server to obtain access and refresh tokens.  - Tokens      - **Access Token**: A token that is sent to the resource server to access the protected resources of the user. The Access token provides secure and temporary access to Method REST APIs and is used by the applications to make requests to the connected app. Each access token will be valid only for an hour and can be used only for the set of operations that are described in the scope.      - **Refresh Token**: A token that can be used to obtain new access tokens. This token has an unlimited lifetime until it is revoked by the end-user.  - **Scopes**: Control the type of resource that the client application can access. Tokens are usually created with various scopes to ensure improved security.  Currently supported/required scopes are as follows:      - `openid` Required, to request access to user id, token issued at time and token expiry time      - `profile` Optional, to request access to user profile information like name, lastname etc      - `email` Optional, to request access to user's email address information      - `api` Required, to request access to Method REST API        ## OAuth2: Authorization Code Flow  If you are building a server-side (or \"web\") application that is capable of securely storing secrets, then the authorization code flow is the recommended method for controlling access to it.  At a high-level, this flow has the following steps:  1. Your application directs the browser to the Method Sign-In page, where the user authenticates.        Example: URL generated by your application to direct a browser to Sign-In page        ```url      https://auth.method.me/connect/authorize      ?client_id={your_client_id}      &nonce=d1f3f984-db5d-443c-a883-36f06f252d96      &redirect_uri={your_redirect_url}      &response_type=code      &scope=openid profile email api offline_access      &state=      ```        > 📌 __**Note**__ For Method users linked to multiple accounts the Method sign-in page will allow you to select which account you want to authenticate. The token you receive at the end of this flow will only be valid for the account you selected. Any requests made using this token will always affect the selected account. To connect to another account you must request a separate token for that account.      2. The browser receives an authorization code from Method Identity Server.        Example: URL with authorization code in `code` query parameter        ```url      {your_redirect_url}      ?code=7bfbe93c9712414f7c53766e2e6399      &scope=openid%20profile%20email%20api%20offline_access      &session_state=l0ckSo5h_GPR_2bicxnUaY_vRr5FRYDAzxQmkI2N2mI.97ac90c0b2eb3b44242aa75a8b3961fb      ```    3. The authorization code is passed to your application.  4. Your application sends this code to Method Identity Server, and Method Identity Server returns access token ID token, and optionally a refresh token.        Example:             Request        ```http      POST /connect/token HTTP/1.1      Host: https://auth.methodlocal.com      Content-Type: application/x-www-form-urlencoded        code=7bfbe93c9712414f7c53766e2e6399      &redirect_uri={your_redirect_url}      &grant_type=authorization_code      &client_id={your_client_id}      &client_secret={your_client_secret}      ```            Response        ```json      {          \"id_token\": \"eyJhbGciOiJSUzI1NiIsImtpZCI\",          \"access_token\": \"eyJhbGciOiJSUzI1NiIsImtpZCI6\",          \"expires_in\": 3600,          \"token_type\": \"Bearer\",          \"refresh_token\": \"b4f33ac42b668f00803305aa7f038\"      }      ```       5. Your application can now use the access token to call the Method REST API on behalf of the user.    ```http      GET /api/v1/tables/Contacts HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI    ```    ## OAuth2: Implicit Flow (Coming Soon)  If you are building a Single-Page Application (SPA) then the Implicit flow is the recommended method for controlling access between your SPA and a resource server. The Implicit flow is intended for applications where the confidentiality of the client secret can't be guaranteed. In this flow, the client doesn't make a request to the /token endpoint but instead receives the access token directly from the /authorize endpoint. The client must be capable of interacting with the resource owner's user-agent and capable of receiving incoming requests (through redirection) from the authorization server.  At a high level, the Implicit flow has the following steps:    1. Your application directs the browser to the Method Sign-In Page, where the user authenticates. Method Identity Server redirects the browser back to the specified redirect URI, along with access and ID tokens as a hash fragment in the URI.    > 📌 __**Note**__ For Method users linked to multiple accounts the Method sign-in page will allow you to select which account you want to authenticate. The token you receive at the end of this flow will only be valid for the account you selected. Any requests made using this token will always affect the selected account. To connect to another account you must request a separate token for that account.    2. Your application extracts the tokens from the URI.  3. Your application can now use these tokens to call the Method REST API on behalf of the user.    ## OAuth2: Client Credentials Flow  The Client Credentials flow is recommended for use in machine-to-machine authentication.   Your application will need to securely store its Client ID and Secret and pass those to Method Identity Server in exchange for an access token.   At a high-level, the flow only has two steps:  1. Your application passes its client credentials to your Method Identity Server.      Example:            Request            ````http      POST /connect/token HTTP/1.1      Host: https://auth.method.me      Content-Type: application/x-www-form-urlencoded        grant_type=client_credentials      &client_id={your_client_id}      &client_secret={your_client_secret}      ````            Response        ````json      {          \"access_token\": \"eyJhbGciOiJSUzI1NiIsImtpZCI\",          \"expires_in\": 3600,          \"token_type\": \"Bearer\"      }      ````          2. Your application can now use the access token to call the Method API.    ```http      GET /api/v1/tables/Contacts HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI    ```          ## API Key  API Key authentication is the easiest of the authentication method to use in machine-to-machine authentication. At a high-level, the flow has 2 steps:  1. [Generate an API key for your account](#section/Getting-Started/Step-2:-Setup-Authentication).  2. Use the API Key in your application to call the Method API.      ```http      GET /api/v1/tables/Contacts HTTP/1.1      Host: https://rest.method.me      Authorization: APIKey eyJhbGciOiJSUzI1NiIsImtpZCI    ```    # HTTP Request Methods  | Method | Description                              |  |--------|------------------------------------------|  | GET    | To retrieve data/resource from the resource server. |  | POST   | To insert or upload any new resource to the server. |  | PUT    | To update an existing resource. This replaces the target resource with the updated content. |  | PATCH  | To update a specific detail of the resource. This method updates the target resource with the provided content without changing other data. |  | DELETE | To delete a resource at a particular location. |    # HTTP Status Codes    | Status Codes | Meaning                  | Description                              |  |--------------|--------------------------|------------------------------------------|  | 200          | OK                       | The API request is successful.           |  | 201          | CREATED                  | Resource created. Ex. Contact created. |  | 204          | NO CONTENT               | There is no content available for the request. Usually, for DELETE, PUT, or PATCH methods. |  | 400          | BAD REQUEST              | The request is invalid. Required fields are missing or related records exceeded the maximum limit. |  | 401          | AUTHORIZATION ERROR      | Invalid API key or Access Token. e.g. Access Token expired.               |  | 403          | FORBIDDEN                | No permission to do the operation. e.g. Token is valid but user does not have necessary permission.       |  | 404          | NOT FOUND                | Invalid request. e.g. Record or Table not found.                         |  | 405          | METHOD NOT ALLOWED       | The specified method is not allowed.     |  | 413          | REQUEST ENTITY TOO LARGE | The server did not accept the request while uploading a file, since the limited file size has exceeded. |  | 415          | UNSUPPORTED MEDIA TYPE   | The server did not accept the request while uploading a file, since the media/ file type is not supported. |  | 429          | TOO MANY REQUESTS        | Number of API requests for the time period has exceeded. |  | 500          | INTERNAL SERVER ERROR    | Generic error that is encountered due to an unexpected server error. |    # API Limits  For a fair usage of our API, we will be limiting requests on an account basis as follows.  - 100 requests per minute per account.   - 5000 + [1000 * Number of Active licenses] (or) 25000 requests per day per account whichever is lower.     Example - If an account has 15 active licenses then the daily limit is 20000 requests calculated as 5000 + [1000 * 15].   If an account has 30 active licenses then the daily limit is 25000 requests,   as the calculated value of 5000 + [1000 * 30] is 35000 which is greater than our maximum daily limit of 25000.    Once this limit has been reached, calls will return error with status code 429.   The response header will contain the number of seconds after which the limit will be reset.   This rate limit is evaluated on a rolling window basis.   Below is a sample response, that indicates that per day(24h) limit is breached and you should retry after 7200 seconds (2 hours).      ```http      HTTP/1.1 429 Too Many Requests      Content-Type: text/plain      Retry-After: 7200      Date: Tue, 02 Jun 2020 13:34:48 GMT      Content-Length: 56        API calls quota exceeded! maximum admitted 6000 per 1d.    ```    # Filter Reference  You must use the appropriate notation for different data types with filter expressions.  - String values must be delimited by single quotation marks.  - Date-Time values must be delimited by single quotation marks and follow the ISO-8601 date-time format.       Complete date plus hours, minutes and seconds:        YYYY-MM-DDThh:mm[:ss][TZD] (eg 2020-03-29T10:05:45-06:00)    Where:        - YYYY = four-digit year      - MM = two-digit month (eg 03=March)      - DD = two-digit day of the month (01 through 31)      - T = a set character indicating the start of the time element      - hh = two digits of an hour (00 through 23, AM/PM not included)      - mm = two digits of a minute (00 through 59)      - ss = two digits of a second (00 through 59). Optional      - TZD = time zone designator (Z or +hh:mm or -hh:mm), the + or - values indicate how far ahead or behind a time zone is from the UTC (Coordinated Universal Time) zone.        Time zone designator is optional and if left out then date-time is assumed to be UTC.       Examples          - To get all Invoices created on April 17, 2020, EDT (Eastern Daylight Time)             ```http      GET /api/v1/tables/Invoice?filter=TimeCreated ge '2020-04-17T00:00-04:00' and TimeCreated lt '2020-04-18T00:00-04:00' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSU            or            GET /api/v1/tables/Invoice?filter=TimeCreated ge '2020-04-17T04:00' and TimeCreated lt '2020-04-18T04:00' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSU        or            GET /api/v1/tables/Invoice?filter=TimeCreated ge '2020-04-17T04:00Z' and TimeCreated lt '2020-04-18T04:00Z' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSU      ```           - To get all Invoices created in April 2020 EDT (Eastern Daylight Time)        ```http      GET /api/v1/tables/Invoice?filter=TimeCreated ge '2020-04-01T00:00-04:00' and TimeCreated lt '2020-05-01T00:00-04:00' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSU      ```    - Numeric values require no delimiters.    You can use the following expressions to construct a filter in Method REST API.    | Filter Operation | Example | Explanation |   |------------------------------------------|------------------------------------------|------------------------------------------|  | **Comparison Operators** |  | `eq` Equal | filter=FirstName eq 'Bill' |  Query on Contacts table. Returns Contacts with FirstName equal to 'Bill' |  | `lt` Less than | filter=TotalBalance lt 100 | Query on Contacts . Returns all Contacts with a balance lower than 100. |  | `gt` Greater than | filter=TotalBalance gt 100 | Query on Contacts . Returns all Contacts with a balance greater than 100. |  | `ge` Greater than or equal to | filter=TotalBalance ge 100 | Query on Contacts . Returns all Contacts with a balance 100 and greater. |  | `le` Less than or equal to | filter=TotalBalance le 100 | Query on Contacts . Returns all Contacts with a balance 100 and lower. |  | `ne` Different from (not equal) | filter=TotalBalance ne 0 | Query on Contacts . Returns all Contacts with a non-zero balance. |  | **Logical Operators** |  | `and` And | filter=FirstName eq 'Bill' and LastName eq 'Wagner' | Query on Contacts table. Returns Contacts with FirstName equal to 'Bill' and LastName equal to 'Wagner' |  | `or` Or | filter=BillAddressCountry eq 'Canada' or BillAddressCountry eq 'USA' | Query on Contacts table. Returns Contacts in Canada and the United States. |  |`not` Not | filter=not (BillAddressCountry eq 'Canada' or BillAddressCountry eq 'USA') | Query on Contacts table. Returns Contacts outside of Canada and the United States. |  | **String Functions** |  |  `endswith` String ends with | filter=endswith(Name,'RT') | Query on Contacts table. Returns all Contacts with names ending with 'RT'. |  | `startswith` String starts with | filter=startswith(Name, 'S') | Query on Contacts table. Returns all Contacts with names beginning with 'S'. |  | `contains` String containing | filter=contains(Name, 'RT') | Query on Contacts table. Returns all Contacts with names containing 'RT' |  | `()` Grouping | filter=(not (BillAddressCountry eq 'Canada' or BillAddressCountry eq 'USA')) and (TotalBalance ge 100) | Query on Contacts table. Returns all Contacts outside Canada and the United States with Balance 100 and greater |    # noqa: E501

    The version of the OpenAPI document: 1.0
    Contact: support@method.me
    Generated by: https://openapi-generator.tech
"""

from __future__ import absolute_import

import atexit
import datetime
from dateutil.parser import parse
import json
import mimetypes
from multiprocessing.pool import ThreadPool
import os
import re
import tempfile

# python 2 and python 3 compatibility library
import six
from six.moves.urllib.parse import quote

from openapi_client.configuration import Configuration
import openapi_client.models
from openapi_client import rest
from openapi_client.exceptions import ApiValueError, ApiException


class ApiClient(object):
    """Generic API client for OpenAPI client library builds.

    OpenAPI generic API client. This client handles the client-
    server communication, and is invariant across implementations. Specifics of
    the methods and models for each application are generated from the OpenAPI
    templates.

    NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech
    Do not edit the class manually.

    :param configuration: .Configuration object for this client
    :param header_name: a header to pass when making calls to the API.
    :param header_value: a header value to pass when making calls to
        the API.
    :param cookie: a cookie to include in the header when making calls
        to the API
    :param pool_threads: The number of threads to use for async requests
        to the API. More threads means more concurrent API requests.
    """

    PRIMITIVE_TYPES = (float, bool, bytes, six.text_type) + six.integer_types
    NATIVE_TYPES_MAPPING = {
        'int': int,
        'long': int if six.PY3 else long,  # noqa: F821
        'float': float,
        'str': str,
        'bool': bool,
        'date': datetime.date,
        'datetime': datetime.datetime,
        'object': object,
    }
    _pool = None

    def __init__(self, configuration=None, header_name=None, header_value=None,
                 cookie=None, pool_threads=1):
        if configuration is None:
            configuration = Configuration.get_default_copy()
        self.configuration = configuration
        self.pool_threads = pool_threads

        self.rest_client = rest.RESTClientObject(configuration)
        self.default_headers = {}
        if header_name is not None:
            self.default_headers[header_name] = header_value
        self.cookie = cookie
        # Set default User-Agent.
        self.user_agent = 'OpenAPI-Generator/1.0.0/python'
        self.client_side_validation = configuration.client_side_validation

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self._pool:
            self._pool.close()
            self._pool.join()
            self._pool = None
            if hasattr(atexit, 'unregister'):
                atexit.unregister(self.close)

    @property
    def pool(self):
        """Create thread pool on first request
         avoids instantiating unused threadpool for blocking clients.
        """
        if self._pool is None:
            atexit.register(self.close)
            self._pool = ThreadPool(self.pool_threads)
        return self._pool

    @property
    def user_agent(self):
        """User agent for this API client"""
        return self.default_headers['User-Agent']

    @user_agent.setter
    def user_agent(self, value):
        self.default_headers['User-Agent'] = value

    def set_default_header(self, header_name, header_value):
        self.default_headers[header_name] = header_value

    def __call_api(
            self, resource_path, method, path_params=None,
            query_params=None, header_params=None, body=None, post_params=None,
            files=None, response_types_map=None, auth_settings=None,
            _return_http_data_only=None, collection_formats=None,
            _preload_content=True, _request_timeout=None, _host=None,
            _request_auth=None):

        config = self.configuration

        # header parameters
        header_params = header_params or {}
        header_params.update(self.default_headers)
        if self.cookie:
            header_params['Cookie'] = self.cookie
        if header_params:
            header_params = self.sanitize_for_serialization(header_params)
            header_params = dict(self.parameters_to_tuples(header_params,
                                                           collection_formats))

        # path parameters
        if path_params:
            path_params = self.sanitize_for_serialization(path_params)
            path_params = self.parameters_to_tuples(path_params,
                                                    collection_formats)
            for k, v in path_params:
                # specified safe chars, encode everything
                resource_path = resource_path.replace(
                    '{%s}' % k,
                    quote(str(v), safe=config.safe_chars_for_path_param)
                )

        # query parameters
        if query_params:
            query_params = self.sanitize_for_serialization(query_params)
            query_params = self.parameters_to_tuples(query_params,
                                                     collection_formats)

        # post parameters
        if post_params or files:
            post_params = post_params if post_params else []
            post_params = self.sanitize_for_serialization(post_params)
            post_params = self.parameters_to_tuples(post_params,
                                                    collection_formats)
            post_params.extend(self.files_parameters(files))

        # auth setting
        self.update_params_for_auth(
            header_params, query_params, auth_settings,
            request_auth=_request_auth)

        # body
        if body:
            body = self.sanitize_for_serialization(body)

        # request url
        if _host is None:
            url = self.configuration.host + resource_path
        else:
            # use server/host defined in path or operation instead
            url = _host + resource_path

        try:
            # perform request and return response
            response_data = self.request(
                method, url, query_params=query_params, headers=header_params,
                post_params=post_params, body=body,
                _preload_content=_preload_content,
                _request_timeout=_request_timeout)
        except ApiException as e:
            e.body = e.body.decode('utf-8') if six.PY3 else e.body
            raise e

        content_type = response_data.getheader('content-type')

        self.last_response = response_data

        return_data = response_data

        if not _preload_content:
            return return_data
        
        response_type = response_types_map.get(response_data.status, None)

        if six.PY3 and response_type not in ["file", "bytes"]:
            match = None
            if content_type is not None:
                match = re.search(r"charset=([a-zA-Z\-\d]+)[\s\;]?", content_type)
            encoding = match.group(1) if match else "utf-8"
            response_data.data = response_data.data.decode(encoding)

        # deserialize response data
        
        if response_type:
            return_data = self.deserialize(response_data, response_type)
        else:
            return_data = None

        if _return_http_data_only:
            return (return_data)
        else:
            return (return_data, response_data.status,
                    response_data.getheaders())

    def sanitize_for_serialization(self, obj):
        """Builds a JSON POST object.

        If obj is None, return None.
        If obj is str, int, long, float, bool, return directly.
        If obj is datetime.datetime, datetime.date
            convert to string in iso8601 format.
        If obj is list, sanitize each element in the list.
        If obj is dict, return the dict.
        If obj is OpenAPI model, return the properties dict.

        :param obj: The data to serialize.
        :return: The serialized form of data.
        """
        if obj is None:
            return None
        elif isinstance(obj, self.PRIMITIVE_TYPES):
            return obj
        elif isinstance(obj, list):
            return [self.sanitize_for_serialization(sub_obj)
                    for sub_obj in obj]
        elif isinstance(obj, tuple):
            return tuple(self.sanitize_for_serialization(sub_obj)
                         for sub_obj in obj)
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()

        if isinstance(obj, dict):
            obj_dict = obj
        else:
            # Convert model obj to dict except
            # attributes `openapi_types`, `attribute_map`
            # and attributes which value is not None.
            # Convert attribute name to json key in
            # model definition for request.
            obj_dict = {obj.attribute_map[attr]: getattr(obj, attr)
                        for attr, _ in six.iteritems(obj.openapi_types)
                        if getattr(obj, attr) is not None}

        return {key: self.sanitize_for_serialization(val)
                for key, val in six.iteritems(obj_dict)}

    def deserialize(self, response, response_type):
        """Deserializes response into an object.

        :param response: RESTResponse object to be deserialized.
        :param response_type: class literal for
            deserialized object, or string of class name.

        :return: deserialized object.
        """
        # handle file downloading
        # save response body into a tmp file and return the instance
        if response_type == "file":
            return self.__deserialize_file(response)

        # fetch data from response object
        try:
            data = json.loads(response.data)
        except ValueError:
            data = response.data

        return self.__deserialize(data, response_type)

    def __deserialize(self, data, klass):
        """Deserializes dict, list, str into an object.

        :param data: dict, list or str.
        :param klass: class literal, or string of class name.

        :return: object.
        """
        if data is None:
            return None

        if type(klass) == str:
            if klass.startswith('list['):
                sub_kls = re.match(r'list\[(.*)\]', klass).group(1)
                return [self.__deserialize(sub_data, sub_kls)
                        for sub_data in data]

            if klass.startswith('dict('):
                sub_kls = re.match(r'dict\(([^,]*), (.*)\)', klass).group(2)
                return {k: self.__deserialize(v, sub_kls)
                        for k, v in six.iteritems(data)}

            # convert str to class
            if klass in self.NATIVE_TYPES_MAPPING:
                klass = self.NATIVE_TYPES_MAPPING[klass]
            else:
                klass = getattr(openapi_client.models, klass)

        if klass in self.PRIMITIVE_TYPES:
            return self.__deserialize_primitive(data, klass)
        elif klass == object:
            return self.__deserialize_object(data)
        elif klass == datetime.date:
            return self.__deserialize_date(data)
        elif klass == datetime.datetime:
            return self.__deserialize_datetime(data)
        else:
            return self.__deserialize_model(data, klass)

    def call_api(self, resource_path, method,
                 path_params=None, query_params=None, header_params=None,
                 body=None, post_params=None, files=None,
                 response_types_map=None, auth_settings=None,
                 async_req=None, _return_http_data_only=None,
                 collection_formats=None,_preload_content=True,
                  _request_timeout=None, _host=None, _request_auth=None):
        """Makes the HTTP request (synchronous) and returns deserialized data.

        To make an async_req request, set the async_req parameter.

        :param resource_path: Path to method endpoint.
        :param method: Method to call.
        :param path_params: Path parameters in the url.
        :param query_params: Query parameters in the url.
        :param header_params: Header parameters to be
            placed in the request header.
        :param body: Request body.
        :param post_params dict: Request post form parameters,
            for `application/x-www-form-urlencoded`, `multipart/form-data`.
        :param auth_settings list: Auth Settings names for the request.
        :param response: Response data type.
        :param files dict: key -> filename, value -> filepath,
            for `multipart/form-data`.
        :param async_req bool: execute request asynchronously
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param collection_formats: dict of collection formats for path, query,
            header, and post parameters.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_token: dict, optional
        :return:
            If async_req parameter is True,
            the request will be called asynchronously.
            The method will return the request thread.
            If parameter async_req is False or missing,
            then the method will return the response directly.
        """
        if not async_req:
            return self.__call_api(resource_path, method,
                                   path_params, query_params, header_params,
                                   body, post_params, files,
                                   response_types_map, auth_settings,
                                   _return_http_data_only, collection_formats,
                                   _preload_content, _request_timeout, _host,
                                   _request_auth)

        return self.pool.apply_async(self.__call_api, (resource_path,
                                                       method, path_params,
                                                       query_params,
                                                       header_params, body,
                                                       post_params, files,
                                                       response_types_map,
                                                       auth_settings,
                                                       _return_http_data_only,
                                                       collection_formats,
                                                       _preload_content,
                                                       _request_timeout,
                                                       _host, _request_auth))

    def request(self, method, url, query_params=None, headers=None,
                post_params=None, body=None, _preload_content=True,
                _request_timeout=None):
        """Makes the HTTP request using RESTClient."""
        if method == "GET":
            return self.rest_client.GET(url,
                                        query_params=query_params,
                                        _preload_content=_preload_content,
                                        _request_timeout=_request_timeout,
                                        headers=headers)
        elif method == "HEAD":
            return self.rest_client.HEAD(url,
                                         query_params=query_params,
                                         _preload_content=_preload_content,
                                         _request_timeout=_request_timeout,
                                         headers=headers)
        elif method == "OPTIONS":
            return self.rest_client.OPTIONS(url,
                                            query_params=query_params,
                                            headers=headers,
                                            _preload_content=_preload_content,
                                            _request_timeout=_request_timeout)
        elif method == "POST":
            return self.rest_client.POST(url,
                                         query_params=query_params,
                                         headers=headers,
                                         post_params=post_params,
                                         _preload_content=_preload_content,
                                         _request_timeout=_request_timeout,
                                         body=body)
        elif method == "PUT":
            return self.rest_client.PUT(url,
                                        query_params=query_params,
                                        headers=headers,
                                        post_params=post_params,
                                        _preload_content=_preload_content,
                                        _request_timeout=_request_timeout,
                                        body=body)
        elif method == "PATCH":
            return self.rest_client.PATCH(url,
                                          query_params=query_params,
                                          headers=headers,
                                          post_params=post_params,
                                          _preload_content=_preload_content,
                                          _request_timeout=_request_timeout,
                                          body=body)
        elif method == "DELETE":
            return self.rest_client.DELETE(url,
                                           query_params=query_params,
                                           headers=headers,
                                           _preload_content=_preload_content,
                                           _request_timeout=_request_timeout,
                                           body=body)
        else:
            raise ApiValueError(
                "http method must be `GET`, `HEAD`, `OPTIONS`,"
                " `POST`, `PATCH`, `PUT` or `DELETE`."
            )

    def parameters_to_tuples(self, params, collection_formats):
        """Get parameters as list of tuples, formatting collections.

        :param params: Parameters as dict or list of two-tuples
        :param dict collection_formats: Parameter collection formats
        :return: Parameters as list of tuples, collections formatted
        """
        new_params = []
        if collection_formats is None:
            collection_formats = {}
        for k, v in six.iteritems(params) if isinstance(params, dict) else params:  # noqa: E501
            if k in collection_formats:
                collection_format = collection_formats[k]
                if collection_format == 'multi':
                    new_params.extend((k, value) for value in v)
                else:
                    if collection_format == 'ssv':
                        delimiter = ' '
                    elif collection_format == 'tsv':
                        delimiter = '\t'
                    elif collection_format == 'pipes':
                        delimiter = '|'
                    else:  # csv is the default
                        delimiter = ','
                    new_params.append(
                        (k, delimiter.join(str(value) for value in v)))
            else:
                new_params.append((k, v))
        return new_params

    def files_parameters(self, files=None):
        """Builds form parameters.

        :param files: File parameters.
        :return: Form parameters with files.
        """
        params = []

        if files:
            for k, v in six.iteritems(files):
                if not v:
                    continue
                file_names = v if type(v) is list else [v]
                for n in file_names:
                    with open(n, 'rb') as f:
                        filename = os.path.basename(f.name)
                        filedata = f.read()
                        mimetype = (mimetypes.guess_type(filename)[0] or
                                    'application/octet-stream')
                        params.append(
                            tuple([k, tuple([filename, filedata, mimetype])]))

        return params

    def select_header_accept(self, accepts):
        """Returns `Accept` based on an array of accepts provided.

        :param accepts: List of headers.
        :return: Accept (e.g. application/json).
        """
        if not accepts:
            return

        accepts = [x.lower() for x in accepts]

        if 'application/json' in accepts:
            return 'application/json'
        else:
            return ', '.join(accepts)

    def select_header_content_type(self, content_types):
        """Returns `Content-Type` based on an array of content_types provided.

        :param content_types: List of content-types.
        :return: Content-Type (e.g. application/json).
        """
        if not content_types:
            return 'application/json'

        content_types = [x.lower() for x in content_types]

        if 'application/json' in content_types or '*/*' in content_types:
            return 'application/json'
        else:
            return content_types[0]

    def update_params_for_auth(self, headers, querys, auth_settings,
                               request_auth=None):
        """Updates header and query params based on authentication setting.

        :param headers: Header parameters dict to be updated.
        :param querys: Query parameters tuple list to be updated.
        :param auth_settings: Authentication setting identifiers list.
        :param request_auth: if set, the provided settings will
                             override the token in the configuration.
        """
        if not auth_settings:
            return

        if request_auth:
            self._apply_auth_params(headers, querys, request_auth)
            return

        for auth in auth_settings:
            auth_setting = self.configuration.auth_settings().get(auth)
            if auth_setting:
                self._apply_auth_params(headers, querys, auth_setting)

    def _apply_auth_params(self, headers, querys, auth_setting):
        """Updates the request parameters based on a single auth_setting

        :param headers: Header parameters dict to be updated.
        :param querys: Query parameters tuple list to be updated.
        :param auth_setting: auth settings for the endpoint
        """
        if auth_setting['in'] == 'cookie':
            headers['Cookie'] = auth_setting['value']
        elif auth_setting['in'] == 'header':
            headers[auth_setting['key']] = auth_setting['value']
        elif auth_setting['in'] == 'query':
            querys.append((auth_setting['key'], auth_setting['value']))
        else:
            raise ApiValueError(
                'Authentication token must be in `query` or `header`'
            )

    def __deserialize_file(self, response):
        """Deserializes body to file

        Saves response body into a file in a temporary folder,
        using the filename from the `Content-Disposition` header if provided.

        :param response:  RESTResponse.
        :return: file path.
        """
        fd, path = tempfile.mkstemp(dir=self.configuration.temp_folder_path)
        os.close(fd)
        os.remove(path)

        content_disposition = response.getheader("Content-Disposition")
        if content_disposition:
            filename = re.search(r'filename=[\'"]?([^\'"\s]+)[\'"]?',
                                 content_disposition).group(1)
            path = os.path.join(os.path.dirname(path), filename)

        with open(path, "wb") as f:
            f.write(response.data)

        return path

    def __deserialize_primitive(self, data, klass):
        """Deserializes string to primitive type.

        :param data: str.
        :param klass: class literal.

        :return: int, long, float, str, bool.
        """
        try:
            return klass(data)
        except UnicodeEncodeError:
            return six.text_type(data)
        except TypeError:
            return data

    def __deserialize_object(self, value):
        """Return an original value.

        :return: object.
        """
        return value

    def __deserialize_date(self, string):
        """Deserializes string to date.

        :param string: str.
        :return: date.
        """
        try:
            return parse(string).date()
        except ImportError:
            return string
        except ValueError:
            raise rest.ApiException(
                status=0,
                reason="Failed to parse `{0}` as date object".format(string)
            )

    def __deserialize_datetime(self, string):
        """Deserializes string to datetime.

        The string should be in iso8601 datetime format.

        :param string: str.
        :return: datetime.
        """
        try:
            return parse(string)
        except ImportError:
            return string
        except ValueError:
            raise rest.ApiException(
                status=0,
                reason=(
                    "Failed to parse `{0}` as datetime object"
                    .format(string)
                )
            )

    def __deserialize_model(self, data, klass):
        """Deserializes list or dict to model.

        :param data: dict, list.
        :param klass: class literal.
        :return: model object.
        """
        has_discriminator = False
        if (hasattr(klass, 'get_real_child_model')
                and klass.discriminator_value_class_map):
            has_discriminator = True

        if not klass.openapi_types and has_discriminator is False:
            return data

        kwargs = {}
        if (data is not None and
                klass.openapi_types is not None and
                isinstance(data, (list, dict))):
            for attr, attr_type in six.iteritems(klass.openapi_types):
                if klass.attribute_map[attr] in data:
                    value = data[klass.attribute_map[attr]]
                    kwargs[attr] = self.__deserialize(value, attr_type)

        instance = klass(**kwargs)

        if has_discriminator:
            klass_name = instance.get_real_child_model(data)
            if klass_name:
                instance = self.__deserialize(data, klass_name)
        return instance
