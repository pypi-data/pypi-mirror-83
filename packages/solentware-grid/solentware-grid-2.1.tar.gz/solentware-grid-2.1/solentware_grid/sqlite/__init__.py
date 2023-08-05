# __init__.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide bsddb3 style cursor access to recordsets implemented on an Sqlite3
database using the sqlite3 package supplied in Python.

Two points worth mention in comparison with the apsw package are: the cursor
returned by sqlite3's execute() method is used, and transactions are started
automatically.

The implementation of recordsets follows the style used in the dpt3.0-dptdb
package available on PyPI.
"""
