# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import json
import docker
import pytest
import asyncio

import connections
from edgehub_control import (
    connect_edgehub,
    disconnect_edgehub,
    edgeHub,
    restart_edgehub,
)
from adapters import adapter_config

client = docker.from_env()

pytestmark = pytest.mark.asyncio

# How long do we have to wait after a module registers to receive
# method calls until we can actually call a method.
time_for_method_to_fully_register = 5

method_name = "test_method"
method_payload = '"Look at me, I\'ve got payload!"'
status_code = 221

method_invoke_parameters = {
    "methodName": method_name,
    "payload": method_payload,
    "responseTimeoutInSeconds": 15,
    "connectTimeoutInSeconds": 15,
}

method_response_body = {"response": "Look at me.  I'm a response!"}


async def do_device_method_call(
    source_module, destination_module, destination_device_id
):
    """
    Helper function which invokes a method call on one module and responds to it from another module
    """
    try:
        adapter_config.logger("enabling methods on the destination")
        await destination_module.enable_methods()

        # start listening for method calls on the destination side
        adapter_config.logger("starting to listen from destination module")
        receiver_future = asyncio.ensure_future(
            destination_module.wait_for_method_and_return_response(
                method_name, status_code, method_invoke_parameters, method_response_body
            )
        )
        await asyncio.sleep(time_for_method_to_fully_register)

        disconnect_edgehub()
        # invoking the call from caller side
        await asyncio.sleep(5)
        connect_edgehub()
        adapter_config.logger("invoking method call")
        response = await source_module.call_device_method(
            destination_device_id, method_invoke_parameters
        )
        adapter_config.logger("method call complete.  Response is:")
        adapter_config.logger(str(response))

        # wait for that response to arrive back at the source and verify that it's all good.
        adapter_config.logger("response = " + str(response) + "\n")
        assert response["status"] == status_code
        # edge bug: the response that edge returns is stringified.  The same response that comes back from an iothub service call is not stringified
        if isinstance(response["payload"], str):
            response["payload"] = json.loads(response["payload"])
        assert response["payload"] == method_response_body

        await receiver_future
    finally:
        connect_edgehub()
        restart_edgehub(hard=False)


"""
Test: device method from service to leaf device fi
invoke a method call from the service API and respond to it from the leaf device

"""


@pytest.mark.testgroup_edgehub_fault_injection
@pytest.mark.module_under_test_has_device_wrapper
async def test_device_method_from_service_to_leaf_device_fi():
    service_client = connections.connect_service_client()
    leaf_device_client = connections.connect_leaf_device_client()

    await do_device_method_call(
        service_client, leaf_device_client, leaf_device_client.device_id
    )

    service_client.disconnect_sync()
    leaf_device_client.disconnect_sync()


@pytest.mark.testgroup_edgehub_fault_injection
@pytest.mark.invokesDeviceMethodCalls
@pytest.mark.module_under_test_has_device_wrapper
async def test_device_method_from_module_to_leaf_device_fi():
    """
    invoke a method call from the test module and respond to it from the leaf device
    """

    module_client = connections.connect_test_module_client()
    leaf_device_client = connections.connect_leaf_device_client()

    await do_device_method_call(
        module_client, leaf_device_client, leaf_device_client.device_id
    )

    module_client.disconnect_sync()
    leaf_device_client.disconnect_sync()
