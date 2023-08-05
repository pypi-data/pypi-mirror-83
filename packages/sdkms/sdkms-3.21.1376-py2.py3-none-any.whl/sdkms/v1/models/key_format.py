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

from .base_enum_object import BaseEnumObject

# NOTE: This class is auto generated by the swagger code generator program.
# Do not edit the class manually.
class KeyFormat(BaseEnumObject):
    """
    Desired key formatting

    Enumeration values::
        KeyFormat.DEFAULT = "Default"
        KeyFormat.PKCS8 = "Pkcs8"

    This class doesnt use python standard enumeration since they dont support unknown values. 
    
    This is an object of type BaseEnumObject and provides similar functionality as a String Enumeration.
    
    Get a standard instance of enum: KeyFormat.FOO or KeyFormat("FOO")
    Get non standard instance of enum: KeyFormat("BAR")
    Enum instance to String value: KeyFormat.FOO.value , KeyFormat.FOO.name (Gives "FOO")
    Equality: KeyFormat.FOO == KeyFormat("FOO") , KeyFormat.FOO != KeyFormat.BAR
    Provides str func:  str(KeyFormat.FOO) == "KeyFormat.FOO"
    
    Also the class maintains a static dict of values. hence KeyFormat.FOO and KeyFormat("FOO") are really backed by same data. 
    """
    
    """
    Inner class that stores the actual value
    """
    class __KeyFormat(BaseEnumObject):

        def __init__(self, value):
            self.__value = value

        @property
        def value(self):
            return self.__value

        @property
        def name(self):
            return self.__value

        def __str__(self):
            return "KeyFormat." + self.__value

    """
    allowed enum values
    """
    DEFAULT = __KeyFormat("Default")
    PKCS8 = __KeyFormat("Pkcs8")

    """
    dictionary that keeps the enum value mapping for static access
    """
    __VALUES = dict()
    __VALUES["Default"] = DEFAULT
    __VALUES["Pkcs8"] = PKCS8

    def __init__(self, name):
        if name in KeyFormat.__VALUES:
            self.__instance = KeyFormat.__VALUES[name]
        else:
            new_value = KeyFormat.__KeyFormat(name)
            KeyFormat.__VALUES[name] = new_value
            self.__instance = new_value

    @property
    def value(self):
        return self.__instance.value

    @property
    def name(self):
        return self.__instance.name

    def __str__(self):
        return "KeyFormat." + self.__instance.name

    """ 
    This is to ensure equals work for both static defined values and client defined ones.
    """
    def __eq__(self, other):
        if (isinstance(self, KeyFormat) or isinstance(self, KeyFormat.__KeyFormat)) and \
                (isinstance(other, KeyFormat) or isinstance(other, KeyFormat.__KeyFormat)):
                return self.value == other.value

        return False

    def __ne__(self, other):
        if (isinstance(self, KeyFormat) or isinstance(self, KeyFormat.__KeyFormat)) and \
                (isinstance(other, KeyFormat) or isinstance(other, KeyFormat.__KeyFormat)):
                return self.value != other.value

        return True


