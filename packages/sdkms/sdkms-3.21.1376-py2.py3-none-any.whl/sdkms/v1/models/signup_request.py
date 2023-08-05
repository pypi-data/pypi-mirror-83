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
class SignupRequest(object):
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
        'user_email': 'str',
        'user_password': 'str',
        'first_name': 'str',
        'last_name': 'str',
        'recaptcha_response': 'str'
    }

    attribute_map = {
        'user_email': 'user_email',
        'user_password': 'user_password',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'recaptcha_response': 'recaptcha_response'
    }

    def __init__(self, user_email=None, user_password=None, first_name=None, last_name=None, recaptcha_response=None):
        """
        SignupRequest - a model defined in Swagger
        """

        self._user_email = None
        self._user_password = None
        self._first_name = None
        self._last_name = None
        self._recaptcha_response = None

        self.user_email = user_email
        self.user_password = user_password
        if first_name is not None:
          self.first_name = first_name
        if last_name is not None:
          self.last_name = last_name
        self.recaptcha_response = recaptcha_response

    @property
    def user_email(self):
        """
        Gets the user_email of this SignupRequest.
        User's email address.

        Type: L{str}
        """
        return self._user_email

    @user_email.setter
    def user_email(self, user_email):
        """
        Sets the user_email of this SignupRequest.
        User's email address.
        """

        self._user_email = user_email

    @property
    def user_password(self):
        """
        Gets the user_password of this SignupRequest.
        The password to assign to this user in SDKMS.

        Type: L{str}
        """
        return self._user_password

    @user_password.setter
    def user_password(self, user_password):
        """
        Sets the user_password of this SignupRequest.
        The password to assign to this user in SDKMS.
        """

        self._user_password = user_password

    @property
    def first_name(self):
        """
        Gets the first_name of this SignupRequest.

        Type: L{str}
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """
        Sets the first_name of this SignupRequest.
        """

        self._first_name = first_name

    @property
    def last_name(self):
        """
        Gets the last_name of this SignupRequest.

        Type: L{str}
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """
        Sets the last_name of this SignupRequest.
        """

        self._last_name = last_name

    @property
    def recaptcha_response(self):
        """
        Gets the recaptcha_response of this SignupRequest.

        Type: L{str}
        """
        return self._recaptcha_response

    @recaptcha_response.setter
    def recaptcha_response(self, recaptcha_response):
        """
        Sets the recaptcha_response of this SignupRequest.
        """

        self._recaptcha_response = recaptcha_response

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
        if not isinstance(other, SignupRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

