# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from multiprocessing.pool import ThreadPool
from internal_device_glue import InternalDeviceGlue
from ..abstract_iothub_apis import AbstractDeviceApi
from .base_module_or_device_api import BaseModuleOrDeviceApi

device_object_list = []


class DeviceApi(BaseModuleOrDeviceApi, AbstractDeviceApi):
    def __init__(self):
        self.glue = InternalDeviceGlue()
        self.pool = ThreadPool()

    def connect_v1(self, transport, connection_string, ca_certificate):
        device_object_list.append(self)
        if "cert" in ca_certificate:
            cert = ca_certificate["cert"]
        else:
            cert = None
        self.glue.connect_v1(transport, connection_string, cert)

    def disconnect(self):
        if self in device_object_list:
            device_object_list.remove(self)

        self.glue.disconnect()
        self.glue = None

    def enable_c2d(self):
        self.glue.enable_c2d()

    def wait_for_c2d_message_async(self):
        return self.pool.apply_async(self.glue.wait_for_c2d_message)

    def get_connection_status(self):
        return self.glue.get_connection_status()

    def wait_for_connecction_status_change_async(self):
        return self.pool.apply_async(self.wait_for_connection_status_change)
