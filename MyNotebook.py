#######################################################################
#
# This module support the tabbed interface (notebook) of the main window
#
#######################################################################

import wx
import os
import sys

import ColorPanel
import PartsTab
import CategoryTab
import Database
import App



#######################################################################
# Main class for the notebook
#######################################################################
class MyNotebook(wx.Notebook):

    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self, frm, id, parent):

        # Create the notebook
        wx.Notebook.__init__(self, 
                             frm, 
                             id, 
                             size=(21,21), 
                             style=wx.BK_DEFAULT)

        # Save the application object
        self.app = parent

        # Save logger
        self.log = self.app.log

        # Save the Database object
        self.db = self.app.db

        # Open the database
        self.db.OpenDataBase("parts.db")

        # Make the Parts tab
        self.partsTab = PartsTab.PartsTab(self, self.db, self.log)
        self.AddPage(self.partsTab, "Parts")

        # Make the Category tab
        self.categoryTab = CategoryTab.CategoryTab(self, self.db, self.log)
        self.AddPage(self.categoryTab, "Category")

        # Make the Project tab
        self.projectTab = self.makeColorPanel(wx.RED)
        self.AddPage(self.projectTab, "Projects")

        # Bind to tab changing routines
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,  self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
    #


    ###################################################################
    # Used for dummy tabs
    ###################################################################
    def makeColorPanel(self, color):
        p = wx.Panel(self, -1)
        win = ColorPanel.ColoredPanel(p, color)
        p.win = win
        def OnCPSize(evt, win=win):
            win.SetPosition((0,0))
            win.SetSize(evt.GetSize())
        #
        p.Bind(wx.EVT_SIZE, OnCPSize)
        return p
    #


    ###################################################################
    # This gets called when the new tab is activated
    ###################################################################
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        self.log.write('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()
    #

    ###################################################################
    # This gets called when a new tab is selected but has yet to be changed
    ###################################################################
    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        self.log.write('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()
    #
#
