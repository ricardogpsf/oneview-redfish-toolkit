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

import collections
from oneview_redfish_toolkit.api.redfish_json_validator \
    import RedfishJsonValidator


class ComputerSystemCollection(RedfishJsonValidator):
    """Creates a Computer System Collection Redfish dict

        Populates self.redfish with some hardcoded ComputerSystemCollection
        values and with the response of Oneview with all server hardware.
    """

    SCHEMA_NAME = 'ComputerSystemCollection'

    def __init__(self, server_hardware):
        """ComputerSystemCollection constructor

            Populates self.redfish with a hardcoded ComputerSystemCollection
            values and with the response of Oneview with all server hardware.

            Args:
                server_hardware: A list of dicts of server hardware.
        """
        super().__init__(self.SCHEMA_NAME)

        self.server_hardware = server_hardware

        self.redfish["@odata.type"] = \
            "#ComputerSystemCollection.ComputerSystemCollection"
        self.redfish["Name"] = "Computer System Collection"
        self.redfish["Members@odata.count"] = len(server_hardware)
        self.redfish["Members"] = list()
        self._set_redfish_members()
        self.redfish["@odata.context"] = \
            "/redfish/v1/$metadata#ComputerSystemCollection" \
            ".ComputerSystemCollection"
        self.redfish["@odata.id"] = "/redfish/v1/Systems"
        self._validate()

    def _set_redfish_members(self):
        """Mounts the list of Redfish members

            Populates self.redfish["Members"] with the links to Redfish
            ComputerSystems.
        """
        for server_hardware, index in \
                zip(self.server_hardware,
                    range(len(self.server_hardware))):

            self.redfish["Members"].append(collections.OrderedDict())
            self.redfish["Members"][index]["@odata.id"] = \
                "/redfish/v1/Systems/" + server_hardware["uuid"]
