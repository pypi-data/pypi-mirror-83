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


class PackagesValidateuploadNuget(object):
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
        'package_file': 'str',
        'republish': 'bool',
        'symbols_file': 'str',
        'tags': 'str'
    }

    attribute_map = {
        'package_file': 'package_file',
        'republish': 'republish',
        'symbols_file': 'symbols_file',
        'tags': 'tags'
    }

    def __init__(self, package_file=None, republish=None, symbols_file=None, tags=None):
        """
        PackagesValidateuploadNuget - a model defined in Swagger
        """

        self._package_file = None
        self._republish = None
        self._symbols_file = None
        self._tags = None

        self.package_file = package_file
        if republish is not None:
          self.republish = republish
        if symbols_file is not None:
          self.symbols_file = symbols_file
        if tags is not None:
          self.tags = tags

    @property
    def package_file(self):
        """
        Gets the package_file of this PackagesValidateuploadNuget.
        The primary file for the package.

        :return: The package_file of this PackagesValidateuploadNuget.
        :rtype: str
        """
        return self._package_file

    @package_file.setter
    def package_file(self, package_file):
        """
        Sets the package_file of this PackagesValidateuploadNuget.
        The primary file for the package.

        :param package_file: The package_file of this PackagesValidateuploadNuget.
        :type: str
        """
        if package_file is None:
            raise ValueError("Invalid value for `package_file`, must not be `None`")

        self._package_file = package_file

    @property
    def republish(self):
        """
        Gets the republish of this PackagesValidateuploadNuget.
        If true, the uploaded package will overwrite any others with the same attributes (e.g. same version); otherwise, it will be flagged as a duplicate.

        :return: The republish of this PackagesValidateuploadNuget.
        :rtype: bool
        """
        return self._republish

    @republish.setter
    def republish(self, republish):
        """
        Sets the republish of this PackagesValidateuploadNuget.
        If true, the uploaded package will overwrite any others with the same attributes (e.g. same version); otherwise, it will be flagged as a duplicate.

        :param republish: The republish of this PackagesValidateuploadNuget.
        :type: bool
        """

        self._republish = republish

    @property
    def symbols_file(self):
        """
        Gets the symbols_file of this PackagesValidateuploadNuget.
        Attaches a symbols file to the package.

        :return: The symbols_file of this PackagesValidateuploadNuget.
        :rtype: str
        """
        return self._symbols_file

    @symbols_file.setter
    def symbols_file(self, symbols_file):
        """
        Sets the symbols_file of this PackagesValidateuploadNuget.
        Attaches a symbols file to the package.

        :param symbols_file: The symbols_file of this PackagesValidateuploadNuget.
        :type: str
        """

        self._symbols_file = symbols_file

    @property
    def tags(self):
        """
        Gets the tags of this PackagesValidateuploadNuget.
        A comma-separated values list of tags to add to the package.

        :return: The tags of this PackagesValidateuploadNuget.
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this PackagesValidateuploadNuget.
        A comma-separated values list of tags to add to the package.

        :param tags: The tags of this PackagesValidateuploadNuget.
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
        if not isinstance(other, PackagesValidateuploadNuget):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
