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

import datetime
import json
import os
import sqlite3

from dateutil.parser import parse as parse_date
from typing import Optional

from .errors import BadStorageURLFormat, BadStorageURLScheme
from .storage import StorageAdaptor, register_storage_adaptor


# Stored as a single database table.  Each row contains a JSON-encoded
# configuration tree, the timestamp when it was saved, a flag indicating
# whether it has been archived, and its service identifier.

STAGED_TIME = '1970-01-01T00:00:00.000'
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S."

LOAD_CURRENT = "select settings " \
               "from config " \
               "where server_id = ?" \
               "  and archived = 0 " \
               "order by saved desc " \
               "limit 1"

LOAD_STAGED = "select settings " \
              "from config " \
              "where server_id = ? " \
              "  and archived = 0 " \
              "and saved = ? "

LOAD_SAVED = "select settings " \
             "from config " \
             "where server_id = ? " \
             "  and archived = 0 " \
             "  and saved = ?"

SAVE_CURRENT = "insert into config (server_id, saved, archived, settings) " \
               "values (?, ?, 0, ?)"

SAVE_STAGED = "insert into config (server_id, saved, archived, settings) " \
              "values (?, ?, 0, ?)"

LIST_SAVED = "select saved " \
             "from config " \
             "where server_id = ? " \
             "  and archived = 0 " \
             "  and saved != ? " \
             "order by saved desc"

ARCHIVE = "update config " \
          "set archived = 1 " \
          "where server_id = ?" \
          "  and saved < ? "


class SqliteStorageAdaptor(StorageAdaptor):
    """Sqlite3 storage adaptor."""

    @staticmethod
    def create(url: str):

        path = SqliteStorageAdaptor._get_path_from_url(url)

        # Check file doesn't exist.
        if os.path.exists(path):
            return

        # Connect (and implicitly create database).
        connection = sqlite3.connect(path)

        # Instantiate schema.
        query = \
            "create table config ( " \
            "    server_id text not null, " \
            "    saved timestamp not null, " \
            "    archived int not null default 0, " \
            "    settings text not null," \
            "    primary key (server_id, saved)" \
            ")"

        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        return

    def __init__(self, server_id: str, url: str):
        super().__init__(server_id, url)

        path = self._get_path_from_url(url)
        self._connection = sqlite3.connect(path)
        return

    def load_current(self) -> Optional[dict]:
        """Load current (latest) saved configuration."""

        cursor = self._connection.cursor()
        cursor.execute(LOAD_CURRENT, [self._server_id])
        row = cursor.fetchone()
        cursor.close()

        if not row:
            return

        return json.loads(row[0])

    def load_staged(self) -> Optional[dict]:
        """Load staged configuration."""

        cursor = self._connection.cursor()
        cursor.execute(LOAD_STAGED, [self._server_id, STAGED_TIME])
        row = cursor.fetchone()
        cursor.close()

        if not row:
            return

        return json.loads(row[0])

    def load_saved(self, name: datetime.datetime) -> Optional[dict]:
        """Load specified saved configuration.

        :param name: Timestamp to load."""

        str_name = SqliteStorageAdaptor._to_timestamp(name)
        cursor = self._connection.cursor()
        cursor.execute(LOAD_SAVED, [self._server_id, str_name])
        row = cursor.fetchone()
        cursor.close()

        if not row:
            return

        return json.loads(row[0])

    def save_current(self, config: dict):
        """Save config as running."""

        buf = json.dumps(config)
        now = self._now()

        cursor = self._connection.cursor()
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute(SAVE_CURRENT, [self._server_id, now, buf])
        cursor.execute("COMMIT")
        cursor.close()
        return

    def save_staged(self, config: dict):
        """Save config as staged."""

        buf = json.dumps(config)

        cursor = self._connection.cursor()
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute(SAVE_STAGED, [self._server_id, STAGED_TIME, buf])
        cursor.execute("COMMIT")
        cursor.close()
        return

    def list_saved(self) -> list:
        """List timestamps of all saved (un-archived) configurations."""

        cursor = self._connection.cursor()
        cursor.execute(LIST_SAVED, [self._server_id, STAGED_TIME])
        rows = cursor.fetchall()
        cursor.close()
        return [parse_date(row[0]) for row in rows]

    def archive(self, cutoff: datetime.datetime):
        """Flag as archived all configurations older than timestamp.

        :param cutoff: Cut-off timestamp."""

        cutoff_str = \
            cutoff.strftime(TIME_FORMAT) + \
            str(cutoff.microsecond / 1000)

        cursor = self._connection.cursor()
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute(ARCHIVE, [self._server_id, cutoff_str])
        cursor.execute("COMMIT")
        cursor.close()
        return

    @staticmethod
    def _now() -> str:
        return SqliteStorageAdaptor._to_timestamp(datetime.datetime.utcnow())

    @staticmethod
    def _to_timestamp(moment: datetime.datetime) -> str:
        return moment.strftime(TIME_FORMAT) + str(moment.microsecond // 1000)

    @staticmethod
    def _get_path_from_url(url: str) -> str:
        point = url.find('://')
        if point == -1:
            raise BadStorageURLFormat("Bad URL format: expecting "
                                      "'sqlite://filename', but got %s" % url)

        scheme = url[:point]
        if scheme != 'sqlite':
            raise BadStorageURLScheme("Bad URL scheme: expecting "
                                      "'sqlite', but got %s" % scheme)

        path = url[point + 3:]
        return path


register_storage_adaptor("sqlite3", SqliteStorageAdaptor)
