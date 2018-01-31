
import wx
import types
import Project
import Database



#**********************************************************************
#
#**********************************************************************
class ProjectDlg(wx.Dialog):

    #******************************************************************
    #
    #******************************************************************
    def __init__(self, 
                 parent, 
                 ID, 
                 title, 
                 projectId,
                 selectedCol,
                 db,
                 size=wx.DefaultSize, 
                 pos=wx.DefaultPosition, 
                 style=wx.DEFAULT_DIALOG_STYLE,
                 ):

        self.db = db
        self.projectId = projectId

        wx.Dialog.__init__(self, 
                           None, 
                           -1, 
                           "Edit",
                           style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)

        # Get the project data for this row
        rows = self.db.GetProjectByFieldValue("ProjectId", self.projectId)

        if (len(rows) != 1):
            print "Invalid results"
            sys.exit(1)
        #
        row = rows[0]

        print "row", row,self.db.GetNumProjectFields()

        # Create a project from the row
        project = Project.Project()
        project.setFromList(row)

        # Create a vertical sizer to put all items in
        vSizer = wx.BoxSizer(wx.VERTICAL)

        # Get list of all fields
        template = self.db.GetProjectTemplate()

        self.values = []

        # For each field in the project
        for iFld in range(self.db.GetNumProjectFields()):

            # Create a sizer for row
            hSizer = wx.BoxSizer(wx.HORIZONTAL)

            # Create label for field name
            label = wx.StaticText(self, -1, template.humanNames[iFld])

            if (template.editables[iFld]):
                st = 0
            else:
                st = wx.TE_READONLY
            #

            # Create item to hold value
            if (type(row[iFld]) is types.IntType):
                value = wx.TextCtrl(self, -1, str(row[iFld]), style = st)
            else:
                value = wx.TextCtrl(self, -1, row[iFld], style = st)
            #
            self.values.append(value)
                
            # Add the label and value to the horizontal row
            hSizer.Add(label, 0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)
            hSizer.Add(value, 0, wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, 5)

            # Add this row to the vertical sizer
            vSizer.Add(hSizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)
        #

        self.values[selectedCol].SetFocus()

        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Horizontal seperator
        line = wx.StaticLine(self, -1, size=(40,-1), style=wx.LI_HORIZONTAL)
        vSizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        # Arrange buttons
        btnsizer = wx.StdDialogButtonSizer()
        
        # OK button
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        # Cancel button
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)

        # Format buttons to match platform style guide
        btnsizer.Realize()

        vSizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(vSizer)
        vSizer.Fit(self)
    #

    #******************************************************************
    #
    #******************************************************************
    def GetProjectData(self):

        retval = []

        # Get list of all fields
        template = self.db.GetProjectTemplate()

        # For each field in the project
        for iFld in range(self.db.GetNumProjectFields()):

            val = self.values[iFld].GetValue()

            # Create item to hold value
            if (type(template.sqlTypes[iFld]) is types.IntType):
                retval.append(int(val))
            else:
                retval.append(val)
            #
        #
        return retval
    #

#

