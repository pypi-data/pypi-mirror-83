# coding: utf-8

"""
    Method REST API

    # Getting Started  Method's REST API gives the ability to create, update, retrieve and delete data from a Method account. It's a simple yet powerful way for programmers to integrate their applications with Method. It has predictable resource URLs and returns HTTP response codes. It also accepts and returns JSON in the HTTP body. You can use your favorite HTTP/REST library for your programming language to use our API.    In case if you would like to test the Method API before beginning your integration we have made some Postman collections available.  - [Postman Collection for OAuth2 Authentication.](../assets/method-identity-server.postman_collection.json)  - [Postman Collection for Method REST API.](../assets/method-restapi.postman_collection.json)    ## Step 1: Choose the Authentication Method  Choose the authentication method based on the application type.      | Application Type | Description | Authentication Method |  |----------|----------|----------|  | **Java Script** | Applications that run exclusively on a browser and are independent of a web server. | [OAuth2: Implicit Flow.](#section/Authentication/OAuth2:-Implicit-Flow-(Coming-Soon)) |  | **Server-Side (or \"web\")** | Applications that are clients running on a dedicated HTTP server. | [OAuth2: Authorization Code Flow.](#section/Authentication/OAuth2:-Authorization-Code-Flow) |  | **Mobile** | Applications that are installed on smart phones and tablets | [OAuth2: Authorization Code Flow.](#section/Authentication/OAuth2:-Authorization-Code-Flow) |  | **Background** | Applications that perform back-end jobs, have no user context or no-manual intervention. | [OAuth2: Client Credentials Flow](#section/Authentication/OAuth2:-Client-Credentials-Flow) or [API Key](#section/Authentication/API-Key). We recommend using OAuth2 - Client Credentials Flow for better security. |    ## Step 2: Setup Authentication  Based on the chosen authentication method, register OAuth2 client for your application, or create an API Key for your account.    We are working on automating the process of OAuth2 client registration.    ### Register OAuth2 client  To register Oauth2 client, send the following information to [api@method.me](mailto:api@method.me) with subject `REST API | OAuth2 Client Request`  - Redirect Url. : Not required for [OAuth2: Client Credentials Flow](#section/Authentication/OAuth2:-Client-Credentials-Flow)  - Application Type.  - Method Account Name.     ### Create API Key  Creation of an API Key can be done directly through your Method Account from the API Integration page  1. **[Log in](https://signin.method.me \"Method\")** to the Method Account you wish to generate an API key for    2. Click the upper-right **blue circle icon** and then select **Integrations**        ![Integrations Preference Menu](../assets/PrefsIntegrations.png \"Integrations Preferences\")    3. Click on **API** from the Integrations list    4. Click on **New** next to the section titled **API keys**    5. Enter a name for your API Key, and click on **Generate API Key**        ![New APIKey Wizard](../assets/newAPIKey.png \"New API Key\")  > 📌 __**Note**__ The Name you enter for your API Key is for display purposes only - To help you distinguish multiple API Keys from one another. It is not used in the Authentication process.         6. An API Key should now be visible for you on the screen. Make sure you Copy this key and keep it safe! **This is the only time it will ever be displayed to you**        ![Generated APIKey](../assets/GeneratedAPIKey.jpg \"Generated API Key\")        ## Step 3: Request OAuth2 Access Token  Request OAuth2 Access Token. See steps to request an access token for the appropriate flow.  - [OAuth2: Authorization Code Flow](#section/Authentication/OAuth2:-Authorization-Code-Flow)  - [OAuth2: Implicit Flow](#section/Authentication/OAuth2:-Implicit-Flow-(Coming-Soon))  - [OAuth2: Client Credentials Flow](#section/Authentication/OAuth2:-Client-Credentials-Flow)    ## Step 4: Make Authenticated Requests  Include OAuth2 Access Token or API Key in the header.    ### OAuth2  Include OAuth2 Access Token in HTTP `Authorization` header as `Bearer <access_token>`.  Example:    ```http  GET /api/v1/tables/Contacts/5 HTTP/1.1  Host: https://rest.method.me  Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7  ```    ### API Key  Include API Key in HTTP `Authorization` header as `APIKey <apikey>`.  Example:      ```http  GET /api/v1/tables/Contacts HTTP/1.1  Host: https://rest.method.me  Authorization: APIKey eyJhbGciOiJSUzI1NiIsImtpZCI  ```    # Authentication  The Method API uses the OAuth2.0 protocol for authentication.   It is an industry-standard protocol specification that enables third-party applications (clients) to gain delegated access to protected resources in Method via API.    **Why should we use OAuth2?**  - Clients are not required to support password authentication or store user credentials.  - Clients gain delegated access, i.e., access only to resources authenticated by the user.  - Users can revoke the client's delegated access anytime.  - OAuth2.0 access tokens expire after a set time. If the client faces a security breach, user data will be compromised only until the access token is valid.    **Terminologies**    The following are some terms you need to know before you start using the Method APIs.  - **Protected resources**: The Method resources, such as Contacts, Activities, Invoice, etc.  - **Resource server**: Method server that hosts protected resources. In this case, it will be Method REST API server.  - **Resource owner**: Any end-user of your account, who can grant access to the protected resources.  - **Client**: An application that sends requests to the resource server to access the protected resources on behalf of the end-user.  - **Client ID**: The consumer key generated from the connected application.  - **Client Secret**: The consumer secret generated from the connected application.  - **Authentication server**: Authorization server provides the necessary credentials (such as Access and Refresh tokens) to the client. In this case, it will be the Method Identity Server.  - **Authentication code**: The authorization server creates a temporary token and sends it to the client via the browser. The client will send this code to the authorization server to obtain access and refresh tokens.  - Tokens      - **Access Token**: A token that is sent to the resource server to access the protected resources of the user. The Access token provides secure and temporary access to Method REST APIs and is used by the applications to make requests to the connected app. Each access token will be valid only for an hour and can be used only for the set of operations that are described in the scope.      - **Refresh Token**: A token that can be used to obtain new access tokens. This token has an unlimited lifetime until it is revoked by the end-user.  - **Scopes**: Control the type of resource that the client application can access. Tokens are usually created with various scopes to ensure improved security.  Currently supported/required scopes are as follows:      - `openid` Required, to request access to user id, token issued at time and token expiry time      - `profile` Optional, to request access to user profile information like name, lastname etc      - `email` Optional, to request access to user's email address information      - `api` Required, to request access to Method REST API        ## OAuth2: Authorization Code Flow  If you are building a server-side (or \"web\") application that is capable of securely storing secrets, then the authorization code flow is the recommended method for controlling access to it.  At a high-level, this flow has the following steps:  1. Your application directs the browser to the Method Sign-In page, where the user authenticates.        Example: URL generated by your application to direct a browser to Sign-In page        ```url      https://auth.method.me/connect/authorize      ?client_id={your_client_id}      &nonce=d1f3f984-db5d-443c-a883-36f06f252d96      &redirect_uri={your_redirect_url}      &response_type=code      &scope=openid profile email api offline_access      &state=      ```        > 📌 __**Note**__ For Method users linked to multiple accounts the Method sign-in page will allow you to select which account you want to authenticate. The token you receive at the end of this flow will only be valid for the account you selected. Any requests made using this token will always affect the selected account. To connect to another account you must request a separate token for that account.      2. The browser receives an authorization code from Method Identity Server.        Example: URL with authorization code in `code` query parameter        ```url      {your_redirect_url}      ?code=7bfbe93c9712414f7c53766e2e6399      &scope=openid%20profile%20email%20api%20offline_access      &session_state=l0ckSo5h_GPR_2bicxnUaY_vRr5FRYDAzxQmkI2N2mI.97ac90c0b2eb3b44242aa75a8b3961fb      ```    3. The authorization code is passed to your application.  4. Your application sends this code to Method Identity Server, and Method Identity Server returns access token ID token, and optionally a refresh token.        Example:             Request        ```http      POST /connect/token HTTP/1.1      Host: https://auth.methodlocal.com      Content-Type: application/x-www-form-urlencoded        code=7bfbe93c9712414f7c53766e2e6399      &redirect_uri={your_redirect_url}      &grant_type=authorization_code      &client_id={your_client_id}      &client_secret={your_client_secret}      ```            Response        ```json      {          \"id_token\": \"eyJhbGciOiJSUzI1NiIsImtpZCI\",          \"access_token\": \"eyJhbGciOiJSUzI1NiIsImtpZCI6\",          \"expires_in\": 3600,          \"token_type\": \"Bearer\",          \"refresh_token\": \"b4f33ac42b668f00803305aa7f038\"      }      ```       5. Your application can now use the access token to call the Method REST API on behalf of the user.    ```http      GET /api/v1/tables/Contacts HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI    ```    ## OAuth2: Implicit Flow (Coming Soon)  If you are building a Single-Page Application (SPA) then the Implicit flow is the recommended method for controlling access between your SPA and a resource server. The Implicit flow is intended for applications where the confidentiality of the client secret can't be guaranteed. In this flow, the client doesn't make a request to the /token endpoint but instead receives the access token directly from the /authorize endpoint. The client must be capable of interacting with the resource owner's user-agent and capable of receiving incoming requests (through redirection) from the authorization server.  At a high level, the Implicit flow has the following steps:    1. Your application directs the browser to the Method Sign-In Page, where the user authenticates. Method Identity Server redirects the browser back to the specified redirect URI, along with access and ID tokens as a hash fragment in the URI.    > 📌 __**Note**__ For Method users linked to multiple accounts the Method sign-in page will allow you to select which account you want to authenticate. The token you receive at the end of this flow will only be valid for the account you selected. Any requests made using this token will always affect the selected account. To connect to another account you must request a separate token for that account.    2. Your application extracts the tokens from the URI.  3. Your application can now use these tokens to call the Method REST API on behalf of the user.    ## OAuth2: Client Credentials Flow  The Client Credentials flow is recommended for use in machine-to-machine authentication.   Your application will need to securely store its Client ID and Secret and pass those to Method Identity Server in exchange for an access token.   At a high-level, the flow only has two steps:  1. Your application passes its client credentials to your Method Identity Server.      Example:            Request            ````http      POST /connect/token HTTP/1.1      Host: https://auth.method.me      Content-Type: application/x-www-form-urlencoded        grant_type=client_credentials      &client_id={your_client_id}      &client_secret={your_client_secret}      ````            Response        ````json      {          \"access_token\": \"eyJhbGciOiJSUzI1NiIsImtpZCI\",          \"expires_in\": 3600,          \"token_type\": \"Bearer\"      }      ````          2. Your application can now use the access token to call the Method API.    ```http      GET /api/v1/tables/Contacts HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI    ```          ## API Key  API Key authentication is the easiest of the authentication method to use in machine-to-machine authentication. At a high-level, the flow has 2 steps:  1. [Generate an API key for your account](#section/Getting-Started/Step-2:-Setup-Authentication).  2. Use the API Key in your application to call the Method API.      ```http      GET /api/v1/tables/Contacts HTTP/1.1      Host: https://rest.method.me      Authorization: APIKey eyJhbGciOiJSUzI1NiIsImtpZCI    ```    # HTTP Request Methods  | Method | Description                              |  |--------|------------------------------------------|  | GET    | To retrieve data/resource from the resource server. |  | POST   | To insert or upload any new resource to the server. |  | PUT    | To update an existing resource. This replaces the target resource with the updated content. |  | PATCH  | To update a specific detail of the resource. This method updates the target resource with the provided content without changing other data. |  | DELETE | To delete a resource at a particular location. |    # HTTP Status Codes    | Status Codes | Meaning                  | Description                              |  |--------------|--------------------------|------------------------------------------|  | 200          | OK                       | The API request is successful.           |  | 201          | CREATED                  | Resource created. Ex. Contact created. |  | 204          | NO CONTENT               | There is no content available for the request. Usually, for DELETE, PUT, or PATCH methods. |  | 400          | BAD REQUEST              | The request is invalid. Required fields are missing or related records exceeded the maximum limit. |  | 401          | AUTHORIZATION ERROR      | Invalid API key or Access Token. e.g. Access Token expired.               |  | 403          | FORBIDDEN                | No permission to do the operation. e.g. Token is valid but user does not have necessary permission.       |  | 404          | NOT FOUND                | Invalid request. e.g. Record or Table not found.                         |  | 405          | METHOD NOT ALLOWED       | The specified method is not allowed.     |  | 413          | REQUEST ENTITY TOO LARGE | The server did not accept the request while uploading a file, since the limited file size has exceeded. |  | 415          | UNSUPPORTED MEDIA TYPE   | The server did not accept the request while uploading a file, since the media/ file type is not supported. |  | 429          | TOO MANY REQUESTS        | Number of API requests for the time period has exceeded. |  | 500          | INTERNAL SERVER ERROR    | Generic error that is encountered due to an unexpected server error. |    # API Limits  For a fair usage of our API, we will be limiting requests on an account basis as follows.  - 100 requests per minute per account.   - 5000 + [1000 * Number of Active licenses] (or) 25000 requests per day per account whichever is lower.     Example - If an account has 15 active licenses then the daily limit is 20000 requests calculated as 5000 + [1000 * 15].   If an account has 30 active licenses then the daily limit is 25000 requests,   as the calculated value of 5000 + [1000 * 30] is 35000 which is greater than our maximum daily limit of 25000.    Once this limit has been reached, calls will return error with status code 429.   The response header will contain the number of seconds after which the limit will be reset.   This rate limit is evaluated on a rolling window basis.   Below is a sample response, that indicates that per day(24h) limit is breached and you should retry after 7200 seconds (2 hours).      ```http      HTTP/1.1 429 Too Many Requests      Content-Type: text/plain      Retry-After: 7200      Date: Tue, 02 Jun 2020 13:34:48 GMT      Content-Length: 56        API calls quota exceeded! maximum admitted 6000 per 1d.    ```    # Filter Reference  You must use the appropriate notation for different data types with filter expressions.  - String values must be delimited by single quotation marks.  - Date-Time values must be delimited by single quotation marks and follow the ISO-8601 date-time format.       Complete date plus hours, minutes and seconds:        YYYY-MM-DDThh:mm[:ss][TZD] (eg 2020-03-29T10:05:45-06:00)    Where:        - YYYY = four-digit year      - MM = two-digit month (eg 03=March)      - DD = two-digit day of the month (01 through 31)      - T = a set character indicating the start of the time element      - hh = two digits of an hour (00 through 23, AM/PM not included)      - mm = two digits of a minute (00 through 59)      - ss = two digits of a second (00 through 59). Optional      - TZD = time zone designator (Z or +hh:mm or -hh:mm), the + or - values indicate how far ahead or behind a time zone is from the UTC (Coordinated Universal Time) zone.        Time zone designator is optional and if left out then date-time is assumed to be UTC.       Examples          - To get all Invoices created on April 17, 2020, EDT (Eastern Daylight Time)             ```http      GET /api/v1/tables/Invoice?filter=TimeCreated ge '2020-04-17T00:00-04:00' and TimeCreated lt '2020-04-18T00:00-04:00' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSU            or            GET /api/v1/tables/Invoice?filter=TimeCreated ge '2020-04-17T04:00' and TimeCreated lt '2020-04-18T04:00' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSU        or            GET /api/v1/tables/Invoice?filter=TimeCreated ge '2020-04-17T04:00Z' and TimeCreated lt '2020-04-18T04:00Z' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSU      ```           - To get all Invoices created in April 2020 EDT (Eastern Daylight Time)        ```http      GET /api/v1/tables/Invoice?filter=TimeCreated ge '2020-04-01T00:00-04:00' and TimeCreated lt '2020-05-01T00:00-04:00' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSU      ```    - Numeric values require no delimiters.    You can use the following expressions to construct a filter in Method REST API.    | Filter Operation | Example | Explanation |   |------------------------------------------|------------------------------------------|------------------------------------------|  | **Comparison Operators** |  | `eq` Equal | filter=FirstName eq 'Bill' |  Query on Contacts table. Returns Contacts with FirstName equal to 'Bill' |  | `lt` Less than | filter=TotalBalance lt 100 | Query on Contacts . Returns all Contacts with a balance lower than 100. |  | `gt` Greater than | filter=TotalBalance gt 100 | Query on Contacts . Returns all Contacts with a balance greater than 100. |  | `ge` Greater than or equal to | filter=TotalBalance ge 100 | Query on Contacts . Returns all Contacts with a balance 100 and greater. |  | `le` Less than or equal to | filter=TotalBalance le 100 | Query on Contacts . Returns all Contacts with a balance 100 and lower. |  | `ne` Different from (not equal) | filter=TotalBalance ne 0 | Query on Contacts . Returns all Contacts with a non-zero balance. |  | **Logical Operators** |  | `and` And | filter=FirstName eq 'Bill' and LastName eq 'Wagner' | Query on Contacts table. Returns Contacts with FirstName equal to 'Bill' and LastName equal to 'Wagner' |  | `or` Or | filter=BillAddressCountry eq 'Canada' or BillAddressCountry eq 'USA' | Query on Contacts table. Returns Contacts in Canada and the United States. |  |`not` Not | filter=not (BillAddressCountry eq 'Canada' or BillAddressCountry eq 'USA') | Query on Contacts table. Returns Contacts outside of Canada and the United States. |  | **String Functions** |  |  `endswith` String ends with | filter=endswith(Name,'RT') | Query on Contacts table. Returns all Contacts with names ending with 'RT'. |  | `startswith` String starts with | filter=startswith(Name, 'S') | Query on Contacts table. Returns all Contacts with names beginning with 'S'. |  | `contains` String containing | filter=contains(Name, 'RT') | Query on Contacts table. Returns all Contacts with names containing 'RT' |  | `()` Grouping | filter=(not (BillAddressCountry eq 'Canada' or BillAddressCountry eq 'USA')) and (TotalBalance ge 100) | Query on Contacts table. Returns all Contacts outside Canada and the United States with Balance 100 and greater |    # noqa: E501

    The version of the OpenAPI document: 1.0
    Contact: support@method.me
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import copy
import logging
import multiprocessing
import sys
import urllib3

import six
from six.moves import http_client as httplib
from openapi_client.exceptions import ApiValueError


JSON_SCHEMA_VALIDATION_KEYWORDS = {
    'multipleOf', 'maximum', 'exclusiveMaximum',
    'minimum', 'exclusiveMinimum', 'maxLength',
    'minLength', 'pattern', 'maxItems', 'minItems'
}

class Configuration(object):
    """NOTE: This class is auto generated by OpenAPI Generator

    Ref: https://openapi-generator.tech
    Do not edit the class manually.

    :param host: Base url
    :param api_key: Dict to store API key(s).
      Each entry in the dict specifies an API key.
      The dict key is the name of the security scheme in the OAS specification.
      The dict value is the API key secret.
    :param api_key_prefix: Dict to store API prefix (e.g. Bearer)
      The dict key is the name of the security scheme in the OAS specification.
      The dict value is an API key prefix when generating the auth data.
    :param username: Username for HTTP basic authentication
    :param password: Password for HTTP basic authentication
    :param discard_unknown_keys: Boolean value indicating whether to discard
      unknown properties. A server may send a response that includes additional
      properties that are not known by the client in the following scenarios:
      1. The OpenAPI document is incomplete, i.e. it does not match the server
         implementation.
      2. The client was generated using an older version of the OpenAPI document
         and the server has been upgraded since then.
      If a schema in the OpenAPI document defines the additionalProperties attribute,
      then all undeclared properties received by the server are injected into the
      additional properties map. In that case, there are undeclared properties, and
      nothing to discard.
    :param disabled_client_side_validations (string): Comma-separated list of
      JSON schema validation keywords to disable JSON schema structural validation
      rules. The following keywords may be specified: multipleOf, maximum,
      exclusiveMaximum, minimum, exclusiveMinimum, maxLength, minLength, pattern,
      maxItems, minItems.
      By default, the validation is performed for data generated locally by the client
      and data received from the server, independent of any validation performed by
      the server side. If the input data does not satisfy the JSON schema validation
      rules specified in the OpenAPI document, an exception is raised.
      If disabled_client_side_validations is set, structural validation is
      disabled. This can be useful to troubleshoot data validation problem, such as
      when the OpenAPI document validation rules do not match the actual API data
      received by the server.
    :param server_index: Index to servers configuration.
    :param server_variables: Mapping with string values to replace variables in
      templated server configuration. The validation of enums is performed for
      variables with defined enum values before.
    :param server_operation_index: Mapping from operation ID to an index to server
      configuration.
    :param server_operation_variables: Mapping from operation ID to a mapping with
      string values to replace variables in templated server configuration.
      The validation of enums is performed for variables with defined enum values before.

    :Example:
    """

    _default = None

    def __init__(self, host=None,
                 api_key=None, api_key_prefix=None,
                 username=None, password=None,
                 discard_unknown_keys=False,
                 disabled_client_side_validations="",
                 server_index=None, server_variables=None,
                 server_operation_index=None, server_operation_variables=None,
                 ):
        """Constructor
        """
        self._base_path = "https://rest.method.me" if host is None else host
        """Default Base url
        """
        self.server_index = 0 if server_index is None and host is None else server_index
        self.server_operation_index = server_operation_index or {}
        """Default server index
        """
        self.server_variables = server_variables or {}
        self.server_operation_variables = server_operation_variables or {}
        """Default server variables
        """
        self.temp_folder_path = None
        """Temp file folder for downloading files
        """
        # Authentication Settings
        self.api_key = {}
        if api_key:
            self.api_key = api_key
        """dict to store API key(s)
        """
        self.api_key_prefix = {}
        if api_key_prefix:
            self.api_key_prefix = api_key_prefix
        """dict to store API prefix (e.g. Bearer)
        """
        self.refresh_api_key_hook = None
        """function hook to refresh API key if expired
        """
        self.username = username
        """Username for HTTP basic authentication
        """
        self.password = password
        """Password for HTTP basic authentication
        """
        self.discard_unknown_keys = discard_unknown_keys
        self.disabled_client_side_validations = disabled_client_side_validations
        self.access_token = None
        """access token for OAuth/Bearer
        """
        self.logger = {}
        """Logging Settings
        """
        self.logger["package_logger"] = logging.getLogger("openapi_client")
        self.logger["urllib3_logger"] = logging.getLogger("urllib3")
        self.logger_format = '%(asctime)s %(levelname)s %(message)s'
        """Log format
        """
        self.logger_stream_handler = None
        """Log stream handler
        """
        self.logger_file_handler = None
        """Log file handler
        """
        self.logger_file = None
        """Debug file location
        """
        self.debug = False
        """Debug switch
        """

        self.verify_ssl = True
        """SSL/TLS verification
           Set this to false to skip verifying SSL certificate when calling API
           from https server.
        """
        self.ssl_ca_cert = None
        """Set this to customize the certificate file to verify the peer.
        """
        self.cert_file = None
        """client certificate file
        """
        self.key_file = None
        """client key file
        """
        self.assert_hostname = None
        """Set this to True/False to enable/disable SSL hostname verification.
        """

        self.connection_pool_maxsize = multiprocessing.cpu_count() * 5
        """urllib3 connection pool's maximum number of connections saved
           per pool. urllib3 uses 1 connection as default value, but this is
           not the best value when you are making a lot of possibly parallel
           requests to the same host, which is often the case here.
           cpu_count * 5 is used as default value to increase performance.
        """

        self.proxy = None
        """Proxy URL
        """
        self.proxy_headers = None
        """Proxy headers
        """
        self.safe_chars_for_path_param = ''
        """Safe chars for path_param
        """
        self.retries = None
        """Adding retries to override urllib3 default value 3
        """
        # Enable client side validation
        self.client_side_validation = True

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k not in ('logger', 'logger_file_handler'):
                setattr(result, k, copy.deepcopy(v, memo))
        # shallow copy of loggers
        result.logger = copy.copy(self.logger)
        # use setters to configure loggers
        result.logger_file = self.logger_file
        result.debug = self.debug
        return result

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name == 'disabled_client_side_validations':
            s = set(filter(None, value.split(',')))
            for v in s:
                if v not in JSON_SCHEMA_VALIDATION_KEYWORDS:
                    raise ApiValueError(
                        "Invalid keyword: '{0}''".format(v))
            self._disabled_client_side_validations = s

    @classmethod
    def set_default(cls, default):
        """Set default instance of configuration.

        It stores default configuration, which can be
        returned by get_default_copy method.

        :param default: object of Configuration
        """
        cls._default = copy.deepcopy(default)

    @classmethod
    def get_default_copy(cls):
        """Return new instance of configuration.

        This method returns newly created, based on default constructor,
        object of Configuration class or returns a copy of default
        configuration passed by the set_default method.

        :return: The configuration object.
        """
        if cls._default is not None:
            return copy.deepcopy(cls._default)
        return Configuration()

    @property
    def logger_file(self):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str
        """
        return self.__logger_file

    @logger_file.setter
    def logger_file(self, value):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str
        """
        self.__logger_file = value
        if self.__logger_file:
            # If set logging file,
            # then add file handler and remove stream handler.
            self.logger_file_handler = logging.FileHandler(self.__logger_file)
            self.logger_file_handler.setFormatter(self.logger_formatter)
            for _, logger in six.iteritems(self.logger):
                logger.addHandler(self.logger_file_handler)

    @property
    def debug(self):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        return self.__debug

    @debug.setter
    def debug(self, value):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        self.__debug = value
        if self.__debug:
            # if debug status is True, turn on debug logging
            for _, logger in six.iteritems(self.logger):
                logger.setLevel(logging.DEBUG)
            # turn on httplib debug
            httplib.HTTPConnection.debuglevel = 1
        else:
            # if debug status is False, turn off debug logging,
            # setting log level to default `logging.WARNING`
            for _, logger in six.iteritems(self.logger):
                logger.setLevel(logging.WARNING)
            # turn off httplib debug
            httplib.HTTPConnection.debuglevel = 0

    @property
    def logger_format(self):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        return self.__logger_format

    @logger_format.setter
    def logger_format(self, value):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        self.__logger_format = value
        self.logger_formatter = logging.Formatter(self.__logger_format)

    def get_api_key_with_prefix(self, identifier, alias=None):
        """Gets API key (with prefix if set).

        :param identifier: The identifier of apiKey.
        :param alias: The alternative identifier of apiKey.
        :return: The token for api key authentication.
        """
        if self.refresh_api_key_hook is not None:
            self.refresh_api_key_hook(self)
        key = self.api_key.get(identifier, self.api_key.get(alias) if alias is not None else None)
        if key:
            prefix = self.api_key_prefix.get(identifier)
            if prefix:
                return "%s %s" % (prefix, key)
            else:
                return key

    def get_basic_auth_token(self):
        """Gets HTTP basic authentication header (string).

        :return: The token for basic HTTP authentication.
        """
        username = ""
        if self.username is not None:
            username = self.username
        password = ""
        if self.password is not None:
            password = self.password
        return urllib3.util.make_headers(
            basic_auth=username + ':' + password
        ).get('authorization')

    def auth_settings(self):
        """Gets Auth Settings dict for api client.

        :return: The Auth Settings information dict.
        """
        auth = {}
        if self.access_token is not None:
            auth['OAuth2'] = {
                'type': 'oauth2',
                'in': 'header',
                'key': 'Authorization',
                'value': 'Bearer ' + self.access_token
            }
        return auth

    def to_debug_report(self):
        """Gets the essential information for debugging.

        :return: The report for debugging.
        """
        return "Python SDK Debug Report:\n"\
               "OS: {env}\n"\
               "Python Version: {pyversion}\n"\
               "Version of the API: 1.0\n"\
               "SDK Package Version: 0.0.1".\
               format(env=sys.platform, pyversion=sys.version)

    def get_host_settings(self):
        """Gets an array of host settings

        :return: An array of host settings
        """
        return [
            {
                'url': "https://rest.method.me",
                'description': "Production",
            }
        ]

    def get_host_from_settings(self, index, variables=None, servers=None):
        """Gets host URL based on the index and variables
        :param index: array index of the host settings
        :param variables: hash of variable and the corresponding value
        :param servers: an array of host settings or None
        :return: URL based on host settings
        """
        if index is None:
            return self._base_path

        variables = {} if variables is None else variables
        servers = self.get_host_settings() if servers is None else servers

        try:
            server = servers[index]
        except IndexError:
            raise ValueError(
                "Invalid index {0} when selecting the host settings. "
                "Must be less than {1}".format(index, len(servers)))

        url = server['url']

        # go through variables and replace placeholders
        for variable_name, variable in server.get('variables', {}).items():
            used_value = variables.get(
                variable_name, variable['default_value'])

            if 'enum_values' in variable \
                    and used_value not in variable['enum_values']:
                raise ValueError(
                    "The variable `{0}` in the host URL has invalid value "
                    "{1}. Must be {2}.".format(
                        variable_name, variables[variable_name],
                        variable['enum_values']))

            url = url.replace("{" + variable_name + "}", used_value)

        return url

    @property
    def host(self):
        """Return generated host."""
        return self.get_host_from_settings(self.server_index, variables=self.server_variables)

    @host.setter
    def host(self, value):
        """Fix base path."""
        self._base_path = value
        self.server_index = None
