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
from agilicus_api.models.list_policies_response import ListPoliciesResponse  # noqa: E501
from agilicus_api.rest import ApiException

class TestListPoliciesResponse(unittest.TestCase):
    """ListPoliciesResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListPoliciesResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.list_policies_response.ListPoliciesResponse()  # noqa: E501
        if include_optional :
            return ListPoliciesResponse(
                authentication_policies = [
                    agilicus_api.models.policy.Policy(
                        metadata = {"id":"ac233asaksjfF","created":"2017-07-07T15:49:51.230+00:00","updated":"2020-01-27T12:19:46.430+00:00"}, 
                        spec = agilicus_api.models.policy_spec.PolicySpec(
                            name = 'Staging org authentication policy', 
                            issuer_id = 'asdfg123hjkl', 
                            org_id = 'asdfg123hjkl', 
                            supported_mfa_methods = ["totp","webauthn"], 
                            default_action = 'enroll', 
                            rules = [
                                agilicus_api.models.policy_rule.PolicyRule(
                                    spec = agilicus_api.models.policy_rule_spec.PolicyRuleSpec(
                                        name = 'blocked IPs rule', 
                                        action = 'enroll', 
                                        priority = 1, 
                                        org_id = 'asdfg123hjkl', 
                                        conditions = [
                                            agilicus_api.models.policy_condition.PolicyCondition(
                                                condition_type = 'type_client_id_list', 
                                                inverted = True, 
                                                value = 'my-city-org', 
                                                operator = 'equals', 
                                                field = 'clients.name', 
                                                created = '2015-07-07T15:49:51.230+02:00', 
                                                updated = '2015-07-07T15:49:51.230+02:00', )
                                            ], ), )
                                ], 
                            policy_groups = [
                                agilicus_api.models.policy_group.PolicyGroup(
                                    spec = agilicus_api.models.policy_group_spec.PolicyGroupSpec(
                                        name = '0', 
                                        rule_ids = [
                                            '123'
                                            ], ), )
                                ], ), )
                    ], 
                limit = 56
            )
        else :
            return ListPoliciesResponse(
                authentication_policies = [
                    agilicus_api.models.policy.Policy(
                        metadata = {"id":"ac233asaksjfF","created":"2017-07-07T15:49:51.230+00:00","updated":"2020-01-27T12:19:46.430+00:00"}, 
                        spec = agilicus_api.models.policy_spec.PolicySpec(
                            name = 'Staging org authentication policy', 
                            issuer_id = 'asdfg123hjkl', 
                            org_id = 'asdfg123hjkl', 
                            supported_mfa_methods = ["totp","webauthn"], 
                            default_action = 'enroll', 
                            rules = [
                                agilicus_api.models.policy_rule.PolicyRule(
                                    spec = agilicus_api.models.policy_rule_spec.PolicyRuleSpec(
                                        name = 'blocked IPs rule', 
                                        action = 'enroll', 
                                        priority = 1, 
                                        org_id = 'asdfg123hjkl', 
                                        conditions = [
                                            agilicus_api.models.policy_condition.PolicyCondition(
                                                condition_type = 'type_client_id_list', 
                                                inverted = True, 
                                                value = 'my-city-org', 
                                                operator = 'equals', 
                                                field = 'clients.name', 
                                                created = '2015-07-07T15:49:51.230+02:00', 
                                                updated = '2015-07-07T15:49:51.230+02:00', )
                                            ], ), )
                                ], 
                            policy_groups = [
                                agilicus_api.models.policy_group.PolicyGroup(
                                    spec = agilicus_api.models.policy_group_spec.PolicyGroupSpec(
                                        name = '0', 
                                        rule_ids = [
                                            '123'
                                            ], ), )
                                ], ), )
                    ],
                limit = 56,
        )

    def testListPoliciesResponse(self):
        """Test ListPoliciesResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
