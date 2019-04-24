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


from .core import Container


class Manager:
    """Service management element, including config, status and control."""

    def __init__(self):
        """Constructor."""

        self._root = Container('')

        config = Container('config')
        self._root.add_child(config)

        config.add_child(Container('running'))
        config.add_child(Container('saved'))
        config.add_child(Container('staged'))

        self._root.add_child(Container('status'))
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
        pass

    def save_running(self):
        """Persist running configuration."""
        pass

    def load_saved(self):
        """Load a previously-saved configuration to running."""
        pass

    def load_staged(self):
        """Load the staged configuration to running."""
        pass

    def save_to_staged(self, name: str):
        """Copy specified configuration to staged.

        :param name: Root node from which to copy."""

