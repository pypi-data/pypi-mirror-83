# callbackexception.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module provides a default CallbackException class for the datagrid
classes with four methods: report_exception, try_command, try_event, and
try_thread.

The 'try_' methods return the method argument and report_exception re-raises
the exception it was called to report.

Module solentware_misc.gui.exceptionhandler defines these four methods in the
ExceptionHandler class for use like 'class DG(ExceptionHandler, DataGrid)'.
"""


class CallbackException(object):
    """The CallbackException class provides dummy methods to report exceptions
    in a modal dialogue and 'do nothing' wrappers for tkinter callbacks and
    methods run in a separate thread.
    """

    def report_exception(self, root=None, title=None, message=None):
        """Re-raise the exception."""
        raise

    def try_command(self, method, widget):
        """Return the method."""
        return method

    def try_event(self, method):
        """Return the method."""
        return method

    def try_thread(self, method, widget):
        """Return the method."""
        return method

