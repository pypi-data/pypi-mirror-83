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
class App(object):
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
        'name': 'str',
        'app_id': 'str',
        'auth_type': 'AppAuthType',
        'description': 'str',
        'interface': 'str',
        'acct_id': 'str',
        'groups': 'list[str]',
        'default_group': 'str',
        'enabled': 'bool',
        'app_type': 'str',
        'creator': 'CreatorType',
        'created_at': 'str',
        'lastused_at': 'str',
        'oauth_config': 'AppOauthConfig',
        'cert_not_after': 'str'
    }

    attribute_map = {
        'name': 'name',
        'app_id': 'app_id',
        'auth_type': 'auth_type',
        'description': 'description',
        'interface': 'interface',
        'acct_id': 'acct_id',
        'groups': 'groups',
        'default_group': 'default_group',
        'enabled': 'enabled',
        'app_type': 'app_type',
        'creator': 'creator',
        'created_at': 'created_at',
        'lastused_at': 'lastused_at',
        'oauth_config': 'oauth_config',
        'cert_not_after': 'cert_not_after'
    }

    def __init__(self, name=None, app_id=None, auth_type=None, description=None, interface=None, acct_id=None, groups=None, default_group=None, enabled=None, app_type=None, creator=None, created_at=None, lastused_at=None, oauth_config=None, cert_not_after=None):
        """
        App - a model defined in Swagger
        """

        self._name = None
        self._app_id = None
        self._auth_type = None
        self._description = None
        self._interface = None
        self._acct_id = None
        self._groups = None
        self._default_group = None
        self._enabled = None
        self._app_type = None
        self._creator = None
        self._created_at = None
        self._lastused_at = None
        self._oauth_config = None
        self._cert_not_after = None

        self.name = name
        self.app_id = app_id
        self.auth_type = auth_type
        if description is not None:
          self.description = description
        if interface is not None:
          self.interface = interface
        self.acct_id = acct_id
        self.groups = groups
        self.default_group = default_group
        self.enabled = enabled
        self.app_type = app_type
        self.creator = creator
        self.created_at = created_at
        if lastused_at is not None:
          self.lastused_at = lastused_at
        if oauth_config is not None:
          self.oauth_config = oauth_config
        if cert_not_after is not None:
          self.cert_not_after = cert_not_after

    @property
    def name(self):
        """
        Gets the name of this App.
        Name of the application. Application names must be unique within an account.

        Type: L{str}
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this App.
        Name of the application. Application names must be unique within an account.
        """

        self._name = name

    @property
    def app_id(self):
        """
        Gets the app_id of this App.
        Application ID uniquely identifying this application.

        Type: L{str}
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id):
        """
        Sets the app_id of this App.
        Application ID uniquely identifying this application.
        """

        self._app_id = app_id

    @property
    def auth_type(self):
        """
        Gets the auth_type of this App.

        Type: L{AppAuthType}
        """
        return self._auth_type

    @auth_type.setter
    def auth_type(self, auth_type):
        """
        Sets the auth_type of this App.
        """

        self._auth_type = auth_type

    @property
    def description(self):
        """
        Gets the description of this App.
        Description of this application.

        Type: L{str}
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this App.
        Description of this application.
        """

        self._description = description

    @property
    def interface(self):
        """
        Gets the interface of this App.
        Interface used with this application (PKCS11, CNG, JCE, KMIP, etc.).

        Type: L{str}
        """
        return self._interface

    @interface.setter
    def interface(self, interface):
        """
        Sets the interface of this App.
        Interface used with this application (PKCS11, CNG, JCE, KMIP, etc.).
        """

        self._interface = interface

    @property
    def acct_id(self):
        """
        Gets the acct_id of this App.
        The account ID of the account that this application belongs to.

        Type: L{str}
        """
        return self._acct_id

    @acct_id.setter
    def acct_id(self, acct_id):
        """
        Sets the acct_id of this App.
        The account ID of the account that this application belongs to.
        """

        self._acct_id = acct_id

    @property
    def groups(self):
        """
        Gets the groups of this App.
        An array of Security Group IDs. The application belongs to each Security Group in this array.

        Type: list[L{str}]
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """
        Sets the groups of this App.
        An array of Security Group IDs. The application belongs to each Security Group in this array.
        """

        self._groups = groups

    @property
    def default_group(self):
        """
        Gets the default_group of this App.
        The default group of this application. This is the group where security objects will be created by default by this application.

        Type: L{str}
        """
        return self._default_group

    @default_group.setter
    def default_group(self, default_group):
        """
        Sets the default_group of this App.
        The default group of this application. This is the group where security objects will be created by default by this application.
        """

        self._default_group = default_group

    @property
    def enabled(self):
        """
        Gets the enabled of this App.
        Whether this application is enabled.

        Type: L{bool}
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this App.
        Whether this application is enabled.
        """

        self._enabled = enabled

    @property
    def app_type(self):
        """
        Gets the app_type of this App.
        The user-defined type of this application.

        Type: L{str}
        """
        return self._app_type

    @app_type.setter
    def app_type(self, app_type):
        """
        Sets the app_type of this App.
        The user-defined type of this application.
        """

        self._app_type = app_type

    @property
    def creator(self):
        """
        Gets the creator of this App.

        Type: L{CreatorType}
        """
        return self._creator

    @creator.setter
    def creator(self, creator):
        """
        Sets the creator of this App.
        """

        self._creator = creator

    @property
    def created_at(self):
        """
        Gets the created_at of this App.
        When this application was created.

        Type: L{str}
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this App.
        When this application was created.
        """

        self._created_at = created_at

    @property
    def lastused_at(self):
        """
        Gets the lastused_at of this App.
        When this application was last used.

        Type: L{str}
        """
        return self._lastused_at

    @lastused_at.setter
    def lastused_at(self, lastused_at):
        """
        Sets the lastused_at of this App.
        When this application was last used.
        """

        self._lastused_at = lastused_at

    @property
    def oauth_config(self):
        """
        Gets the oauth_config of this App.

        Type: L{AppOauthConfig}
        """
        return self._oauth_config

    @oauth_config.setter
    def oauth_config(self, oauth_config):
        """
        Sets the oauth_config of this App.
        """

        self._oauth_config = oauth_config

    @property
    def cert_not_after(self):
        """
        Gets the cert_not_after of this App.
        Certificate expiration date.

        Type: L{str}
        """
        return self._cert_not_after

    @cert_not_after.setter
    def cert_not_after(self, cert_not_after):
        """
        Sets the cert_not_after of this App.
        Certificate expiration date.
        """

        self._cert_not_after = cert_not_after

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
        if not isinstance(other, App):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

