# coding: utf-8

"""
    Cloudsmith API

    The API to the Cloudsmith Service

    OpenAPI spec version: v1
    Contact: support@cloudsmith.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class RepositoryTokenRefresh(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'clients': 'int',
        'created_at': 'str',
        'created_by': 'str',
        'created_by_url': 'str',
        'default': 'bool',
        'disable_url': 'str',
        'downloads': 'int',
        'enable_url': 'str',
        'has_limits': 'bool',
        'identifier': 'int',
        'is_active': 'bool',
        'is_limited': 'bool',
        'limit_bandwidth': 'int',
        'limit_bandwidth_unit': 'str',
        'limit_date_range_from': 'str',
        'limit_date_range_to': 'str',
        'limit_num_clients': 'int',
        'limit_num_downloads': 'int',
        'limit_package_query': 'str',
        'limit_path_query': 'str',
        'metadata': 'object',
        'name': 'str',
        'refresh_url': 'str',
        'reset_url': 'str',
        'scheduled_reset_at': 'str',
        'scheduled_reset_period': 'str',
        'self_url': 'str',
        'slug_perm': 'str',
        'token': 'str',
        'updated_at': 'str',
        'updated_by': 'str',
        'updated_by_url': 'str',
        'usage': 'str',
        'user': 'str',
        'user_url': 'str'
    }

    attribute_map = {
        'clients': 'clients',
        'created_at': 'created_at',
        'created_by': 'created_by',
        'created_by_url': 'created_by_url',
        'default': 'default',
        'disable_url': 'disable_url',
        'downloads': 'downloads',
        'enable_url': 'enable_url',
        'has_limits': 'has_limits',
        'identifier': 'identifier',
        'is_active': 'is_active',
        'is_limited': 'is_limited',
        'limit_bandwidth': 'limit_bandwidth',
        'limit_bandwidth_unit': 'limit_bandwidth_unit',
        'limit_date_range_from': 'limit_date_range_from',
        'limit_date_range_to': 'limit_date_range_to',
        'limit_num_clients': 'limit_num_clients',
        'limit_num_downloads': 'limit_num_downloads',
        'limit_package_query': 'limit_package_query',
        'limit_path_query': 'limit_path_query',
        'metadata': 'metadata',
        'name': 'name',
        'refresh_url': 'refresh_url',
        'reset_url': 'reset_url',
        'scheduled_reset_at': 'scheduled_reset_at',
        'scheduled_reset_period': 'scheduled_reset_period',
        'self_url': 'self_url',
        'slug_perm': 'slug_perm',
        'token': 'token',
        'updated_at': 'updated_at',
        'updated_by': 'updated_by',
        'updated_by_url': 'updated_by_url',
        'usage': 'usage',
        'user': 'user',
        'user_url': 'user_url'
    }

    def __init__(self, clients=None, created_at=None, created_by=None, created_by_url=None, default=None, disable_url=None, downloads=None, enable_url=None, has_limits=None, identifier=None, is_active=None, is_limited=None, limit_bandwidth=None, limit_bandwidth_unit=None, limit_date_range_from=None, limit_date_range_to=None, limit_num_clients=None, limit_num_downloads=None, limit_package_query=None, limit_path_query=None, metadata=None, name=None, refresh_url=None, reset_url=None, scheduled_reset_at=None, scheduled_reset_period=None, self_url=None, slug_perm=None, token=None, updated_at=None, updated_by=None, updated_by_url=None, usage=None, user=None, user_url=None):
        """
        RepositoryTokenRefresh - a model defined in Swagger
        """

        self._clients = None
        self._created_at = None
        self._created_by = None
        self._created_by_url = None
        self._default = None
        self._disable_url = None
        self._downloads = None
        self._enable_url = None
        self._has_limits = None
        self._identifier = None
        self._is_active = None
        self._is_limited = None
        self._limit_bandwidth = None
        self._limit_bandwidth_unit = None
        self._limit_date_range_from = None
        self._limit_date_range_to = None
        self._limit_num_clients = None
        self._limit_num_downloads = None
        self._limit_package_query = None
        self._limit_path_query = None
        self._metadata = None
        self._name = None
        self._refresh_url = None
        self._reset_url = None
        self._scheduled_reset_at = None
        self._scheduled_reset_period = None
        self._self_url = None
        self._slug_perm = None
        self._token = None
        self._updated_at = None
        self._updated_by = None
        self._updated_by_url = None
        self._usage = None
        self._user = None
        self._user_url = None

        if clients is not None:
          self.clients = clients
        if created_at is not None:
          self.created_at = created_at
        if created_by is not None:
          self.created_by = created_by
        if created_by_url is not None:
          self.created_by_url = created_by_url
        if default is not None:
          self.default = default
        if disable_url is not None:
          self.disable_url = disable_url
        if downloads is not None:
          self.downloads = downloads
        if enable_url is not None:
          self.enable_url = enable_url
        if has_limits is not None:
          self.has_limits = has_limits
        if identifier is not None:
          self.identifier = identifier
        if is_active is not None:
          self.is_active = is_active
        if is_limited is not None:
          self.is_limited = is_limited
        if limit_bandwidth is not None:
          self.limit_bandwidth = limit_bandwidth
        if limit_bandwidth_unit is not None:
          self.limit_bandwidth_unit = limit_bandwidth_unit
        if limit_date_range_from is not None:
          self.limit_date_range_from = limit_date_range_from
        if limit_date_range_to is not None:
          self.limit_date_range_to = limit_date_range_to
        if limit_num_clients is not None:
          self.limit_num_clients = limit_num_clients
        if limit_num_downloads is not None:
          self.limit_num_downloads = limit_num_downloads
        if limit_package_query is not None:
          self.limit_package_query = limit_package_query
        if limit_path_query is not None:
          self.limit_path_query = limit_path_query
        if metadata is not None:
          self.metadata = metadata
        if name is not None:
          self.name = name
        if refresh_url is not None:
          self.refresh_url = refresh_url
        if reset_url is not None:
          self.reset_url = reset_url
        if scheduled_reset_at is not None:
          self.scheduled_reset_at = scheduled_reset_at
        if scheduled_reset_period is not None:
          self.scheduled_reset_period = scheduled_reset_period
        if self_url is not None:
          self.self_url = self_url
        if slug_perm is not None:
          self.slug_perm = slug_perm
        if token is not None:
          self.token = token
        if updated_at is not None:
          self.updated_at = updated_at
        if updated_by is not None:
          self.updated_by = updated_by
        if updated_by_url is not None:
          self.updated_by_url = updated_by_url
        if usage is not None:
          self.usage = usage
        if user is not None:
          self.user = user
        if user_url is not None:
          self.user_url = user_url

    @property
    def clients(self):
        """
        Gets the clients of this RepositoryTokenRefresh.
        

        :return: The clients of this RepositoryTokenRefresh.
        :rtype: int
        """
        return self._clients

    @clients.setter
    def clients(self, clients):
        """
        Sets the clients of this RepositoryTokenRefresh.
        

        :param clients: The clients of this RepositoryTokenRefresh.
        :type: int
        """

        self._clients = clients

    @property
    def created_at(self):
        """
        Gets the created_at of this RepositoryTokenRefresh.
        The datetime the token was updated at.

        :return: The created_at of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this RepositoryTokenRefresh.
        The datetime the token was updated at.

        :param created_at: The created_at of this RepositoryTokenRefresh.
        :type: str
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """
        Gets the created_by of this RepositoryTokenRefresh.
        

        :return: The created_by of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this RepositoryTokenRefresh.
        

        :param created_by: The created_by of this RepositoryTokenRefresh.
        :type: str
        """

        self._created_by = created_by

    @property
    def created_by_url(self):
        """
        Gets the created_by_url of this RepositoryTokenRefresh.
        

        :return: The created_by_url of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._created_by_url

    @created_by_url.setter
    def created_by_url(self, created_by_url):
        """
        Sets the created_by_url of this RepositoryTokenRefresh.
        

        :param created_by_url: The created_by_url of this RepositoryTokenRefresh.
        :type: str
        """

        self._created_by_url = created_by_url

    @property
    def default(self):
        """
        Gets the default of this RepositoryTokenRefresh.
        If selected this is the default token for this repository.

        :return: The default of this RepositoryTokenRefresh.
        :rtype: bool
        """
        return self._default

    @default.setter
    def default(self, default):
        """
        Sets the default of this RepositoryTokenRefresh.
        If selected this is the default token for this repository.

        :param default: The default of this RepositoryTokenRefresh.
        :type: bool
        """

        self._default = default

    @property
    def disable_url(self):
        """
        Gets the disable_url of this RepositoryTokenRefresh.
        

        :return: The disable_url of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._disable_url

    @disable_url.setter
    def disable_url(self, disable_url):
        """
        Sets the disable_url of this RepositoryTokenRefresh.
        

        :param disable_url: The disable_url of this RepositoryTokenRefresh.
        :type: str
        """

        self._disable_url = disable_url

    @property
    def downloads(self):
        """
        Gets the downloads of this RepositoryTokenRefresh.
        

        :return: The downloads of this RepositoryTokenRefresh.
        :rtype: int
        """
        return self._downloads

    @downloads.setter
    def downloads(self, downloads):
        """
        Sets the downloads of this RepositoryTokenRefresh.
        

        :param downloads: The downloads of this RepositoryTokenRefresh.
        :type: int
        """

        self._downloads = downloads

    @property
    def enable_url(self):
        """
        Gets the enable_url of this RepositoryTokenRefresh.
        

        :return: The enable_url of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._enable_url

    @enable_url.setter
    def enable_url(self, enable_url):
        """
        Sets the enable_url of this RepositoryTokenRefresh.
        

        :param enable_url: The enable_url of this RepositoryTokenRefresh.
        :type: str
        """

        self._enable_url = enable_url

    @property
    def has_limits(self):
        """
        Gets the has_limits of this RepositoryTokenRefresh.
        

        :return: The has_limits of this RepositoryTokenRefresh.
        :rtype: bool
        """
        return self._has_limits

    @has_limits.setter
    def has_limits(self, has_limits):
        """
        Sets the has_limits of this RepositoryTokenRefresh.
        

        :param has_limits: The has_limits of this RepositoryTokenRefresh.
        :type: bool
        """

        self._has_limits = has_limits

    @property
    def identifier(self):
        """
        Gets the identifier of this RepositoryTokenRefresh.
        

        :return: The identifier of this RepositoryTokenRefresh.
        :rtype: int
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this RepositoryTokenRefresh.
        

        :param identifier: The identifier of this RepositoryTokenRefresh.
        :type: int
        """

        self._identifier = identifier

    @property
    def is_active(self):
        """
        Gets the is_active of this RepositoryTokenRefresh.
        If enabled, the token will allow downloads based on configured restrictions (if any).

        :return: The is_active of this RepositoryTokenRefresh.
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """
        Sets the is_active of this RepositoryTokenRefresh.
        If enabled, the token will allow downloads based on configured restrictions (if any).

        :param is_active: The is_active of this RepositoryTokenRefresh.
        :type: bool
        """

        self._is_active = is_active

    @property
    def is_limited(self):
        """
        Gets the is_limited of this RepositoryTokenRefresh.
        

        :return: The is_limited of this RepositoryTokenRefresh.
        :rtype: bool
        """
        return self._is_limited

    @is_limited.setter
    def is_limited(self, is_limited):
        """
        Sets the is_limited of this RepositoryTokenRefresh.
        

        :param is_limited: The is_limited of this RepositoryTokenRefresh.
        :type: bool
        """

        self._is_limited = is_limited

    @property
    def limit_bandwidth(self):
        """
        Gets the limit_bandwidth of this RepositoryTokenRefresh.
        The maximum download bandwidth allowed for the token. Values are expressed as the selected unit of bandwidth. Please note that since downloads are calculated asynchronously (after the download happens), the limit may not be imposed immediately but at a later point. 

        :return: The limit_bandwidth of this RepositoryTokenRefresh.
        :rtype: int
        """
        return self._limit_bandwidth

    @limit_bandwidth.setter
    def limit_bandwidth(self, limit_bandwidth):
        """
        Sets the limit_bandwidth of this RepositoryTokenRefresh.
        The maximum download bandwidth allowed for the token. Values are expressed as the selected unit of bandwidth. Please note that since downloads are calculated asynchronously (after the download happens), the limit may not be imposed immediately but at a later point. 

        :param limit_bandwidth: The limit_bandwidth of this RepositoryTokenRefresh.
        :type: int
        """

        self._limit_bandwidth = limit_bandwidth

    @property
    def limit_bandwidth_unit(self):
        """
        Gets the limit_bandwidth_unit of this RepositoryTokenRefresh.
        

        :return: The limit_bandwidth_unit of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._limit_bandwidth_unit

    @limit_bandwidth_unit.setter
    def limit_bandwidth_unit(self, limit_bandwidth_unit):
        """
        Sets the limit_bandwidth_unit of this RepositoryTokenRefresh.
        

        :param limit_bandwidth_unit: The limit_bandwidth_unit of this RepositoryTokenRefresh.
        :type: str
        """

        self._limit_bandwidth_unit = limit_bandwidth_unit

    @property
    def limit_date_range_from(self):
        """
        Gets the limit_date_range_from of this RepositoryTokenRefresh.
        The starting date/time the token is allowed to be used from.

        :return: The limit_date_range_from of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._limit_date_range_from

    @limit_date_range_from.setter
    def limit_date_range_from(self, limit_date_range_from):
        """
        Sets the limit_date_range_from of this RepositoryTokenRefresh.
        The starting date/time the token is allowed to be used from.

        :param limit_date_range_from: The limit_date_range_from of this RepositoryTokenRefresh.
        :type: str
        """

        self._limit_date_range_from = limit_date_range_from

    @property
    def limit_date_range_to(self):
        """
        Gets the limit_date_range_to of this RepositoryTokenRefresh.
        The ending date/time the token is allowed to be used until.

        :return: The limit_date_range_to of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._limit_date_range_to

    @limit_date_range_to.setter
    def limit_date_range_to(self, limit_date_range_to):
        """
        Sets the limit_date_range_to of this RepositoryTokenRefresh.
        The ending date/time the token is allowed to be used until.

        :param limit_date_range_to: The limit_date_range_to of this RepositoryTokenRefresh.
        :type: str
        """

        self._limit_date_range_to = limit_date_range_to

    @property
    def limit_num_clients(self):
        """
        Gets the limit_num_clients of this RepositoryTokenRefresh.
        The maximum number of unique clients allowed for the token. Please note that since clients are calculated asynchronously (after the download happens), the limit may not be imposed immediately but at a later point.

        :return: The limit_num_clients of this RepositoryTokenRefresh.
        :rtype: int
        """
        return self._limit_num_clients

    @limit_num_clients.setter
    def limit_num_clients(self, limit_num_clients):
        """
        Sets the limit_num_clients of this RepositoryTokenRefresh.
        The maximum number of unique clients allowed for the token. Please note that since clients are calculated asynchronously (after the download happens), the limit may not be imposed immediately but at a later point.

        :param limit_num_clients: The limit_num_clients of this RepositoryTokenRefresh.
        :type: int
        """

        self._limit_num_clients = limit_num_clients

    @property
    def limit_num_downloads(self):
        """
        Gets the limit_num_downloads of this RepositoryTokenRefresh.
        The maximum number of downloads allowed for the token. Please note that since downloads are calculated asynchronously (after the download happens), the limit may not be imposed immediately but at a later point.

        :return: The limit_num_downloads of this RepositoryTokenRefresh.
        :rtype: int
        """
        return self._limit_num_downloads

    @limit_num_downloads.setter
    def limit_num_downloads(self, limit_num_downloads):
        """
        Sets the limit_num_downloads of this RepositoryTokenRefresh.
        The maximum number of downloads allowed for the token. Please note that since downloads are calculated asynchronously (after the download happens), the limit may not be imposed immediately but at a later point.

        :param limit_num_downloads: The limit_num_downloads of this RepositoryTokenRefresh.
        :type: int
        """

        self._limit_num_downloads = limit_num_downloads

    @property
    def limit_package_query(self):
        """
        Gets the limit_package_query of this RepositoryTokenRefresh.
        The package-based search query to apply to restrict downloads to. This uses the same syntax as the standard search used for repositories, and also supports boolean logic operators such as OR/AND/NOT and parentheses for grouping. This will still allow access to non-package files, such as metadata.

        :return: The limit_package_query of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._limit_package_query

    @limit_package_query.setter
    def limit_package_query(self, limit_package_query):
        """
        Sets the limit_package_query of this RepositoryTokenRefresh.
        The package-based search query to apply to restrict downloads to. This uses the same syntax as the standard search used for repositories, and also supports boolean logic operators such as OR/AND/NOT and parentheses for grouping. This will still allow access to non-package files, such as metadata.

        :param limit_package_query: The limit_package_query of this RepositoryTokenRefresh.
        :type: str
        """

        self._limit_package_query = limit_package_query

    @property
    def limit_path_query(self):
        """
        Gets the limit_path_query of this RepositoryTokenRefresh.
        The path-based search query to apply to restrict downloads to. This supports boolean logic operators such as OR/AND/NOT and parentheses for grouping. The path evaluated does not include the domain name, the namespace, the entitlement code used, the package format, etc. and it always starts with a forward slash.

        :return: The limit_path_query of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._limit_path_query

    @limit_path_query.setter
    def limit_path_query(self, limit_path_query):
        """
        Sets the limit_path_query of this RepositoryTokenRefresh.
        The path-based search query to apply to restrict downloads to. This supports boolean logic operators such as OR/AND/NOT and parentheses for grouping. The path evaluated does not include the domain name, the namespace, the entitlement code used, the package format, etc. and it always starts with a forward slash.

        :param limit_path_query: The limit_path_query of this RepositoryTokenRefresh.
        :type: str
        """

        self._limit_path_query = limit_path_query

    @property
    def metadata(self):
        """
        Gets the metadata of this RepositoryTokenRefresh.
        

        :return: The metadata of this RepositoryTokenRefresh.
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this RepositoryTokenRefresh.
        

        :param metadata: The metadata of this RepositoryTokenRefresh.
        :type: object
        """

        self._metadata = metadata

    @property
    def name(self):
        """
        Gets the name of this RepositoryTokenRefresh.
        

        :return: The name of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this RepositoryTokenRefresh.
        

        :param name: The name of this RepositoryTokenRefresh.
        :type: str
        """

        self._name = name

    @property
    def refresh_url(self):
        """
        Gets the refresh_url of this RepositoryTokenRefresh.
        

        :return: The refresh_url of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._refresh_url

    @refresh_url.setter
    def refresh_url(self, refresh_url):
        """
        Sets the refresh_url of this RepositoryTokenRefresh.
        

        :param refresh_url: The refresh_url of this RepositoryTokenRefresh.
        :type: str
        """

        self._refresh_url = refresh_url

    @property
    def reset_url(self):
        """
        Gets the reset_url of this RepositoryTokenRefresh.
        

        :return: The reset_url of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._reset_url

    @reset_url.setter
    def reset_url(self, reset_url):
        """
        Sets the reset_url of this RepositoryTokenRefresh.
        

        :param reset_url: The reset_url of this RepositoryTokenRefresh.
        :type: str
        """

        self._reset_url = reset_url

    @property
    def scheduled_reset_at(self):
        """
        Gets the scheduled_reset_at of this RepositoryTokenRefresh.
        The time at which the scheduled reset period has elapsed and the token limits were automatically reset to zero.

        :return: The scheduled_reset_at of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._scheduled_reset_at

    @scheduled_reset_at.setter
    def scheduled_reset_at(self, scheduled_reset_at):
        """
        Sets the scheduled_reset_at of this RepositoryTokenRefresh.
        The time at which the scheduled reset period has elapsed and the token limits were automatically reset to zero.

        :param scheduled_reset_at: The scheduled_reset_at of this RepositoryTokenRefresh.
        :type: str
        """

        self._scheduled_reset_at = scheduled_reset_at

    @property
    def scheduled_reset_period(self):
        """
        Gets the scheduled_reset_period of this RepositoryTokenRefresh.
        

        :return: The scheduled_reset_period of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._scheduled_reset_period

    @scheduled_reset_period.setter
    def scheduled_reset_period(self, scheduled_reset_period):
        """
        Sets the scheduled_reset_period of this RepositoryTokenRefresh.
        

        :param scheduled_reset_period: The scheduled_reset_period of this RepositoryTokenRefresh.
        :type: str
        """

        self._scheduled_reset_period = scheduled_reset_period

    @property
    def self_url(self):
        """
        Gets the self_url of this RepositoryTokenRefresh.
        

        :return: The self_url of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._self_url

    @self_url.setter
    def self_url(self, self_url):
        """
        Sets the self_url of this RepositoryTokenRefresh.
        

        :param self_url: The self_url of this RepositoryTokenRefresh.
        :type: str
        """

        self._self_url = self_url

    @property
    def slug_perm(self):
        """
        Gets the slug_perm of this RepositoryTokenRefresh.
        

        :return: The slug_perm of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._slug_perm

    @slug_perm.setter
    def slug_perm(self, slug_perm):
        """
        Sets the slug_perm of this RepositoryTokenRefresh.
        

        :param slug_perm: The slug_perm of this RepositoryTokenRefresh.
        :type: str
        """

        self._slug_perm = slug_perm

    @property
    def token(self):
        """
        Gets the token of this RepositoryTokenRefresh.
        

        :return: The token of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """
        Sets the token of this RepositoryTokenRefresh.
        

        :param token: The token of this RepositoryTokenRefresh.
        :type: str
        """

        self._token = token

    @property
    def updated_at(self):
        """
        Gets the updated_at of this RepositoryTokenRefresh.
        The datetime the token was updated at.

        :return: The updated_at of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """
        Sets the updated_at of this RepositoryTokenRefresh.
        The datetime the token was updated at.

        :param updated_at: The updated_at of this RepositoryTokenRefresh.
        :type: str
        """

        self._updated_at = updated_at

    @property
    def updated_by(self):
        """
        Gets the updated_by of this RepositoryTokenRefresh.
        

        :return: The updated_by of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """
        Sets the updated_by of this RepositoryTokenRefresh.
        

        :param updated_by: The updated_by of this RepositoryTokenRefresh.
        :type: str
        """

        self._updated_by = updated_by

    @property
    def updated_by_url(self):
        """
        Gets the updated_by_url of this RepositoryTokenRefresh.
        

        :return: The updated_by_url of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._updated_by_url

    @updated_by_url.setter
    def updated_by_url(self, updated_by_url):
        """
        Sets the updated_by_url of this RepositoryTokenRefresh.
        

        :param updated_by_url: The updated_by_url of this RepositoryTokenRefresh.
        :type: str
        """

        self._updated_by_url = updated_by_url

    @property
    def usage(self):
        """
        Gets the usage of this RepositoryTokenRefresh.
        

        :return: The usage of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._usage

    @usage.setter
    def usage(self, usage):
        """
        Sets the usage of this RepositoryTokenRefresh.
        

        :param usage: The usage of this RepositoryTokenRefresh.
        :type: str
        """

        self._usage = usage

    @property
    def user(self):
        """
        Gets the user of this RepositoryTokenRefresh.
        

        :return: The user of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this RepositoryTokenRefresh.
        

        :param user: The user of this RepositoryTokenRefresh.
        :type: str
        """

        self._user = user

    @property
    def user_url(self):
        """
        Gets the user_url of this RepositoryTokenRefresh.
        

        :return: The user_url of this RepositoryTokenRefresh.
        :rtype: str
        """
        return self._user_url

    @user_url.setter
    def user_url(self, user_url):
        """
        Sets the user_url of this RepositoryTokenRefresh.
        

        :param user_url: The user_url of this RepositoryTokenRefresh.
        :type: str
        """

        self._user_url = user_url

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, RepositoryTokenRefresh):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
