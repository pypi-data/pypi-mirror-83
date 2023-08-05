# coding: utf-8

"""
    Fortanix SDKMS REST API

    This is a set of REST APIs for accessing the Fortanix Self-Defending Key Management System. This includes APIs for managing accounts, and for performing cryptographic and key management operations. 

    OpenAPI spec version: 1.0.0-20200608
    Contact: support@fortanix.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""


from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..api_client import ApiClient


# NOTE: This class is auto generated by the swagger code generator program.
# Do not edit the class manually.
# Ref: https://github.com/swagger-api/swagger-codegen
class WrappingAndUnwrappingApi(object):
    """
    @undocumented: unwrap_key_with_http_info
    @undocumented: unwrap_key_ex_with_http_info
    @undocumented: wrap_key_with_http_info
    @undocumented: wrap_key_ex_with_http_info
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def unwrap_key(self, key_id, body, async_call=False, **kwargs):
        """
        Unwrap (decrypt) a wrapped key and import it into SDKMS. This allows securely importing into SDKMS security objects that were previously wrapped by SDKMS or another key management system. A new security object will be created in SDKMS with the unwrapped data. <br> The key-id parameter in the URL specifies the key that will be used to unwrap the other security object. This key must have the unwrapkey operation enabled. <br> The alg and mode parameters specify the encryption algorithm and cipher mode being used by the unwrapping key. The obj_type parameter specifies the object type of the security object being unwrapped. The size or elliptic curve of the object being unwrapped does not need to be specified. 
        @type async_call: bool
        @param async_call: Whether the call should be performed asynchronously. (Default is False).
        @type key_id: L{str}
        @param key_id: kid of security object (required)
        @type body: L{UnwrapKeyRequest}
        @param body: Unwrap key request (required)
        @rtype: L{KeyObject}
        @return:
        
        If the method is called asynchronously, returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if async_call:
            return self.unwrap_key_with_http_info(key_id, body, async_call=async_call, **kwargs)
        else:
            (data) = self.unwrap_key_with_http_info(key_id, body, async_call=async_call, **kwargs)
            return data

    def unwrap_key_with_http_info(self, key_id, body, async_call=False, **kwargs):
        """
        Unwrap (decrypt) a wrapped key and import it into SDKMS. This allows securely importing into SDKMS security objects that were previously wrapped by SDKMS or another key management system. A new security object will be created in SDKMS with the unwrapped data. <br> The key-id parameter in the URL specifies the key that will be used to unwrap the other security object. This key must have the unwrapkey operation enabled. <br> The alg and mode parameters specify the encryption algorithm and cipher mode being used by the unwrapping key. The obj_type parameter specifies the object type of the security object being unwrapped. The size or elliptic curve of the object being unwrapped does not need to be specified. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_call=True::
            >>> thread = api.unwrap_key_with_http_info(key_id, body, async_call=True)
            >>> result = thread.get()

        @type async_call: bool
        @param async_call: Whether the call should be performed asynchronously. (Default is False).
        @type key_id: L{str}
        @param key_id: kid of security object (required)
        @type body: L{UnwrapKeyRequest}
        @param body: Unwrap key request (required)
        @rtype: L{KeyObject}
        @return:

        If the method is called asynchronously, returns the request thread.
        """

        all_params = ['key_id', 'body']
        all_params.append('async_call')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method unwrap_key" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'key_id' is set
        if ('key_id' not in params) or (params['key_id'] is None):
            raise ValueError("Missing the required parameter `key_id` when calling `unwrap_key`")
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `unwrap_key`")


        collection_formats = {}

        path_params = {}
        if 'key_id' in params:
            path_params['key-id'] = params['key_id']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = ['bearerToken']

        return self.api_client.call_api('/crypto/v1/keys/{key-id}/unwrapkey', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='KeyObject',
                                        auth_settings=auth_settings,
                                        async_call=params.get('async_call'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def unwrap_key_ex(self, body, async_call=False, **kwargs):
        """
        Unwrap (decrypt) a wrapped key and import it into SDKMS. This allows securely importing into SDKMS security objects that were previously wrapped by SDKMS or another key management system. A new security object will be created in SDKMS with the unwrapped data. <br> The key-id parameter in the URL specifies the key that will be used to unwrap the other security object. This key must have the unwrapkey operation enabled. <br> The alg and mode parameters specify the encryption algorithm and cipher mode being used by the unwrapping key. The obj_type parameter specifies the object type of the security object being unwrapped. The size or elliptic curve of the object being unwrapped does not need to be specified. 
        @type async_call: bool
        @param async_call: Whether the call should be performed asynchronously. (Default is False).
        @type body: L{UnwrapKeyRequestEx}
        @param body: Unwrap key request (required)
        @rtype: L{KeyObject}
        @return:
        
        If the method is called asynchronously, returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if async_call:
            return self.unwrap_key_ex_with_http_info(body, async_call=async_call, **kwargs)
        else:
            (data) = self.unwrap_key_ex_with_http_info(body, async_call=async_call, **kwargs)
            return data

    def unwrap_key_ex_with_http_info(self, body, async_call=False, **kwargs):
        """
        Unwrap (decrypt) a wrapped key and import it into SDKMS. This allows securely importing into SDKMS security objects that were previously wrapped by SDKMS or another key management system. A new security object will be created in SDKMS with the unwrapped data. <br> The key-id parameter in the URL specifies the key that will be used to unwrap the other security object. This key must have the unwrapkey operation enabled. <br> The alg and mode parameters specify the encryption algorithm and cipher mode being used by the unwrapping key. The obj_type parameter specifies the object type of the security object being unwrapped. The size or elliptic curve of the object being unwrapped does not need to be specified. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_call=True::
            >>> thread = api.unwrap_key_ex_with_http_info(body, async_call=True)
            >>> result = thread.get()

        @type async_call: bool
        @param async_call: Whether the call should be performed asynchronously. (Default is False).
        @type body: L{UnwrapKeyRequestEx}
        @param body: Unwrap key request (required)
        @rtype: L{KeyObject}
        @return:

        If the method is called asynchronously, returns the request thread.
        """

        all_params = ['body']
        all_params.append('async_call')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method unwrap_key_ex" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `unwrap_key_ex`")


        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = ['bearerToken']

        return self.api_client.call_api('/crypto/v1/unwrapkey', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='KeyObject',
                                        auth_settings=auth_settings,
                                        async_call=params.get('async_call'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def wrap_key(self, key_id, body, async_call=False, **kwargs):
        """
        Wrap (encrypt) an existing security object with a key. This allows keys to be securely exported from SDKMS so they can be later imported into SDKMS or another key management system. <br> The key-id parameter in the URL specifies the key that will be used to wrap the other security object. The security object being wrapped is specified inside of the request body. <br> The alg and mode parameters specify the encryption algorithm and cipher mode being used for the wrapping key. The algorithm of the key being wrapped is not provided to this API call. <br> The key being wrapped must have the export operation enabled. The wrapping key must have the wrapkey operation enabled. <br> The following wrapping operations are supported:   * Symmetric keys, HMAC keys, opaque objects, and secret objects may be wrapped with symmetric or asymmetric keys.   * Asymmetric keys may be wrapped with symmetric keys. Wrapping an asymmetric key with an asymmetric key is not supported.  When wrapping with an asymmetric key, the wrapped object size must fit as plaintext for the wrapping key size and algorithm. 
        @type async_call: bool
        @param async_call: Whether the call should be performed asynchronously. (Default is False).
        @type key_id: L{str}
        @param key_id: kid of security object (required)
        @type body: L{WrapKeyRequest}
        @param body: Wrap key request (required)
        @rtype: L{WrapKeyResponse}
        @return:
        
        If the method is called asynchronously, returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if async_call:
            return self.wrap_key_with_http_info(key_id, body, async_call=async_call, **kwargs)
        else:
            (data) = self.wrap_key_with_http_info(key_id, body, async_call=async_call, **kwargs)
            return data

    def wrap_key_with_http_info(self, key_id, body, async_call=False, **kwargs):
        """
        Wrap (encrypt) an existing security object with a key. This allows keys to be securely exported from SDKMS so they can be later imported into SDKMS or another key management system. <br> The key-id parameter in the URL specifies the key that will be used to wrap the other security object. The security object being wrapped is specified inside of the request body. <br> The alg and mode parameters specify the encryption algorithm and cipher mode being used for the wrapping key. The algorithm of the key being wrapped is not provided to this API call. <br> The key being wrapped must have the export operation enabled. The wrapping key must have the wrapkey operation enabled. <br> The following wrapping operations are supported:   * Symmetric keys, HMAC keys, opaque objects, and secret objects may be wrapped with symmetric or asymmetric keys.   * Asymmetric keys may be wrapped with symmetric keys. Wrapping an asymmetric key with an asymmetric key is not supported.  When wrapping with an asymmetric key, the wrapped object size must fit as plaintext for the wrapping key size and algorithm. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_call=True::
            >>> thread = api.wrap_key_with_http_info(key_id, body, async_call=True)
            >>> result = thread.get()

        @type async_call: bool
        @param async_call: Whether the call should be performed asynchronously. (Default is False).
        @type key_id: L{str}
        @param key_id: kid of security object (required)
        @type body: L{WrapKeyRequest}
        @param body: Wrap key request (required)
        @rtype: L{WrapKeyResponse}
        @return:

        If the method is called asynchronously, returns the request thread.
        """

        all_params = ['key_id', 'body']
        all_params.append('async_call')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method wrap_key" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'key_id' is set
        if ('key_id' not in params) or (params['key_id'] is None):
            raise ValueError("Missing the required parameter `key_id` when calling `wrap_key`")
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `wrap_key`")


        collection_formats = {}

        path_params = {}
        if 'key_id' in params:
            path_params['key-id'] = params['key_id']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = ['bearerToken']

        return self.api_client.call_api('/crypto/v1/keys/{key-id}/wrapkey', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='WrapKeyResponse',
                                        auth_settings=auth_settings,
                                        async_call=params.get('async_call'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def wrap_key_ex(self, body, async_call=False, **kwargs):
        """
        Wrap (encrypt) an existing security object with a key. This allows keys to be securely exported from SDKMS so they can be later imported into SDKMS or another key management system. <br> The key-id parameter in the URL specifies the key that will be used to wrap the other security object. The security object being wrapped is specified inside of the request body. <br> The alg and mode parameters specify the encryption algorithm and cipher mode being used for the wrapping key. The algorithm of the key being wrapped is not provided to this API call. <br> The key being wrapped must have the export operation enabled. The wrapping key must have the wrapkey operation enabled. <br> The following wrapping operations are supported:   * Symmetric keys, HMAC keys, opaque objects, and secret objects may be wrapped with symmetric or asymmetric keys.   * Asymmetric keys may be wrapped with symmetric keys. Wrapping an asymmetric key with an asymmetric key is not supported.  When wrapping with an asymmetric key, the wrapped object size must fit as plaintext for the wrapping key size and algorithm. 
        @type async_call: bool
        @param async_call: Whether the call should be performed asynchronously. (Default is False).
        @type body: L{WrapKeyRequestEx}
        @param body: Wrap key request (required)
        @rtype: L{WrapKeyResponse}
        @return:
        
        If the method is called asynchronously, returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if async_call:
            return self.wrap_key_ex_with_http_info(body, async_call=async_call, **kwargs)
        else:
            (data) = self.wrap_key_ex_with_http_info(body, async_call=async_call, **kwargs)
            return data

    def wrap_key_ex_with_http_info(self, body, async_call=False, **kwargs):
        """
        Wrap (encrypt) an existing security object with a key. This allows keys to be securely exported from SDKMS so they can be later imported into SDKMS or another key management system. <br> The key-id parameter in the URL specifies the key that will be used to wrap the other security object. The security object being wrapped is specified inside of the request body. <br> The alg and mode parameters specify the encryption algorithm and cipher mode being used for the wrapping key. The algorithm of the key being wrapped is not provided to this API call. <br> The key being wrapped must have the export operation enabled. The wrapping key must have the wrapkey operation enabled. <br> The following wrapping operations are supported:   * Symmetric keys, HMAC keys, opaque objects, and secret objects may be wrapped with symmetric or asymmetric keys.   * Asymmetric keys may be wrapped with symmetric keys. Wrapping an asymmetric key with an asymmetric key is not supported.  When wrapping with an asymmetric key, the wrapped object size must fit as plaintext for the wrapping key size and algorithm. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_call=True::
            >>> thread = api.wrap_key_ex_with_http_info(body, async_call=True)
            >>> result = thread.get()

        @type async_call: bool
        @param async_call: Whether the call should be performed asynchronously. (Default is False).
        @type body: L{WrapKeyRequestEx}
        @param body: Wrap key request (required)
        @rtype: L{WrapKeyResponse}
        @return:

        If the method is called asynchronously, returns the request thread.
        """

        all_params = ['body']
        all_params.append('async_call')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method wrap_key_ex" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `wrap_key_ex`")


        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = ['bearerToken']

        return self.api_client.call_api('/crypto/v1/wrapkey', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='WrapKeyResponse',
                                        auth_settings=auth_settings,
                                        async_call=params.get('async_call'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
