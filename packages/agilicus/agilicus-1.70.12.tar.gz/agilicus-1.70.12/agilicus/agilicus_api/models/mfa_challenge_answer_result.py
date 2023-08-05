# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.10.20
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from agilicus_api.configuration import Configuration


class MFAChallengeAnswerResult(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'action': 'str',
        'supported_mfa_methods': 'list[str]'
    }

    attribute_map = {
        'action': 'action',
        'supported_mfa_methods': 'supported_mfa_methods'
    }

    def __init__(self, action=None, supported_mfa_methods=None, local_vars_configuration=None):  # noqa: E501
        """MFAChallengeAnswerResult - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._action = None
        self._supported_mfa_methods = None
        self.discriminator = None

        self.action = action
        self.supported_mfa_methods = supported_mfa_methods

    @property
    def action(self):
        """Gets the action of this MFAChallengeAnswerResult.  # noqa: E501

        The action to take as a result of the question. do_mfa - the user should be challenged to present a second factor for authentication dont_mfa - the user does not need to present a second factor for authentication. Proceed with the login workflow. This is depricated in favour of allow_login deny_login - the user should not be allowed to proceed. Terminate the login. allow_login - the user should be allowed to proceed with the login workflow.   # noqa: E501

        :return: The action of this MFAChallengeAnswerResult.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this MFAChallengeAnswerResult.

        The action to take as a result of the question. do_mfa - the user should be challenged to present a second factor for authentication dont_mfa - the user does not need to present a second factor for authentication. Proceed with the login workflow. This is depricated in favour of allow_login deny_login - the user should not be allowed to proceed. Terminate the login. allow_login - the user should be allowed to proceed with the login workflow.   # noqa: E501

        :param action: The action of this MFAChallengeAnswerResult.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and action is None:  # noqa: E501
            raise ValueError("Invalid value for `action`, must not be `None`")  # noqa: E501
        allowed_values = ["do_mfa", "dont_mfa", "deny_login", "allow_login"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and action not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `action` ({0}), must be one of {1}"  # noqa: E501
                .format(action, allowed_values)
            )

        self._action = action

    @property
    def supported_mfa_methods(self):
        """Gets the supported_mfa_methods of this MFAChallengeAnswerResult.  # noqa: E501

        The list of supported multi-factor challenge methods for the organisation  # noqa: E501

        :return: The supported_mfa_methods of this MFAChallengeAnswerResult.  # noqa: E501
        :rtype: list[str]
        """
        return self._supported_mfa_methods

    @supported_mfa_methods.setter
    def supported_mfa_methods(self, supported_mfa_methods):
        """Sets the supported_mfa_methods of this MFAChallengeAnswerResult.

        The list of supported multi-factor challenge methods for the organisation  # noqa: E501

        :param supported_mfa_methods: The supported_mfa_methods of this MFAChallengeAnswerResult.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and supported_mfa_methods is None:  # noqa: E501
            raise ValueError("Invalid value for `supported_mfa_methods`, must not be `None`")  # noqa: E501

        self._supported_mfa_methods = supported_mfa_methods

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MFAChallengeAnswerResult):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MFAChallengeAnswerResult):
            return True

        return self.to_dict() != other.to_dict()
