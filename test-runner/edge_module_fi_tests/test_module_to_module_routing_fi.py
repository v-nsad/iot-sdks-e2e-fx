# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import pytest
import connections
import asyncio
from edgehub_control import connect_edgehub, disconnect_edgehub, restart_edgehub
from horton_settings import settings

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="module", autouse=True)
def set_channels(request):
    global friend_to_test_output
    global test_to_friend_input
    friend_to_test_output = "to" + settings.test_module.module_id
    test_to_friend_input = "from" + settings.test_module.module_id


friend_to_test_output = None
friend_to_test_input = "fromFriend"

test_to_friend_output = "toFriend"
test_to_friend_input = None

receive_timeout = 60


@pytest.mark.callsSendOutputEvent
async def test_module_to_friend_routing(sample_payload):
    payload = sample_payload()
    test_client = connections.connect_test_module_client()
    friend_client = connections.connect_friend_module_client()
    await friend_client.enable_input_messages()

    friend_input_future = asyncio.ensure_future(
        friend_client.wait_for_input_event(test_to_friend_input)
    )

    await test_client.send_output_event(test_to_friend_output, payload)

    received_message = await friend_input_future
    assert received_message == payload

    friend_client.disconnect_sync()
    test_client.disconnect_sync()


@pytest.mark.testgroup_edgehub_fault_injection
@pytest.mark.receivesInputMessages
async def test_friend_to_module_routing_fi(sample_payload):
    payload = sample_payload()

    test_client = connections.connect_test_module_client()
    await test_client.enable_input_messages()
    friend_client = connections.connect_friend_module_client()

    test_input_future = asyncio.ensure_future(
        test_client.wait_for_input_event(friend_to_test_input)
    )

    await friend_client.send_output_event(friend_to_test_output, payload)

    received_message = await test_input_future
    assert received_message == payload

    friend_client.disconnect_sync()
    test_client.disconnect_sync()
