# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.10.20
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from agilicus_api.api_client import ApiClient
from agilicus_api.exceptions import (
    ApiTypeError,
    ApiValueError
)


class FilesApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def add_file(self, name, file_zip, **kwargs):  # noqa: E501
        """upload a file  # noqa: E501

        Upload a file  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_file(name, file_zip, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: Name of file (required)
        :param file file_zip: The contents of the file in binary format (required)
        :param str org_id: Unique identifier
        :param str tag: A file tag
        :param str label: A file label
        :param StorageRegion region:
        :param FileVisibility visibility:
        :param str md5_hash: MD5 Hash of file in base64
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: FileSummary
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.add_file_with_http_info(name, file_zip, **kwargs)  # noqa: E501

    def add_file_with_http_info(self, name, file_zip, **kwargs):  # noqa: E501
        """upload a file  # noqa: E501

        Upload a file  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_file_with_http_info(name, file_zip, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: Name of file (required)
        :param file file_zip: The contents of the file in binary format (required)
        :param str org_id: Unique identifier
        :param str tag: A file tag
        :param str label: A file label
        :param StorageRegion region:
        :param FileVisibility visibility:
        :param str md5_hash: MD5 Hash of file in base64
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(FileSummary, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['name', 'file_zip', 'org_id', 'tag', 'label', 'region', 'visibility', 'md5_hash']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method add_file" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and ('name' not in local_var_params or  # noqa: E501
                                                        local_var_params['name'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `name` when calling `add_file`")  # noqa: E501
        # verify the required parameter 'file_zip' is set
        if self.api_client.client_side_validation and ('file_zip' not in local_var_params or  # noqa: E501
                                                        local_var_params['file_zip'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `file_zip` when calling `add_file`")  # noqa: E501

        if self.api_client.client_side_validation and ('name' in local_var_params and  # noqa: E501
                                                        len(local_var_params['name']) > 100):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `name` when calling `add_file`, length must be less than or equal to `100`")  # noqa: E501
        if self.api_client.client_side_validation and ('name' in local_var_params and  # noqa: E501
                                                        len(local_var_params['name']) < 1):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `name` when calling `add_file`, length must be greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'org_id' in local_var_params:
            form_params.append(('org_id', local_var_params['org_id']))  # noqa: E501
        if 'tag' in local_var_params:
            form_params.append(('tag', local_var_params['tag']))  # noqa: E501
        if 'label' in local_var_params:
            form_params.append(('label', local_var_params['label']))  # noqa: E501
        if 'region' in local_var_params:
            form_params.append(('region', local_var_params['region']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'visibility' in local_var_params:
            form_params.append(('visibility', local_var_params['visibility']))  # noqa: E501
        if 'md5_hash' in local_var_params:
            form_params.append(('md5_hash', local_var_params['md5_hash']))  # noqa: E501
        if 'file_zip' in local_var_params:
            local_var_files['file_zip'] = local_var_params['file_zip']  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['token-valid']  # noqa: E501

        return self.api_client.call_api(
            '/v1/files', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FileSummary',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_file(self, file_id, **kwargs):  # noqa: E501
        """Delete a File  # noqa: E501

        Delete a File  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_file(file_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str file_id: file_id path (required)
        :param str org_id: Organisation Unique identifier
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.delete_file_with_http_info(file_id, **kwargs)  # noqa: E501

    def delete_file_with_http_info(self, file_id, **kwargs):  # noqa: E501
        """Delete a File  # noqa: E501

        Delete a File  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_file_with_http_info(file_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str file_id: file_id path (required)
        :param str org_id: Organisation Unique identifier
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['file_id', 'org_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_file" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'file_id' is set
        if self.api_client.client_side_validation and ('file_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['file_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `file_id` when calling `delete_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'file_id' in local_var_params:
            path_params['file_id'] = local_var_params['file_id']  # noqa: E501

        query_params = []
        if 'org_id' in local_var_params and local_var_params['org_id'] is not None:  # noqa: E501
            query_params.append(('org_id', local_var_params['org_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['token-valid']  # noqa: E501

        return self.api_client.call_api(
            '/v1/files/{file_id}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_download(self, file_id, **kwargs):  # noqa: E501
        """Download File  # noqa: E501

        Download File  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_download(file_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str file_id: file_id path (required)
        :param str org_id: Organisation Unique identifier
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_download_with_http_info(file_id, **kwargs)  # noqa: E501

    def get_download_with_http_info(self, file_id, **kwargs):  # noqa: E501
        """Download File  # noqa: E501

        Download File  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_download_with_http_info(file_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str file_id: file_id path (required)
        :param str org_id: Organisation Unique identifier
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(file, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['file_id', 'org_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_download" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'file_id' is set
        if self.api_client.client_side_validation and ('file_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['file_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `file_id` when calling `get_download`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'file_id' in local_var_params:
            path_params['file_id'] = local_var_params['file_id']  # noqa: E501

        query_params = []
        if 'org_id' in local_var_params and local_var_params['org_id'] is not None:  # noqa: E501
            query_params.append(('org_id', local_var_params['org_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/octet-stream'])  # noqa: E501

        # Authentication setting
        auth_settings = ['token-valid']  # noqa: E501

        return self.api_client.call_api(
            '/v1/files_download/{file_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_file(self, file_id, **kwargs):  # noqa: E501
        """Get File metadata  # noqa: E501

        Get File metadata  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file(file_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str file_id: file_id path (required)
        :param str org_id: Organisation Unique identifier
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: FileSummary
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_file_with_http_info(file_id, **kwargs)  # noqa: E501

    def get_file_with_http_info(self, file_id, **kwargs):  # noqa: E501
        """Get File metadata  # noqa: E501

        Get File metadata  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_with_http_info(file_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str file_id: file_id path (required)
        :param str org_id: Organisation Unique identifier
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(FileSummary, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['file_id', 'org_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_file" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'file_id' is set
        if self.api_client.client_side_validation and ('file_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['file_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `file_id` when calling `get_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'file_id' in local_var_params:
            path_params['file_id'] = local_var_params['file_id']  # noqa: E501

        query_params = []
        if 'org_id' in local_var_params and local_var_params['org_id'] is not None:  # noqa: E501
            query_params.append(('org_id', local_var_params['org_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['token-valid']  # noqa: E501

        return self.api_client.call_api(
            '/v1/files/{file_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FileSummary',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_files(self, **kwargs):  # noqa: E501
        """Query Files  # noqa: E501

        Query Files  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_files(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int limit: limit the number of rows in the response
        :param str org_id: Organisation Unique identifier
        :param str user_id: Query based on user id
        :param str tag: Search files based on tag
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ListFilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.list_files_with_http_info(**kwargs)  # noqa: E501

    def list_files_with_http_info(self, **kwargs):  # noqa: E501
        """Query Files  # noqa: E501

        Query Files  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_files_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int limit: limit the number of rows in the response
        :param str org_id: Organisation Unique identifier
        :param str user_id: Query based on user id
        :param str tag: Search files based on tag
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ListFilesResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['limit', 'org_id', 'user_id', 'tag']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_files" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] > 500:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `list_files`, must be a value less than or equal to `500`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `list_files`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'org_id' in local_var_params and local_var_params['org_id'] is not None:  # noqa: E501
            query_params.append(('org_id', local_var_params['org_id']))  # noqa: E501
        if 'user_id' in local_var_params and local_var_params['user_id'] is not None:  # noqa: E501
            query_params.append(('user_id', local_var_params['user_id']))  # noqa: E501
        if 'tag' in local_var_params and local_var_params['tag'] is not None:  # noqa: E501
            query_params.append(('tag', local_var_params['tag']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['token-valid']  # noqa: E501

        return self.api_client.call_api(
            '/v1/files', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListFilesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def replace_file(self, file_id, file, **kwargs):  # noqa: E501
        """Update a file  # noqa: E501

        Update a file  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_file(file_id, file, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str file_id: file_id path (required)
        :param File file: Upload file request (required)
        :param str org_id: Organisation Unique identifier
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: FileSummary
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.replace_file_with_http_info(file_id, file, **kwargs)  # noqa: E501

    def replace_file_with_http_info(self, file_id, file, **kwargs):  # noqa: E501
        """Update a file  # noqa: E501

        Update a file  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_file_with_http_info(file_id, file, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str file_id: file_id path (required)
        :param File file: Upload file request (required)
        :param str org_id: Organisation Unique identifier
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(FileSummary, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['file_id', 'file', 'org_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method replace_file" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'file_id' is set
        if self.api_client.client_side_validation and ('file_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['file_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `file_id` when calling `replace_file`")  # noqa: E501
        # verify the required parameter 'file' is set
        if self.api_client.client_side_validation and ('file' not in local_var_params or  # noqa: E501
                                                        local_var_params['file'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `file` when calling `replace_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'file_id' in local_var_params:
            path_params['file_id'] = local_var_params['file_id']  # noqa: E501

        query_params = []
        if 'org_id' in local_var_params and local_var_params['org_id'] is not None:  # noqa: E501
            query_params.append(('org_id', local_var_params['org_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'file' in local_var_params:
            body_params = local_var_params['file']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['token-valid']  # noqa: E501

        return self.api_client.call_api(
            '/v1/files/{file_id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FileSummary',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
