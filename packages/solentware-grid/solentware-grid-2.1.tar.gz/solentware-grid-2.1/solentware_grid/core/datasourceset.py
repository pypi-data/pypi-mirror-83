# datasourceset.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module provides the DataSourceSet class to access a sequence of
recordsets.

A recordset holds all the selected records in the order they appear on the
database.  The sequence of recordsets allows the records to be presented in
arbitrary order.

An obvious use is to display records in some sorted order: the records for each
sorted value are presented in the order they appear in the database.

"""

from .dataclient import DataSource


class DataSourceSet(DataSource):
    
    """Provide bsddb3 style cursor access to a sequence of recordsets.
    """

    def __init__(self, dbhome, dbset, dbname, newrow=None):
        """Delegate to superclass then create an empty dictionary of recordsets
        indicating this datasource is not associated with any recordsets.

        """
        super(DataSourceSet, self).__init__(
            dbhome, dbset, dbname, newrow=newrow)

        self.key_sets = []
        self.recordsets = dict()
        
    def close(self):
        """Close resources."""
        self._clear_recordsets()
        
    def get_recordset(
        self,
        dbname,
        key=None,
        from_=None):
        """Create a recordset and add it to the dictionary of recorsets.

        dbname - index used to partition records
        key - find records with value key on dbname,
            when key=None find all records in from_
        from_: find records in record set from_ or record list from_,
            when from_=None find from all records in file.
        """
        if key is None:
            if from_ is None:
                return self._find_all_records()
            else:
                return self._in_recordset_find(dbname, from_)
        elif from_ is None:
            return self._find_field_equals_value(dbname, key)
        else:
            return self._in_recordset_field_equals_value(dbname, from_, key)

    def set_recordsets(
        self,
        dbname,
        partial_keys=None,
        constant_keys=None,
        include_without_constant_keys=False,
        population=None):
        """To be defined.

        dbname: index containing partial key values
        partial_keys: all combinations used as a partial key
        constant_keys: values added to each combintion
        include_without_constant_keys: all combinations without constant_keys
                                    added, as well, if True
        population: subset of records to partition by partial_keys.  Use all
                    records if None
        """
        # maybe method _position_identified_players_display_at_selection from
        # playergrids needs to be changed so fill_view can be called in this
        # method


    def _clear_recordsets(self):
        """Destroy all recordsets."""
        self.recordsets.clear()
        
