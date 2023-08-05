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
from .base_list_object import BaseListObject

class BatchVerifyRequest(BaseListObject):
    """
    Array of Verify requests to be performed in batch 

    This class BatchVerifyRequest denotes list of VerifyRequestEx
    In python subclassing a list is not recommended, hence this class stores the list of VerifyRequestEx as its parameter.

    Initialize object: batch_verify_request = BatchVerifyRequest()
    Add object to BatchVerifyRequest object: batch_verify_request.append(VerifyRequestEx())
    Insert object to BatchVerifyRequest object at index: batch_verify_request.insert(1, VerifyRequestEx())
    Delete an object from BatchVerifyRequest object at index: batch_verify_request.remove(1)
    Get the list of VerifyRequestEx: list()

    This class serializes as a list of VerifyRequestEx.
    """

    inner_type = 'VerifyRequestEx'

    def __init__(self):
        self._list = []

    def __getitem__(self, item):
        return self._list.__getitem__(item)

    def append(self, element):
        self._list.append(element)

    def insert(self, index, element):
        self._list.insert(index, element)   

    def remove(self, index):
        self._list.remove(index)

    @property
    def list(self):
        return self._list

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self._list)
 
    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()



