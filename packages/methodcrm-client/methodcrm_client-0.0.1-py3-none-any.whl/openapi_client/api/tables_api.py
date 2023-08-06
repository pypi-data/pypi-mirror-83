# coding: utf-8

"""
    Method REST API

    # Getting Started  Method's REST API gives the ability to create, update, retrieve and delete data from a Method account. It's a simple yet powerful way for programmers to integrate their applications with Method. It has predictable resource URLs and returns HTTP response codes. It also accepts and returns JSON in the HTTP body. You can use your favorite HTTP/REST library for your programming language to use our API.    In case if you would like to test the Method API before beginning your integration we have made some Postman collections available.  - [Postman Collection for OAuth2 Authentication.](../assets/method-identity-server.postman_collection.json)  - [Postman Collection for Method REST API.](../assets/method-restapi.postman_collection.json)    ## Step 1: Choose the Authentication Method  Choose the authentication method based on the application type.      | Application Type | Description | Authentication Method |  |----------|----------|----------|  | **Java Script** | Applications that run exclusively on a browser and are independent of a web server. | [OAuth2: Implicit Flow.](#section/Authentication/OAuth2:-Implicit-Flow-(Coming-Soon)) |  | **Server-Side (or \"web\")** | Applications that are clients running on a dedicated HTTP server. | [OAuth2: Authorization Code Flow.](#section/Authentication/OAuth2:-Authorization-Code-Flow) |  | **Mobile** | Applications that are installed on smart phones and tablets | [OAuth2: Authorization Code Flow.](#section/Authentication/OAuth2:-Authorization-Code-Flow) |  | **Background** | Applications that perform back-end jobs, have no user context or no-manual intervention. | [OAuth2: Client Credentials Flow](#section/Authentication/OAuth2:-Client-Credentials-Flow) or [API Key](#section/Authentication/API-Key). We recommend using OAuth2 - Client Credentials Flow for better security. |    ## Step 2: Setup Authentication  Based on the chosen authentication method, register OAuth2 client for your application, or create an API Key for your account.    We are working on automating the process of OAuth2 client registration.    ### Register OAuth2 client  To register Oauth2 client, send the following information to [api@method.me](mailto:api@method.me) with subject `REST API | OAuth2 Client Request`  - Redirect Url. : Not required for [OAuth2: Client Credentials Flow](#section/Authentication/OAuth2:-Client-Credentials-Flow)  - Application Type.  - Method Account Name.     ### Create API Key  Creation of an API Key can be done directly through your Method Account from the API Integration page  1. **[Log in](https://signin.method.me \"Method\")** to the Method Account you wish to generate an API key for    2. Click the upper-right **blue circle icon** and then select **Integrations**        ![Integrations Preference Menu](../assets/PrefsIntegrations.png \"Integrations Preferences\")    3. Click on **API** from the Integrations list    4. Click on **New** next to the section titled **API keys**    5. Enter a name for your API Key, and click on **Generate API Key**        ![New APIKey Wizard](../assets/newAPIKey.png \"New API Key\")  > 📌 __**Note**__ The Name you enter for your API Key is for display purposes only - To help you distinguish multiple API Keys from one another. It is not used in the Authentication process.         6. An API Key should now be visible for you on the screen. Make sure you Copy this key and keep it safe! **This is the only time it will ever be displayed to you**        ![Generated APIKey](../assets/GeneratedAPIKey.jpg \"Generated API Key\")        ## Step 3: Request OAuth2 Access Token  Request OAuth2 Access Token. See steps to request an access token for the appropriate flow.  - [OAuth2: Authorization Code Flow](#section/Authentication/OAuth2:-Authorization-Code-Flow)  - [OAuth2: Implicit Flow](#section/Authentication/OAuth2:-Implicit-Flow-(Coming-Soon))  - [OAuth2: Client Credentials Flow](#section/Authentication/OAuth2:-Client-Credentials-Flow)    ## Step 4: Make Authenticated Requests  Include OAuth2 Access Token or API Key in the header.    ### OAuth2  Include OAuth2 Access Token in HTTP `Authorization` header as `Bearer <access_token>`.  Example:    ```http  GET /api/v1/tables/Contacts/5 HTTP/1.1  Host: https://rest.method.me  Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7  ```    ### API Key  Include API Key in HTTP `Authorization` header as `APIKey <apikey>`.  Example:      ```http  GET /api/v1/tables/Contacts HTTP/1.1  Host: https://rest.method.me  Authorization: APIKey eyJhbGciOiJSUzI1NiIsImtpZCI  ```    # Authentication  The Method API uses the OAuth2.0 protocol for authentication.   It is an industry-standard protocol specification that enables third-party applications (clients) to gain delegated access to protected resources in Method via API.    **Why should we use OAuth2?**  - Clients are not required to support password authentication or store user credentials.  - Clients gain delegated access, i.e., access only to resources authenticated by the user.  - Users can revoke the client's delegated access anytime.  - OAuth2.0 access tokens expire after a set time. If the client faces a security breach, user data will be compromised only until the access token is valid.    **Terminologies**    The following are some terms you need to know before you start using the Method APIs.  - **Protected resources**: The Method resources, such as Contacts, Activities, Invoice, etc.  - **Resource server**: Method server that hosts protected resources. In this case, it will be Method REST API server.  - **Resource owner**: Any end-user of your account, who can grant access to the protected resources.  - **Client**: An application that sends requests to the resource server to access the protected resources on behalf of the end-user.  - **Client ID**: The consumer key generated from the connected application.  - **Client Secret**: The consumer secret generated from the connected application.  - **Authentication server**: Authorization server provides the necessary credentials (such as Access and Refresh tokens) to the client. In this case, it will be the Method Identity Server.  - **Authentication code**: The authorization server creates a temporary token and sends it to the client via the browser. The client will send this code to the authorization server to obtain access and refresh tokens.  - Tokens      - **Access Token**: A token that is sent to the resource server to access the protected resources of the user. The Access token provides secure and temporary access to Method REST APIs and is used by the applications to make requests to the connected app. Each access token will be valid only for an hour and can be used only for the set of operations that are described in the scope.      - **Refresh Token**: A token that can be used to obtain new access tokens. This token has an unlimited lifetime until it is revoked by the end-user.  - **Scopes**: Control the type of resource that the client application can access. Tokens are usually created with various scopes to ensure improved security.  Currently supported/required scopes are as follows:      - `openid` Required, to request access to user id, token issued at time and token expiry time      - `profile` Optional, to request access to user profile information like name, lastname etc      - `email` Optional, to request access to user's email address information      - `api` Required, to request access to Method REST API        ## OAuth2: Authorization Code Flow  If you are building a server-side (or \"web\") application that is capable of securely storing secrets, then the authorization code flow is the recommended method for controlling access to it.  At a high-level, this flow has the following steps:  1. Your application directs the browser to the Method Sign-In page, where the user authenticates.        Example: URL generated by your application to direct a browser to Sign-In page        ```url      https://auth.method.me/connect/authorize      ?client_id={your_client_id}      &nonce=d1f3f984-db5d-443c-a883-36f06f252d96      &redirect_uri={your_redirect_url}      &response_type=code      &scope=openid profile email api offline_access      &state=      ```        > 📌 __**Note**__ For Method users linked to multiple accounts the Method sign-in page will allow you to select which account you want to authenticate. The token you receive at the end of this flow will only be valid for the account you selected. Any requests made using this token will always affect the selected account. To connect to another account you must request a separate token for that account.      2. The browser receives an authorization code from Method Identity Server.        Example: URL with authorization code in `code` query parameter        ```url      {your_redirect_url}      ?code=7bfbe93c9712414f7c53766e2e6399      &scope=openid%20profile%20email%20api%20offline_access      &session_state=l0ckSo5h_GPR_2bicxnUaY_vRr5FRYDAzxQmkI2N2mI.97ac90c0b2eb3b44242aa75a8b3961fb      ```    3. The authorization code is passed to your application.  4. Your application sends this code to Method Identity Server, and Method Identity Server returns access token ID token, and optionally a refresh token.        Example:             Request        ```http      POST /connect/token HTTP/1.1      Host: https://auth.methodlocal.com      Content-Type: application/x-www-form-urlencoded        code=7bfbe93c9712414f7c53766e2e6399      &redirect_uri={your_redirect_url}      &grant_type=authorization_code      &client_id={your_client_id}      &client_secret={your_client_secret}      ```            Response        ```json      {          \"id_token\": \"eyJhbGciOiJSUzI1NiIsImtpZCI\",          \"access_token\": \"eyJhbGciOiJSUzI1NiIsImtpZCI6\",          \"expires_in\": 3600,          \"token_type\": \"Bearer\",          \"refresh_token\": \"b4f33ac42b668f00803305aa7f038\"      }      ```       5. Your application can now use the access token to call the Method REST API on behalf of the user.    ```http      GET /api/v1/tables/Contacts HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI    ```    ## OAuth2: Implicit Flow (Coming Soon)  If you are building a Single-Page Application (SPA) then the Implicit flow is the recommended method for controlling access between your SPA and a resource server. The Implicit flow is intended for applications where the confidentiality of the client secret can't be guaranteed. In this flow, the client doesn't make a request to the /token endpoint but instead receives the access token directly from the /authorize endpoint. The client must be capable of interacting with the resource owner's user-agent and capable of receiving incoming requests (through redirection) from the authorization server.  At a high level, the Implicit flow has the following steps:    1. Your application directs the browser to the Method Sign-In Page, where the user authenticates. Method Identity Server redirects the browser back to the specified redirect URI, along with access and ID tokens as a hash fragment in the URI.    > 📌 __**Note**__ For Method users linked to multiple accounts the Method sign-in page will allow you to select which account you want to authenticate. The token you receive at the end of this flow will only be valid for the account you selected. Any requests made using this token will always affect the selected account. To connect to another account you must request a separate token for that account.    2. Your application extracts the tokens from the URI.  3. Your application can now use these tokens to call the Method REST API on behalf of the user.    ## OAuth2: Client Credentials Flow  The Client Credentials flow is recommended for use in machine-to-machine authentication.   Your application will need to securely store its Client ID and Secret and pass those to Method Identity Server in exchange for an access token.   At a high-level, the flow only has two steps:  1. Your application passes its client credentials to your Method Identity Server.      Example:            Request            ````http      POST /connect/token HTTP/1.1      Host: https://auth.method.me      Content-Type: application/x-www-form-urlencoded        grant_type=client_credentials      &client_id={your_client_id}      &client_secret={your_client_secret}      ````            Response        ````json      {          \"access_token\": \"eyJhbGciOiJSUzI1NiIsImtpZCI\",          \"expires_in\": 3600,          \"token_type\": \"Bearer\"      }      ````          2. Your application can now use the access token to call the Method API.    ```http      GET /api/v1/tables/Contacts HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI    ```          ## API Key  API Key authentication is the easiest of the authentication method to use in machine-to-machine authentication. At a high-level, the flow has 2 steps:  1. [Generate an API key for your account](#section/Getting-Started/Step-2:-Setup-Authentication).  2. Use the API Key in your application to call the Method API.      ```http      GET /api/v1/tables/Contacts HTTP/1.1      Host: https://rest.method.me      Authorization: APIKey eyJhbGciOiJSUzI1NiIsImtpZCI    ```    # HTTP Request Methods  | Method | Description                              |  |--------|------------------------------------------|  | GET    | To retrieve data/resource from the resource server. |  | POST   | To insert or upload any new resource to the server. |  | PUT    | To update an existing resource. This replaces the target resource with the updated content. |  | PATCH  | To update a specific detail of the resource. This method updates the target resource with the provided content without changing other data. |  | DELETE | To delete a resource at a particular location. |    # HTTP Status Codes    | Status Codes | Meaning                  | Description                              |  |--------------|--------------------------|------------------------------------------|  | 200          | OK                       | The API request is successful.           |  | 201          | CREATED                  | Resource created. Ex. Contact created. |  | 204          | NO CONTENT               | There is no content available for the request. Usually, for DELETE, PUT, or PATCH methods. |  | 400          | BAD REQUEST              | The request is invalid. Required fields are missing or related records exceeded the maximum limit. |  | 401          | AUTHORIZATION ERROR      | Invalid API key or Access Token. e.g. Access Token expired.               |  | 403          | FORBIDDEN                | No permission to do the operation. e.g. Token is valid but user does not have necessary permission.       |  | 404          | NOT FOUND                | Invalid request. e.g. Record or Table not found.                         |  | 405          | METHOD NOT ALLOWED       | The specified method is not allowed.     |  | 413          | REQUEST ENTITY TOO LARGE | The server did not accept the request while uploading a file, since the limited file size has exceeded. |  | 415          | UNSUPPORTED MEDIA TYPE   | The server did not accept the request while uploading a file, since the media/ file type is not supported. |  | 429          | TOO MANY REQUESTS        | Number of API requests for the time period has exceeded. |  | 500          | INTERNAL SERVER ERROR    | Generic error that is encountered due to an unexpected server error. |    # API Limits  For a fair usage of our API, we will be limiting requests on an account basis as follows.  - 100 requests per minute per account.   - 5000 + [1000 * Number of Active licenses] (or) 25000 requests per day per account whichever is lower.     Example - If an account has 15 active licenses then the daily limit is 20000 requests calculated as 5000 + [1000 * 15].   If an account has 30 active licenses then the daily limit is 25000 requests,   as the calculated value of 5000 + [1000 * 30] is 35000 which is greater than our maximum daily limit of 25000.    Once this limit has been reached, calls will return error with status code 429.   The response header will contain the number of seconds after which the limit will be reset.   This rate limit is evaluated on a rolling window basis.   Below is a sample response, that indicates that per day(24h) limit is breached and you should retry after 7200 seconds (2 hours).      ```http      HTTP/1.1 429 Too Many Requests      Content-Type: text/plain      Retry-After: 7200      Date: Tue, 02 Jun 2020 13:34:48 GMT      Content-Length: 56        API calls quota exceeded! maximum admitted 6000 per 1d.    ```    # Filter Reference  You must use the appropriate notation for different data types with filter expressions.  - String values must be delimited by single quotation marks.  - Date-Time values must be delimited by single quotation marks and follow the ISO-8601 date-time format.       Complete date plus hours, minutes and seconds:        YYYY-MM-DDThh:mm[:ss][TZD] (eg 2020-03-29T10:05:45-06:00)    Where:        - YYYY = four-digit year      - MM = two-digit month (eg 03=March)      - DD = two-digit day of the month (01 through 31)      - T = a set character indicating the start of the time element      - hh = two digits of an hour (00 through 23, AM/PM not included)      - mm = two digits of a minute (00 through 59)      - ss = two digits of a second (00 through 59). Optional      - TZD = time zone designator (Z or +hh:mm or -hh:mm), the + or - values indicate how far ahead or behind a time zone is from the UTC (Coordinated Universal Time) zone.        Time zone designator is optional and if left out then date-time is assumed to be UTC.       Examples          - To get all Invoices created on April 17, 2020, EDT (Eastern Daylight Time)             ```http      GET /api/v1/tables/Invoice?filter=TimeCreated ge '2020-04-17T00:00-04:00' and TimeCreated lt '2020-04-18T00:00-04:00' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSU            or            GET /api/v1/tables/Invoice?filter=TimeCreated ge '2020-04-17T04:00' and TimeCreated lt '2020-04-18T04:00' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSU        or            GET /api/v1/tables/Invoice?filter=TimeCreated ge '2020-04-17T04:00Z' and TimeCreated lt '2020-04-18T04:00Z' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSU      ```           - To get all Invoices created in April 2020 EDT (Eastern Daylight Time)        ```http      GET /api/v1/tables/Invoice?filter=TimeCreated ge '2020-04-01T00:00-04:00' and TimeCreated lt '2020-05-01T00:00-04:00' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer eyJhbGciOiJSU      ```    - Numeric values require no delimiters.    You can use the following expressions to construct a filter in Method REST API.    | Filter Operation | Example | Explanation |   |------------------------------------------|------------------------------------------|------------------------------------------|  | **Comparison Operators** |  | `eq` Equal | filter=FirstName eq 'Bill' |  Query on Contacts table. Returns Contacts with FirstName equal to 'Bill' |  | `lt` Less than | filter=TotalBalance lt 100 | Query on Contacts . Returns all Contacts with a balance lower than 100. |  | `gt` Greater than | filter=TotalBalance gt 100 | Query on Contacts . Returns all Contacts with a balance greater than 100. |  | `ge` Greater than or equal to | filter=TotalBalance ge 100 | Query on Contacts . Returns all Contacts with a balance 100 and greater. |  | `le` Less than or equal to | filter=TotalBalance le 100 | Query on Contacts . Returns all Contacts with a balance 100 and lower. |  | `ne` Different from (not equal) | filter=TotalBalance ne 0 | Query on Contacts . Returns all Contacts with a non-zero balance. |  | **Logical Operators** |  | `and` And | filter=FirstName eq 'Bill' and LastName eq 'Wagner' | Query on Contacts table. Returns Contacts with FirstName equal to 'Bill' and LastName equal to 'Wagner' |  | `or` Or | filter=BillAddressCountry eq 'Canada' or BillAddressCountry eq 'USA' | Query on Contacts table. Returns Contacts in Canada and the United States. |  |`not` Not | filter=not (BillAddressCountry eq 'Canada' or BillAddressCountry eq 'USA') | Query on Contacts table. Returns Contacts outside of Canada and the United States. |  | **String Functions** |  |  `endswith` String ends with | filter=endswith(Name,'RT') | Query on Contacts table. Returns all Contacts with names ending with 'RT'. |  | `startswith` String starts with | filter=startswith(Name, 'S') | Query on Contacts table. Returns all Contacts with names beginning with 'S'. |  | `contains` String containing | filter=contains(Name, 'RT') | Query on Contacts table. Returns all Contacts with names containing 'RT' |  | `()` Grouping | filter=(not (BillAddressCountry eq 'Canada' or BillAddressCountry eq 'USA')) and (TotalBalance ge 100) | Query on Contacts table. Returns all Contacts outside Canada and the United States with Balance 100 and greater |    # noqa: E501

    The version of the OpenAPI document: 1.0
    Contact: support@method.me
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from openapi_client.api_client import ApiClient
from openapi_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class TablesApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def tables_create_record(self, table, **kwargs):  # noqa: E501
        """Create Record  # noqa: E501

        To insert record in a table.  Specify `{table}` in URL path.     Include all required fields. Linked fields are ignored.     ### Examples  - To create record in Contacts table      ```http      POST /api/v1/tables/Contacts HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      Content-Type: application/json            {          \"Email\": \"david@landscaping.com\",          \"FirstName\": \"David\",          \"LastName\": \"Henderson\",          \"Phone\": \"1112223333\"      }      ```    - To create Invoice + InvoiceLine(s) in a single request.   Use `__` as prefix before related table name.   This will create invoice, invoice line(s) and also sync the invoice.  **Maximum of 50 related records can be created in a single request.**        ````http      POST /api/v1/tables/Invoice HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      Content-Type: application/json        {               \"TxnDate\": \"2020-06-01T16:00:00\",          \"BillAddressAddr1\": \"Blue Jet Airways\",          \"BillAddressAddr2\": \"213 E Washington St\",          \"BillAddressCity\": \"Ashland\",          \"BillAddressState\": \"OH\",          \"BillAddressPostalCode\": \"44805\",          \"BillAddressCountry\": \"USA\",          \"IsPending\": false,          \"IsFinanceCharge\": false,          \"DueDate\": \"2020-06-01T16:00:00\",          \"IsPaid\": false,          \"IsToBePrinted\": false,          \"IsToBeEmailed\": false,          \"IsTaxIncluded\": false,          \"IsWaitingForSyncApproval\": false,          \"TenantID\": 1,          \"ARAccount\": \"Accounts Receivable\",          \"Customer\": \"Blue Jet Airways\",          \"__InvoiceLine\":[              {                  \"Desc\": \"Plans and Permits\",                  \"Quantity\": 1,                  \"Rate\": 400,                  \"IsRatePercent\": false,                  \"ServiceDate\": \"2020-06-30T16:15:25\",                  \"UnitOfMeasure\": \"\",                  \"LineOrder\": 1,                  \"LastModifiedDate\": \"2020-06-01T16:16:08.597\",                  \"Item\": \"01 Plans and Permits\",                  \"SalesTaxCode\": \"Non\",                  \"TenantID\": 1              },              {                  \"Desc\": \"Plans and Permits\",                  \"Quantity\": 3,                  \"Rate\": 500.00000,                  \"IsRatePercent\": false,                  \"ServiceDate\": \"2020-06-30T16:15:25\",                  \"UnitOfMeasure\": \"\",                  \"LineOrder\": 2,                  \"LastModifiedDate\": \"2020-06-01T16:16:08.597\",                  \"Item\": \"01 Plans and Permits\",                  \"SalesTaxCode\": \"Non\",                  \"TenantID\": 1              }          ]      }      ````            # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_create_record(table, async_req=True)
        >>> result = thread.get()

        :param table: Table name (required)
        :type table: str
        :param body:
        :type body: object
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: int
        """
        kwargs['_return_http_data_only'] = True
        return self.tables_create_record_with_http_info(table, **kwargs)  # noqa: E501

    def tables_create_record_with_http_info(self, table, **kwargs):  # noqa: E501
        """Create Record  # noqa: E501

        To insert record in a table.  Specify `{table}` in URL path.     Include all required fields. Linked fields are ignored.     ### Examples  - To create record in Contacts table      ```http      POST /api/v1/tables/Contacts HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      Content-Type: application/json            {          \"Email\": \"david@landscaping.com\",          \"FirstName\": \"David\",          \"LastName\": \"Henderson\",          \"Phone\": \"1112223333\"      }      ```    - To create Invoice + InvoiceLine(s) in a single request.   Use `__` as prefix before related table name.   This will create invoice, invoice line(s) and also sync the invoice.  **Maximum of 50 related records can be created in a single request.**        ````http      POST /api/v1/tables/Invoice HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      Content-Type: application/json        {               \"TxnDate\": \"2020-06-01T16:00:00\",          \"BillAddressAddr1\": \"Blue Jet Airways\",          \"BillAddressAddr2\": \"213 E Washington St\",          \"BillAddressCity\": \"Ashland\",          \"BillAddressState\": \"OH\",          \"BillAddressPostalCode\": \"44805\",          \"BillAddressCountry\": \"USA\",          \"IsPending\": false,          \"IsFinanceCharge\": false,          \"DueDate\": \"2020-06-01T16:00:00\",          \"IsPaid\": false,          \"IsToBePrinted\": false,          \"IsToBeEmailed\": false,          \"IsTaxIncluded\": false,          \"IsWaitingForSyncApproval\": false,          \"TenantID\": 1,          \"ARAccount\": \"Accounts Receivable\",          \"Customer\": \"Blue Jet Airways\",          \"__InvoiceLine\":[              {                  \"Desc\": \"Plans and Permits\",                  \"Quantity\": 1,                  \"Rate\": 400,                  \"IsRatePercent\": false,                  \"ServiceDate\": \"2020-06-30T16:15:25\",                  \"UnitOfMeasure\": \"\",                  \"LineOrder\": 1,                  \"LastModifiedDate\": \"2020-06-01T16:16:08.597\",                  \"Item\": \"01 Plans and Permits\",                  \"SalesTaxCode\": \"Non\",                  \"TenantID\": 1              },              {                  \"Desc\": \"Plans and Permits\",                  \"Quantity\": 3,                  \"Rate\": 500.00000,                  \"IsRatePercent\": false,                  \"ServiceDate\": \"2020-06-30T16:15:25\",                  \"UnitOfMeasure\": \"\",                  \"LineOrder\": 2,                  \"LastModifiedDate\": \"2020-06-01T16:16:08.597\",                  \"Item\": \"01 Plans and Permits\",                  \"SalesTaxCode\": \"Non\",                  \"TenantID\": 1              }          ]      }      ````            # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_create_record_with_http_info(table, async_req=True)
        >>> result = thread.get()

        :param table: Table name (required)
        :type table: str
        :param body:
        :type body: object
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(int, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'table',
            'body'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method tables_create_record" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}
        if 'table' in local_var_params:
            path_params['table'] = local_var_params['table']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501
        
        response_types_map = {
            400: "ValidationProblemDetails",
            500: "ProblemDetails",
            201: "int",
        }

        return self.api_client.call_api(
            '/api/v1/tables/{table}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def tables_delete_record(self, table, record_id, **kwargs):  # noqa: E501
        """Delete Record  # noqa: E501

        To delete records from a table. Specify `{table}` and `{recordId}` in url path.       ### Examples  - To delete RecordId 5 from Contacts table        ```http      DELETE /api/v1/tables/Contacts/5 HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_delete_record(table, record_id, async_req=True)
        >>> result = thread.get()

        :param table: Table name (required)
        :type table: str
        :param record_id: RecordId of the record (required)
        :type record_id: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        return self.tables_delete_record_with_http_info(table, record_id, **kwargs)  # noqa: E501

    def tables_delete_record_with_http_info(self, table, record_id, **kwargs):  # noqa: E501
        """Delete Record  # noqa: E501

        To delete records from a table. Specify `{table}` and `{recordId}` in url path.       ### Examples  - To delete RecordId 5 from Contacts table        ```http      DELETE /api/v1/tables/Contacts/5 HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_delete_record_with_http_info(table, record_id, async_req=True)
        >>> result = thread.get()

        :param table: Table name (required)
        :type table: str
        :param record_id: RecordId of the record (required)
        :type record_id: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        local_var_params = locals()

        all_params = [
            'table',
            'record_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method tables_delete_record" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'record_id' is set
        if self.api_client.client_side_validation and ('record_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['record_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `record_id` when calling `tables_delete_record`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'table' in local_var_params:
            path_params['table'] = local_var_params['table']  # noqa: E501
        if 'record_id' in local_var_params:
            path_params['recordId'] = local_var_params['record_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501
        
        response_types_map = {}

        return self.api_client.call_api(
            '/api/v1/tables/{table}/{recordId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def tables_get_record(self, table, record_id, **kwargs):  # noqa: E501
        """Get Record  # noqa: E501

        To request data for specific record in a Table. Specify `{table}` and `{recordId}` in URL path.     By default the response contains all fields including linked and drop-down fields, but you can request specific fields by using `select` query parameter.     ### Examples  - To get all field values from Contacts table for RecordId 5        ```http      GET /api/v1/tables/Contacts/5 HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```    - To get FirstName and LastName field values from Contacts table for RecordId 5        ```http      GET /api/v1/tables/Contacts/5?select=FirstName,LastName HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```        # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_get_record(table, record_id, async_req=True)
        >>> result = thread.get()

        :param table: Table name (required)
        :type table: str
        :param record_id: RecordId of the record (required)
        :type record_id: int
        :param select: Comma separated list of fields to be returned in the response
        :type select: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: dict(str, object)
        """
        kwargs['_return_http_data_only'] = True
        return self.tables_get_record_with_http_info(table, record_id, **kwargs)  # noqa: E501

    def tables_get_record_with_http_info(self, table, record_id, **kwargs):  # noqa: E501
        """Get Record  # noqa: E501

        To request data for specific record in a Table. Specify `{table}` and `{recordId}` in URL path.     By default the response contains all fields including linked and drop-down fields, but you can request specific fields by using `select` query parameter.     ### Examples  - To get all field values from Contacts table for RecordId 5        ```http      GET /api/v1/tables/Contacts/5 HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```    - To get FirstName and LastName field values from Contacts table for RecordId 5        ```http      GET /api/v1/tables/Contacts/5?select=FirstName,LastName HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```        # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_get_record_with_http_info(table, record_id, async_req=True)
        >>> result = thread.get()

        :param table: Table name (required)
        :type table: str
        :param record_id: RecordId of the record (required)
        :type record_id: int
        :param select: Comma separated list of fields to be returned in the response
        :type select: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(dict(str, object), status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'table',
            'record_id',
            'select'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method tables_get_record" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'record_id' is set
        if self.api_client.client_side_validation and ('record_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['record_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `record_id` when calling `tables_get_record`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'table' in local_var_params:
            path_params['table'] = local_var_params['table']  # noqa: E501
        if 'record_id' in local_var_params:
            path_params['recordId'] = local_var_params['record_id']  # noqa: E501

        query_params = []
        if 'select' in local_var_params and local_var_params['select'] is not None:  # noqa: E501
            query_params.append(('select', local_var_params['select']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501
        
        response_types_map = {
            400: "ValidationProblemDetails",
            500: "ProblemDetails",
            200: "dict(str, object)",
        }

        return self.api_client.call_api(
            '/api/v1/tables/{table}/{recordId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def tables_patch_record(self, table, record_id, **kwargs):  # noqa: E501
        """Update Record  # noqa: E501

        To update records in a table.  Specify `{table}` and `{recordId}` in URL path.   Include only the fields you want to modify. Linked fields cannot be modified directly and will be ignored.     ### Examples  - To update LastName, Note and IsActive fields of a Contact with RecordID 5      ```http      PATCH /api/v1/tables/Contacts/5 HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      Content-Type: application/json            {          \"LastName\": \"Anderson\",          \"Note\": \"LastName modified and set active\",          \"IsActive\": true,      }      ```    - To Update Invoice + InvoiceLine(s) in a single request.   Use `__` as a prefix before related table name. This will update the invoice, create or update invoice line(s) and also sync the invoice.    > 📌 __**Note**__ Maximum of 50 related records can be created or updated in a single request.        ````http      PATCH /api/v1/tables/Invoice/4553 HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      Content-Type: application/json        {               \"TxnDate\": \"2020-06-01T16:00:00\",          \"BillAddressAddr1\": \"Blue Jet Airways\",          \"BillAddressAddr2\": \"213 E Washington St\",          \"BillAddressCity\": \"Ashland\",          \"BillAddressState\": \"OH\",          \"BillAddressPostalCode\": \"44805\",          \"BillAddressCountry\": \"USA\",          \"IsPending\": false,          \"IsFinanceCharge\": false,          \"DueDate\": \"2020-06-01T16:00:00\",          \"IsPaid\": false,          \"IsToBePrinted\": false,          \"IsToBeEmailed\": false,          \"IsTaxIncluded\": false,          \"IsWaitingForSyncApproval\": false,          \"TenantID\": 1,          \"ARAccount\": \"Accounts Receivable\",          \"Customer\": \"Blue Jet Airways\",          \"__InvoiceLine\":[              {                  \"RecordID\": 4821,                  \"Desc\": \"Plans and Permits\",                  \"Quantity\": 1,                  \"Rate\": 800,                  \"IsRatePercent\": false,                  \"ServiceDate\": \"2020-06-30T16:15:25\",                  \"UnitOfMeasure\": \"\",                  \"LineOrder\": 1,                  \"LastModifiedDate\": \"2020-06-01T16:16:08.597\",                  \"Item\": \"01 Plans and Permits\",                  \"SalesTaxCode\": \"Non\",                  \"TenantID\": 1              },              {                   \"RecordID\": 4820,                  \"Desc\": \"Plans and Permits\",                  \"Quantity\": 3,                  \"Rate\": 900.00000,                  \"IsRatePercent\": false,                  \"ServiceDate\": \"2020-06-30T16:15:25\",                  \"UnitOfMeasure\": \"\",                  \"LineOrder\": 2,                  \"LastModifiedDate\": \"2020-06-01T16:16:08.597\",                  \"Item\": \"01 Plans and Permits\",                  \"SalesTaxCode\": \"Non\",                  \"TenantID\": 1              },              {                  \"Desc\": \"Plans and Permits\",                  \"Quantity\": 6,                  \"Rate\": 100.00000,                  \"IsRatePercent\": false,                  \"ServiceDate\": \"2020-06-30T16:15:25\",                  \"UnitOfMeasure\": \"\",                  \"LineOrder\": 3,                  \"LastModifiedDate\": \"2020-06-01T16:16:08.597\",                  \"Item\": \"01 Plans and Permits\",                  \"SalesTaxCode\": \"Non\",                  \"TenantID\": 1              }          ]      }      ````      # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_patch_record(table, record_id, async_req=True)
        >>> result = thread.get()

        :param table: Table name (required)
        :type table: str
        :param record_id: RecordId of the record (required)
        :type record_id: int
        :param body:
        :type body: object
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        return self.tables_patch_record_with_http_info(table, record_id, **kwargs)  # noqa: E501

    def tables_patch_record_with_http_info(self, table, record_id, **kwargs):  # noqa: E501
        """Update Record  # noqa: E501

        To update records in a table.  Specify `{table}` and `{recordId}` in URL path.   Include only the fields you want to modify. Linked fields cannot be modified directly and will be ignored.     ### Examples  - To update LastName, Note and IsActive fields of a Contact with RecordID 5      ```http      PATCH /api/v1/tables/Contacts/5 HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      Content-Type: application/json            {          \"LastName\": \"Anderson\",          \"Note\": \"LastName modified and set active\",          \"IsActive\": true,      }      ```    - To Update Invoice + InvoiceLine(s) in a single request.   Use `__` as a prefix before related table name. This will update the invoice, create or update invoice line(s) and also sync the invoice.    > 📌 __**Note**__ Maximum of 50 related records can be created or updated in a single request.        ````http      PATCH /api/v1/tables/Invoice/4553 HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      Content-Type: application/json        {               \"TxnDate\": \"2020-06-01T16:00:00\",          \"BillAddressAddr1\": \"Blue Jet Airways\",          \"BillAddressAddr2\": \"213 E Washington St\",          \"BillAddressCity\": \"Ashland\",          \"BillAddressState\": \"OH\",          \"BillAddressPostalCode\": \"44805\",          \"BillAddressCountry\": \"USA\",          \"IsPending\": false,          \"IsFinanceCharge\": false,          \"DueDate\": \"2020-06-01T16:00:00\",          \"IsPaid\": false,          \"IsToBePrinted\": false,          \"IsToBeEmailed\": false,          \"IsTaxIncluded\": false,          \"IsWaitingForSyncApproval\": false,          \"TenantID\": 1,          \"ARAccount\": \"Accounts Receivable\",          \"Customer\": \"Blue Jet Airways\",          \"__InvoiceLine\":[              {                  \"RecordID\": 4821,                  \"Desc\": \"Plans and Permits\",                  \"Quantity\": 1,                  \"Rate\": 800,                  \"IsRatePercent\": false,                  \"ServiceDate\": \"2020-06-30T16:15:25\",                  \"UnitOfMeasure\": \"\",                  \"LineOrder\": 1,                  \"LastModifiedDate\": \"2020-06-01T16:16:08.597\",                  \"Item\": \"01 Plans and Permits\",                  \"SalesTaxCode\": \"Non\",                  \"TenantID\": 1              },              {                   \"RecordID\": 4820,                  \"Desc\": \"Plans and Permits\",                  \"Quantity\": 3,                  \"Rate\": 900.00000,                  \"IsRatePercent\": false,                  \"ServiceDate\": \"2020-06-30T16:15:25\",                  \"UnitOfMeasure\": \"\",                  \"LineOrder\": 2,                  \"LastModifiedDate\": \"2020-06-01T16:16:08.597\",                  \"Item\": \"01 Plans and Permits\",                  \"SalesTaxCode\": \"Non\",                  \"TenantID\": 1              },              {                  \"Desc\": \"Plans and Permits\",                  \"Quantity\": 6,                  \"Rate\": 100.00000,                  \"IsRatePercent\": false,                  \"ServiceDate\": \"2020-06-30T16:15:25\",                  \"UnitOfMeasure\": \"\",                  \"LineOrder\": 3,                  \"LastModifiedDate\": \"2020-06-01T16:16:08.597\",                  \"Item\": \"01 Plans and Permits\",                  \"SalesTaxCode\": \"Non\",                  \"TenantID\": 1              }          ]      }      ````      # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_patch_record_with_http_info(table, record_id, async_req=True)
        >>> result = thread.get()

        :param table: Table name (required)
        :type table: str
        :param record_id: RecordId of the record (required)
        :type record_id: int
        :param body:
        :type body: object
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        local_var_params = locals()

        all_params = [
            'table',
            'record_id',
            'body'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method tables_patch_record" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'record_id' is set
        if self.api_client.client_side_validation and ('record_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['record_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `record_id` when calling `tables_patch_record`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'table' in local_var_params:
            path_params['table'] = local_var_params['table']  # noqa: E501
        if 'record_id' in local_var_params:
            path_params['recordId'] = local_var_params['record_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in local_var_params:
            body_params = local_var_params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501
        
        response_types_map = {}

        return self.api_client.call_api(
            '/api/v1/tables/{table}/{recordId}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def tables_query_records(self, table, **kwargs):  # noqa: E501
        """Query Records  # noqa: E501

        To query records from a table. Specify `{table}` in url path.     - `filter` query parameter allows filtering records in a table. You can filter on any table fields, linked fields, and system fields.   See [Filter Reference](#section/Filter-Reference) for more options and examples about this format.  - `skip` and `top` query parameters together allow paginating through the records.   The default value of `top` is 10 and the maximum allowed value of `top` is 100.   i.e Maximum of 100 records can be requested in a single request, use the `nextLink` to get the next 100 rocords.   - By default the query result contains all fields including linked and drop-down fields, but you can request specific fields by using a `select` query parameter.   - `orderby` query parameter allows to requesting records in either ascending order using `asc` or in descending order using `desc`.   If asc or desc not specified, then the resources will be ordered in ascending order.   By default, records are ordered in descending order by `RecordID` field.    ### Examples  - To get first 10 Contacts that have `BillAddressCountry` equal to `Canada`      ```http      GET /api/v1/tables/Contacts?filter=BillAddressCountry eq 'Canada' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```  - To get next 10 Contacts that have `BillAddressCountry` equal to `Canada`      ```http      GET /api/v1/tables/Contacts?skip=10&top=10&filter=BillAddressCountry eq 'Canada' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```    - To get Contacts ordered by `TotalBalance` descending, followed by `LastModifiedDate` ascending      ```http      GET /api/v1/tables/Contacts?skip=10&top=10&filter=BillAddressCountry eq 'Canada'&orderby=TotalBalance desc,LastModifiedDate HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```    - To exclude all fields in result except `BillAddressCountry`,`FirstName`,`LastName` and `RecordID`      ```http      GET /api/v1/tables/Contacts?skip=10&top=10&filter=BillAddressCountry eq 'Canada'&select=BillAddressCountry,FirstName,LastName,RecordID&orderby=TotalBalance desc,LastModifiedDate HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_query_records(table, async_req=True)
        >>> result = thread.get()

        :param table: Table name (required)
        :type table: str
        :param select: List of fields to be returned in the response
        :type select: str
        :param filter: Filter criteria. e.g. Firstname eq 'Amy' <br/> <a href='#section/Filter-Reference'>Filter Reference</a>
        :type filter: str
        :param orderby: Order by specified fields
        :type orderby: str
        :param top: Return only this amount of records
        :type top: int
        :param skip: How many matched records to skip before the first return
        :type skip: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: QueryRecordsResult
        """
        kwargs['_return_http_data_only'] = True
        return self.tables_query_records_with_http_info(table, **kwargs)  # noqa: E501

    def tables_query_records_with_http_info(self, table, **kwargs):  # noqa: E501
        """Query Records  # noqa: E501

        To query records from a table. Specify `{table}` in url path.     - `filter` query parameter allows filtering records in a table. You can filter on any table fields, linked fields, and system fields.   See [Filter Reference](#section/Filter-Reference) for more options and examples about this format.  - `skip` and `top` query parameters together allow paginating through the records.   The default value of `top` is 10 and the maximum allowed value of `top` is 100.   i.e Maximum of 100 records can be requested in a single request, use the `nextLink` to get the next 100 rocords.   - By default the query result contains all fields including linked and drop-down fields, but you can request specific fields by using a `select` query parameter.   - `orderby` query parameter allows to requesting records in either ascending order using `asc` or in descending order using `desc`.   If asc or desc not specified, then the resources will be ordered in ascending order.   By default, records are ordered in descending order by `RecordID` field.    ### Examples  - To get first 10 Contacts that have `BillAddressCountry` equal to `Canada`      ```http      GET /api/v1/tables/Contacts?filter=BillAddressCountry eq 'Canada' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```  - To get next 10 Contacts that have `BillAddressCountry` equal to `Canada`      ```http      GET /api/v1/tables/Contacts?skip=10&top=10&filter=BillAddressCountry eq 'Canada' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```    - To get Contacts ordered by `TotalBalance` descending, followed by `LastModifiedDate` ascending      ```http      GET /api/v1/tables/Contacts?skip=10&top=10&filter=BillAddressCountry eq 'Canada'&orderby=TotalBalance desc,LastModifiedDate HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```    - To exclude all fields in result except `BillAddressCountry`,`FirstName`,`LastName` and `RecordID`      ```http      GET /api/v1/tables/Contacts?skip=10&top=10&filter=BillAddressCountry eq 'Canada'&select=BillAddressCountry,FirstName,LastName,RecordID&orderby=TotalBalance desc,LastModifiedDate HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_query_records_with_http_info(table, async_req=True)
        >>> result = thread.get()

        :param table: Table name (required)
        :type table: str
        :param select: List of fields to be returned in the response
        :type select: str
        :param filter: Filter criteria. e.g. Firstname eq 'Amy' <br/> <a href='#section/Filter-Reference'>Filter Reference</a>
        :type filter: str
        :param orderby: Order by specified fields
        :type orderby: str
        :param top: Return only this amount of records
        :type top: int
        :param skip: How many matched records to skip before the first return
        :type skip: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(QueryRecordsResult, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'table',
            'select',
            'filter',
            'orderby',
            'top',
            'skip'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method tables_query_records" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}
        if 'table' in local_var_params:
            path_params['table'] = local_var_params['table']  # noqa: E501

        query_params = []
        if 'select' in local_var_params and local_var_params['select'] is not None:  # noqa: E501
            query_params.append(('select', local_var_params['select']))  # noqa: E501
        if 'filter' in local_var_params and local_var_params['filter'] is not None:  # noqa: E501
            query_params.append(('filter', local_var_params['filter']))  # noqa: E501
        if 'orderby' in local_var_params and local_var_params['orderby'] is not None:  # noqa: E501
            query_params.append(('orderby', local_var_params['orderby']))  # noqa: E501
        if 'top' in local_var_params and local_var_params['top'] is not None:  # noqa: E501
            query_params.append(('top', local_var_params['top']))  # noqa: E501
        if 'skip' in local_var_params and local_var_params['skip'] is not None:  # noqa: E501
            query_params.append(('skip', local_var_params['skip']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501
        
        response_types_map = {
            400: "ValidationProblemDetails",
            500: "ProblemDetails",
            200: "QueryRecordsResult",
        }

        return self.api_client.call_api(
            '/api/v1/tables/{table}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def tables_record_count(self, table, **kwargs):  # noqa: E501
        """Record Count  # noqa: E501

        To get count of records in a table. Specify `{table}` in url path.    - `filter` query parameter allows filtering records in a table. You can filter on any table fields, linked fields, and system fields.   See [Filter Reference](#section/Filter-Reference) for more options and examples about this format.      ### Examples  - To get count of Contacts that have `BillAddressCountry` equal to `Canada`      ```http      GET /api/v1/tables/Contacts/count?filter=BillAddressCountry eq 'Canada' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```  - To get total count of Contacts       ```http      GET /api/v1/tables/Contacts/count HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```      # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_record_count(table, async_req=True)
        >>> result = thread.get()

        :param table: Table name (required)
        :type table: str
        :param filter: Filter criteria. e.g. Firstname eq 'Amy' <br/> <a href='#section/Filter-Reference'>Filter Reference</a>
        :type filter: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: int
        """
        kwargs['_return_http_data_only'] = True
        return self.tables_record_count_with_http_info(table, **kwargs)  # noqa: E501

    def tables_record_count_with_http_info(self, table, **kwargs):  # noqa: E501
        """Record Count  # noqa: E501

        To get count of records in a table. Specify `{table}` in url path.    - `filter` query parameter allows filtering records in a table. You can filter on any table fields, linked fields, and system fields.   See [Filter Reference](#section/Filter-Reference) for more options and examples about this format.      ### Examples  - To get count of Contacts that have `BillAddressCountry` equal to `Canada`      ```http      GET /api/v1/tables/Contacts/count?filter=BillAddressCountry eq 'Canada' HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```  - To get total count of Contacts       ```http      GET /api/v1/tables/Contacts/count HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      ```      # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_record_count_with_http_info(table, async_req=True)
        >>> result = thread.get()

        :param table: Table name (required)
        :type table: str
        :param filter: Filter criteria. e.g. Firstname eq 'Amy' <br/> <a href='#section/Filter-Reference'>Filter Reference</a>
        :type filter: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(int, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'table',
            'filter'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method tables_record_count" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}
        if 'table' in local_var_params:
            path_params['table'] = local_var_params['table']  # noqa: E501

        query_params = []
        if 'filter' in local_var_params and local_var_params['filter'] is not None:  # noqa: E501
            query_params.append(('filter', local_var_params['filter']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501
        
        response_types_map = {
            400: "ValidationProblemDetails",
            500: "ProblemDetails",
            200: "int",
        }

        return self.api_client.call_api(
            '/api/v1/tables/{table}/count', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def tables_sync_record(self, table, record_id, **kwargs):  # noqa: E501
        """Sync Record  # noqa: E501

        To sync a record in a table with QuickBooks.  Specify `{table}` and `{recordId}` in URL path.   This endpoint works only with syncable tables.   You can find the list of syncable tables for [QuickBooks Desktop](https://help.method.me/en/articles/2589623-supported-tables-for-quickbooks-desktop) and [QuickBooks Online](https://help.method.me/en/articles/2589601-supported-tables-for-quickbooks-online) in our Help Center.   For accounting transactions like Estimates, Invoices etc this endpoint also performs an additional functionality of calculating the total amount.    ### Examples   - To trigger sync for an Invoice with RecordID 10        ```http      POST /api/v1/tables/Invoice/10/Sync HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      Content-Type: application/json      ```    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_sync_record(table, record_id, async_req=True)
        >>> result = thread.get()

        :param table: TableName (required)
        :type table: str
        :param record_id: RecordId of the record (required)
        :type record_id: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        return self.tables_sync_record_with_http_info(table, record_id, **kwargs)  # noqa: E501

    def tables_sync_record_with_http_info(self, table, record_id, **kwargs):  # noqa: E501
        """Sync Record  # noqa: E501

        To sync a record in a table with QuickBooks.  Specify `{table}` and `{recordId}` in URL path.   This endpoint works only with syncable tables.   You can find the list of syncable tables for [QuickBooks Desktop](https://help.method.me/en/articles/2589623-supported-tables-for-quickbooks-desktop) and [QuickBooks Online](https://help.method.me/en/articles/2589601-supported-tables-for-quickbooks-online) in our Help Center.   For accounting transactions like Estimates, Invoices etc this endpoint also performs an additional functionality of calculating the total amount.    ### Examples   - To trigger sync for an Invoice with RecordID 10        ```http      POST /api/v1/tables/Invoice/10/Sync HTTP/1.1      Host: https://rest.method.me      Authorization: Bearer PW27taD3a4egNzZ1F1aiL2nA3Sarhk3CM2dENVWAA7      Content-Type: application/json      ```    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tables_sync_record_with_http_info(table, record_id, async_req=True)
        >>> result = thread.get()

        :param table: TableName (required)
        :type table: str
        :param record_id: RecordId of the record (required)
        :type record_id: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        local_var_params = locals()

        all_params = [
            'table',
            'record_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method tables_sync_record" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'record_id' is set
        if self.api_client.client_side_validation and ('record_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['record_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `record_id` when calling `tables_sync_record`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'table' in local_var_params:
            path_params['table'] = local_var_params['table']  # noqa: E501
        if 'record_id' in local_var_params:
            path_params['recordId'] = local_var_params['record_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501
        
        response_types_map = {}

        return self.api_client.call_api(
            '/api/v1/tables/{table}/{recordId}/Sync', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))
