# datasourcecursor.py
# Copyright 2019 Roger Marsh
# Licence: See LICENCE (BSD licence)

# Build this module like dptdatasource.py
# See use of CreateRecordList and DestroyRecordSet methods, whose analogues
# will be sibling methods of 'self.dbhome.get_table_connection(...)'
"""This module provides a cursor on a datasource's recordset.

"""

from .dataclient import DataSource


class DataSourceCursorError(Exception):
    pass


class DataSourceCursor(DataSource):
    
    """Provide bsddb3 style cursor access to recordset of arbitrary records.
    """

    def __init__(self, *a, **k):
        """Delegate to superclass then set the recordset attribute to None,
        indicating this datasource is not associated with a recordset.

        """
        super().__init__(*a, **k)

        self.recordset = None
        # Not sure if equivalent of this (from dptdatasource) is needed
        #self.dbhome.table[self.dbset]._sources[self] = None
        # which would imply that the close() method be transplanted as well.
        
    def get_cursor(self):
        """Create and return cursor on this datasource's recordset."""
        if self.recordset:
            if self.dbidentity == self.recordset._recordset.dbidentity:
                c = self.recordset.dbhome.create_recordset_cursor(
                    self.recordset._recordset)
            else:
                raise DataSourceCursorError(
                    'Recordset and DataSource are for different databases')
        else:
            self.recordset = self.dbhome.recordlist_nil(self.dbset)
            c = self.recordset.dbhome.create_recordset_cursor(
                self.recordset._recordset)
        return c

    def set_recordset(self, recordset):
        """Set recordset as this datasource's recordset if the recordset and
        this datasource are associated with the same database identity."""
        if self.recordset:
            if self.recordset.dbidentity == recordset._recordset.dbidentity:
                self.recordset._recordset.close()
                self.recordset = recordset
            else:
                raise DataSourceCursorError(
                    'New and existing Recordsets are for different databases')
        elif self.dbidentity == recordset._recordset.dbidentity:
            self.recordset = recordset
        else:
            raise DataSourceCursorError(
                'New Recordset and DataSource are for different databases')
