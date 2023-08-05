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
from agilicus_api.models.list_totp_enrollment_response import ListTOTPEnrollmentResponse  # noqa: E501
from agilicus_api.rest import ApiException

class TestListTOTPEnrollmentResponse(unittest.TestCase):
    """ListTOTPEnrollmentResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListTOTPEnrollmentResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.list_totp_enrollment_response.ListTOTPEnrollmentResponse()  # noqa: E501
        if include_optional :
            return ListTOTPEnrollmentResponse(
                totp = [
                    agilicus_api.models.totp_enrollment.TOTPEnrollment(
                        metadata = {"id":"ac233asaksjfF","created":"2017-07-07T15:49:51.230+00:00","updated":"2020-01-27T12:19:46.430+00:00"}, 
                        spec = agilicus_api.models.totp_enrollment_spec.TOTPEnrollmentSpec(
                            user_id = '123', ), 
                        status = agilicus_api.models.totp_enrollment_status.TOTPEnrollmentStatus(
                            state = 'pending', 
                            key = 'asdas43ADlaksda8739asfoafsalkasjd', ), )
                    ], 
                limit = 56
            )
        else :
            return ListTOTPEnrollmentResponse(
                limit = 56,
        )

    def testListTOTPEnrollmentResponse(self):
        """Test ListTOTPEnrollmentResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
