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
class MacGenerateRequestEx(object):
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
        'key': 'SobjectDescriptor',
        'alg': 'DigestAlgorithm',
        'data': 'bytearray'
    }

    attribute_map = {
        'key': 'key',
        'alg': 'alg',
        'data': 'data'
    }

    def __init__(self, key=None, alg=None, data=None):
        """
        MacGenerateRequestEx - a model defined in Swagger
        """

        self._key = None
        self._alg = None
        self._data = None

        self.key = key
        if alg is not None:
          self.alg = alg
        self.data = data

    @property
    def key(self):
        """
        Gets the key of this MacGenerateRequestEx.

        Type: L{SobjectDescriptor}
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this MacGenerateRequestEx.
        """

        self._key = key

    @property
    def alg(self):
        """
        Gets the alg of this MacGenerateRequestEx.

        Type: L{DigestAlgorithm}
        """
        return self._alg

    @alg.setter
    def alg(self, alg):
        """
        Sets the alg of this MacGenerateRequestEx.
        """

        self._alg = alg

    @property
    def data(self):
        """
        Gets the data of this MacGenerateRequestEx.
        Data to compute the MAC of.

        Type: L{bytearray}
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        Sets the data of this MacGenerateRequestEx.
        Data to compute the MAC of.
        """

        if not isinstance(data, bytearray):
            raise ValueError("Invalid value for `data`, `data` must be a bytearray")
        self._data = data

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
        if not isinstance(other, MacGenerateRequestEx):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

