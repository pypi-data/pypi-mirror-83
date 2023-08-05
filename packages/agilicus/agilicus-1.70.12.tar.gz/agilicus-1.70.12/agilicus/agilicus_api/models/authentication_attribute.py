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


class AuthenticationAttribute(object):
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
        'attribute_name': 'str',
        'internal_attribute_path': 'str'
    }

    attribute_map = {
        'attribute_name': 'attribute_name',
        'internal_attribute_path': 'internal_attribute_path'
    }

    def __init__(self, attribute_name=None, internal_attribute_path=None, local_vars_configuration=None):  # noqa: E501
        """AuthenticationAttribute - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._attribute_name = None
        self._internal_attribute_path = None
        self.discriminator = None

        self.attribute_name = attribute_name
        self.internal_attribute_path = internal_attribute_path

    @property
    def attribute_name(self):
        """Gets the attribute_name of this AuthenticationAttribute.  # noqa: E501

        The of the attribute in the relying party's schema. Case sensitive.  # noqa: E501

        :return: The attribute_name of this AuthenticationAttribute.  # noqa: E501
        :rtype: str
        """
        return self._attribute_name

    @attribute_name.setter
    def attribute_name(self, attribute_name):
        """Sets the attribute_name of this AuthenticationAttribute.

        The of the attribute in the relying party's schema. Case sensitive.  # noqa: E501

        :param attribute_name: The attribute_name of this AuthenticationAttribute.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and attribute_name is None:  # noqa: E501
            raise ValueError("Invalid value for `attribute_name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                attribute_name is not None and len(attribute_name) > 511):
            raise ValueError("Invalid value for `attribute_name`, length must be less than or equal to `511`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                attribute_name is not None and not re.search(r'^[A-Za-z][A-Za-z0-9_]*$', attribute_name)):  # noqa: E501
            raise ValueError(r"Invalid value for `attribute_name`, must be a follow pattern or equal to `/^[A-Za-z][A-Za-z0-9_]*$/`")  # noqa: E501

        self._attribute_name = attribute_name

    @property
    def internal_attribute_path(self):
        """Gets the internal_attribute_path of this AuthenticationAttribute.  # noqa: E501

        The object path to a field to use as the attribute. If the value is not present, null or empty, the attribute will be omitted.   # noqa: E501

        :return: The internal_attribute_path of this AuthenticationAttribute.  # noqa: E501
        :rtype: str
        """
        return self._internal_attribute_path

    @internal_attribute_path.setter
    def internal_attribute_path(self, internal_attribute_path):
        """Sets the internal_attribute_path of this AuthenticationAttribute.

        The object path to a field to use as the attribute. If the value is not present, null or empty, the attribute will be omitted.   # noqa: E501

        :param internal_attribute_path: The internal_attribute_path of this AuthenticationAttribute.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and internal_attribute_path is None:  # noqa: E501
            raise ValueError("Invalid value for `internal_attribute_path`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                internal_attribute_path is not None and len(internal_attribute_path) > 511):
            raise ValueError("Invalid value for `internal_attribute_path`, length must be less than or equal to `511`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                internal_attribute_path is not None and not re.search(r'^([^\.]+\.?)*[^\.]+$', internal_attribute_path)):  # noqa: E501
            raise ValueError(r"Invalid value for `internal_attribute_path`, must be a follow pattern or equal to `/^([^\.]+\.?)*[^\.]+$/`")  # noqa: E501

        self._internal_attribute_path = internal_attribute_path

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
        if not isinstance(other, AuthenticationAttribute):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AuthenticationAttribute):
            return True

        return self.to_dict() != other.to_dict()
