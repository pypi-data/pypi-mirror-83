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


class RepositoryWebhook(object):
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
        'created_at': 'str',
        'created_by': 'str',
        'created_by_url': 'str',
        'disable_reason': 'str',
        'disable_reason_str': 'str',
        'events': 'list[str]',
        'identifier': 'int',
        'is_active': 'bool',
        'is_last_response_bad': 'bool',
        'last_response_status': 'int',
        'last_response_status_str': 'str',
        'num_sent': 'int',
        'package_query': 'str',
        'request_body_format': 'str',
        'request_body_format_str': 'str',
        'request_body_template_format': 'str',
        'request_body_template_format_str': 'str',
        'request_content_type': 'str',
        'secret_header': 'str',
        'self_url': 'str',
        'slug_perm': 'str',
        'target_url': 'str',
        'templates': 'list[WebhooksownerrepoTemplates]',
        'updated_at': 'str',
        'updated_by': 'str',
        'updated_by_url': 'str',
        'verify_ssl': 'bool'
    }

    attribute_map = {
        'created_at': 'created_at',
        'created_by': 'created_by',
        'created_by_url': 'created_by_url',
        'disable_reason': 'disable_reason',
        'disable_reason_str': 'disable_reason_str',
        'events': 'events',
        'identifier': 'identifier',
        'is_active': 'is_active',
        'is_last_response_bad': 'is_last_response_bad',
        'last_response_status': 'last_response_status',
        'last_response_status_str': 'last_response_status_str',
        'num_sent': 'num_sent',
        'package_query': 'package_query',
        'request_body_format': 'request_body_format',
        'request_body_format_str': 'request_body_format_str',
        'request_body_template_format': 'request_body_template_format',
        'request_body_template_format_str': 'request_body_template_format_str',
        'request_content_type': 'request_content_type',
        'secret_header': 'secret_header',
        'self_url': 'self_url',
        'slug_perm': 'slug_perm',
        'target_url': 'target_url',
        'templates': 'templates',
        'updated_at': 'updated_at',
        'updated_by': 'updated_by',
        'updated_by_url': 'updated_by_url',
        'verify_ssl': 'verify_ssl'
    }

    def __init__(self, created_at=None, created_by=None, created_by_url=None, disable_reason=None, disable_reason_str=None, events=None, identifier=None, is_active=None, is_last_response_bad=None, last_response_status=None, last_response_status_str=None, num_sent=None, package_query=None, request_body_format=None, request_body_format_str=None, request_body_template_format=None, request_body_template_format_str=None, request_content_type=None, secret_header=None, self_url=None, slug_perm=None, target_url=None, templates=None, updated_at=None, updated_by=None, updated_by_url=None, verify_ssl=None):
        """
        RepositoryWebhook - a model defined in Swagger
        """

        self._created_at = None
        self._created_by = None
        self._created_by_url = None
        self._disable_reason = None
        self._disable_reason_str = None
        self._events = None
        self._identifier = None
        self._is_active = None
        self._is_last_response_bad = None
        self._last_response_status = None
        self._last_response_status_str = None
        self._num_sent = None
        self._package_query = None
        self._request_body_format = None
        self._request_body_format_str = None
        self._request_body_template_format = None
        self._request_body_template_format_str = None
        self._request_content_type = None
        self._secret_header = None
        self._self_url = None
        self._slug_perm = None
        self._target_url = None
        self._templates = None
        self._updated_at = None
        self._updated_by = None
        self._updated_by_url = None
        self._verify_ssl = None

        if created_at is not None:
          self.created_at = created_at
        if created_by is not None:
          self.created_by = created_by
        if created_by_url is not None:
          self.created_by_url = created_by_url
        if disable_reason is not None:
          self.disable_reason = disable_reason
        if disable_reason_str is not None:
          self.disable_reason_str = disable_reason_str
        self.events = events
        if identifier is not None:
          self.identifier = identifier
        if is_active is not None:
          self.is_active = is_active
        if is_last_response_bad is not None:
          self.is_last_response_bad = is_last_response_bad
        if last_response_status is not None:
          self.last_response_status = last_response_status
        if last_response_status_str is not None:
          self.last_response_status_str = last_response_status_str
        if num_sent is not None:
          self.num_sent = num_sent
        if package_query is not None:
          self.package_query = package_query
        if request_body_format is not None:
          self.request_body_format = request_body_format
        if request_body_format_str is not None:
          self.request_body_format_str = request_body_format_str
        if request_body_template_format is not None:
          self.request_body_template_format = request_body_template_format
        if request_body_template_format_str is not None:
          self.request_body_template_format_str = request_body_template_format_str
        if request_content_type is not None:
          self.request_content_type = request_content_type
        if secret_header is not None:
          self.secret_header = secret_header
        if self_url is not None:
          self.self_url = self_url
        if slug_perm is not None:
          self.slug_perm = slug_perm
        self.target_url = target_url
        self.templates = templates
        if updated_at is not None:
          self.updated_at = updated_at
        if updated_by is not None:
          self.updated_by = updated_by
        if updated_by_url is not None:
          self.updated_by_url = updated_by_url
        if verify_ssl is not None:
          self.verify_ssl = verify_ssl

    @property
    def created_at(self):
        """
        Gets the created_at of this RepositoryWebhook.
        

        :return: The created_at of this RepositoryWebhook.
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this RepositoryWebhook.
        

        :param created_at: The created_at of this RepositoryWebhook.
        :type: str
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """
        Gets the created_by of this RepositoryWebhook.
        

        :return: The created_by of this RepositoryWebhook.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this RepositoryWebhook.
        

        :param created_by: The created_by of this RepositoryWebhook.
        :type: str
        """

        self._created_by = created_by

    @property
    def created_by_url(self):
        """
        Gets the created_by_url of this RepositoryWebhook.
        

        :return: The created_by_url of this RepositoryWebhook.
        :rtype: str
        """
        return self._created_by_url

    @created_by_url.setter
    def created_by_url(self, created_by_url):
        """
        Sets the created_by_url of this RepositoryWebhook.
        

        :param created_by_url: The created_by_url of this RepositoryWebhook.
        :type: str
        """

        self._created_by_url = created_by_url

    @property
    def disable_reason(self):
        """
        Gets the disable_reason of this RepositoryWebhook.
        

        :return: The disable_reason of this RepositoryWebhook.
        :rtype: str
        """
        return self._disable_reason

    @disable_reason.setter
    def disable_reason(self, disable_reason):
        """
        Sets the disable_reason of this RepositoryWebhook.
        

        :param disable_reason: The disable_reason of this RepositoryWebhook.
        :type: str
        """

        self._disable_reason = disable_reason

    @property
    def disable_reason_str(self):
        """
        Gets the disable_reason_str of this RepositoryWebhook.
        

        :return: The disable_reason_str of this RepositoryWebhook.
        :rtype: str
        """
        return self._disable_reason_str

    @disable_reason_str.setter
    def disable_reason_str(self, disable_reason_str):
        """
        Sets the disable_reason_str of this RepositoryWebhook.
        

        :param disable_reason_str: The disable_reason_str of this RepositoryWebhook.
        :type: str
        """

        self._disable_reason_str = disable_reason_str

    @property
    def events(self):
        """
        Gets the events of this RepositoryWebhook.
        

        :return: The events of this RepositoryWebhook.
        :rtype: list[str]
        """
        return self._events

    @events.setter
    def events(self, events):
        """
        Sets the events of this RepositoryWebhook.
        

        :param events: The events of this RepositoryWebhook.
        :type: list[str]
        """
        if events is None:
            raise ValueError("Invalid value for `events`, must not be `None`")

        self._events = events

    @property
    def identifier(self):
        """
        Gets the identifier of this RepositoryWebhook.
        

        :return: The identifier of this RepositoryWebhook.
        :rtype: int
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this RepositoryWebhook.
        

        :param identifier: The identifier of this RepositoryWebhook.
        :type: int
        """

        self._identifier = identifier

    @property
    def is_active(self):
        """
        Gets the is_active of this RepositoryWebhook.
        If enabled, the webhook will trigger on events and send payloads to the configured target URL.

        :return: The is_active of this RepositoryWebhook.
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """
        Sets the is_active of this RepositoryWebhook.
        If enabled, the webhook will trigger on events and send payloads to the configured target URL.

        :param is_active: The is_active of this RepositoryWebhook.
        :type: bool
        """

        self._is_active = is_active

    @property
    def is_last_response_bad(self):
        """
        Gets the is_last_response_bad of this RepositoryWebhook.
        

        :return: The is_last_response_bad of this RepositoryWebhook.
        :rtype: bool
        """
        return self._is_last_response_bad

    @is_last_response_bad.setter
    def is_last_response_bad(self, is_last_response_bad):
        """
        Sets the is_last_response_bad of this RepositoryWebhook.
        

        :param is_last_response_bad: The is_last_response_bad of this RepositoryWebhook.
        :type: bool
        """

        self._is_last_response_bad = is_last_response_bad

    @property
    def last_response_status(self):
        """
        Gets the last_response_status of this RepositoryWebhook.
        

        :return: The last_response_status of this RepositoryWebhook.
        :rtype: int
        """
        return self._last_response_status

    @last_response_status.setter
    def last_response_status(self, last_response_status):
        """
        Sets the last_response_status of this RepositoryWebhook.
        

        :param last_response_status: The last_response_status of this RepositoryWebhook.
        :type: int
        """

        self._last_response_status = last_response_status

    @property
    def last_response_status_str(self):
        """
        Gets the last_response_status_str of this RepositoryWebhook.
        

        :return: The last_response_status_str of this RepositoryWebhook.
        :rtype: str
        """
        return self._last_response_status_str

    @last_response_status_str.setter
    def last_response_status_str(self, last_response_status_str):
        """
        Sets the last_response_status_str of this RepositoryWebhook.
        

        :param last_response_status_str: The last_response_status_str of this RepositoryWebhook.
        :type: str
        """

        self._last_response_status_str = last_response_status_str

    @property
    def num_sent(self):
        """
        Gets the num_sent of this RepositoryWebhook.
        

        :return: The num_sent of this RepositoryWebhook.
        :rtype: int
        """
        return self._num_sent

    @num_sent.setter
    def num_sent(self, num_sent):
        """
        Sets the num_sent of this RepositoryWebhook.
        

        :param num_sent: The num_sent of this RepositoryWebhook.
        :type: int
        """

        self._num_sent = num_sent

    @property
    def package_query(self):
        """
        Gets the package_query of this RepositoryWebhook.
        The package-based search query for webhooks to fire. This uses the same syntax as the standard search used for repositories, and also supports boolean logic operators such as OR/AND/NOT and parentheses for grouping. If a package does not match, the webhook will not fire.

        :return: The package_query of this RepositoryWebhook.
        :rtype: str
        """
        return self._package_query

    @package_query.setter
    def package_query(self, package_query):
        """
        Sets the package_query of this RepositoryWebhook.
        The package-based search query for webhooks to fire. This uses the same syntax as the standard search used for repositories, and also supports boolean logic operators such as OR/AND/NOT and parentheses for grouping. If a package does not match, the webhook will not fire.

        :param package_query: The package_query of this RepositoryWebhook.
        :type: str
        """

        self._package_query = package_query

    @property
    def request_body_format(self):
        """
        Gets the request_body_format of this RepositoryWebhook.
        The format of the payloads for webhook requests.

        :return: The request_body_format of this RepositoryWebhook.
        :rtype: str
        """
        return self._request_body_format

    @request_body_format.setter
    def request_body_format(self, request_body_format):
        """
        Sets the request_body_format of this RepositoryWebhook.
        The format of the payloads for webhook requests.

        :param request_body_format: The request_body_format of this RepositoryWebhook.
        :type: str
        """

        self._request_body_format = request_body_format

    @property
    def request_body_format_str(self):
        """
        Gets the request_body_format_str of this RepositoryWebhook.
        

        :return: The request_body_format_str of this RepositoryWebhook.
        :rtype: str
        """
        return self._request_body_format_str

    @request_body_format_str.setter
    def request_body_format_str(self, request_body_format_str):
        """
        Sets the request_body_format_str of this RepositoryWebhook.
        

        :param request_body_format_str: The request_body_format_str of this RepositoryWebhook.
        :type: str
        """

        self._request_body_format_str = request_body_format_str

    @property
    def request_body_template_format(self):
        """
        Gets the request_body_template_format of this RepositoryWebhook.
        The format of the payloads for webhook requests.

        :return: The request_body_template_format of this RepositoryWebhook.
        :rtype: str
        """
        return self._request_body_template_format

    @request_body_template_format.setter
    def request_body_template_format(self, request_body_template_format):
        """
        Sets the request_body_template_format of this RepositoryWebhook.
        The format of the payloads for webhook requests.

        :param request_body_template_format: The request_body_template_format of this RepositoryWebhook.
        :type: str
        """

        self._request_body_template_format = request_body_template_format

    @property
    def request_body_template_format_str(self):
        """
        Gets the request_body_template_format_str of this RepositoryWebhook.
        

        :return: The request_body_template_format_str of this RepositoryWebhook.
        :rtype: str
        """
        return self._request_body_template_format_str

    @request_body_template_format_str.setter
    def request_body_template_format_str(self, request_body_template_format_str):
        """
        Sets the request_body_template_format_str of this RepositoryWebhook.
        

        :param request_body_template_format_str: The request_body_template_format_str of this RepositoryWebhook.
        :type: str
        """

        self._request_body_template_format_str = request_body_template_format_str

    @property
    def request_content_type(self):
        """
        Gets the request_content_type of this RepositoryWebhook.
        The value that will be sent for the 'Content Type' header. 

        :return: The request_content_type of this RepositoryWebhook.
        :rtype: str
        """
        return self._request_content_type

    @request_content_type.setter
    def request_content_type(self, request_content_type):
        """
        Sets the request_content_type of this RepositoryWebhook.
        The value that will be sent for the 'Content Type' header. 

        :param request_content_type: The request_content_type of this RepositoryWebhook.
        :type: str
        """

        self._request_content_type = request_content_type

    @property
    def secret_header(self):
        """
        Gets the secret_header of this RepositoryWebhook.
        The header to send the predefined secret in. This must be unique from existing headers or it won't be sent. You can use this as a form of authentication on the endpoint side.

        :return: The secret_header of this RepositoryWebhook.
        :rtype: str
        """
        return self._secret_header

    @secret_header.setter
    def secret_header(self, secret_header):
        """
        Sets the secret_header of this RepositoryWebhook.
        The header to send the predefined secret in. This must be unique from existing headers or it won't be sent. You can use this as a form of authentication on the endpoint side.

        :param secret_header: The secret_header of this RepositoryWebhook.
        :type: str
        """

        self._secret_header = secret_header

    @property
    def self_url(self):
        """
        Gets the self_url of this RepositoryWebhook.
        

        :return: The self_url of this RepositoryWebhook.
        :rtype: str
        """
        return self._self_url

    @self_url.setter
    def self_url(self, self_url):
        """
        Sets the self_url of this RepositoryWebhook.
        

        :param self_url: The self_url of this RepositoryWebhook.
        :type: str
        """

        self._self_url = self_url

    @property
    def slug_perm(self):
        """
        Gets the slug_perm of this RepositoryWebhook.
        

        :return: The slug_perm of this RepositoryWebhook.
        :rtype: str
        """
        return self._slug_perm

    @slug_perm.setter
    def slug_perm(self, slug_perm):
        """
        Sets the slug_perm of this RepositoryWebhook.
        

        :param slug_perm: The slug_perm of this RepositoryWebhook.
        :type: str
        """

        self._slug_perm = slug_perm

    @property
    def target_url(self):
        """
        Gets the target_url of this RepositoryWebhook.
        The destination URL that webhook payloads will be POST'ed to.

        :return: The target_url of this RepositoryWebhook.
        :rtype: str
        """
        return self._target_url

    @target_url.setter
    def target_url(self, target_url):
        """
        Sets the target_url of this RepositoryWebhook.
        The destination URL that webhook payloads will be POST'ed to.

        :param target_url: The target_url of this RepositoryWebhook.
        :type: str
        """
        if target_url is None:
            raise ValueError("Invalid value for `target_url`, must not be `None`")

        self._target_url = target_url

    @property
    def templates(self):
        """
        Gets the templates of this RepositoryWebhook.
        

        :return: The templates of this RepositoryWebhook.
        :rtype: list[WebhooksownerrepoTemplates]
        """
        return self._templates

    @templates.setter
    def templates(self, templates):
        """
        Sets the templates of this RepositoryWebhook.
        

        :param templates: The templates of this RepositoryWebhook.
        :type: list[WebhooksownerrepoTemplates]
        """
        if templates is None:
            raise ValueError("Invalid value for `templates`, must not be `None`")

        self._templates = templates

    @property
    def updated_at(self):
        """
        Gets the updated_at of this RepositoryWebhook.
        

        :return: The updated_at of this RepositoryWebhook.
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """
        Sets the updated_at of this RepositoryWebhook.
        

        :param updated_at: The updated_at of this RepositoryWebhook.
        :type: str
        """

        self._updated_at = updated_at

    @property
    def updated_by(self):
        """
        Gets the updated_by of this RepositoryWebhook.
        

        :return: The updated_by of this RepositoryWebhook.
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """
        Sets the updated_by of this RepositoryWebhook.
        

        :param updated_by: The updated_by of this RepositoryWebhook.
        :type: str
        """

        self._updated_by = updated_by

    @property
    def updated_by_url(self):
        """
        Gets the updated_by_url of this RepositoryWebhook.
        

        :return: The updated_by_url of this RepositoryWebhook.
        :rtype: str
        """
        return self._updated_by_url

    @updated_by_url.setter
    def updated_by_url(self, updated_by_url):
        """
        Sets the updated_by_url of this RepositoryWebhook.
        

        :param updated_by_url: The updated_by_url of this RepositoryWebhook.
        :type: str
        """

        self._updated_by_url = updated_by_url

    @property
    def verify_ssl(self):
        """
        Gets the verify_ssl of this RepositoryWebhook.
        If enabled, SSL certificates is verified when webhooks are sent. It's recommended to leave this enabled as not verifying the integrity of SSL certificates leaves you susceptible to Man-in-the-Middle (MITM) attacks.

        :return: The verify_ssl of this RepositoryWebhook.
        :rtype: bool
        """
        return self._verify_ssl

    @verify_ssl.setter
    def verify_ssl(self, verify_ssl):
        """
        Sets the verify_ssl of this RepositoryWebhook.
        If enabled, SSL certificates is verified when webhooks are sent. It's recommended to leave this enabled as not verifying the integrity of SSL certificates leaves you susceptible to Man-in-the-Middle (MITM) attacks.

        :param verify_ssl: The verify_ssl of this RepositoryWebhook.
        :type: bool
        """

        self._verify_ssl = verify_ssl

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
        if not isinstance(other, RepositoryWebhook):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
