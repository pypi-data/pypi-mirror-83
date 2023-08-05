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
from agilicus_api.models.mfa_challenge_question_input import MFAChallengeQuestionInput  # noqa: E501
from agilicus_api.rest import ApiException

class TestMFAChallengeQuestionInput(unittest.TestCase):
    """MFAChallengeQuestionInput unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test MFAChallengeQuestionInput
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.mfa_challenge_question_input.MFAChallengeQuestionInput()  # noqa: E501
        if include_optional :
            return MFAChallengeQuestionInput(
                login_info = agilicus_api.models.mfa_challenge_question_login_info.MFAChallengeQuestionLoginInfo(
                    user_preference = 'organisation_policy', 
                    client_id = 'app-1', 
                    client_guid = 'absjfladasdf23', 
                    issuer_org_id = 'absjfladasdf23', 
                    issuer_guid = 'absjfladasdf23', 
                    org_id = 'absjfladasdf23', 
                    user_id = 'jjkkGmwB9oTJWDjIglTU', 
                    user_object = agilicus_api.models.user_summary.UserSummary(
                        id = '123', 
                        external_id = '123', 
                        enabled = False, 
                        status = 'active', 
                        first_name = 'Alice', 
                        last_name = 'Kim', 
                        email = 'foo@example.com', 
                        provider = 'Google', 
                        roles = {"app-1":["viewer"],"app-2":["owner"]}, 
                        org_id = '123', 
                        created = '2015-07-07T15:49:51.230+02:00', 
                        updated = '2015-07-07T15:49:51.230+02:00', 
                        auto_created = True, 
                        upstream_user_identities = [
                            agilicus_api.models.upstream_user_identity.UpstreamUserIdentity(
                                metadata = {"id":"ac233asaksjfF","created":"2017-07-07T15:49:51.230+00:00","updated":"2020-01-27T12:19:46.430+00:00"}, 
                                spec = agilicus_api.models.upstream_user_identity_spec.UpstreamUserIdentitySpec(
                                    upstream_user_id = 'aa-bb-cc-11-22-33', 
                                    upstream_idp_id = 'https://auth.cloud.egov.city', 
                                    local_user_id = 'tuU7smH86zAXMl76sua6xQ', ), )
                            ], ), 
                    upstream_idp = 'city-adfs', 
                    ip_address = '127.0.0.1', 
                    amr_claim_present = True, 
                    last_mfa_login = '2015-07-07T15:49:51.230+02:00', )
            )
        else :
            return MFAChallengeQuestionInput(
                login_info = agilicus_api.models.mfa_challenge_question_login_info.MFAChallengeQuestionLoginInfo(
                    user_preference = 'organisation_policy', 
                    client_id = 'app-1', 
                    client_guid = 'absjfladasdf23', 
                    issuer_org_id = 'absjfladasdf23', 
                    issuer_guid = 'absjfladasdf23', 
                    org_id = 'absjfladasdf23', 
                    user_id = 'jjkkGmwB9oTJWDjIglTU', 
                    user_object = agilicus_api.models.user_summary.UserSummary(
                        id = '123', 
                        external_id = '123', 
                        enabled = False, 
                        status = 'active', 
                        first_name = 'Alice', 
                        last_name = 'Kim', 
                        email = 'foo@example.com', 
                        provider = 'Google', 
                        roles = {"app-1":["viewer"],"app-2":["owner"]}, 
                        org_id = '123', 
                        created = '2015-07-07T15:49:51.230+02:00', 
                        updated = '2015-07-07T15:49:51.230+02:00', 
                        auto_created = True, 
                        upstream_user_identities = [
                            agilicus_api.models.upstream_user_identity.UpstreamUserIdentity(
                                metadata = {"id":"ac233asaksjfF","created":"2017-07-07T15:49:51.230+00:00","updated":"2020-01-27T12:19:46.430+00:00"}, 
                                spec = agilicus_api.models.upstream_user_identity_spec.UpstreamUserIdentitySpec(
                                    upstream_user_id = 'aa-bb-cc-11-22-33', 
                                    upstream_idp_id = 'https://auth.cloud.egov.city', 
                                    local_user_id = 'tuU7smH86zAXMl76sua6xQ', ), )
                            ], ), 
                    upstream_idp = 'city-adfs', 
                    ip_address = '127.0.0.1', 
                    amr_claim_present = True, 
                    last_mfa_login = '2015-07-07T15:49:51.230+02:00', ),
        )

    def testMFAChallengeQuestionInput(self):
        """Test MFAChallengeQuestionInput"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
