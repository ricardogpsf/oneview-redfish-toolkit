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

# Python libs
import json
import unittest
from unittest import mock

# 3rd party libs
from flask import Flask
from flask import Response
from flask_api import status
from hpOneView.exceptions import HPOneViewException
from oneview_redfish_toolkit import util

# Module libs
from oneview_redfish_toolkit.api.redfish_error import RedfishError
from oneview_redfish_toolkit.blueprints import network_interface


class TestNetworkInterface(unittest.TestCase):
    """Tests for NetworkInterface blueprint"""

    @mock.patch.object(util, 'OneViewClient')
    def setUp(self, oneview_client_mockup):
        """Tests preparation"""

        # Load config on util
        util.load_config('redfish.conf')

        # creates a test client
        self.app = Flask(__name__)

        self.app.register_blueprint(network_interface.network_interface)

        @self.app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
        def internal_server_error(error):
            """Creates a Internal Server Error response"""

            redfish_error = RedfishError(
                "InternalError",
                "The request failed due to an internal service error.  "
                "The service is still operational.")
            redfish_error.add_extended_info("InternalError")
            error_str = redfish_error.serialize()
            return Response(
                response=error_str,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                mimetype="application/json")

        @self.app.errorhandler(status.HTTP_404_NOT_FOUND)
        def not_found(error):
            """Creates a Not Found Error response"""
            redfish_error = RedfishError(
                "GeneralError", error.description)
            error_str = redfish_error.serialize()
            return Response(
                response=error_str,
                status=status.HTTP_404_NOT_FOUND,
                mimetype='application/json')

        self.app = self.app.test_client()

        # propagate the exceptions to the test client
        self.app.testing = True

    @mock.patch.object(network_interface, 'g')
    def test_get_network_interface(self, g):
        """Tests NetworkInterfaceCollection"""

        # Loading server_hardware mockup value
        with open(
            'oneview_redfish_toolkit/mockups/oneview/ServerHardware.json'
        ) as f:
            server_hardware = json.load(f)

        # Loading NetworkInterfaceCollection mockup result
        with open(
            'oneview_redfish_toolkit/mockups/redfish/'
            'NetworkInterface3.json'
        ) as f:
            network_interface_mockup = json.load(f)

        # Create mock response
        g.oneview_client.server_hardware.get.return_value = server_hardware

        # Get NetworkInterfaceCollection
        response = self.app.get(
            "/redfish/v1/Systems/30303437-3034-4D32-3230-313133364752/"
            "NetworkInterfaces/3"
        )

        # Gets json from response
        result = json.loads(response.data.decode("utf-8"))

        # Tests response
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("application/json", response.mimetype)
        self.assertEqual(network_interface_mockup, result)

    @mock.patch.object(network_interface, 'g')
    def test_get_network_interface_invalid_id(self, g):
        """Tests NetworkInterfaceCollection"""

        # Loading server_hardware mockup value
        with open(
            'oneview_redfish_toolkit/mockups/oneview/ServerHardware.json'
        ) as f:
            server_hardware = json.load(f)

        # Create mock response
        g.oneview_client.server_hardware.get.return_value = server_hardware

        # Get NetworkInterfaceCollection
        response = self.app.get(
            "/redfish/v1/Systems/30303437-3034-4D32-3230-313133364752/"
            "NetworkInterfaces/invalid_id"
        )

        # Tests response
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual("application/json", response.mimetype)

    @mock.patch.object(network_interface, 'g')
    def test_get_network_interface_sh_not_found(
        self, g):
        """Tests NetworkInterface server hardware not found"""

        e = HPOneViewException({
            'errorCode': 'RESOURCE_NOT_FOUND',
            'message': 'server-hardware not found',
        })
        g.oneview_client.server_hardware.get.side_effect = e

        # Get NetworkInterfaceCollection
        response = self.app.get(
            "/redfish/v1/Systems/30303437-3034-4D32-3230-313133364752/"
            "NetworkInterfaces/3"
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual("application/json", response.mimetype)

    @mock.patch.object(network_interface, 'g')
    def test_get_network_interface_sh_exception(
        self, g):
        """Tests NetworkInterface unknown exception"""

        e = HPOneViewException({
            'errorCode': 'ANOTHER_ERROR',
            'message': 'server-hardware error',
        })
        g.oneview_client.server_hardware.get.side_effect = e

        # Get NetworkInterfaceCollection
        response = self.app.get(
            "/redfish/v1/Systems/30303437-3034-4D32-3230-313133364752/"
            "NetworkInterfaces/3"
        )

        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            response.status_code
        )
        self.assertEqual("application/json", response.mimetype)
