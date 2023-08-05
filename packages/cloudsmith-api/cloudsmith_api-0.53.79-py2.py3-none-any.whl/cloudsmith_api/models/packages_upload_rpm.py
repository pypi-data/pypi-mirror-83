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


class PackagesUploadRpm(object):
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
        'distribution': 'str',
        'package_file': 'str',
        'republish': 'bool',
        'tags': 'str'
    }

    attribute_map = {
        'distribution': 'distribution',
        'package_file': 'package_file',
        'republish': 'republish',
        'tags': 'tags'
    }

    def __init__(self, distribution=None, package_file=None, republish=None, tags=None):
        """
        PackagesUploadRpm - a model defined in Swagger
        """

        self._distribution = None
        self._package_file = None
        self._republish = None
        self._tags = None

        self.distribution = distribution
        self.package_file = package_file
        if republish is not None:
          self.republish = republish
        if tags is not None:
          self.tags = tags

    @property
    def distribution(self):
        """
        Gets the distribution of this PackagesUploadRpm.
        The distribution to store the package for.

        :return: The distribution of this PackagesUploadRpm.
        :rtype: str
        """
        return self._distribution

    @distribution.setter
    def distribution(self, distribution):
        """
        Sets the distribution of this PackagesUploadRpm.
        The distribution to store the package for.

        :param distribution: The distribution of this PackagesUploadRpm.
        :type: str
        """
        if distribution is None:
            raise ValueError("Invalid value for `distribution`, must not be `None`")

        self._distribution = distribution

    @property
    def package_file(self):
        """
        Gets the package_file of this PackagesUploadRpm.
        The primary file for the package.

        :return: The package_file of this PackagesUploadRpm.
        :rtype: str
        """
        return self._package_file

    @package_file.setter
    def package_file(self, package_file):
        """
        Sets the package_file of this PackagesUploadRpm.
        The primary file for the package.

        :param package_file: The package_file of this PackagesUploadRpm.
        :type: str
        """
        if package_file is None:
            raise ValueError("Invalid value for `package_file`, must not be `None`")

        self._package_file = package_file

    @property
    def republish(self):
        """
        Gets the republish of this PackagesUploadRpm.
        If true, the uploaded package will overwrite any others with the same attributes (e.g. same version); otherwise, it will be flagged as a duplicate.

        :return: The republish of this PackagesUploadRpm.
        :rtype: bool
        """
        return self._republish

    @republish.setter
    def republish(self, republish):
        """
        Sets the republish of this PackagesUploadRpm.
        If true, the uploaded package will overwrite any others with the same attributes (e.g. same version); otherwise, it will be flagged as a duplicate.

        :param republish: The republish of this PackagesUploadRpm.
        :type: bool
        """

        self._republish = republish

    @property
    def tags(self):
        """
        Gets the tags of this PackagesUploadRpm.
        A comma-separated values list of tags to add to the package.

        :return: The tags of this PackagesUploadRpm.
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this PackagesUploadRpm.
        A comma-separated values list of tags to add to the package.

        :param tags: The tags of this PackagesUploadRpm.
        :type: str
        """

        self._tags = tags

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
        if not isinstance(other, PackagesUploadRpm):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
