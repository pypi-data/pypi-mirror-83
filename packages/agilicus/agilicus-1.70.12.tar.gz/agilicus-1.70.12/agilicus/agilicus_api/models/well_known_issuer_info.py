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


class WellKnownIssuerInfo(object):
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
        'issuer_id': 'str',
        'supported_mfa_methods': 'list[str]'
    }

    attribute_map = {
        'issuer_id': 'issuer_id',
        'supported_mfa_methods': 'supported_mfa_methods'
    }

    def __init__(self, issuer_id=None, supported_mfa_methods=None, local_vars_configuration=None):  # noqa: E501
        """WellKnownIssuerInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._issuer_id = None
        self._supported_mfa_methods = None
        self.discriminator = None

        if issuer_id is not None:
            self.issuer_id = issuer_id
        self.supported_mfa_methods = supported_mfa_methods

    @property
    def issuer_id(self):
        """Gets the issuer_id of this WellKnownIssuerInfo.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The issuer_id of this WellKnownIssuerInfo.  # noqa: E501
        :rtype: str
        """
        return self._issuer_id

    @issuer_id.setter
    def issuer_id(self, issuer_id):
        """Sets the issuer_id of this WellKnownIssuerInfo.

        Unique identifier  # noqa: E501

        :param issuer_id: The issuer_id of this WellKnownIssuerInfo.  # noqa: E501
        :type: str
        """

        self._issuer_id = issuer_id

    @property
    def supported_mfa_methods(self):
        """Gets the supported_mfa_methods of this WellKnownIssuerInfo.  # noqa: E501

        A list of supported MFA methods. An empty list implies that no MFA methods are acceptable  # noqa: E501

        :return: The supported_mfa_methods of this WellKnownIssuerInfo.  # noqa: E501
        :rtype: list[str]
        """
        return self._supported_mfa_methods

    @supported_mfa_methods.setter
    def supported_mfa_methods(self, supported_mfa_methods):
        """Sets the supported_mfa_methods of this WellKnownIssuerInfo.

        A list of supported MFA methods. An empty list implies that no MFA methods are acceptable  # noqa: E501

        :param supported_mfa_methods: The supported_mfa_methods of this WellKnownIssuerInfo.  # noqa: E501
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
        if not isinstance(other, WellKnownIssuerInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, WellKnownIssuerInfo):
            return True

        return self.to_dict() != other.to_dict()
