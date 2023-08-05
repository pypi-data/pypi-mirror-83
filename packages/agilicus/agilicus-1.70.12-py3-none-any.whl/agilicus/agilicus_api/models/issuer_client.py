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


class IssuerClient(object):
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
        'id': 'str',
        'issuer_id': 'str',
        'name': 'str',
        'secret': 'str',
        'application': 'str',
        'org_id': 'str',
        'restricted_organisations': 'list[str]',
        'saml_metadata_file': 'str',
        'organisation_scope': 'str',
        'redirects': 'list[str]',
        'mfa_challenge': 'str',
        'attributes': 'list[AuthenticationAttribute]'
    }

    attribute_map = {
        'id': 'id',
        'issuer_id': 'issuer_id',
        'name': 'name',
        'secret': 'secret',
        'application': 'application',
        'org_id': 'org_id',
        'restricted_organisations': 'restricted_organisations',
        'saml_metadata_file': 'saml_metadata_file',
        'organisation_scope': 'organisation_scope',
        'redirects': 'redirects',
        'mfa_challenge': 'mfa_challenge',
        'attributes': 'attributes'
    }

    def __init__(self, id=None, issuer_id=None, name=None, secret=None, application=None, org_id=None, restricted_organisations=None, saml_metadata_file=None, organisation_scope='here_only', redirects=None, mfa_challenge='user_preference', attributes=None, local_vars_configuration=None):  # noqa: E501
        """IssuerClient - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._issuer_id = None
        self._name = None
        self._secret = None
        self._application = None
        self._org_id = None
        self._restricted_organisations = None
        self._saml_metadata_file = None
        self._organisation_scope = None
        self._redirects = None
        self._mfa_challenge = None
        self._attributes = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if issuer_id is not None:
            self.issuer_id = issuer_id
        self.name = name
        if secret is not None:
            self.secret = secret
        if application is not None:
            self.application = application
        if org_id is not None:
            self.org_id = org_id
        if restricted_organisations is not None:
            self.restricted_organisations = restricted_organisations
        if saml_metadata_file is not None:
            self.saml_metadata_file = saml_metadata_file
        if organisation_scope is not None:
            self.organisation_scope = organisation_scope
        if redirects is not None:
            self.redirects = redirects
        if mfa_challenge is not None:
            self.mfa_challenge = mfa_challenge
        if attributes is not None:
            self.attributes = attributes

    @property
    def id(self):
        """Gets the id of this IssuerClient.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The id of this IssuerClient.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this IssuerClient.

        Unique identifier  # noqa: E501

        :param id: The id of this IssuerClient.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def issuer_id(self):
        """Gets the issuer_id of this IssuerClient.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The issuer_id of this IssuerClient.  # noqa: E501
        :rtype: str
        """
        return self._issuer_id

    @issuer_id.setter
    def issuer_id(self, issuer_id):
        """Sets the issuer_id of this IssuerClient.

        Unique identifier  # noqa: E501

        :param issuer_id: The issuer_id of this IssuerClient.  # noqa: E501
        :type: str
        """

        self._issuer_id = issuer_id

    @property
    def name(self):
        """Gets the name of this IssuerClient.  # noqa: E501

        issuer client id  # noqa: E501

        :return: The name of this IssuerClient.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this IssuerClient.

        issuer client id  # noqa: E501

        :param name: The name of this IssuerClient.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 100):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def secret(self):
        """Gets the secret of this IssuerClient.  # noqa: E501

        issuer client secret  # noqa: E501

        :return: The secret of this IssuerClient.  # noqa: E501
        :rtype: str
        """
        return self._secret

    @secret.setter
    def secret(self, secret):
        """Sets the secret of this IssuerClient.

        issuer client secret  # noqa: E501

        :param secret: The secret of this IssuerClient.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                secret is not None and len(secret) > 255):
            raise ValueError("Invalid value for `secret`, length must be less than or equal to `255`")  # noqa: E501

        self._secret = secret

    @property
    def application(self):
        """Gets the application of this IssuerClient.  # noqa: E501

        application associated with client  # noqa: E501

        :return: The application of this IssuerClient.  # noqa: E501
        :rtype: str
        """
        return self._application

    @application.setter
    def application(self, application):
        """Sets the application of this IssuerClient.

        application associated with client  # noqa: E501

        :param application: The application of this IssuerClient.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                application is not None and len(application) > 100):
            raise ValueError("Invalid value for `application`, length must be less than or equal to `100`")  # noqa: E501

        self._application = application

    @property
    def org_id(self):
        """Gets the org_id of this IssuerClient.  # noqa: E501

        org_id associated with client  # noqa: E501

        :return: The org_id of this IssuerClient.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Sets the org_id of this IssuerClient.

        org_id associated with client  # noqa: E501

        :param org_id: The org_id of this IssuerClient.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                org_id is not None and len(org_id) > 40):
            raise ValueError("Invalid value for `org_id`, length must be less than or equal to `40`")  # noqa: E501

        self._org_id = org_id

    @property
    def restricted_organisations(self):
        """Gets the restricted_organisations of this IssuerClient.  # noqa: E501

        List of organisation IDs which are allowed to authenticate using this client. If a user is not a member of one of these organisations, their authentication attempt will be denied. Note that this list intersects with `organisation_scope`. For example, if `organisation_scope` is `here-and-down` and this list contains two organisations below the current organisation, only those two will be allowed, despite there potentially being more sub organisations. If the list is empty, no restrictions are applied by this field. Note that other restrictions may be applied, such as by `organisation_scope`.   # noqa: E501

        :return: The restricted_organisations of this IssuerClient.  # noqa: E501
        :rtype: list[str]
        """
        return self._restricted_organisations

    @restricted_organisations.setter
    def restricted_organisations(self, restricted_organisations):
        """Sets the restricted_organisations of this IssuerClient.

        List of organisation IDs which are allowed to authenticate using this client. If a user is not a member of one of these organisations, their authentication attempt will be denied. Note that this list intersects with `organisation_scope`. For example, if `organisation_scope` is `here-and-down` and this list contains two organisations below the current organisation, only those two will be allowed, despite there potentially being more sub organisations. If the list is empty, no restrictions are applied by this field. Note that other restrictions may be applied, such as by `organisation_scope`.   # noqa: E501

        :param restricted_organisations: The restricted_organisations of this IssuerClient.  # noqa: E501
        :type: list[str]
        """

        self._restricted_organisations = restricted_organisations

    @property
    def saml_metadata_file(self):
        """Gets the saml_metadata_file of this IssuerClient.  # noqa: E501

        The Service Provider's metadata file required for the SAML protocol.   # noqa: E501

        :return: The saml_metadata_file of this IssuerClient.  # noqa: E501
        :rtype: str
        """
        return self._saml_metadata_file

    @saml_metadata_file.setter
    def saml_metadata_file(self, saml_metadata_file):
        """Sets the saml_metadata_file of this IssuerClient.

        The Service Provider's metadata file required for the SAML protocol.   # noqa: E501

        :param saml_metadata_file: The saml_metadata_file of this IssuerClient.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                saml_metadata_file is not None and len(saml_metadata_file) > 1048576):
            raise ValueError("Invalid value for `saml_metadata_file`, length must be less than or equal to `1048576`")  # noqa: E501

        self._saml_metadata_file = saml_metadata_file

    @property
    def organisation_scope(self):
        """Gets the organisation_scope of this IssuerClient.  # noqa: E501

        How to limit which organisations are allowed to authenticate using this client. Note that this interacts with `restricted_organisations`: that list, if not empty, further limits the allowed organisations. * `any` indicates that there are no restrictions. All organisations served by   the issuer will be allowed to log in using this client. * `here-only` indicates that   only the organisation referenced by `org_id` may be used. * `here-and-down` indicates that the organisation referenced by `org_id`   and its children may be used.   # noqa: E501

        :return: The organisation_scope of this IssuerClient.  # noqa: E501
        :rtype: str
        """
        return self._organisation_scope

    @organisation_scope.setter
    def organisation_scope(self, organisation_scope):
        """Sets the organisation_scope of this IssuerClient.

        How to limit which organisations are allowed to authenticate using this client. Note that this interacts with `restricted_organisations`: that list, if not empty, further limits the allowed organisations. * `any` indicates that there are no restrictions. All organisations served by   the issuer will be allowed to log in using this client. * `here-only` indicates that   only the organisation referenced by `org_id` may be used. * `here-and-down` indicates that the organisation referenced by `org_id`   and its children may be used.   # noqa: E501

        :param organisation_scope: The organisation_scope of this IssuerClient.  # noqa: E501
        :type: str
        """
        allowed_values = ["any", "here_and_down", "here_only"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and organisation_scope not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `organisation_scope` ({0}), must be one of {1}"  # noqa: E501
                .format(organisation_scope, allowed_values)
            )

        self._organisation_scope = organisation_scope

    @property
    def redirects(self):
        """Gets the redirects of this IssuerClient.  # noqa: E501

        List of redirect uris  # noqa: E501

        :return: The redirects of this IssuerClient.  # noqa: E501
        :rtype: list[str]
        """
        return self._redirects

    @redirects.setter
    def redirects(self, redirects):
        """Sets the redirects of this IssuerClient.

        List of redirect uris  # noqa: E501

        :param redirects: The redirects of this IssuerClient.  # noqa: E501
        :type: list[str]
        """

        self._redirects = redirects

    @property
    def mfa_challenge(self):
        """Gets the mfa_challenge of this IssuerClient.  # noqa: E501

        When to present an mfa challenge to a user upon login. If the system determines that an MFA challenge is required, and the user does not yet have a authenticatin mechanism valid for this login session, the user will be presented with the option to enrol a new mechanism. * `always` means that the user will always be required to validate against a second factor. * `user_preference` means that the whether the user is required to validate depends on the user's preferences.   A user could choose to always require MFA for their logins, or they could decide not to. Note that in this case,   other policy could override the preference to force the user to authenticate with MFA even if the user indicated   that they prefer not to. * `trust_upstream` means to always perform MFA, but that the upstream IDP will be trusted to have performed MFA if    the upstream indicates that it has done so. Otherwise, MFA will be performed by the system after the upstream    returns the to Issuer.   # noqa: E501

        :return: The mfa_challenge of this IssuerClient.  # noqa: E501
        :rtype: str
        """
        return self._mfa_challenge

    @mfa_challenge.setter
    def mfa_challenge(self, mfa_challenge):
        """Sets the mfa_challenge of this IssuerClient.

        When to present an mfa challenge to a user upon login. If the system determines that an MFA challenge is required, and the user does not yet have a authenticatin mechanism valid for this login session, the user will be presented with the option to enrol a new mechanism. * `always` means that the user will always be required to validate against a second factor. * `user_preference` means that the whether the user is required to validate depends on the user's preferences.   A user could choose to always require MFA for their logins, or they could decide not to. Note that in this case,   other policy could override the preference to force the user to authenticate with MFA even if the user indicated   that they prefer not to. * `trust_upstream` means to always perform MFA, but that the upstream IDP will be trusted to have performed MFA if    the upstream indicates that it has done so. Otherwise, MFA will be performed by the system after the upstream    returns the to Issuer.   # noqa: E501

        :param mfa_challenge: The mfa_challenge of this IssuerClient.  # noqa: E501
        :type: str
        """
        allowed_values = ["always", "user_preference", "trust_upstream"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and mfa_challenge not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `mfa_challenge` ({0}), must be one of {1}"  # noqa: E501
                .format(mfa_challenge, allowed_values)
            )

        self._mfa_challenge = mfa_challenge

    @property
    def attributes(self):
        """Gets the attributes of this IssuerClient.  # noqa: E501

        A list of attributes to derive from information about the user. The user's information returned to the relying party making a request using this client will be extended with these attributes. Only one attribute for a given `attribute_name` can exist per-client at a time. Add an attribute to this list when the default attributes do not provide sufficient information for the client application, or for when the client application expects the attributes to be named differently.   # noqa: E501

        :return: The attributes of this IssuerClient.  # noqa: E501
        :rtype: list[AuthenticationAttribute]
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """Sets the attributes of this IssuerClient.

        A list of attributes to derive from information about the user. The user's information returned to the relying party making a request using this client will be extended with these attributes. Only one attribute for a given `attribute_name` can exist per-client at a time. Add an attribute to this list when the default attributes do not provide sufficient information for the client application, or for when the client application expects the attributes to be named differently.   # noqa: E501

        :param attributes: The attributes of this IssuerClient.  # noqa: E501
        :type: list[AuthenticationAttribute]
        """

        self._attributes = attributes

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
        if not isinstance(other, IssuerClient):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, IssuerClient):
            return True

        return self.to_dict() != other.to_dict()
