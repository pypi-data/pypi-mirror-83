# __init__.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Provide bsddb3 style cursor access to recordsets implemented on a DPT
database using the dpt3.0-dptdb package available on PyPI.

Two points worth mention on transactions in DPT compared with Sqlite3 are:
transactions are started automatically, and transactions are committed by
default in the absence of exceptions.

The recordset idea used in DPT databases is followed in solentware_base, a
sibling of solentware_grid on www.solentware.co.uk.
"""
