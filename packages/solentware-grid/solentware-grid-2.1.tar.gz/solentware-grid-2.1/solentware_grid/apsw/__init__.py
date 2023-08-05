# __init__.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide bsddb3 style cursor access to recordsets implemented on an Sqlite3
database using the apsw package available on PyPI.

Two points worth mention in comparison with the sqlite3 package are: cursors
have to be created explicitly, and transactions have to be started explicitly.

The implementation of recordsets follows the style used in the dpt3.0-dptdb
package available on PyPI.
"""
