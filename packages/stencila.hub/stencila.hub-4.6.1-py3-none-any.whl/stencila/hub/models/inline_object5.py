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


class InlineObject5(object):
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
        'status_message': 'str',
        'summary_string': 'str',
        'runtime_formatted': 'str',
        'url': 'str',
        'position': 'int',
        'children': 'list[int]',
        'key': 'str',
        'description': 'str',
        'created': 'datetime',
        'updated': 'datetime',
        'began': 'datetime',
        'ended': 'datetime',
        'status': 'str',
        'is_active': 'bool',
        'method': 'str',
        'params': 'str',
        'result': 'str',
        'error': 'str',
        'log': 'str',
        'runtime': 'float',
        'worker': 'str',
        'retries': 'int',
        'callback_id': 'str',
        'callback_method': 'str',
        'project': 'int',
        'snapshot': 'str',
        'creator': 'int',
        'queue': 'int',
        'parent': 'int',
        'callback_type': 'int',
        'users': 'list[int]',
        'anon_users': 'list[str]'
    }

    attribute_map = {
        'id': 'id',
        'status_message': 'statusMessage',
        'summary_string': 'summaryString',
        'runtime_formatted': 'runtimeFormatted',
        'url': 'url',
        'position': 'position',
        'children': 'children',
        'key': 'key',
        'description': 'description',
        'created': 'created',
        'updated': 'updated',
        'began': 'began',
        'ended': 'ended',
        'status': 'status',
        'is_active': 'isActive',
        'method': 'method',
        'params': 'params',
        'result': 'result',
        'error': 'error',
        'log': 'log',
        'runtime': 'runtime',
        'worker': 'worker',
        'retries': 'retries',
        'callback_id': 'callbackId',
        'callback_method': 'callbackMethod',
        'project': 'project',
        'snapshot': 'snapshot',
        'creator': 'creator',
        'queue': 'queue',
        'parent': 'parent',
        'callback_type': 'callbackType',
        'users': 'users',
        'anon_users': 'anonUsers'
    }

    def __init__(self, id=None, status_message=None, summary_string=None, runtime_formatted=None, url=None, position=None, children=None, key=None, description=None, created=None, updated=None, began=None, ended=None, status=None, is_active=None, method=None, params=None, result=None, error=None, log=None, runtime=None, worker=None, retries=None, callback_id=None, callback_method=None, project=None, snapshot=None, creator=None, queue=None, parent=None, callback_type=None, users=None, anon_users=None, local_vars_configuration=None):  # noqa: E501
        """InlineObject5 - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._status_message = None
        self._summary_string = None
        self._runtime_formatted = None
        self._url = None
        self._position = None
        self._children = None
        self._key = None
        self._description = None
        self._created = None
        self._updated = None
        self._began = None
        self._ended = None
        self._status = None
        self._is_active = None
        self._method = None
        self._params = None
        self._result = None
        self._error = None
        self._log = None
        self._runtime = None
        self._worker = None
        self._retries = None
        self._callback_id = None
        self._callback_method = None
        self._project = None
        self._snapshot = None
        self._creator = None
        self._queue = None
        self._parent = None
        self._callback_type = None
        self._users = None
        self._anon_users = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if status_message is not None:
            self.status_message = status_message
        if summary_string is not None:
            self.summary_string = summary_string
        if runtime_formatted is not None:
            self.runtime_formatted = runtime_formatted
        if url is not None:
            self.url = url
        if position is not None:
            self.position = position
        if children is not None:
            self.children = children
        if key is not None:
            self.key = key
        self.description = description
        if created is not None:
            self.created = created
        if updated is not None:
            self.updated = updated
        self.began = began
        self.ended = ended
        self.status = status
        if is_active is not None:
            self.is_active = is_active
        if method is not None:
            self.method = method
        if params is not None:
            self.params = params
        self.result = result
        self.error = error
        self.log = log
        self.runtime = runtime
        self.worker = worker
        self.retries = retries
        self.callback_id = callback_id
        self.callback_method = callback_method
        self.project = project
        self.snapshot = snapshot
        if creator is not None:
            self.creator = creator
        if queue is not None:
            self.queue = queue
        self.parent = parent
        self.callback_type = callback_type
        if users is not None:
            self.users = users
        if anon_users is not None:
            self.anon_users = anon_users

    @property
    def id(self):
        """Gets the id of this InlineObject5.  # noqa: E501

        An autoincrementing integer to allow selecting jobs in the order they were created.  # noqa: E501

        :return: The id of this InlineObject5.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InlineObject5.

        An autoincrementing integer to allow selecting jobs in the order they were created.  # noqa: E501

        :param id: The id of this InlineObject5.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def status_message(self):
        """Gets the status_message of this InlineObject5.  # noqa: E501


        :return: The status_message of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """Sets the status_message of this InlineObject5.


        :param status_message: The status_message of this InlineObject5.  # noqa: E501
        :type status_message: str
        """
        if (self.local_vars_configuration.client_side_validation and
                status_message is not None and len(status_message) < 1):
            raise ValueError("Invalid value for `status_message`, length must be greater than or equal to `1`")  # noqa: E501

        self._status_message = status_message

    @property
    def summary_string(self):
        """Gets the summary_string of this InlineObject5.  # noqa: E501


        :return: The summary_string of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._summary_string

    @summary_string.setter
    def summary_string(self, summary_string):
        """Sets the summary_string of this InlineObject5.


        :param summary_string: The summary_string of this InlineObject5.  # noqa: E501
        :type summary_string: str
        """
        if (self.local_vars_configuration.client_side_validation and
                summary_string is not None and len(summary_string) < 1):
            raise ValueError("Invalid value for `summary_string`, length must be greater than or equal to `1`")  # noqa: E501

        self._summary_string = summary_string

    @property
    def runtime_formatted(self):
        """Gets the runtime_formatted of this InlineObject5.  # noqa: E501


        :return: The runtime_formatted of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._runtime_formatted

    @runtime_formatted.setter
    def runtime_formatted(self, runtime_formatted):
        """Sets the runtime_formatted of this InlineObject5.


        :param runtime_formatted: The runtime_formatted of this InlineObject5.  # noqa: E501
        :type runtime_formatted: str
        """
        if (self.local_vars_configuration.client_side_validation and
                runtime_formatted is not None and len(runtime_formatted) < 1):
            raise ValueError("Invalid value for `runtime_formatted`, length must be greater than or equal to `1`")  # noqa: E501

        self._runtime_formatted = runtime_formatted

    @property
    def url(self):
        """Gets the url of this InlineObject5.  # noqa: E501


        :return: The url of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this InlineObject5.


        :param url: The url of this InlineObject5.  # noqa: E501
        :type url: str
        """

        self._url = url

    @property
    def position(self):
        """Gets the position of this InlineObject5.  # noqa: E501


        :return: The position of this InlineObject5.  # noqa: E501
        :rtype: int
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the position of this InlineObject5.


        :param position: The position of this InlineObject5.  # noqa: E501
        :type position: int
        """

        self._position = position

    @property
    def children(self):
        """Gets the children of this InlineObject5.  # noqa: E501


        :return: The children of this InlineObject5.  # noqa: E501
        :rtype: list[int]
        """
        return self._children

    @children.setter
    def children(self, children):
        """Sets the children of this InlineObject5.


        :param children: The children of this InlineObject5.  # noqa: E501
        :type children: list[int]
        """

        self._children = children

    @property
    def key(self):
        """Gets the key of this InlineObject5.  # noqa: E501

        A unique, and very difficult to guess, key to access the job with.  # noqa: E501

        :return: The key of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this InlineObject5.

        A unique, and very difficult to guess, key to access the job with.  # noqa: E501

        :param key: The key of this InlineObject5.  # noqa: E501
        :type key: str
        """
        if (self.local_vars_configuration.client_side_validation and
                key is not None and len(key) > 64):
            raise ValueError("Invalid value for `key`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                key is not None and len(key) < 1):
            raise ValueError("Invalid value for `key`, length must be greater than or equal to `1`")  # noqa: E501

        self._key = key

    @property
    def description(self):
        """Gets the description of this InlineObject5.  # noqa: E501

        A short description of the job.  # noqa: E501

        :return: The description of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this InlineObject5.

        A short description of the job.  # noqa: E501

        :param description: The description of this InlineObject5.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def created(self):
        """Gets the created of this InlineObject5.  # noqa: E501

        The time the job was created.  # noqa: E501

        :return: The created of this InlineObject5.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this InlineObject5.

        The time the job was created.  # noqa: E501

        :param created: The created of this InlineObject5.  # noqa: E501
        :type created: datetime
        """

        self._created = created

    @property
    def updated(self):
        """Gets the updated of this InlineObject5.  # noqa: E501

        The time the job was last updated.  # noqa: E501

        :return: The updated of this InlineObject5.  # noqa: E501
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this InlineObject5.

        The time the job was last updated.  # noqa: E501

        :param updated: The updated of this InlineObject5.  # noqa: E501
        :type updated: datetime
        """

        self._updated = updated

    @property
    def began(self):
        """Gets the began of this InlineObject5.  # noqa: E501

        The time the job began.  # noqa: E501

        :return: The began of this InlineObject5.  # noqa: E501
        :rtype: datetime
        """
        return self._began

    @began.setter
    def began(self, began):
        """Sets the began of this InlineObject5.

        The time the job began.  # noqa: E501

        :param began: The began of this InlineObject5.  # noqa: E501
        :type began: datetime
        """

        self._began = began

    @property
    def ended(self):
        """Gets the ended of this InlineObject5.  # noqa: E501

        The time the job ended.  # noqa: E501

        :return: The ended of this InlineObject5.  # noqa: E501
        :rtype: datetime
        """
        return self._ended

    @ended.setter
    def ended(self, ended):
        """Sets the ended of this InlineObject5.

        The time the job ended.  # noqa: E501

        :param ended: The ended of this InlineObject5.  # noqa: E501
        :type ended: datetime
        """

        self._ended = ended

    @property
    def status(self):
        """Gets the status of this InlineObject5.  # noqa: E501

        The current status of the job.  # noqa: E501

        :return: The status of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InlineObject5.

        The current status of the job.  # noqa: E501

        :param status: The status of this InlineObject5.  # noqa: E501
        :type status: str
        """
        allowed_values = [None,"WAITING", "DISPATCHED", "PENDING", "RECEIVED", "STARTED", "RUNNING", "SUCCESS", "FAILURE", "CANCELLED", "REVOKED", "TERMINATED", "REJECTED", "RETRY"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and status not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def is_active(self):
        """Gets the is_active of this InlineObject5.  # noqa: E501

        Is the job active?  # noqa: E501

        :return: The is_active of this InlineObject5.  # noqa: E501
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """Sets the is_active of this InlineObject5.

        Is the job active?  # noqa: E501

        :param is_active: The is_active of this InlineObject5.  # noqa: E501
        :type is_active: bool
        """

        self._is_active = is_active

    @property
    def method(self):
        """Gets the method of this InlineObject5.  # noqa: E501

        The job method.  # noqa: E501

        :return: The method of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method):
        """Sets the method of this InlineObject5.

        The job method.  # noqa: E501

        :param method: The method of this InlineObject5.  # noqa: E501
        :type method: str
        """
        allowed_values = ["parallel", "series", "chain", "clean", "archive", "pull", "push", "decode", "encode", "convert", "pin", "compile", "build", "execute", "session", "sleep"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and method not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `method` ({0}), must be one of {1}"  # noqa: E501
                .format(method, allowed_values)
            )

        self._method = method

    @property
    def params(self):
        """Gets the params of this InlineObject5.  # noqa: E501

        The parameters of the job; a JSON object.  # noqa: E501

        :return: The params of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._params

    @params.setter
    def params(self, params):
        """Sets the params of this InlineObject5.

        The parameters of the job; a JSON object.  # noqa: E501

        :param params: The params of this InlineObject5.  # noqa: E501
        :type params: str
        """

        self._params = params

    @property
    def result(self):
        """Gets the result of this InlineObject5.  # noqa: E501

        The result of the job; a JSON value.  # noqa: E501

        :return: The result of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._result

    @result.setter
    def result(self, result):
        """Sets the result of this InlineObject5.

        The result of the job; a JSON value.  # noqa: E501

        :param result: The result of this InlineObject5.  # noqa: E501
        :type result: str
        """

        self._result = result

    @property
    def error(self):
        """Gets the error of this InlineObject5.  # noqa: E501

        Any error associated with the job; a JSON object with type, message etc.  # noqa: E501

        :return: The error of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this InlineObject5.

        Any error associated with the job; a JSON object with type, message etc.  # noqa: E501

        :param error: The error of this InlineObject5.  # noqa: E501
        :type error: str
        """

        self._error = error

    @property
    def log(self):
        """Gets the log of this InlineObject5.  # noqa: E501

        The job log; a JSON array of log objects, including any errors.  # noqa: E501

        :return: The log of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._log

    @log.setter
    def log(self, log):
        """Sets the log of this InlineObject5.

        The job log; a JSON array of log objects, including any errors.  # noqa: E501

        :param log: The log of this InlineObject5.  # noqa: E501
        :type log: str
        """

        self._log = log

    @property
    def runtime(self):
        """Gets the runtime of this InlineObject5.  # noqa: E501

        The running time of the job.  # noqa: E501

        :return: The runtime of this InlineObject5.  # noqa: E501
        :rtype: float
        """
        return self._runtime

    @runtime.setter
    def runtime(self, runtime):
        """Sets the runtime of this InlineObject5.

        The running time of the job.  # noqa: E501

        :param runtime: The runtime of this InlineObject5.  # noqa: E501
        :type runtime: float
        """

        self._runtime = runtime

    @property
    def worker(self):
        """Gets the worker of this InlineObject5.  # noqa: E501

        The identifier of the worker that ran the job.  # noqa: E501

        :return: The worker of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._worker

    @worker.setter
    def worker(self, worker):
        """Sets the worker of this InlineObject5.

        The identifier of the worker that ran the job.  # noqa: E501

        :param worker: The worker of this InlineObject5.  # noqa: E501
        :type worker: str
        """
        if (self.local_vars_configuration.client_side_validation and
                worker is not None and len(worker) > 64):
            raise ValueError("Invalid value for `worker`, length must be less than or equal to `64`")  # noqa: E501

        self._worker = worker

    @property
    def retries(self):
        """Gets the retries of this InlineObject5.  # noqa: E501

        The number of retries to fulfil the job.  # noqa: E501

        :return: The retries of this InlineObject5.  # noqa: E501
        :rtype: int
        """
        return self._retries

    @retries.setter
    def retries(self, retries):
        """Sets the retries of this InlineObject5.

        The number of retries to fulfil the job.  # noqa: E501

        :param retries: The retries of this InlineObject5.  # noqa: E501
        :type retries: int
        """

        self._retries = retries

    @property
    def callback_id(self):
        """Gets the callback_id of this InlineObject5.  # noqa: E501

        The id of the object to call back.  # noqa: E501

        :return: The callback_id of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._callback_id

    @callback_id.setter
    def callback_id(self, callback_id):
        """Sets the callback_id of this InlineObject5.

        The id of the object to call back.  # noqa: E501

        :param callback_id: The callback_id of this InlineObject5.  # noqa: E501
        :type callback_id: str
        """
        if (self.local_vars_configuration.client_side_validation and
                callback_id is not None and len(callback_id) > 256):
            raise ValueError("Invalid value for `callback_id`, length must be less than or equal to `256`")  # noqa: E501

        self._callback_id = callback_id

    @property
    def callback_method(self):
        """Gets the callback_method of this InlineObject5.  # noqa: E501

        The name of the method to call back.  # noqa: E501

        :return: The callback_method of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._callback_method

    @callback_method.setter
    def callback_method(self, callback_method):
        """Sets the callback_method of this InlineObject5.

        The name of the method to call back.  # noqa: E501

        :param callback_method: The callback_method of this InlineObject5.  # noqa: E501
        :type callback_method: str
        """
        if (self.local_vars_configuration.client_side_validation and
                callback_method is not None and len(callback_method) > 128):
            raise ValueError("Invalid value for `callback_method`, length must be less than or equal to `128`")  # noqa: E501

        self._callback_method = callback_method

    @property
    def project(self):
        """Gets the project of this InlineObject5.  # noqa: E501

        The project this job is associated with.  # noqa: E501

        :return: The project of this InlineObject5.  # noqa: E501
        :rtype: int
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this InlineObject5.

        The project this job is associated with.  # noqa: E501

        :param project: The project of this InlineObject5.  # noqa: E501
        :type project: int
        """

        self._project = project

    @property
    def snapshot(self):
        """Gets the snapshot of this InlineObject5.  # noqa: E501

        The snapshot that this job is associated with. Usually `session` jobs for the snapshot.  # noqa: E501

        :return: The snapshot of this InlineObject5.  # noqa: E501
        :rtype: str
        """
        return self._snapshot

    @snapshot.setter
    def snapshot(self, snapshot):
        """Sets the snapshot of this InlineObject5.

        The snapshot that this job is associated with. Usually `session` jobs for the snapshot.  # noqa: E501

        :param snapshot: The snapshot of this InlineObject5.  # noqa: E501
        :type snapshot: str
        """

        self._snapshot = snapshot

    @property
    def creator(self):
        """Gets the creator of this InlineObject5.  # noqa: E501

        The user who created the job.  # noqa: E501

        :return: The creator of this InlineObject5.  # noqa: E501
        :rtype: int
        """
        return self._creator

    @creator.setter
    def creator(self, creator):
        """Sets the creator of this InlineObject5.

        The user who created the job.  # noqa: E501

        :param creator: The creator of this InlineObject5.  # noqa: E501
        :type creator: int
        """

        self._creator = creator

    @property
    def queue(self):
        """Gets the queue of this InlineObject5.  # noqa: E501

        The queue that this job was routed to  # noqa: E501

        :return: The queue of this InlineObject5.  # noqa: E501
        :rtype: int
        """
        return self._queue

    @queue.setter
    def queue(self, queue):
        """Sets the queue of this InlineObject5.

        The queue that this job was routed to  # noqa: E501

        :param queue: The queue of this InlineObject5.  # noqa: E501
        :type queue: int
        """

        self._queue = queue

    @property
    def parent(self):
        """Gets the parent of this InlineObject5.  # noqa: E501

        The parent job  # noqa: E501

        :return: The parent of this InlineObject5.  # noqa: E501
        :rtype: int
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """Sets the parent of this InlineObject5.

        The parent job  # noqa: E501

        :param parent: The parent of this InlineObject5.  # noqa: E501
        :type parent: int
        """

        self._parent = parent

    @property
    def callback_type(self):
        """Gets the callback_type of this InlineObject5.  # noqa: E501

        The type of the object to call back.  # noqa: E501

        :return: The callback_type of this InlineObject5.  # noqa: E501
        :rtype: int
        """
        return self._callback_type

    @callback_type.setter
    def callback_type(self, callback_type):
        """Sets the callback_type of this InlineObject5.

        The type of the object to call back.  # noqa: E501

        :param callback_type: The callback_type of this InlineObject5.  # noqa: E501
        :type callback_type: int
        """

        self._callback_type = callback_type

    @property
    def users(self):
        """Gets the users of this InlineObject5.  # noqa: E501

        Users who have created or connected to the job; not necessarily currently connected.  # noqa: E501

        :return: The users of this InlineObject5.  # noqa: E501
        :rtype: list[int]
        """
        return self._users

    @users.setter
    def users(self, users):
        """Sets the users of this InlineObject5.

        Users who have created or connected to the job; not necessarily currently connected.  # noqa: E501

        :param users: The users of this InlineObject5.  # noqa: E501
        :type users: list[int]
        """

        self._users = users

    @property
    def anon_users(self):
        """Gets the anon_users of this InlineObject5.  # noqa: E501

        Anonymous users who have created or connected to the job.  # noqa: E501

        :return: The anon_users of this InlineObject5.  # noqa: E501
        :rtype: list[str]
        """
        return self._anon_users

    @anon_users.setter
    def anon_users(self, anon_users):
        """Sets the anon_users of this InlineObject5.

        Anonymous users who have created or connected to the job.  # noqa: E501

        :param anon_users: The anon_users of this InlineObject5.  # noqa: E501
        :type anon_users: list[str]
        """

        self._anon_users = anon_users

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
        if not isinstance(other, InlineObject5):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineObject5):
            return True

        return self.to_dict() != other.to_dict()
