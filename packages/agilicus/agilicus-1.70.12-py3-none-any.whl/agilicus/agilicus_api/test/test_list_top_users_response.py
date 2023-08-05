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
import datetime

import agilicus_api
from agilicus_api.models.list_top_users_response import ListTopUsersResponse  # noqa: E501
from agilicus_api.rest import ApiException

class TestListTopUsersResponse(unittest.TestCase):
    """ListTopUsersResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListTopUsersResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.list_top_users_response.ListTopUsersResponse()  # noqa: E501
        if include_optional :
            return ListTopUsersResponse(
                top_users = [
                    agilicus_api.models.user_metrics.UserMetrics(
                        email = 'foo@example.com', 
                        count = 56, 
                        user_id = '0', )
                    ], 
                limit = 56
            )
        else :
            return ListTopUsersResponse(
                limit = 56,
        )

    def testListTopUsersResponse(self):
        """Test ListTopUsersResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
