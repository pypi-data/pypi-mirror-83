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


class UpstreamUserIdentitySpec(object):
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
        'upstream_user_id': 'str',
        'upstream_idp_id': 'str',
        'local_user_id': 'str'
    }

    attribute_map = {
        'upstream_user_id': 'upstream_user_id',
        'upstream_idp_id': 'upstream_idp_id',
        'local_user_id': 'local_user_id'
    }

    def __init__(self, upstream_user_id=None, upstream_idp_id=None, local_user_id=None, local_vars_configuration=None):  # noqa: E501
        """UpstreamUserIdentitySpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._upstream_user_id = None
        self._upstream_idp_id = None
        self._local_user_id = None
        self.discriminator = None

        self.upstream_user_id = upstream_user_id
        self.upstream_idp_id = upstream_idp_id
        self.local_user_id = local_user_id

    @property
    def upstream_user_id(self):
        """Gets the upstream_user_id of this UpstreamUserIdentitySpec.  # noqa: E501

        The unique id of the user in the upstream identifier provider. This need not be globally unique within the system. However, the pair of it and `upstream_idp_id` must be.   # noqa: E501

        :return: The upstream_user_id of this UpstreamUserIdentitySpec.  # noqa: E501
        :rtype: str
        """
        return self._upstream_user_id

    @upstream_user_id.setter
    def upstream_user_id(self, upstream_user_id):
        """Sets the upstream_user_id of this UpstreamUserIdentitySpec.

        The unique id of the user in the upstream identifier provider. This need not be globally unique within the system. However, the pair of it and `upstream_idp_id` must be.   # noqa: E501

        :param upstream_user_id: The upstream_user_id of this UpstreamUserIdentitySpec.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and upstream_user_id is None:  # noqa: E501
            raise ValueError("Invalid value for `upstream_user_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                upstream_user_id is not None and len(upstream_user_id) > 1024):
            raise ValueError("Invalid value for `upstream_user_id`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                upstream_user_id is not None and len(upstream_user_id) < 1):
            raise ValueError("Invalid value for `upstream_user_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._upstream_user_id = upstream_user_id

    @property
    def upstream_idp_id(self):
        """Gets the upstream_idp_id of this UpstreamUserIdentitySpec.  # noqa: E501

        The unique id of the upstream identity provider within the system. When the user authenticates using the corresponding upstream identity provider, they will join against the user record owning this `UpstreamUseridentitySpec` by linking with the `upstream_user_id` as given by the upstream identity. Typically this will be the issuer URI. Note that it is case sensitive.   # noqa: E501

        :return: The upstream_idp_id of this UpstreamUserIdentitySpec.  # noqa: E501
        :rtype: str
        """
        return self._upstream_idp_id

    @upstream_idp_id.setter
    def upstream_idp_id(self, upstream_idp_id):
        """Sets the upstream_idp_id of this UpstreamUserIdentitySpec.

        The unique id of the upstream identity provider within the system. When the user authenticates using the corresponding upstream identity provider, they will join against the user record owning this `UpstreamUseridentitySpec` by linking with the `upstream_user_id` as given by the upstream identity. Typically this will be the issuer URI. Note that it is case sensitive.   # noqa: E501

        :param upstream_idp_id: The upstream_idp_id of this UpstreamUserIdentitySpec.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and upstream_idp_id is None:  # noqa: E501
            raise ValueError("Invalid value for `upstream_idp_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                upstream_idp_id is not None and len(upstream_idp_id) > 511):
            raise ValueError("Invalid value for `upstream_idp_id`, length must be less than or equal to `511`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                upstream_idp_id is not None and len(upstream_idp_id) < 1):
            raise ValueError("Invalid value for `upstream_idp_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._upstream_idp_id = upstream_idp_id

    @property
    def local_user_id(self):
        """Gets the local_user_id of this UpstreamUserIdentitySpec.  # noqa: E501

        The unique id of the user within the system. This is the user to which this identity is tied.   # noqa: E501

        :return: The local_user_id of this UpstreamUserIdentitySpec.  # noqa: E501
        :rtype: str
        """
        return self._local_user_id

    @local_user_id.setter
    def local_user_id(self, local_user_id):
        """Sets the local_user_id of this UpstreamUserIdentitySpec.

        The unique id of the user within the system. This is the user to which this identity is tied.   # noqa: E501

        :param local_user_id: The local_user_id of this UpstreamUserIdentitySpec.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and local_user_id is None:  # noqa: E501
            raise ValueError("Invalid value for `local_user_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                local_user_id is not None and len(local_user_id) > 40):
            raise ValueError("Invalid value for `local_user_id`, length must be less than or equal to `40`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                local_user_id is not None and len(local_user_id) < 1):
            raise ValueError("Invalid value for `local_user_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._local_user_id = local_user_id

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
        if not isinstance(other, UpstreamUserIdentitySpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpstreamUserIdentitySpec):
            return True

        return self.to_dict() != other.to_dict()
