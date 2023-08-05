# coding: utf-8

"""
    Fortanix SDKMS REST API

    This is a set of REST APIs for accessing the Fortanix Self-Defending Key Management System. This includes APIs for managing accounts, and for performing cryptographic and key management operations. 

    OpenAPI spec version: 1.0.0-20200608
    Contact: support@fortanix.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""


from pprint import pformat
from six import iteritems
import re




# NOTE: This class is auto generated by the swagger code generator program.
# Do not edit the class manually.
class SobjectDescriptor(object):
    """
    @undocumented: swagger_types
    @undocumented: attribute_map
    @undocumented: to_dict
    @undocumented: to_str
    @undocumented: __repr__
    @undocumented: __eq__
    @undocumented: __ne__
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'kid': 'str',
        'name': 'str',
        'transient_key': 'str'
    }

    attribute_map = {
        'kid': 'kid',
        'name': 'name',
        'transient_key': 'transient_key'
    }

    def __init__(self, kid=None, name=None, transient_key=None):
        """
        SobjectDescriptor - a model defined in Swagger
        """

        self._kid = None
        self._name = None
        self._transient_key = None

        if kid is not None:
          self.kid = kid
        if name is not None:
          self.name = name
        if transient_key is not None:
          self.transient_key = transient_key

    @property
    def kid(self):
        """
        Gets the kid of this SobjectDescriptor.
        Key ID uniquely identifying this persisted security object.

        Type: L{str}
        """
        return self._kid

    @kid.setter
    def kid(self, kid):
        """
        Sets the kid of this SobjectDescriptor.
        Key ID uniquely identifying this persisted security object.
        """

        self._kid = kid

    @property
    def name(self):
        """
        Gets the name of this SobjectDescriptor.
        Name of this persisted security object.

        Type: L{str}
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this SobjectDescriptor.
        Name of this persisted security object.
        """

        self._name = name

    @property
    def transient_key(self):
        """
        Gets the transient_key of this SobjectDescriptor.
        Transient key blob.

        Type: L{str}
        """
        return self._transient_key

    @transient_key.setter
    def transient_key(self, transient_key):
        """
        Sets the transient_key of this SobjectDescriptor.
        Transient key blob.
        """

        self._transient_key = transient_key

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
        if not isinstance(other, SobjectDescriptor):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

