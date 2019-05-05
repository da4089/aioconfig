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

from .storage import StorageAdaptor, create_storage_adaptor, register_storage_adaptor
from .core import List, Object, Property
from .manager import Manager
from .errors import *
from .access import AccessAdaptor, create_access_adaptor, register_access_adaptor

import aioconfig.sqlite_storage
import aioconfig.rest_access


# FIXME: import functools
FUNCS = {}


# FIXME
# The meat of this is a call to parent.add_child() with a node as a
# parameter.  Given the node, I can get its name.  Given the parent,
# I can get its path to root, and thus each ancestor node's name too.
# I can get the parent from the node itself also.
# So ... can I remove the need to include the path element name?


# The intention here is that getter functions on an object are decorated
# to record their path in the management tree.  This then records the
# *bound* method as the getter for the decorated path.
#
# When the path has asterisks embedded, it applies to all children of
# the enclosing container.  It might be that I want to distinguish
# between a dictionary container and a list container?  List containers
# apply the same properties to all elements, dictionaries don't.

def get(path: str):
    def register_getter_with_path(func):
        FUNCS[path] = func
        return func
    return register_getter_with_path


def set(path: str):
    def register_setter_with_path(func):
        FUNCS[path] = func
        return func
    return register_setter_with_path


def delete(path: str):
    def register_deleter_with_path(func):
        FUNCS[path] = func
        return func
    return register_deleter_with_path


def create_child(path: str):
    def register_creator_with_path(func):
        FUNCS[path] = func
        return func
    return register_creator_with_path


def create_element(path: str):
    def register_creator_with_path(func):
        FUNCS[path] = func
        return func
    return register_creator_with_path

def create_object(path: str):
    def register_creator_with_path(func):
        FUNCS[path] = func
        return func
    return register_creator_with_path

