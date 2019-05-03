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

# FIXME!
# So, the open issue here is that when populating the 'running' tree,
# the nodes need to be the right cloas to interact with the server,
# implementing their configuration values.
#
# How do we know, when copying from saved/staged, what class to use?
#
# So, there's a function in the *server* which currently does this,
# switching on the full path of the node.
#
# This is a bit ugly.  Perhaps a solution with a decorator would be
# nicer?

import datetime
from .core import Object, Property, Node


class Manager:
    """Service management element, including config, status and control."""

    def __init__(self):
        """Constructor."""

        self._root = Object('')

        config = Object('config')
        self._root.add_child(config)

        config.add_child(Object('running'))
        config.add_child(Object('saved'))
        config.add_child(Object('staged'))

        self._root.add_child(Object('status'))
        return

    def get_node(self, name: str):
        """Return a node reference by name.

        :param name: Full path to node."""

        names = name.split('.')

        current = self._root
        while names:
            current = current.get_child(names[0])
            if not current:
                raise NameError("Lookup failed: %s" % names[0])
            names.pop(0)

        return current

    def load(self, url: str):
        """Load values of nodes from specified storage.

        :param url: Configuration storage URL."""

        self.restore_staged()
        self.restore_running()
        return

    def prune_saved(self, cutoff: datetime.datetime):
        """Delete saved trees older than 'cutoff'.

        :param cutoff: Discard saved trees older than this."""
        pass

    def save_running(self):
        """Persist running configuration."""

        now = datetime.datetime.utcnow()
        name = now.strftime('%Y-%m-%dT%H:%M:%S.') + "%06u" % now.microsecond

        saved = self.get_node('config.saved')
        saved.add_child(Object(name))

        return self.copy('running', 'saved.' + name)

    def restore_running(self, savepoint: str = None):
        """Load a previously-saved configuration to running.

        :param savepoint: Timestamp name of configuration to restore."""
        if not savepoint:
            savepoint = 'current'
        return self.copy(savepoint, 'running')

    def save_staged(self):
        """Persist staged configuration."""
        return self.copy('staged', 'saved.staged')

    def restore_staged(self):
        """Load the persisted staged configuration."""
        return self.copy('saved.staged', 'staged')

    def deploy_staged(self):
        """Copy staged configuration to running."""
        return self.copy('staged', 'running')

    def save_to_staged(self, name: str = None):
        """Copy specified configuration to staged.

        :param name: Root node from which to copy."""
        if not name:
            name = 'running'
        return self.copy(name, 'staged')

    def copy(self, source: str, dest: str):
        """Deep copy tree.

        :param source: Source tree root node name.
        :param dest: Destination tree root node name."""

        src = self.get_node(source)
        dst = self.get_node(dest)

        # Deep copy source to destination.
        for child in src.values():
            self._copy(child, dst)

        return dest

    def _copy(self, src: Node, dst_parent: Object):
        """(Internal) Copying helper function."""

        if src.is_leaf():
            leaf = dst_parent.add_child(Property(src.get_name(), dst_parent))
            leaf.set(src.get())

        else:
            c = dst_parent.add_child(Object(src.get_name(), dst_parent))
            for child in src.values():
                self._copy(child, c)