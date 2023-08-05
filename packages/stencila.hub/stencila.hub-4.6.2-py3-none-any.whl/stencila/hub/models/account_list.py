# coding: utf-8

"""
    Stencila Hub API

    ## Authentication  Many endpoints in the Stencila Hub API require an authentication token. These tokens carry many privileges, so be sure to keep them secure. Do not place your tokens in publicly accessible areas such as client-side code. The API is only served over HTTPS to avoid exposing tokens and other data on the network.  To obtain a token, [`POST /api/tokens`](#operations-tokens-tokens_create) with either a `username` and `password` pair, or an [OpenID Connect](https://openid.net/connect/) token. Then use the token in the `Authorization` header of subsequent requests with the prefix `Token` e.g.      curl -H \"Authorization: Token 48866b1e38a2e9db0baada2140b2327937f4a3636dd5f2dfd8c212341c88d34\" https://hub.stenci.la/api/projects/  Alternatively, you can use `Basic` authentication with the token used as the username and no password. This can be more convenient when using command line tools such as [cURL](https://curl.haxx.se/) e.g.      curl -u 48866b1e38a2e9db0baada2140b2327937f4a3636dd5f2dfd8c212341c88d34: https://hub.stenci.la/api/projects/  Or, the less ubiquitous, but more accessible [httpie](https://httpie.org/):      http --auth 48866b1e38a2e9db0baada2140b2327937f4a3636dd5f2dfd8c212341c88d34: https://hub.stenci.la/api/projects/  In both examples above, the trailing colon is not required but avoids being asked for a password.  ## Versioning  The Stencila Hub is released using semantic versioning. The current version is available from the [`GET /api/status`](/api/status) endpoint. Please see the [Github release page](https://github.com/stencila/hub/releases) and the [changelog](https://github.com/stencila/hub/blob/master/CHANGELOG.md) for details on each release. We currently do not provide versioning of the API but plan to do so soon (probably by using a `Accept: application/vnd.stencila.hub+json;version=1.0` request header). If you are using, or interested in using, the API please contact us and we may be able to expedite this.   # noqa: E501

    The version of the OpenAPI document: v1
    Contact: hello@stenci.la
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from stencila.hub.configuration import Configuration


class AccountList(object):
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
        'id': 'int',
        'name': 'str',
        'user': 'int',
        'creator': 'int',
        'created': 'datetime',
        'display_name': 'str',
        'location': 'str',
        'image': 'str',
        'website': 'str',
        'email': 'str',
        'theme': 'str',
        'extra_head': 'str',
        'extra_top': 'str',
        'extra_bottom': 'str',
        'hosts': 'str',
        'role': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'user': 'user',
        'creator': 'creator',
        'created': 'created',
        'display_name': 'displayName',
        'location': 'location',
        'image': 'image',
        'website': 'website',
        'email': 'email',
        'theme': 'theme',
        'extra_head': 'extraHead',
        'extra_top': 'extraTop',
        'extra_bottom': 'extraBottom',
        'hosts': 'hosts',
        'role': 'role'
    }

    def __init__(self, id=None, name=None, user=None, creator=None, created=None, display_name=None, location=None, image=None, website=None, email=None, theme=None, extra_head=None, extra_top=None, extra_bottom=None, hosts=None, role=None, local_vars_configuration=None):  # noqa: E501
        """AccountList - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._user = None
        self._creator = None
        self._created = None
        self._display_name = None
        self._location = None
        self._image = None
        self._website = None
        self._email = None
        self._theme = None
        self._extra_head = None
        self._extra_top = None
        self._extra_bottom = None
        self._hosts = None
        self._role = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.name = name
        self.user = user
        self.creator = creator
        if created is not None:
            self.created = created
        self.display_name = display_name
        self.location = location
        self.image = image
        self.website = website
        self.email = email
        if theme is not None:
            self.theme = theme
        self.extra_head = extra_head
        self.extra_top = extra_top
        self.extra_bottom = extra_bottom
        self.hosts = hosts
        if role is not None:
            self.role = role

    @property
    def id(self):
        """Gets the id of this AccountList.  # noqa: E501


        :return: The id of this AccountList.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AccountList.


        :param id: The id of this AccountList.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this AccountList.  # noqa: E501

        Name of the account. Lowercase and no spaces or leading numbers. Will be used in URLS e.g. https://hub.stenci.la/awesome-org  # noqa: E501

        :return: The name of this AccountList.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AccountList.

        Name of the account. Lowercase and no spaces or leading numbers. Will be used in URLS e.g. https://hub.stenci.la/awesome-org  # noqa: E501

        :param name: The name of this AccountList.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def user(self):
        """Gets the user of this AccountList.  # noqa: E501

        The user for this account. Only applies to personal accounts.  # noqa: E501

        :return: The user of this AccountList.  # noqa: E501
        :rtype: int
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this AccountList.

        The user for this account. Only applies to personal accounts.  # noqa: E501

        :param user: The user of this AccountList.  # noqa: E501
        :type user: int
        """

        self._user = user

    @property
    def creator(self):
        """Gets the creator of this AccountList.  # noqa: E501

        The user who created the account.  # noqa: E501

        :return: The creator of this AccountList.  # noqa: E501
        :rtype: int
        """
        return self._creator

    @creator.setter
    def creator(self, creator):
        """Sets the creator of this AccountList.

        The user who created the account.  # noqa: E501

        :param creator: The creator of this AccountList.  # noqa: E501
        :type creator: int
        """

        self._creator = creator

    @property
    def created(self):
        """Gets the created of this AccountList.  # noqa: E501

        The time the account was created.  # noqa: E501

        :return: The created of this AccountList.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this AccountList.

        The time the account was created.  # noqa: E501

        :param created: The created of this AccountList.  # noqa: E501
        :type created: datetime
        """

        self._created = created

    @property
    def display_name(self):
        """Gets the display_name of this AccountList.  # noqa: E501

        Name to display in account profile.  # noqa: E501

        :return: The display_name of this AccountList.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this AccountList.

        Name to display in account profile.  # noqa: E501

        :param display_name: The display_name of this AccountList.  # noqa: E501
        :type display_name: str
        """
        if (self.local_vars_configuration.client_side_validation and
                display_name is not None and len(display_name) > 256):
            raise ValueError("Invalid value for `display_name`, length must be less than or equal to `256`")  # noqa: E501

        self._display_name = display_name

    @property
    def location(self):
        """Gets the location of this AccountList.  # noqa: E501

        Location to display in account profile.  # noqa: E501

        :return: The location of this AccountList.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this AccountList.

        Location to display in account profile.  # noqa: E501

        :param location: The location of this AccountList.  # noqa: E501
        :type location: str
        """
        if (self.local_vars_configuration.client_side_validation and
                location is not None and len(location) > 256):
            raise ValueError("Invalid value for `location`, length must be less than or equal to `256`")  # noqa: E501

        self._location = location

    @property
    def image(self):
        """Gets the image of this AccountList.  # noqa: E501

        Image for the account.  # noqa: E501

        :return: The image of this AccountList.  # noqa: E501
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this AccountList.

        Image for the account.  # noqa: E501

        :param image: The image of this AccountList.  # noqa: E501
        :type image: str
        """

        self._image = image

    @property
    def website(self):
        """Gets the website of this AccountList.  # noqa: E501

        URL to display in account profile.  # noqa: E501

        :return: The website of this AccountList.  # noqa: E501
        :rtype: str
        """
        return self._website

    @website.setter
    def website(self, website):
        """Sets the website of this AccountList.

        URL to display in account profile.  # noqa: E501

        :param website: The website of this AccountList.  # noqa: E501
        :type website: str
        """
        if (self.local_vars_configuration.client_side_validation and
                website is not None and len(website) > 200):
            raise ValueError("Invalid value for `website`, length must be less than or equal to `200`")  # noqa: E501

        self._website = website

    @property
    def email(self):
        """Gets the email of this AccountList.  # noqa: E501

        An email to display in account profile. Will not be used by Stencila to contact you.  # noqa: E501

        :return: The email of this AccountList.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this AccountList.

        An email to display in account profile. Will not be used by Stencila to contact you.  # noqa: E501

        :param email: The email of this AccountList.  # noqa: E501
        :type email: str
        """
        if (self.local_vars_configuration.client_side_validation and
                email is not None and len(email) > 254):
            raise ValueError("Invalid value for `email`, length must be less than or equal to `254`")  # noqa: E501

        self._email = email

    @property
    def theme(self):
        """Gets the theme of this AccountList.  # noqa: E501

        The default theme for the account.  # noqa: E501

        :return: The theme of this AccountList.  # noqa: E501
        :rtype: str
        """
        return self._theme

    @theme.setter
    def theme(self, theme):
        """Sets the theme of this AccountList.

        The default theme for the account.  # noqa: E501

        :param theme: The theme of this AccountList.  # noqa: E501
        :type theme: str
        """
        allowed_values = ["bootstrap", "elife", "f1000", "galleria", "giga", "latex", "nature", "plos", "rpng", "skeleton", "stencila", "tufte", "wilmore"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and theme not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `theme` ({0}), must be one of {1}"  # noqa: E501
                .format(theme, allowed_values)
            )

        self._theme = theme

    @property
    def extra_head(self):
        """Gets the extra_head of this AccountList.  # noqa: E501

        Content to inject into the <head> element of HTML served for this account.  # noqa: E501

        :return: The extra_head of this AccountList.  # noqa: E501
        :rtype: str
        """
        return self._extra_head

    @extra_head.setter
    def extra_head(self, extra_head):
        """Sets the extra_head of this AccountList.

        Content to inject into the <head> element of HTML served for this account.  # noqa: E501

        :param extra_head: The extra_head of this AccountList.  # noqa: E501
        :type extra_head: str
        """

        self._extra_head = extra_head

    @property
    def extra_top(self):
        """Gets the extra_top of this AccountList.  # noqa: E501

        Content to inject at the top of the <body> element of HTML served for this account.  # noqa: E501

        :return: The extra_top of this AccountList.  # noqa: E501
        :rtype: str
        """
        return self._extra_top

    @extra_top.setter
    def extra_top(self, extra_top):
        """Sets the extra_top of this AccountList.

        Content to inject at the top of the <body> element of HTML served for this account.  # noqa: E501

        :param extra_top: The extra_top of this AccountList.  # noqa: E501
        :type extra_top: str
        """

        self._extra_top = extra_top

    @property
    def extra_bottom(self):
        """Gets the extra_bottom of this AccountList.  # noqa: E501

        Content to inject at the bottom of the <body> element of HTML served for this account.  # noqa: E501

        :return: The extra_bottom of this AccountList.  # noqa: E501
        :rtype: str
        """
        return self._extra_bottom

    @extra_bottom.setter
    def extra_bottom(self, extra_bottom):
        """Sets the extra_bottom of this AccountList.

        Content to inject at the bottom of the <body> element of HTML served for this account.  # noqa: E501

        :param extra_bottom: The extra_bottom of this AccountList.  # noqa: E501
        :type extra_bottom: str
        """

        self._extra_bottom = extra_bottom

    @property
    def hosts(self):
        """Gets the hosts of this AccountList.  # noqa: E501

        A space separated list of valid hosts for the account. Used for setting Content Security Policy headers when serving content for this account.  # noqa: E501

        :return: The hosts of this AccountList.  # noqa: E501
        :rtype: str
        """
        return self._hosts

    @hosts.setter
    def hosts(self, hosts):
        """Sets the hosts of this AccountList.

        A space separated list of valid hosts for the account. Used for setting Content Security Policy headers when serving content for this account.  # noqa: E501

        :param hosts: The hosts of this AccountList.  # noqa: E501
        :type hosts: str
        """

        self._hosts = hosts

    @property
    def role(self):
        """Gets the role of this AccountList.  # noqa: E501

        Role of the current user on the account (if any).  # noqa: E501

        :return: The role of this AccountList.  # noqa: E501
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this AccountList.

        Role of the current user on the account (if any).  # noqa: E501

        :param role: The role of this AccountList.  # noqa: E501
        :type role: str
        """
        if (self.local_vars_configuration.client_side_validation and
                role is not None and len(role) < 1):
            raise ValueError("Invalid value for `role`, length must be greater than or equal to `1`")  # noqa: E501

        self._role = role

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
        if not isinstance(other, AccountList):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AccountList):
            return True

        return self.to_dict() != other.to_dict()
