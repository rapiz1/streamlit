# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import ipaddress

from tornado.httputil import HTTPServerRequest
from tornado.web import HTTPError

from streamlit import config


class IpAllowlistMixin:
    _ip_ranges: List[Union[ipaddress.IPv4Network, ipaddress.IPv6Network]] = []

    @classmethod
    def initialize_ip_allowlist(cls) -> None:
        for subnet in config.get_option("server.ipAllowlist").split(","):
            if len(subnet):
                cls._ip_ranges.append(ipaddress.ip_network(subnet))

    def prepare(self) -> None:
        if len(self._ip_ranges) == 0:
            return
        client_ip = ipaddress.ip_address(self.request.remote_ip)
        for allowed_subnet in self._ip_ranges:
            if client_ip in allowed_subnet:
                return
        raise HTTPError(403)
