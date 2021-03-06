# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.
from swagger_server.controllers import module_controller
from swagger_server.controllers import device_controller
import internal_control_glue


def log_message(msg):
    internal_control_glue.log_message(msg)


def cleanup_resources():
    module_controller.module_glue.cleanup_resources()
    device_controller.device_glue.cleanup_resources()


def set_flags(flags):
    internal_control_glue.set_flags(flags)


def get_capabilities():
    return internal_control_glue.get_capabilities()


def network_disconnect(transport, disconnect_type):
    print("wrapper disconnect")
    return internal_control_glue.network_disconnect(transport, disconnect_type)


def network_reconnect():
    return internal_control_glue.network_reconnect()
