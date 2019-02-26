#!/usr/bin/env python

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import pytest
import random
import connections
from environment import runtime_config
from adapters import print_message as log_message
from edgehub_control import (
    edgeHub,
    disconnect_edgehub,
    connect_edgehub,
    restart_edgehub,
)
from time import sleep


@pytest.mark.timeout(180)
@pytest.mark.testgroup_edgehub_fault_injection
@pytest.mark.supportsTwin
def test_module_can_set_reported_properties_and_service_can_retrieve_them_fi():
    try:
        reported_properties_sent = {"foo": random.randint(1, 9999)}
        log_message("connecting module client")
        module_client = connections.connect_test_module_client()
        log_message("enabling twin")
        module_client.enable_twin()
        log_message("disabling edgehub")
        sleep(2)
        disconnect_edgehub()
        connect_edgehub()
        module_client.patch_twin(reported_properties_sent)
        sleep(2)
        log_message("patched twin")
        log_message("disconnecting module client")
        module_client.disconnect()
        log_message("module client disconnected")
        log_message("connecting registry client")
        registry_client = connections.connect_registry_client()
        log_message("disabling edgehub")
        sleep(2)
        disconnect_edgehub()
        connect_edgehub()
        sleep(2)
        log_message("reconnected edgehub")
        log_message("getting twin")
        twin_received = registry_client.get_module_twin(
            runtime_config.test_module.device_id, runtime_config.test_module.module_id
        )
        log_message("disconnecting registry client")
        registry_client.disconnect()
        log_message("registry client disconnected")

        reported_properties_received = twin_received["properties"]["reported"]
        if "$version" in reported_properties_received:
            del reported_properties_received["$version"]
        if "$metadata" in reported_properties_received:
            del reported_properties_received["$metadata"]
        log_message("expected:" + str(reported_properties_sent))
        log_message("received:" + str(reported_properties_received))

        assert reported_properties_sent == reported_properties_received
    finally:
        restart_edgehub()
        sleep(5)
