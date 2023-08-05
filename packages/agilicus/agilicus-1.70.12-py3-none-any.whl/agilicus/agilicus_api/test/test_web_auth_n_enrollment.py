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
from agilicus_api.models.web_auth_n_enrollment import WebAuthNEnrollment  # noqa: E501
from agilicus_api.rest import ApiException

class TestWebAuthNEnrollment(unittest.TestCase):
    """WebAuthNEnrollment unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test WebAuthNEnrollment
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.web_auth_n_enrollment.WebAuthNEnrollment()  # noqa: E501
        if include_optional :
            return WebAuthNEnrollment(
                metadata = {"id":"ac233asaksjfF","created":"2017-07-07T15:49:51.230+00:00","updated":"2020-01-27T12:19:46.430+00:00"}, 
                spec = agilicus_api.models.web_auth_n_enrollment_spec.WebAuthNEnrollmentSpec(
                    user_id = '123', 
                    relying_party_id = '123', 
                    attestation_format = 'platform', 
                    attestation_conveyance = 'direct', 
                    user_verification = 'discouraged', ), 
                status = agilicus_api.models.web_auth_n_enrollment_status.WebAuthNEnrollmentStatus(
                    challenge = 'asdas43ADlaksda8739asfoafsalkasjd', 
                    credential_id = 'YQ==', 
                    transports = [
                        'ble'
                        ], )
            )
        else :
            return WebAuthNEnrollment(
                spec = agilicus_api.models.web_auth_n_enrollment_spec.WebAuthNEnrollmentSpec(
                    user_id = '123', 
                    relying_party_id = '123', 
                    attestation_format = 'platform', 
                    attestation_conveyance = 'direct', 
                    user_verification = 'discouraged', ),
        )

    def testWebAuthNEnrollment(self):
        """Test WebAuthNEnrollment"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
