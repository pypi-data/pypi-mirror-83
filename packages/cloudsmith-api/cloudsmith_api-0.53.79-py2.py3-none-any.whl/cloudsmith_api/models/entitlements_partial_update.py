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


class EntitlementsPartialUpdate(object):
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
        'is_active': 'bool',
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
        'scheduled_reset_at': 'str',
        'scheduled_reset_period': 'str',
        'token': 'str'
    }

    attribute_map = {
        'is_active': 'is_active',
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
        'scheduled_reset_at': 'scheduled_reset_at',
        'scheduled_reset_period': 'scheduled_reset_period',
        'token': 'token'
    }

    def __init__(self, is_active=None, limit_bandwidth=None, limit_bandwidth_unit=None, limit_date_range_from=None, limit_date_range_to=None, limit_num_clients=None, limit_num_downloads=None, limit_package_query=None, limit_path_query=None, metadata=None, name=None, scheduled_reset_at=None, scheduled_reset_period=None, token=None):
        """
        EntitlementsPartialUpdate - a model defined in Swagger
        """

        self._is_active = None
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
        self._scheduled_reset_at = None
        self._scheduled_reset_period = None
        self._token = None

        if is_active is not None:
          self.is_active = is_active
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
        if scheduled_reset_at is not None:
          self.scheduled_reset_at = scheduled_reset_at
        if scheduled_reset_period is not None:
          self.scheduled_reset_period = scheduled_reset_period
        if token is not None:
          self.token = token

    @property
    def is_active(self):
        """
        Gets the is_active of this EntitlementsPartialUpdate.
        If enabled, the token will allow downloads based on configured restrictions (if any).

        :return: The is_active of this EntitlementsPartialUpdate.
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """
        Sets the is_active of this EntitlementsPartialUpdate.
        If enabled, the token will allow downloads based on configured restrictions (if any).

        :param is_active: The is_active of this EntitlementsPartialUpdate.
        :type: bool
        """

        self._is_active = is_active

    @property
    def limit_bandwidth(self):
        """
        Gets the limit_bandwidth of this EntitlementsPartialUpdate.
        The maximum download bandwidth allowed for the token. Values are expressed as the selected unit of bandwidth. Please note that since downloads are calculated asynchronously (after the download happens), the limit may not be imposed immediately but at a later point. 

        :return: The limit_bandwidth of this EntitlementsPartialUpdate.
        :rtype: int
        """
        return self._limit_bandwidth

    @limit_bandwidth.setter
    def limit_bandwidth(self, limit_bandwidth):
        """
        Sets the limit_bandwidth of this EntitlementsPartialUpdate.
        The maximum download bandwidth allowed for the token. Values are expressed as the selected unit of bandwidth. Please note that since downloads are calculated asynchronously (after the download happens), the limit may not be imposed immediately but at a later point. 

        :param limit_bandwidth: The limit_bandwidth of this EntitlementsPartialUpdate.
        :type: int
        """

        self._limit_bandwidth = limit_bandwidth

    @property
    def limit_bandwidth_unit(self):
        """
        Gets the limit_bandwidth_unit of this EntitlementsPartialUpdate.
        None

        :return: The limit_bandwidth_unit of this EntitlementsPartialUpdate.
        :rtype: str
        """
        return self._limit_bandwidth_unit

    @limit_bandwidth_unit.setter
    def limit_bandwidth_unit(self, limit_bandwidth_unit):
        """
        Sets the limit_bandwidth_unit of this EntitlementsPartialUpdate.
        None

        :param limit_bandwidth_unit: The limit_bandwidth_unit of this EntitlementsPartialUpdate.
        :type: str
        """

        self._limit_bandwidth_unit = limit_bandwidth_unit

    @property
    def limit_date_range_from(self):
        """
        Gets the limit_date_range_from of this EntitlementsPartialUpdate.
        The starting date/time the token is allowed to be used from.

        :return: The limit_date_range_from of this EntitlementsPartialUpdate.
        :rtype: str
        """
        return self._limit_date_range_from

    @limit_date_range_from.setter
    def limit_date_range_from(self, limit_date_range_from):
        """
        Sets the limit_date_range_from of this EntitlementsPartialUpdate.
        The starting date/time the token is allowed to be used from.

        :param limit_date_range_from: The limit_date_range_from of this EntitlementsPartialUpdate.
        :type: str
        """

        self._limit_date_range_from = limit_date_range_from

    @property
    def limit_date_range_to(self):
        """
        Gets the limit_date_range_to of this EntitlementsPartialUpdate.
        The ending date/time the token is allowed to be used until.

        :return: The limit_date_range_to of this EntitlementsPartialUpdate.
        :rtype: str
        """
        return self._limit_date_range_to

    @limit_date_range_to.setter
    def limit_date_range_to(self, limit_date_range_to):
        """
        Sets the limit_date_range_to of this EntitlementsPartialUpdate.
        The ending date/time the token is allowed to be used until.

        :param limit_date_range_to: The limit_date_range_to of this EntitlementsPartialUpdate.
        :type: str
        """

        self._limit_date_range_to = limit_date_range_to

    @property
    def limit_num_clients(self):
        """
        Gets the limit_num_clients of this EntitlementsPartialUpdate.
        The maximum number of unique clients allowed for the token. Please note that since clients are calculated asynchronously (after the download happens), the limit may not be imposed immediately but at a later point.

        :return: The limit_num_clients of this EntitlementsPartialUpdate.
        :rtype: int
        """
        return self._limit_num_clients

    @limit_num_clients.setter
    def limit_num_clients(self, limit_num_clients):
        """
        Sets the limit_num_clients of this EntitlementsPartialUpdate.
        The maximum number of unique clients allowed for the token. Please note that since clients are calculated asynchronously (after the download happens), the limit may not be imposed immediately but at a later point.

        :param limit_num_clients: The limit_num_clients of this EntitlementsPartialUpdate.
        :type: int
        """

        self._limit_num_clients = limit_num_clients

    @property
    def limit_num_downloads(self):
        """
        Gets the limit_num_downloads of this EntitlementsPartialUpdate.
        The maximum number of downloads allowed for the token. Please note that since downloads are calculated asynchronously (after the download happens), the limit may not be imposed immediately but at a later point.

        :return: The limit_num_downloads of this EntitlementsPartialUpdate.
        :rtype: int
        """
        return self._limit_num_downloads

    @limit_num_downloads.setter
    def limit_num_downloads(self, limit_num_downloads):
        """
        Sets the limit_num_downloads of this EntitlementsPartialUpdate.
        The maximum number of downloads allowed for the token. Please note that since downloads are calculated asynchronously (after the download happens), the limit may not be imposed immediately but at a later point.

        :param limit_num_downloads: The limit_num_downloads of this EntitlementsPartialUpdate.
        :type: int
        """

        self._limit_num_downloads = limit_num_downloads

    @property
    def limit_package_query(self):
        """
        Gets the limit_package_query of this EntitlementsPartialUpdate.
        The package-based search query to apply to restrict downloads to. This uses the same syntax as the standard search used for repositories, and also supports boolean logic operators such as OR/AND/NOT and parentheses for grouping. This will still allow access to non-package files, such as metadata.

        :return: The limit_package_query of this EntitlementsPartialUpdate.
        :rtype: str
        """
        return self._limit_package_query

    @limit_package_query.setter
    def limit_package_query(self, limit_package_query):
        """
        Sets the limit_package_query of this EntitlementsPartialUpdate.
        The package-based search query to apply to restrict downloads to. This uses the same syntax as the standard search used for repositories, and also supports boolean logic operators such as OR/AND/NOT and parentheses for grouping. This will still allow access to non-package files, such as metadata.

        :param limit_package_query: The limit_package_query of this EntitlementsPartialUpdate.
        :type: str
        """

        self._limit_package_query = limit_package_query

    @property
    def limit_path_query(self):
        """
        Gets the limit_path_query of this EntitlementsPartialUpdate.
        The path-based search query to apply to restrict downloads to. This supports boolean logic operators such as OR/AND/NOT and parentheses for grouping. The path evaluated does not include the domain name, the namespace, the entitlement code used, the package format, etc. and it always starts with a forward slash.

        :return: The limit_path_query of this EntitlementsPartialUpdate.
        :rtype: str
        """
        return self._limit_path_query

    @limit_path_query.setter
    def limit_path_query(self, limit_path_query):
        """
        Sets the limit_path_query of this EntitlementsPartialUpdate.
        The path-based search query to apply to restrict downloads to. This supports boolean logic operators such as OR/AND/NOT and parentheses for grouping. The path evaluated does not include the domain name, the namespace, the entitlement code used, the package format, etc. and it always starts with a forward slash.

        :param limit_path_query: The limit_path_query of this EntitlementsPartialUpdate.
        :type: str
        """

        self._limit_path_query = limit_path_query

    @property
    def metadata(self):
        """
        Gets the metadata of this EntitlementsPartialUpdate.
        None

        :return: The metadata of this EntitlementsPartialUpdate.
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this EntitlementsPartialUpdate.
        None

        :param metadata: The metadata of this EntitlementsPartialUpdate.
        :type: object
        """

        self._metadata = metadata

    @property
    def name(self):
        """
        Gets the name of this EntitlementsPartialUpdate.
        None

        :return: The name of this EntitlementsPartialUpdate.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this EntitlementsPartialUpdate.
        None

        :param name: The name of this EntitlementsPartialUpdate.
        :type: str
        """

        self._name = name

    @property
    def scheduled_reset_at(self):
        """
        Gets the scheduled_reset_at of this EntitlementsPartialUpdate.
        The time at which the scheduled reset period has elapsed and the token limits were automatically reset to zero.

        :return: The scheduled_reset_at of this EntitlementsPartialUpdate.
        :rtype: str
        """
        return self._scheduled_reset_at

    @scheduled_reset_at.setter
    def scheduled_reset_at(self, scheduled_reset_at):
        """
        Sets the scheduled_reset_at of this EntitlementsPartialUpdate.
        The time at which the scheduled reset period has elapsed and the token limits were automatically reset to zero.

        :param scheduled_reset_at: The scheduled_reset_at of this EntitlementsPartialUpdate.
        :type: str
        """

        self._scheduled_reset_at = scheduled_reset_at

    @property
    def scheduled_reset_period(self):
        """
        Gets the scheduled_reset_period of this EntitlementsPartialUpdate.
        None

        :return: The scheduled_reset_period of this EntitlementsPartialUpdate.
        :rtype: str
        """
        return self._scheduled_reset_period

    @scheduled_reset_period.setter
    def scheduled_reset_period(self, scheduled_reset_period):
        """
        Sets the scheduled_reset_period of this EntitlementsPartialUpdate.
        None

        :param scheduled_reset_period: The scheduled_reset_period of this EntitlementsPartialUpdate.
        :type: str
        """

        self._scheduled_reset_period = scheduled_reset_period

    @property
    def token(self):
        """
        Gets the token of this EntitlementsPartialUpdate.
        None

        :return: The token of this EntitlementsPartialUpdate.
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """
        Sets the token of this EntitlementsPartialUpdate.
        None

        :param token: The token of this EntitlementsPartialUpdate.
        :type: str
        """

        self._token = token

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
        if not isinstance(other, EntitlementsPartialUpdate):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
