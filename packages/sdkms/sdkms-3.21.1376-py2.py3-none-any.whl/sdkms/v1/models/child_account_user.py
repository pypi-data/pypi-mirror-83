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
class ChildAccountUser(object):
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
        'user_id': 'str',
        'user_email': 'str',
        'account_role': 'list[UserAccountFlags]',
        'groups': 'UserGroupMap',
        'created_at': 'str',
        'last_logged_in_at': 'str'
    }

    attribute_map = {
        'user_id': 'user_id',
        'user_email': 'user_email',
        'account_role': 'account_role',
        'groups': 'groups',
        'created_at': 'created_at',
        'last_logged_in_at': 'last_logged_in_at'
    }

    def __init__(self, user_id=None, user_email=None, account_role=None, groups=None, created_at=None, last_logged_in_at=None):
        """
        ChildAccountUser - a model defined in Swagger
        """

        self._user_id = None
        self._user_email = None
        self._account_role = None
        self._groups = None
        self._created_at = None
        self._last_logged_in_at = None

        self.user_id = user_id
        self.user_email = user_email
        if account_role is not None:
          self.account_role = account_role
        self.groups = groups
        if created_at is not None:
          self.created_at = created_at
        if last_logged_in_at is not None:
          self.last_logged_in_at = last_logged_in_at

    @property
    def user_id(self):
        """
        Gets the user_id of this ChildAccountUser.
        User ID uniquely identifying this user.

        Type: L{str}
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this ChildAccountUser.
        User ID uniquely identifying this user.
        """

        self._user_id = user_id

    @property
    def user_email(self):
        """
        Gets the user_email of this ChildAccountUser.
        The User's email address.

        Type: L{str}
        """
        return self._user_email

    @user_email.setter
    def user_email(self, user_email):
        """
        Sets the user_email of this ChildAccountUser.
        The User's email address.
        """

        self._user_email = user_email

    @property
    def account_role(self):
        """
        Gets the account_role of this ChildAccountUser.

        Type: list[L{UserAccountFlags}]
        """
        return self._account_role

    @account_role.setter
    def account_role(self, account_role):
        """
        Sets the account_role of this ChildAccountUser.
        """

        self._account_role = account_role

    @property
    def groups(self):
        """
        Gets the groups of this ChildAccountUser.

        Type: L{UserGroupMap}
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """
        Sets the groups of this ChildAccountUser.
        """

        self._groups = groups

    @property
    def created_at(self):
        """
        Gets the created_at of this ChildAccountUser.
        When this user was added to account.

        Type: L{str}
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this ChildAccountUser.
        When this user was added to account.
        """

        self._created_at = created_at

    @property
    def last_logged_in_at(self):
        """
        Gets the last_logged_in_at of this ChildAccountUser.
        When this user last logged in.

        Type: L{str}
        """
        return self._last_logged_in_at

    @last_logged_in_at.setter
    def last_logged_in_at(self, last_logged_in_at):
        """
        Sets the last_logged_in_at of this ChildAccountUser.
        When this user last logged in.
        """

        self._last_logged_in_at = last_logged_in_at

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
        if not isinstance(other, ChildAccountUser):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

