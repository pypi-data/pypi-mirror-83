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
class UserRequest(object):
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
        'account_role': 'list[UserAccountFlags]',
        'add_groups': 'UserGroupMap',
        'del_groups': 'UserGroupMap',
        'mod_groups': 'UserGroupMap',
        'enabled': 'bool',
        'add_u2f_devices': 'list[U2fAddDeviceRequest]',
        'del_u2f_devices': 'list[U2fDelDeviceRequest]',
        'rename_u2f_devices': 'list[U2fRenameDeviceRequest]'
    }

    attribute_map = {
        'user_email': 'user_email',
        'user_password': 'user_password',
        'account_role': 'account_role',
        'add_groups': 'add_groups',
        'del_groups': 'del_groups',
        'mod_groups': 'mod_groups',
        'enabled': 'enabled',
        'add_u2f_devices': 'add_u2f_devices',
        'del_u2f_devices': 'del_u2f_devices',
        'rename_u2f_devices': 'rename_u2f_devices'
    }

    def __init__(self, user_email=None, user_password=None, account_role=None, add_groups=None, del_groups=None, mod_groups=None, enabled=None, add_u2f_devices=None, del_u2f_devices=None, rename_u2f_devices=None):
        """
        UserRequest - a model defined in Swagger
        """

        self._user_email = None
        self._user_password = None
        self._account_role = None
        self._add_groups = None
        self._del_groups = None
        self._mod_groups = None
        self._enabled = None
        self._add_u2f_devices = None
        self._del_u2f_devices = None
        self._rename_u2f_devices = None

        self.user_email = user_email
        self.user_password = user_password
        if account_role is not None:
          self.account_role = account_role
        if add_groups is not None:
          self.add_groups = add_groups
        if del_groups is not None:
          self.del_groups = del_groups
        if mod_groups is not None:
          self.mod_groups = mod_groups
        if enabled is not None:
          self.enabled = enabled
        if add_u2f_devices is not None:
          self.add_u2f_devices = add_u2f_devices
        if del_u2f_devices is not None:
          self.del_u2f_devices = del_u2f_devices
        if rename_u2f_devices is not None:
          self.rename_u2f_devices = rename_u2f_devices

    @property
    def user_email(self):
        """
        Gets the user_email of this UserRequest.
        User's email address.

        Type: L{str}
        """
        return self._user_email

    @user_email.setter
    def user_email(self, user_email):
        """
        Sets the user_email of this UserRequest.
        User's email address.
        """

        self._user_email = user_email

    @property
    def user_password(self):
        """
        Gets the user_password of this UserRequest.
        The password to assign to this user in SDKMS.

        Type: L{str}
        """
        return self._user_password

    @user_password.setter
    def user_password(self, user_password):
        """
        Sets the user_password of this UserRequest.
        The password to assign to this user in SDKMS.
        """

        self._user_password = user_password

    @property
    def account_role(self):
        """
        Gets the account_role of this UserRequest.

        Type: list[L{UserAccountFlags}]
        """
        return self._account_role

    @account_role.setter
    def account_role(self, account_role):
        """
        Sets the account_role of this UserRequest.
        """

        self._account_role = account_role

    @property
    def add_groups(self):
        """
        Gets the add_groups of this UserRequest.
        The user will be added to the specified security groups with the specified roles.

        Type: L{UserGroupMap}
        """
        return self._add_groups

    @add_groups.setter
    def add_groups(self, add_groups):
        """
        Sets the add_groups of this UserRequest.
        The user will be added to the specified security groups with the specified roles.
        """

        self._add_groups = add_groups

    @property
    def del_groups(self):
        """
        Gets the del_groups of this UserRequest.
        The user will be removed from the specified security groups.

        Type: L{UserGroupMap}
        """
        return self._del_groups

    @del_groups.setter
    def del_groups(self, del_groups):
        """
        Sets the del_groups of this UserRequest.
        The user will be removed from the specified security groups.
        """

        self._del_groups = del_groups

    @property
    def mod_groups(self):
        """
        Gets the mod_groups of this UserRequest.
        The user's role in the specified groups will be updated to the specified roles.

        Type: L{UserGroupMap}
        """
        return self._mod_groups

    @mod_groups.setter
    def mod_groups(self, mod_groups):
        """
        Sets the mod_groups of this UserRequest.
        The user's role in the specified groups will be updated to the specified roles.
        """

        self._mod_groups = mod_groups

    @property
    def enabled(self):
        """
        Gets the enabled of this UserRequest.
        Whether this application is enabled.

        Type: L{bool}
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this UserRequest.
        Whether this application is enabled.
        """

        self._enabled = enabled

    @property
    def add_u2f_devices(self):
        """
        Gets the add_u2f_devices of this UserRequest.

        Type: list[L{U2fAddDeviceRequest}]
        """
        return self._add_u2f_devices

    @add_u2f_devices.setter
    def add_u2f_devices(self, add_u2f_devices):
        """
        Sets the add_u2f_devices of this UserRequest.
        """

        self._add_u2f_devices = add_u2f_devices

    @property
    def del_u2f_devices(self):
        """
        Gets the del_u2f_devices of this UserRequest.

        Type: list[L{U2fDelDeviceRequest}]
        """
        return self._del_u2f_devices

    @del_u2f_devices.setter
    def del_u2f_devices(self, del_u2f_devices):
        """
        Sets the del_u2f_devices of this UserRequest.
        """

        self._del_u2f_devices = del_u2f_devices

    @property
    def rename_u2f_devices(self):
        """
        Gets the rename_u2f_devices of this UserRequest.

        Type: list[L{U2fRenameDeviceRequest}]
        """
        return self._rename_u2f_devices

    @rename_u2f_devices.setter
    def rename_u2f_devices(self, rename_u2f_devices):
        """
        Sets the rename_u2f_devices of this UserRequest.
        """

        self._rename_u2f_devices = rename_u2f_devices

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
        if not isinstance(other, UserRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

