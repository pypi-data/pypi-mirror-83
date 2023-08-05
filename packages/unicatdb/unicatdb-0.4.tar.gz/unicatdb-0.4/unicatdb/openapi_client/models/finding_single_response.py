# coding: utf-8

"""
    UniCatDB API

    UniCatDB application API documentation, with examples and live testing.  This API is built in accordance with the **JSON API 1.0 standard**. For general information, see [the documentation](http://jsonapi.org/format/).  **Notes:** * JSON API standard requires use of the JSON API media type (application/vnd.api+json) for exchanging data. Clients must send all JSON API data with the headers `Content-Type: application/vnd.api+json` (POST, PATCH) and `Accept: application/vnd.api+json` (GET, DELETE). * [Relationships](http://jsonapi.org/format/#fetching-relationships) and their [inclusions](http://jsonapi.org/format/#fetching-includes) via the `include` query parameter, as specified by the standard, **are not implemented**, since there are no relationships present in the data model. * The standard does not prescribe any filtering strategies. This API implements two strategies which can be combined: **Basic filtering** based on the used [JSON API library](https://json-api-dotnet.github.io/#/filtering) and **Custom filtering** which allow for any possible query to the MongoDB server and can be extended and customize in the future. For more information about filtering, see the description of the `filter` down bellow. * **Non-standard PATCH behavior:** Sucessfull PATCH reuest always result in HTTP 200 response with the updated resource object, even if the server does not perform any additional modifications. HTTP 204 is never used in PATCH responses.   # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from unicatdb.openapi_client.configuration import Configuration


class FindingSingleResponse(object):
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
        'data': 'FindingResourceObject'
    }

    attribute_map = {
        'data': 'data'
    }

    def __init__(self, data=None, local_vars_configuration=None):  # noqa: E501
        """FindingSingleResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._data = None
        self.discriminator = None

        if data is not None:
            self.data = data

    @property
    def data(self):
        """Gets the data of this FindingSingleResponse.  # noqa: E501


        :return: The data of this FindingSingleResponse.  # noqa: E501
        :rtype: FindingResourceObject
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this FindingSingleResponse.


        :param data: The data of this FindingSingleResponse.  # noqa: E501
        :type data: FindingResourceObject
        """

        self._data = data

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
        if not isinstance(other, FindingSingleResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FindingSingleResponse):
            return True

        return self.to_dict() != other.to_dict()
