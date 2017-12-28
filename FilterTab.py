
import wx
import sys
import os
import time
import Part


#######################################################################
# Creates a Parts Tab
#######################################################################
class FilterTab(wx.Window):

    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self, parent):

        wx.Window.__init__(self, parent, -1)
        self.SetBackgroundColour(wx.GREEN)

        # Now continue with the normal construction of the dialog
        # contents
        vSizer = wx.BoxSizer(wx.VERTICAL)


        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        labelObj = wx.StaticText(self, -1, "title")
        hSizer.Add(labelObj, 1, flag=wx.ALIGN_CENTRE|wx.ALL, border=5)

        textObj = wx.TextCtrl(self, -1, "text")
        hSizer.Add(textObj, 1, flag=wx.ALIGN_CENTRE|wx.ALL, border=5)

        vSizer.Add(hSizer, 
                  1, 
                  flag=wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                  border=5)


        # Seperator before buttons
        #line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        #sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        # Sizer for button row
        #btnsizer = wx.StdDialogButtonSizer()
        
        # OK button
        #ok_btn = wx.Button(self, wx.ID_OK)
        #ok_btn.SetDefault()
        #btnsizer.AddButton(ok_btn)
        #ok_btn.Bind(wx.EVT_BUTTON, self.OnOK)

        # Cancel button
        #cancel_btn = wx.Button(self, wx.ID_CANCEL)
        #btnsizer.AddButton(cancel_btn)
        #cancel_btn.Bind(wx.EVT_BUTTON, self.OnCancel)

        #btnsizer.Realize()

        # Add buttons to dialog
        #sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Make dialog
        self.SetSizer(vSizer)
        vSizer.Fit(self)
    #


    ###################################################################
    #
    ###################################################################
    def OnOK(self, evt):
        strings = []
        for i in self.text:
            strings.append(i.GetValue())
        #
        self.retval = Part.Part()
        self.retval.createFromList(strings)
        self.EndModal(wx.ID_OK)
    #


    ###################################################################
    #
    ###################################################################
    def OnCancel(self, evt):
        self.EndModal(wx.ID_CANCEL)
    #


    ###################################################################
    #
    ###################################################################
    def GetValue(self):
        return self.retval
    #


    ###################################################################
    #
    ###################################################################
    def AddEntry(self, sizer, title, text):

        box = wx.BoxSizer(wx.HORIZONTAL)

        labelObj = wx.StaticText(self, -1, title)
        box.Add(labelObj, 1, flag=wx.ALIGN_CENTRE|wx.ALL, border=5)

        textObj = wx.TextCtrl(self, -1, text)
        box.Add(textObj, 1, flag=wx.ALIGN_CENTRE|wx.ALL, border=5)

        sizer.Add(box, 1, flag=wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)

        return textObj
    #
#

