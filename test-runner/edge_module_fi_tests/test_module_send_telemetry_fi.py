# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import pytest
import connections
from edgehub_control import (
    edgeHub,
    disconnect_edgehub,
    connect_edgehub,
    restart_edgehub,
)

pytestmark = pytest.mark.asyncio

local_timeout = 60  # Seconds


@pytest.mark.testgroup_edgehub_fault_injection
@pytest.mark.callsSendEvent
@pytest.mark.timeout(
    timeout=180
)  # extra timeout in case eventhub needs to retry due to resource error
async def test_module_send_event_iothub_fi(
    test_object_stringified, test_object_stringified_2, logger, eventhub
):
    """ Sends event through Edge Hub to IoT Hub and validates the message is received using the Event Hub API.

    The module client is in the langauge being tested, and the eventhub client is directly connected to Azure to receive the event.
    """
    module_client = connections.connect_test_module_client()
    await eventhub.connect()
    await module_client.send_event(test_object_stringified)
    received_message = await eventhub.wait_for_next_event(
        module_client.device_id, expected=test_object_stringified
    )
    if not received_message:
        logger("Intial message not received")
        assert False
    disconnect_edgehub()  # DISCONNECT EDGEHUB
    module_client.send_event(test_object_stringified_2)  # do not await
    connect_edgehub()  # RECONNECT EDGEHUB
    received_message = await eventhub.wait_for_next_event(
        module_client.device_id, expected=test_object_stringified_2
    )
    if not received_message:
        logger("Second message not received")
        assert False
    module_client.disconnect_sync()
