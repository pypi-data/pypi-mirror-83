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


class ListPoliciesResponse(object):
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
        'authentication_policies': 'list[Policy]',
        'limit': 'int'
    }

    attribute_map = {
        'authentication_policies': 'authentication_policies',
        'limit': 'limit'
    }

    def __init__(self, authentication_policies=None, limit=None, local_vars_configuration=None):  # noqa: E501
        """ListPoliciesResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._authentication_policies = None
        self._limit = None
        self.discriminator = None

        self.authentication_policies = authentication_policies
        self.limit = limit

    @property
    def authentication_policies(self):
        """Gets the authentication_policies of this ListPoliciesResponse.  # noqa: E501

        List of policies  # noqa: E501

        :return: The authentication_policies of this ListPoliciesResponse.  # noqa: E501
        :rtype: list[Policy]
        """
        return self._authentication_policies

    @authentication_policies.setter
    def authentication_policies(self, authentication_policies):
        """Sets the authentication_policies of this ListPoliciesResponse.

        List of policies  # noqa: E501

        :param authentication_policies: The authentication_policies of this ListPoliciesResponse.  # noqa: E501
        :type: list[Policy]
        """
        if self.local_vars_configuration.client_side_validation and authentication_policies is None:  # noqa: E501
            raise ValueError("Invalid value for `authentication_policies`, must not be `None`")  # noqa: E501

        self._authentication_policies = authentication_policies

    @property
    def limit(self):
        """Gets the limit of this ListPoliciesResponse.  # noqa: E501

        Limit of policies in the response  # noqa: E501

        :return: The limit of this ListPoliciesResponse.  # noqa: E501
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListPoliciesResponse.

        Limit of policies in the response  # noqa: E501

        :param limit: The limit of this ListPoliciesResponse.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and limit is None:  # noqa: E501
            raise ValueError("Invalid value for `limit`, must not be `None`")  # noqa: E501

        self._limit = limit

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
        if not isinstance(other, ListPoliciesResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ListPoliciesResponse):
            return True

        return self.to_dict() != other.to_dict()
