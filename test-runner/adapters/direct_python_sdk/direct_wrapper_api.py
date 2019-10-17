# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import internal_wrapper_glue
from ..abstract_wrapper_api import AbstractWrapperApi
from ..decorators import emulate_async


class WrapperApi(AbstractWrapperApi):
    def log_message_sync(self, message):
        internal_wrapper_glue.log_message(message)

    def cleanup_sync(self):
        pass

    def get_capabilities_sync(self):
        return internal_wrapper_glue.get_capabilities()

    def set_flags_sync(self, flags):
        internal_wrapper_glue.set_flags(flags)

    @emulate_async
    def network_disconnect(self, transport, disconnection_type):
        internal_wrapper_glue.network_disconnect(transport, disconnection_type)

    @emulate_async
    def network_reconnect(self):
        internal_wrapper_glue.network_reconnect()

    def network_reconnect_sync(self):
        internal_wrapper_glue.network_reconnect()
