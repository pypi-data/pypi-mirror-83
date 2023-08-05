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


from __future__ import absolute_import

import os
import sys
import unittest

import sdkms/v1
from sdkms/v1.rest import ApiException
from sdkms/v1.apis.digest_api import DigestApi


class TestDigestApi(unittest.TestCase):
    """ DigestApi unit test stubs """

    def setUp(self):
        self.api = sdkms/v1.apis.digest_api.DigestApi()

    def tearDown(self):
        pass

    def test_compute_digest(self):
        """
        Test case for compute_digest

        Compute a message digest of data
        """
        pass

    def test_compute_mac(self):
        """
        Test case for compute_mac

        Compute MAC using a key
        """
        pass

    def test_compute_mac_ex(self):
        """
        Test case for compute_mac_ex

        Compute MAC using a key
        """
        pass

    def test_verify_mac(self):
        """
        Test case for verify_mac

        Verify MAC using a key
        """
        pass

    def test_verify_mac_ex(self):
        """
        Test case for verify_mac_ex

        Verify MAC using a key
        """
        pass


if __name__ == '__main__':
    unittest.main()
