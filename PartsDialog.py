
import wx
import sys
import os
import time
import Part

#######################################################################
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
#######################################################################
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)


#######################################################################
#
#######################################################################
class PartsDialog(wx.Dialog):

    ###################################################################
    #
    ###################################################################
    def __init__(
            self, 
            parent, 
            ID, 
            title, 
            seed,
            size  = wx.DefaultSize, 
            pos   = wx.DefaultPosition, 
            style = wx.DEFAULT_DIALOG_STYLE,
            ):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.text = []
        self.text.append(self.AddEntry(sizer, "MyPartNum",     seed.MyPartNum))
        self.text.append(self.AddEntry(sizer, "MyBarcode",     seed.MyBarcode))
        self.text.append(self.AddEntry(sizer, "MyWebsite",     seed.MyWebsite))
        self.text.append(self.AddEntry(sizer, "Vendor",        seed.Vendor))
        self.text.append(self.AddEntry(sizer, "VendorPartNum", seed.VendorPartNum))
        self.text.append(self.AddEntry(sizer, "VendorBarcode", seed.VendorBarcode))
        self.text.append(self.AddEntry(sizer, "VendorWebsite", seed.VendorWebsite))
        self.text.append(self.AddEntry(sizer, "Mfg",           seed.Mfg))
        self.text.append(self.AddEntry(sizer, "MfgPartNum",    seed.MfgPartNum))
        self.text.append(self.AddEntry(sizer, "MfgBarcode",    seed.MfgBarcode))
        self.text.append(self.AddEntry(sizer, "MfgWebsite",    seed.MfgWebsite))
        self.text.append(self.AddEntry(sizer, "Quantity",      seed.Quantity))
        self.text.append(self.AddEntry(sizer, "Title",         seed.Title))
        self.text.append(self.AddEntry(sizer, "Description",   seed.Description))
        self.text.append(self.AddEntry(sizer, "Class",         seed.Class))
        self.text.append(self.AddEntry(sizer, "Package",       seed.Package))
        self.text.append(self.AddEntry(sizer, "Location",      seed.Location))
        self.text.append(self.AddEntry(sizer, "Notes",         seed.Notes))

        # Seperator before buttons
        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        # Sizer for button row
        btnsizer = wx.StdDialogButtonSizer()
        
        # OK button
        ok_btn = wx.Button(self, wx.ID_OK)
        ok_btn.SetDefault()
        btnsizer.AddButton(ok_btn)
        ok_btn.Bind(wx.EVT_BUTTON, self.OnOK)

        # Cancel button
        cancel_btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(cancel_btn)
        cancel_btn.Bind(wx.EVT_BUTTON, self.OnCancel)

        btnsizer.Realize()

        # Add buttons to dialog
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        # Make dialog
        self.SetSizer(sizer)
        sizer.Fit(self)
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

