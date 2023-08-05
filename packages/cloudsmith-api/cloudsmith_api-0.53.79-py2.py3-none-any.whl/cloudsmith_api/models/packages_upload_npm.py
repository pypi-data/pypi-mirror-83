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


class PackagesUploadNpm(object):
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
        'npm_dist_tag': 'str',
        'package_file': 'str',
        'republish': 'bool',
        'tags': 'str'
    }

    attribute_map = {
        'npm_dist_tag': 'npm_dist_tag',
        'package_file': 'package_file',
        'republish': 'republish',
        'tags': 'tags'
    }

    def __init__(self, npm_dist_tag=None, package_file=None, republish=None, tags=None):
        """
        PackagesUploadNpm - a model defined in Swagger
        """

        self._npm_dist_tag = None
        self._package_file = None
        self._republish = None
        self._tags = None

        if npm_dist_tag is not None:
          self.npm_dist_tag = npm_dist_tag
        self.package_file = package_file
        if republish is not None:
          self.republish = republish
        if tags is not None:
          self.tags = tags

    @property
    def npm_dist_tag(self):
        """
        Gets the npm_dist_tag of this PackagesUploadNpm.
        The default npm dist-tag for this package/version - This will replace any other package/version if they are using the same tag.

        :return: The npm_dist_tag of this PackagesUploadNpm.
        :rtype: str
        """
        return self._npm_dist_tag

    @npm_dist_tag.setter
    def npm_dist_tag(self, npm_dist_tag):
        """
        Sets the npm_dist_tag of this PackagesUploadNpm.
        The default npm dist-tag for this package/version - This will replace any other package/version if they are using the same tag.

        :param npm_dist_tag: The npm_dist_tag of this PackagesUploadNpm.
        :type: str
        """

        self._npm_dist_tag = npm_dist_tag

    @property
    def package_file(self):
        """
        Gets the package_file of this PackagesUploadNpm.
        The primary file for the package.

        :return: The package_file of this PackagesUploadNpm.
        :rtype: str
        """
        return self._package_file

    @package_file.setter
    def package_file(self, package_file):
        """
        Sets the package_file of this PackagesUploadNpm.
        The primary file for the package.

        :param package_file: The package_file of this PackagesUploadNpm.
        :type: str
        """
        if package_file is None:
            raise ValueError("Invalid value for `package_file`, must not be `None`")

        self._package_file = package_file

    @property
    def republish(self):
        """
        Gets the republish of this PackagesUploadNpm.
        If true, the uploaded package will overwrite any others with the same attributes (e.g. same version); otherwise, it will be flagged as a duplicate.

        :return: The republish of this PackagesUploadNpm.
        :rtype: bool
        """
        return self._republish

    @republish.setter
    def republish(self, republish):
        """
        Sets the republish of this PackagesUploadNpm.
        If true, the uploaded package will overwrite any others with the same attributes (e.g. same version); otherwise, it will be flagged as a duplicate.

        :param republish: The republish of this PackagesUploadNpm.
        :type: bool
        """

        self._republish = republish

    @property
    def tags(self):
        """
        Gets the tags of this PackagesUploadNpm.
        A comma-separated values list of tags to add to the package.

        :return: The tags of this PackagesUploadNpm.
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this PackagesUploadNpm.
        A comma-separated values list of tags to add to the package.

        :param tags: The tags of this PackagesUploadNpm.
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
        if not isinstance(other, PackagesUploadNpm):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
