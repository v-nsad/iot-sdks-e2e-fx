# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.
import logging
import subprocess
from azure.iot.device import IoTHubModuleClient

logger = logging.getLogger(__name__)

do_async = False

all_disconnect_types = ["DROP", "REJECT"]
mqtt_port = 8883
mqttws_port = 443
uninitialized = "uninitialized"
sudo_prefix = uninitialized


def log_message(msg):
    if isinstance(msg, dict) and "message" in msg:
        print(msg["message"])
    else:
        print(str(msg))


def set_flags(flags):
    global do_async
    logger.info("setting flags to {}".format(flags))
    if "test_async" in flags and flags["test_async"]:
        do_async = True


def get_capabilities():
    # TODO: Once the method invoke is pulled into master for the python sdk, we should remove
    # the logic for checking invoke_method on the moduleClient.
    caps = {
        "flags": {
            "supports_async": True,
            "security_messages": True,
            "v2_connect_group": True,
            "dropped_connection_tests": True,
            "net_control_app": True,
        },
        "skip_list": [],
    }
    if not getattr(IoTHubModuleClient, "invoke_method", None):
        caps["skip_list"].append("invokesModuleMethodCalls")
        caps["skip_list"].append("invokesDeviceMethodCalls")
    return caps
