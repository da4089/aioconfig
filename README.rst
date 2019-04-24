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
