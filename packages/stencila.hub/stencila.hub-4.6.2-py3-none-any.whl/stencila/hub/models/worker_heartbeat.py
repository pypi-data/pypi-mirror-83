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


class WorkerHeartbeat(object):
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
        'time': 'datetime',
        'clock': 'int',
        'active': 'int',
        'processed': 'int',
        'load': 'str'
    }

    attribute_map = {
        'time': 'time',
        'clock': 'clock',
        'active': 'active',
        'processed': 'processed',
        'load': 'load'
    }

    def __init__(self, time=None, clock=None, active=None, processed=None, load=None, local_vars_configuration=None):  # noqa: E501
        """WorkerHeartbeat - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._time = None
        self._clock = None
        self._active = None
        self._processed = None
        self._load = None
        self.discriminator = None

        self.time = time
        self.clock = clock
        self.active = active
        self.processed = processed
        self.load = load

    @property
    def time(self):
        """Gets the time of this WorkerHeartbeat.  # noqa: E501

        The time of the heartbeat.  # noqa: E501

        :return: The time of this WorkerHeartbeat.  # noqa: E501
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this WorkerHeartbeat.

        The time of the heartbeat.  # noqa: E501

        :param time: The time of this WorkerHeartbeat.  # noqa: E501
        :type time: datetime
        """
        if self.local_vars_configuration.client_side_validation and time is None:  # noqa: E501
            raise ValueError("Invalid value for `time`, must not be `None`")  # noqa: E501

        self._time = time

    @property
    def clock(self):
        """Gets the clock of this WorkerHeartbeat.  # noqa: E501

        The tick number of the worker's monotonic clock  # noqa: E501

        :return: The clock of this WorkerHeartbeat.  # noqa: E501
        :rtype: int
        """
        return self._clock

    @clock.setter
    def clock(self, clock):
        """Sets the clock of this WorkerHeartbeat.

        The tick number of the worker's monotonic clock  # noqa: E501

        :param clock: The clock of this WorkerHeartbeat.  # noqa: E501
        :type clock: int
        """
        if self.local_vars_configuration.client_side_validation and clock is None:  # noqa: E501
            raise ValueError("Invalid value for `clock`, must not be `None`")  # noqa: E501

        self._clock = clock

    @property
    def active(self):
        """Gets the active of this WorkerHeartbeat.  # noqa: E501

        The number of active jobs on the worker.  # noqa: E501

        :return: The active of this WorkerHeartbeat.  # noqa: E501
        :rtype: int
        """
        return self._active

    @active.setter
    def active(self, active):
        """Sets the active of this WorkerHeartbeat.

        The number of active jobs on the worker.  # noqa: E501

        :param active: The active of this WorkerHeartbeat.  # noqa: E501
        :type active: int
        """
        if self.local_vars_configuration.client_side_validation and active is None:  # noqa: E501
            raise ValueError("Invalid value for `active`, must not be `None`")  # noqa: E501

        self._active = active

    @property
    def processed(self):
        """Gets the processed of this WorkerHeartbeat.  # noqa: E501

        The number of jobs that have been processed by the worker.  # noqa: E501

        :return: The processed of this WorkerHeartbeat.  # noqa: E501
        :rtype: int
        """
        return self._processed

    @processed.setter
    def processed(self, processed):
        """Sets the processed of this WorkerHeartbeat.

        The number of jobs that have been processed by the worker.  # noqa: E501

        :param processed: The processed of this WorkerHeartbeat.  # noqa: E501
        :type processed: int
        """
        if self.local_vars_configuration.client_side_validation and processed is None:  # noqa: E501
            raise ValueError("Invalid value for `processed`, must not be `None`")  # noqa: E501

        self._processed = processed

    @property
    def load(self):
        """Gets the load of this WorkerHeartbeat.  # noqa: E501

        An array of the system load over the last 1, 5 and 15 minutes. From os.getloadavg().  # noqa: E501

        :return: The load of this WorkerHeartbeat.  # noqa: E501
        :rtype: str
        """
        return self._load

    @load.setter
    def load(self, load):
        """Sets the load of this WorkerHeartbeat.

        An array of the system load over the last 1, 5 and 15 minutes. From os.getloadavg().  # noqa: E501

        :param load: The load of this WorkerHeartbeat.  # noqa: E501
        :type load: str
        """
        if self.local_vars_configuration.client_side_validation and load is None:  # noqa: E501
            raise ValueError("Invalid value for `load`, must not be `None`")  # noqa: E501

        self._load = load

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
        if not isinstance(other, WorkerHeartbeat):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, WorkerHeartbeat):
            return True

        return self.to_dict() != other.to_dict()
