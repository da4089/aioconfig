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

#from .manager import Manager


# Adaptor registry.
ACCESS_ADAPTORS = {}


class AccessAdaptor:
    def __init__(self, manager: 'Manager', url: str):
        """Constructor.

        :param manager: Reference to Manager to access.
        :param url: Access URL."""

        self._manager = manager
        self._url = url
        return

    async def start(self):
        pass

    async def stop(self):
        pass


def register_access_adaptor(scheme: str, cls):
    """Register a configuration access adaptor implementation.

    :param scheme: URL scheme for this adaptor.
    :param cls: Adaptor implementation class reference."""

    if scheme in ACCESS_ADAPTORS:
        raise KeyError("Adaptor scheme %s already registered" % scheme)

    ACCESS_ADAPTORS[scheme] = cls
    return


def create_access_adaptor(manager: 'Manager', url: str) -> AccessAdaptor:
    """Create an access adaptor instance.

    :param manager: Reference Manager instance.
    :param url: Adaptor URL."""

    scheme = url[:url.find(':')]
    cls = ACCESS_ADAPTORS.get(scheme)
    if cls is None:
        raise KeyError("No implementation for scheme %s" % scheme)

    adaptor = cls(manager, url)
    return adaptor
