# -*- coding: utf-8 -*-

# Copyright (2017) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
    Tests for subscription_collection.py
"""

import json

from oneview_redfish_toolkit.api.subscription_collection \
    import SubscriptionCollection
from oneview_redfish_toolkit import util

import unittest
from unittest import mock


class TestSubscriptionCollection(unittest.TestCase):
    """Tests for SubscriptionCollection class"""

    @mock.patch.object(util, 'OneViewClient')
    def setUp(self, mock_ov):
        """Tests preparation"""

        # Loading variable in util module
        util.load_config('redfish.conf')

        # Loading SubscriptionCollection result mockup
        with open(
            'oneview_redfish_toolkit/mockups/redfish/'
            'SubscriptionCollection.json'
        ) as f:
            self.subscription_collection_mockup = json.load(f)

    def test_class_instantiation(self):
        # Tests if class is correctly instantiated and validated

        try:
            subscription = SubscriptionCollection({})
        except Exception as e:
            self.fail("Failed to instantiate SubscriptionCollection class."
                      " Error: {}".format(e))
        self.assertIsInstance(subscription, SubscriptionCollection)

    def test_serialize(self):
        # Tests the serialize function result against known result

        try:
            subscription_collection = SubscriptionCollection({})
        except Exception as e:
            self.fail("Failed to instantiate SubscriptionCollection class."
                      " Error: {}".format(e))

        try:
            result = json.loads(subscription_collection.serialize())
        except Exception as e:
            self.fail("Failed to serialize. Error: ".format(e))

        self.assertEqual(self.subscription_collection_mockup, result)
