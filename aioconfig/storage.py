# -*- coding: utf-8 -*-
########################################################################
# aioconfig
# Copyright (C) 2019, David Arnold.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
########################################################################

# Provider registry.
STORAGE_ADAPTORS = {}


class StorageAdaptor:
    """Base class for configuration adaptors."""

    def __init__(self, server_id: str, url: str):
        """Constructor.

        :param server_id: Server instance identifier.
        :param url: Configuration store URL."""

        self._server_id = server_id
        self._url = url
        return


def register_storage_adaptor(scheme: str, cls):
    """Register a configuration adaptor implementation.

    :param scheme: URL scheme for this adaptor.
    :param cls: Adaptor implementation class reference."""

    if scheme in STORAGE_ADAPTORS:
        raise KeyError("Adaptor scheme %s already registered" % scheme)

    STORAGE_ADAPTORS[scheme] = cls
    return


def create_storage_adaptor(server_id: str, url: str) -> StorageAdaptor:
    """Create a storage adaptor instance.

    :param server_id: Server instance identifier.
    :param url: Configuration store URL."""

    scheme = url[:url.find(':')]
    cls = STORAGE_ADAPTORS.get(scheme)
    if cls is None:
        raise KeyError("No implementation for scheme %s" % scheme)

    config = cls(server_id, url)
    return config