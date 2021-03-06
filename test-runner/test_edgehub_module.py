# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import pytest
from timeouts import timeouts
from base_client_tests import BaseClientTests
from telemetry_tests import TelemetryTests
from twin_tests import TwinTests
from input_output_tests import InputOutputTests
from method_tests import (
    ReceiveMethodCallFromServiceTests,
    ReceiveMethodCallFromModuleTests,
    InvokeMethodCallOnModuleTests,
    InvokeMethodCallOnLeafDeviceTests,
)
import dropped_connection_tests
import drop_scenario

pytestmark = pytest.mark.asyncio


class EdgeHubModuleClient(object):
    @pytest.fixture
    def client(self, test_module):
        return test_module


@pytest.mark.testgroup_edgehub_module_client
@pytest.mark.describe("EdgeHub ModuleClient")
@pytest.mark.timeout(timeouts.generic_test_timeout)
class TestEdgeHubModuleClient(
    EdgeHubModuleClient,
    BaseClientTests,
    TelemetryTests,
    TwinTests,
    InputOutputTests,
    ReceiveMethodCallFromServiceTests,
    ReceiveMethodCallFromModuleTests,
    InvokeMethodCallOnModuleTests,
    InvokeMethodCallOnLeafDeviceTests,
):
    pass


@pytest.mark.describe(
    "EdgeHub ModuleClient dropped connections - network glitched and client still connected"
)
@pytest.mark.testgroup_edgehub_module_quick_drop
@pytest.mark.testgroup_edgehub_module_full_drop
@pytest.mark.timeout(timeouts.dropped_connection_test_timeout)
class TestEdgeHubModuleNetworkGlitchClientConnected(
    EdgeHubModuleClient,
    drop_scenario.NetworkGlitchClientConnected,
    dropped_connection_tests.DroppedConnectionEdgeHubModuleTests,
):
    pass


@pytest.mark.describe(
    "EdgeHub ModuleClient dropped connections - network glitched and client disconencted"
)
@pytest.mark.testgroup_edgehub_module_full_drop
@pytest.mark.timeout(timeouts.dropped_connection_test_timeout)
class TestEdgeHubModuleNetworkGlitchClientDisconnected(
    EdgeHubModuleClient,
    drop_scenario.NetworkGlitchClientDisconnected,
    dropped_connection_tests.DroppedConnectionEdgeHubModuleTests,
):
    pass


@pytest.mark.describe(
    "EdgeHub ModuleClient dropped connections - network dropped and client disconencted"
)
@pytest.mark.testgroup_edgehub_module_full_drop
@pytest.mark.timeout(timeouts.dropped_connection_test_timeout)
class TestEdgeHubModuleNetworkDroppedClientDisconnected(
    EdgeHubModuleClient,
    drop_scenario.NetworkDroppedClientDisconnected,
    dropped_connection_tests.DroppedConnectionEdgeHubModuleTests,
):
    pass
