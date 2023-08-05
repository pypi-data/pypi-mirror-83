# datashow.py
# Copyright 2015 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module provide base classes for record display
dialogues.

"""

import tkinter

from ..core.dataclient import DataClient

# minimum_width and mininimum_height arguments for wm_minsize() calls
# maybe candidate arguments for DataControl.edit_dialog() calls elsewhere
minimum_width = 600
minimum_height = 200


class RecordShow(DataClient):
    
    """Show a database record.
    """

    def __init__(self, instance):
        """Delegate to superclass then set number of rows to 1.

        instance - the record to be displayed

        instance.newrecord is set None to indicate a record display.

        blockchange is set False to indicate deletion is allowed unless an
        update notification changes the situation.

        """
        super(RecordShow, self).__init__()
        self.rows = 1
        self.object = instance
        self.object.newrecord = None
        self.blockchange = False

    def on_data_change(self, instance):
        """Block record deletion if instance is record being deleted.

        instance - the updated record, which cannot be deleted by self

        Implication is that record has been modified separately and it is
        not correct to update based on the record as held in self.
        
        """
        if instance == self.object:
            self.blockchange = True
        

class DataShow(RecordShow):
    
    """A show record dialogue.
    """

    def __init__(self, instance, parent, oldview, title):
        """Delegate to superclass then create the dialogue.

        instance - passed to superclass as instance argument
        parent - parent widget for dialog
        oldview - widget displaying the record
        title - title for dialogue
        """
        super(DataShow, self).__init__(instance)
        self.parent = parent
        self.oldview = oldview
        parent.bind('<Destroy>', self.on_destroy)
        oldview.get_top_widget().pack(fill=tkinter.BOTH, expand=tkinter.TRUE)
        oldview.get_top_widget().pack_propagate(False)
        oldview.takefocus_widget.configure(takefocus=tkinter.TRUE)
        oldview.takefocus_widget.focus_set()
        parent.wm_title(title)
        parent.wm_minsize(width=minimum_width, height=minimum_height)
        self.status = tkinter.Label(parent)
        self.status.pack(side=tkinter.BOTTOM)
        self.buttons = tkinter.Frame(parent)
        self.buttons.pack(
            fill=tkinter.X,
            expand=tkinter.FALSE,
            side=tkinter.TOP)
        self.ok = tkinter.Button(
            master=self.buttons,
            text='Ok',
            command=self.try_command(self.dialog_on_ok, self.buttons))
        self.ok.pack(expand=tkinter.TRUE, side=tkinter.LEFT)
        
    def dialog_clear_error_markers(self):
        """Set status report to ''."""
        self.status.configure(text='')
        
    def dialog_status(self):
        """Return widget used to display status reports and error messages."""
        return self.status

    def on_data_change(self, instance):
        """Delegate to superclass then destroy dialogue if deleted."""
        super(DataShow, self).on_data_change(instance)
        if self.blockchange:
            if self.ok:
                self.ok.destroy()
                self.ok = None

    def dialog_ok(self):
        """Delete record and return show action response."""
        if self.datasource is not None:
            if self.datasource.dbhome.get_table_connection(
                self.datasource.dbset):
                return True
            else:
                if self.ok:
                    self.ok.destroy()
                    self.ok = None
                self.blockchange = True
                return False

    def dialog_on_ok(self):
        """Destroy dialogue"""
        self.dialog_clear_error_markers()
        if self.blockchange:
            self.ok.destroy()
            self.ok = None
            return
        dok = self.dialog_ok()
        self.parent.destroy()
        self.set_data_source()

    def ok_by_keypress_binding(self, event=None):
        """Delegate to dialog_on_ok after accepting event argument."""
        self.dialog_on_ok()

    def bind_buttons_to_widget(self, widget):
        """Bind button commands to underlined character for widget."""
        for b, u, f in ((self.ok, 0, self.ok_by_keypress_binding),):
            b.configure(underline=u)
            widget.bind(
                b.configure('text')[-1][u].lower().join(('<Alt-', '>')),
                self.try_event(f))

    def on_destroy(self, event=None):
        """Tidy up after destruction of dialogue widget and all children."""
        if event.widget == self.parent:
            self.tidy_on_destroy()

    def tidy_on_destroy(self):
        """Do nothing. Override as required."""
