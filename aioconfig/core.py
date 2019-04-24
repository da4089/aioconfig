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

from typing import Union


NodeType = Union['Container', 'Leaf']


class Container:
    """Base class for container nodes."""

    def __init__(self, name: str):
        """Constructor.

        :param name: Name for tree node."""
        self._name = name
        self._parent = None
        self._children = {}
        return

    @staticmethod
    def is_leaf() -> bool:
        """Return False for Container instances."""
        return False

    def get_name(self) -> str:
        """Return the name of this node."""
        return self._name

    def set_parent(self, parent: 'Container'):
        """Set the container for this node.

        :param parent: Reference to parent container."""
        self._parent = parent
        return

    def get_parent(self) -> 'Container':
        """Get the container for this node."""
        return self._parent

    def add_child(self, node: NodeType) -> NodeType:
        """Add a child to this node.

        :param node: Leaf or Container child node."""

        name = node.get_name()
        if name in self._children:
            raise KeyError("Child name already exists: %s" % name)

        self._children[name] = node
        return node

    def remove_child(self, name: str) -> NodeType:
        """Remove a child from this node.

        :param name: Name of child node.
        :returns: Reference to removed child node."""
        node = self._children.get(name)
        if not node:
            raise KeyError("No such child: %s" % name)

        del self._children[name]
        return node

    def has_child(self, name: str) -> bool:
        """Test whether named child exists.

        :param name: Name of child node.
        :returns: True if child exists, False otherwise."""

        return name in self._children

    def get_child(self, name: str) -> NodeType:
        """Return named child.

        :param name: Name of child node.
        :returns: Child node."""

        return self._children.get(name)

    def items(self):
        pass

    def keys(self):
        pass

    def values(self):
        pass


class Leaf:
    """Base class for leaf nodes."""

    def __init__(self, name: str, parent: Container):
        """Constructor.

        :param name: Name for tree node.
        :param parent: Reference to parent container."""
        self._name = name
        self._parent = parent
        return

    @staticmethod
    def is_leaf() -> bool:
        """Returns True for Leaf instances."""
        return True

    def get_name(self) -> str:
        """Return the name of this node."""
        return self._name

    def set_parent(self, parent: Container):
        """Set the container for this node.

        :param parent: Reference to parent container."""
        self._parent = parent
        return

    def get_parent(self) -> Container:
        """Get the container for this node."""
        return self._parent

    def set(self, value) -> object:
        """Set the value of this node.

        :param value: Value to be assigned to this node.
        :returns: 'value' if successful, otherwise None.

        A returned value of None indicates that this node's value may
        not be (over)written."""
        pass

    def get(self) -> object:
        """Get the value of this node.

        :returns: Node's value if successful, otherwise None.

        A returned value of None indicates that this node's value may
        not be read."""
        pass

    def delete(self):
        """Destroy this node."""
        pass
