
import wx
import sys
import os
import time
import Part


#######################################################################
# Creates a Parts Tab
#######################################################################
class FilterTab(wx.ScrolledWindow):

    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self, parent):

        wx.ScrolledWindow.__init__(self, parent, -1, size=wx.DefaultSize)
        self.SetVirtualSize( (1000,1000) )
        self.SetScrollRate(20,20)

        self.parent = parent
        self.db = self.parent.db
        self.fields = self.db.fields

        # Create vertical sizer for fields
        vSizer = wx.BoxSizer(wx.VERTICAL)

        # Create and polulate the initial filter
        self.filtVal = Part.Part()
        self.filtVal.setAll("*")

        # For each field in the list
        flds = self.fields.getFields()

        i = 0
        for fld in flds:
            self.AddEntry(vSizer, fld.HumanName, self.filtVal.getValueByIndex(i))
            i = i + 1
        #

        # Add sizer to window
        self.SetSizer(vSizer)
        vSizer.Fit(self)
    #

    ###################################################################
    # Helper routine to create a single line 
    ###################################################################
    def AddEntry(self, sizer, title, text):

        box = wx.BoxSizer(wx.HORIZONTAL)

        labelObj = wx.StaticText(self, -1, title)
        box.Add(labelObj, 1, flag=wx.ALIGN_CENTRE|wx.ALL, border=5)

        textObj = wx.TextCtrl(self, -1, text)
        box.Add(textObj, 1, flag=wx.ALIGN_CENTRE|wx.ALL, border=5)

        sizer.Add(box, 
                  1, 
                  flag=wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                  border=1)

    #
#

