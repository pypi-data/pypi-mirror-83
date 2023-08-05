# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.10.20
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import agilicus_api
from agilicus_api.api.issuers_api import IssuersApi  # noqa: E501
from agilicus_api.rest import ApiException


class TestIssuersApi(unittest.TestCase):
    """IssuersApi unit test stubs"""

    def setUp(self):
        self.api = agilicus_api.api.issuers_api.IssuersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_client(self):
        """Test case for create_client

        Create a client  # noqa: E501
        """
        pass

    def test_create_issuer(self):
        """Test case for create_issuer

        Create an issuer  # noqa: E501
        """
        pass

    def test_create_policy(self):
        """Test case for create_policy

        Create a policy  # noqa: E501
        """
        pass

    def test_create_policy_rule(self):
        """Test case for create_policy_rule

        Create a policy rule  # noqa: E501
        """
        pass

    def test_delete_client(self):
        """Test case for delete_client

        Delete a client  # noqa: E501
        """
        pass

    def test_delete_policy(self):
        """Test case for delete_policy

        Delete a Policy  # noqa: E501
        """
        pass

    def test_delete_policy_rule(self):
        """Test case for delete_policy_rule

        Delete a Policy Rule  # noqa: E501
        """
        pass

    def test_delete_root(self):
        """Test case for delete_root

        Delete an Issuer  # noqa: E501
        """
        pass

    def test_get_client(self):
        """Test case for get_client

        Get client  # noqa: E501
        """
        pass

    def test_get_issuer(self):
        """Test case for get_issuer

        Get issuer  # noqa: E501
        """
        pass

    def test_get_policy(self):
        """Test case for get_policy

        Get a policy  # noqa: E501
        """
        pass

    def test_get_policy_rule(self):
        """Test case for get_policy_rule

        Get a policy rule  # noqa: E501
        """
        pass

    def test_get_root(self):
        """Test case for get_root

        Get issuer  # noqa: E501
        """
        pass

    def test_get_wellknown_issuer_info(self):
        """Test case for get_wellknown_issuer_info

        Get well-known issuer information  # noqa: E501
        """
        pass

    def test_list_clients(self):
        """Test case for list_clients

        Query Clients  # noqa: E501
        """
        pass

    def test_list_issuer_roots(self):
        """Test case for list_issuer_roots

        Query Issuers  # noqa: E501
        """
        pass

    def test_list_issuers(self):
        """Test case for list_issuers

        Query Issuers  # noqa: E501
        """
        pass

    def test_list_policies(self):
        """Test case for list_policies

        Query Policies  # noqa: E501
        """
        pass

    def test_list_policy_rules(self):
        """Test case for list_policy_rules

        Query Policies  # noqa: E501
        """
        pass

    def test_list_wellknown_issuer_info(self):
        """Test case for list_wellknown_issuer_info

        list well-known issuer information  # noqa: E501
        """
        pass

    def test_replace_client(self):
        """Test case for replace_client

        Update a client  # noqa: E501
        """
        pass

    def test_replace_issuer(self):
        """Test case for replace_issuer

        Update an issuer  # noqa: E501
        """
        pass

    def test_replace_policy(self):
        """Test case for replace_policy

        Update a policy  # noqa: E501
        """
        pass

    def test_replace_policy_rule(self):
        """Test case for replace_policy_rule

        Update a policy rule  # noqa: E501
        """
        pass

    def test_replace_root(self):
        """Test case for replace_root

        Update an issuer  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
