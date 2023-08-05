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


class PackageUsageMetric(object):
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
        'active_packages': 'list[MetricsownerrepopackagesusageActivePackages]',
        'downloads_per_package': 'object',
        'inactive_packages': 'list[MetricsownerrepopackagesusageActivePackages]',
        'totals': 'object'
    }

    attribute_map = {
        'active_packages': 'active_packages',
        'downloads_per_package': 'downloads_per_package',
        'inactive_packages': 'inactive_packages',
        'totals': 'totals'
    }

    def __init__(self, active_packages=None, downloads_per_package=None, inactive_packages=None, totals=None):
        """
        PackageUsageMetric - a model defined in Swagger
        """

        self._active_packages = None
        self._downloads_per_package = None
        self._inactive_packages = None
        self._totals = None

        self.active_packages = active_packages
        self.downloads_per_package = downloads_per_package
        self.inactive_packages = inactive_packages
        self.totals = totals

    @property
    def active_packages(self):
        """
        Gets the active_packages of this PackageUsageMetric.
        

        :return: The active_packages of this PackageUsageMetric.
        :rtype: list[MetricsownerrepopackagesusageActivePackages]
        """
        return self._active_packages

    @active_packages.setter
    def active_packages(self, active_packages):
        """
        Sets the active_packages of this PackageUsageMetric.
        

        :param active_packages: The active_packages of this PackageUsageMetric.
        :type: list[MetricsownerrepopackagesusageActivePackages]
        """
        if active_packages is None:
            raise ValueError("Invalid value for `active_packages`, must not be `None`")

        self._active_packages = active_packages

    @property
    def downloads_per_package(self):
        """
        Gets the downloads_per_package of this PackageUsageMetric.
        

        :return: The downloads_per_package of this PackageUsageMetric.
        :rtype: object
        """
        return self._downloads_per_package

    @downloads_per_package.setter
    def downloads_per_package(self, downloads_per_package):
        """
        Sets the downloads_per_package of this PackageUsageMetric.
        

        :param downloads_per_package: The downloads_per_package of this PackageUsageMetric.
        :type: object
        """
        if downloads_per_package is None:
            raise ValueError("Invalid value for `downloads_per_package`, must not be `None`")

        self._downloads_per_package = downloads_per_package

    @property
    def inactive_packages(self):
        """
        Gets the inactive_packages of this PackageUsageMetric.
        

        :return: The inactive_packages of this PackageUsageMetric.
        :rtype: list[MetricsownerrepopackagesusageActivePackages]
        """
        return self._inactive_packages

    @inactive_packages.setter
    def inactive_packages(self, inactive_packages):
        """
        Sets the inactive_packages of this PackageUsageMetric.
        

        :param inactive_packages: The inactive_packages of this PackageUsageMetric.
        :type: list[MetricsownerrepopackagesusageActivePackages]
        """
        if inactive_packages is None:
            raise ValueError("Invalid value for `inactive_packages`, must not be `None`")

        self._inactive_packages = inactive_packages

    @property
    def totals(self):
        """
        Gets the totals of this PackageUsageMetric.
        

        :return: The totals of this PackageUsageMetric.
        :rtype: object
        """
        return self._totals

    @totals.setter
    def totals(self, totals):
        """
        Sets the totals of this PackageUsageMetric.
        

        :param totals: The totals of this PackageUsageMetric.
        :type: object
        """
        if totals is None:
            raise ValueError("Invalid value for `totals`, must not be `None`")

        self._totals = totals

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
        if not isinstance(other, PackageUsageMetric):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
