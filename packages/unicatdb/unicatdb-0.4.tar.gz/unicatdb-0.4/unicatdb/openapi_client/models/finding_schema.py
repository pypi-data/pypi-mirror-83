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


class FindingSchema(object):
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
        'name': 'str',
        'color': 'str',
        'map_icon': 'str',
        'map_polygon_icon': 'str',
        'definition_groups': 'list[FindingSchemaDefinitionGroup]',
        'taxonomy_tree': 'TaxonomyTree'
    }

    attribute_map = {
        'name': 'name',
        'color': 'color',
        'map_icon': 'mapIcon',
        'map_polygon_icon': 'mapPolygonIcon',
        'definition_groups': 'definitionGroups',
        'taxonomy_tree': 'taxonomyTree'
    }

    def __init__(self, name=None, color=None, map_icon=None, map_polygon_icon=None, definition_groups=None, taxonomy_tree=None, local_vars_configuration=None):  # noqa: E501
        """FindingSchema - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._color = None
        self._map_icon = None
        self._map_polygon_icon = None
        self._definition_groups = None
        self._taxonomy_tree = None
        self.discriminator = None

        self.name = name
        self.color = color
        self.map_icon = map_icon
        self.map_polygon_icon = map_polygon_icon
        if definition_groups is not None:
            self.definition_groups = definition_groups
        if taxonomy_tree is not None:
            self.taxonomy_tree = taxonomy_tree

    @property
    def name(self):
        """Gets the name of this FindingSchema.  # noqa: E501


        :return: The name of this FindingSchema.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this FindingSchema.


        :param name: The name of this FindingSchema.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def color(self):
        """Gets the color of this FindingSchema.  # noqa: E501


        :return: The color of this FindingSchema.  # noqa: E501
        :rtype: str
        """
        return self._color

    @color.setter
    def color(self, color):
        """Sets the color of this FindingSchema.


        :param color: The color of this FindingSchema.  # noqa: E501
        :type color: str
        """
        if self.local_vars_configuration.client_side_validation and color is None:  # noqa: E501
            raise ValueError("Invalid value for `color`, must not be `None`")  # noqa: E501

        self._color = color

    @property
    def map_icon(self):
        """Gets the map_icon of this FindingSchema.  # noqa: E501


        :return: The map_icon of this FindingSchema.  # noqa: E501
        :rtype: str
        """
        return self._map_icon

    @map_icon.setter
    def map_icon(self, map_icon):
        """Sets the map_icon of this FindingSchema.


        :param map_icon: The map_icon of this FindingSchema.  # noqa: E501
        :type map_icon: str
        """
        if self.local_vars_configuration.client_side_validation and map_icon is None:  # noqa: E501
            raise ValueError("Invalid value for `map_icon`, must not be `None`")  # noqa: E501

        self._map_icon = map_icon

    @property
    def map_polygon_icon(self):
        """Gets the map_polygon_icon of this FindingSchema.  # noqa: E501


        :return: The map_polygon_icon of this FindingSchema.  # noqa: E501
        :rtype: str
        """
        return self._map_polygon_icon

    @map_polygon_icon.setter
    def map_polygon_icon(self, map_polygon_icon):
        """Sets the map_polygon_icon of this FindingSchema.


        :param map_polygon_icon: The map_polygon_icon of this FindingSchema.  # noqa: E501
        :type map_polygon_icon: str
        """
        if self.local_vars_configuration.client_side_validation and map_polygon_icon is None:  # noqa: E501
            raise ValueError("Invalid value for `map_polygon_icon`, must not be `None`")  # noqa: E501

        self._map_polygon_icon = map_polygon_icon

    @property
    def definition_groups(self):
        """Gets the definition_groups of this FindingSchema.  # noqa: E501


        :return: The definition_groups of this FindingSchema.  # noqa: E501
        :rtype: list[FindingSchemaDefinitionGroup]
        """
        return self._definition_groups

    @definition_groups.setter
    def definition_groups(self, definition_groups):
        """Sets the definition_groups of this FindingSchema.


        :param definition_groups: The definition_groups of this FindingSchema.  # noqa: E501
        :type definition_groups: list[FindingSchemaDefinitionGroup]
        """

        self._definition_groups = definition_groups

    @property
    def taxonomy_tree(self):
        """Gets the taxonomy_tree of this FindingSchema.  # noqa: E501


        :return: The taxonomy_tree of this FindingSchema.  # noqa: E501
        :rtype: TaxonomyTree
        """
        return self._taxonomy_tree

    @taxonomy_tree.setter
    def taxonomy_tree(self, taxonomy_tree):
        """Sets the taxonomy_tree of this FindingSchema.


        :param taxonomy_tree: The taxonomy_tree of this FindingSchema.  # noqa: E501
        :type taxonomy_tree: TaxonomyTree
        """

        self._taxonomy_tree = taxonomy_tree

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
        if not isinstance(other, FindingSchema):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FindingSchema):
            return True

        return self.to_dict() != other.to_dict()
