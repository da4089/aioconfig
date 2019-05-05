aioconfig
=========

This package provides a set of classes that can be used to implement a
configuration and control system for server processes.

Features
--------

* Configuration information stored in a tree structure
* Tree root structure standardised
* Running, staged, and saved configurations

  * Runtime changes to running configuration supported
  * Saving running config creates persistent snapshot
  * Revert to saved, or apply staged configuration at runtime
* Pluggable persistence modules

  * Postgres
  * MongoDB
  * Sqlite
  * Files
* Pluggable access modules

  * REST (JSON over HTTPS)
  * telnet
* Access modules use `asyncio`, so module can be added to server code
  with minimal impact

How it Works
------------

Service functionality should be enclosed in a top-level class.  That
class should have accessor methods to configure and manage the service:
getting and setting properties, creating and destroying managed objects.

The main function for the service should create instances of both the
service class, and the Manager class from this package.  The manager's
constructor takes a URL, giving both the scheme and location of the
service's persisted configuration data.

The manager uses that persisted data to configure the service via
its accessor functions.  Using the manager's (optional) access APIs,
the service's configuration and state can be monitored, controlled, and
updated at runtime.

Configuration can be persisted in flat files, Sqlite, PostgreSQL, or
MongoDB.  And access can be via REST or telnet (or both).

A configuration staging area is supported, so that complex changes can
be assembled and checked prior to being applied.  And when the running
configuration is saved, the previous saved configuration is retained,
so the change can be rolled back, and historical comparisons made at any
time.

