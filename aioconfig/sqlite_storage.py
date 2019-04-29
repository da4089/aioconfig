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

import sqlite3

from .errors import BadStorageURLFormat, BadStorageURLScheme
from .storage import StorageAdaptor


class SqliteStorageAdaptor(StorageAdaptor):
    """Sqlite3 storage adaptor."""

    def __init__(self, server_id: str, url: str):
        super().__init__(server_id, url)

        point = url.find('://')
        if point == -1:
            raise BadStorageURLFormat("Bad URL format: expecting "
                                      "'sqlite://filename', but got %s" % url)

        scheme = url[:point]
        if scheme != 'sqlite':
            raise BadStorageURLScheme("Bad URL scheme: expecting "
                                      "'sqlite', but got %s" % scheme)

        path = url[point + 3:]

        self._connection = sqlite3.connect(path)
        return
