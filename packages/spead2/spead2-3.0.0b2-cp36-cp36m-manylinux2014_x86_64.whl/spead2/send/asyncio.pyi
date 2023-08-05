# Copyright 2019 National Research Foundation (SARAO)
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import socket
from typing import List, Optional, overload

import spead2
import spead2.send

from spead2 import _EndpointList

class _AsyncStream(spead2.send._Stream):
    @property
    def fd(self) -> int: ...
    def flush(self) -> None: ...
    def async_send_heap(self, heap: spead2.send.Heap, cnt: int = ...,
                        substream_index: int = ...,
                        *,
                        loop: Optional[asyncio.AbstractEventLoop] = None) -> asyncio.Future[int]: ...
    async def async_flush(self) -> None: ...

class UdpStream(spead2.send._UdpStream, _AsyncStream):
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 hostname: str, port: int,
                 config: spead2.send.StreamConfig,
                 buffer_size: int, socket: socket.socket,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 hostname: str, port: int,
                 config: spead2.send.StreamConfig = ...,
                 buffer_size: int = ..., interface_address: str = ...,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 hostname: str, port: int,
                 config: spead2.send.StreamConfig,
                 ttl: int,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 multicast_group: str, port: int,
                 config: spead2.send.StreamConfig,
                 ttl: int, interface_address: str,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 multicast_group: str, port: int,
                 config: spead2.send.StreamConfig,
                 ttl: int, interface_index: int,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 socket: socket.socket, hostname: str, port: int,
                 config: spead2.send.StreamConfig = ...,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...

    # Endpoint list variants
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 endpoints: _EndpointList,
                 config: spead2.send.StreamConfig,
                 buffer_size: int, socket: socket.socket,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 endpoints: _EndpointList,
                 config: spead2.send.StreamConfig = ...,
                 buffer_size: int = ..., interface_address: str = ...,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 endpoints: _EndpointList,
                 config: spead2.send.StreamConfig,
                 ttl: int,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 endpoints: _EndpointList,
                 config: spead2.send.StreamConfig,
                 ttl: int, interface_address: str,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 endpoints: _EndpointList,
                 config: spead2.send.StreamConfig,
                 ttl: int, interface_index: int,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 socket: socket.socket,
                 endpoints: _EndpointList,
                 config: spead2.send.StreamConfig = ...,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...

class UdpIbvStream(spead2.send._UdpIbvStream, _AsyncStream):
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 multicast_group: str, port: int,
                 config: spead2.send.StreamConfig,
                 interface_address: str,
                 buffer_size: int = ..., ttl: int = ...,
                 comp_vector: int = ..., max_pool: int = ...,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...

    @overload
    def __init__(self, thread_pool: spead2.ThreadPool,
                 endpoints: _EndpointList,
                 config: spead2.send.StreamConfig,
                 interface_address: str,
                 buffer_size: int = ..., ttl: int = ...,
                 comp_vector: int = ..., max_pool: int = ...,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...

class TcpStream(spead2.send._TcpStream, _AsyncStream):
    def __init__(self, thread_pool: spead2.ThreadPool, socket: socket.socket,
                 config: spead2.send.StreamConfig = ...,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
    @classmethod
    async def connect(self, thread_pool: spead2.ThreadPool,
                      hostname: str, port: int,
                      config: spead2.send.StreamConfig = ...,
                      buffer_size: int = ..., interface_address: str = ...,
                      *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...


class InprocStream(spead2.send._InprocStream, _AsyncStream):
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool, queue: spead2.InprocQueue,
                 config: spead2.send.StreamConfig = ...,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
    @overload
    def __init__(self, thread_pool: spead2.ThreadPool, queues: List[spead2.InprocQueue],
                 config: spead2.send.StreamConfig = ...,
                 *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None: ...
