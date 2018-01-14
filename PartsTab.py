
import wx
import wx.grid  as  gridlib
import time
import sys
import types

import PartsDlg


#######################################################################
#
#######################################################################
class PartsTab(gridlib.Grid):

    ###################################################################
    #
    ###################################################################
    def __init__(self, parent, db, log):

        gridlib.Grid.__init__(self, parent, -1)

        self.db = db

        self.moveTo = None

        # Get list of all field info
        flds = self.db.GetPartAllFieldInfo()
        n = len(flds)

        # Create Grid
        self.CreateGrid(0, n)  # Row, col

        # Add the column headers
        for f in flds:
            self.SetColLabelValue(f.Id, f.HumanName)
        #

        # Column widths
        for i in range(n):
          self.AutoSizeColumn(i)
        #

        # Set all text columns as left and bottom aligned
        self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)

        # For each item in the database
        rows = self.db.GetAllParts()
        iRow = 0
        for row in rows:
            self.AppendRecord(row)
            for iCol in range(len(row)):
                self.SetReadOnly(iRow, iCol, True)
            iRow = iRow + 1
        #

        #self.SetCellFont(0, 0, wx.Font(12, wx.ROMAN, wx.ITALIC, wx.NORMAL))

        #self.SetCellTextColour(1, 1, wx.RED)

        #self.SetCellBackgroundColour(2, 2, wx.CYAN)

        #self.SetReadOnly(3, 3, True)

        #self.SetCellEditor(5, 0, gridlib.GridCellNumberEditor(1,1000))
        #self.SetCellValue(5, 0, "123")

        #self.SetCellEditor(6, 0, gridlib.GridCellFloatEditor())
        #self.SetCellValue(6, 0, "123.34")

        #self.SetCellEditor(7, 0, gridlib.GridCellNumberEditor())

        #self.SetCellValue(6, 3, "You can veto editing this cell")

        # attribute objects let you keep a set of formatting values
        # in one spot, and reuse them if needed
        #attr = gridlib.GridCellAttr()
        #attr.SetTextColour(wx.BLACK)
        #attr.SetBackgroundColour(wx.RED)
        #attr.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

        # you can set cell attributes for the whole row (or column)
        #self.SetRowAttr(5, attr)

        # overflow cells
        #self.SetCellValue( 9, 1, "This default cell will overflow into neighboring cells, but not if you turn overflow off.");

        #self.SetCellSize(11, 1, 3, 3);
        #self.SetCellAlignment(11, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);
        #self.SetCellValue(11, 1, "This cell is set to span 3 rows and 3 columns");


        #editor = gridlib.GridCellTextEditor()
        #editor.SetParameters('10')
        #self.SetCellEditor(0, 4, editor)
        #self.SetCellValue(0, 4, "Limited text")

        #renderer = gridlib.GridCellAutoWrapStringRenderer()
        #self.SetCellRenderer(15,0, renderer)
        #self.SetCellValue(15,0, "The text in this cell will be rendered with word-wrapping")

        
        # Register events
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK,   self.OnCellLeftClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK,  self.OnCellRightClick)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK,  self.OnCellLeftDClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)

        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK,   self.OnLabelLeftClick)
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK,  self.OnLabelRightClick)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_DCLICK,  self.OnLabelLeftDClick)
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnLabelRightDClick)

        self.Bind(gridlib.EVT_GRID_ROW_SIZE, self.OnRowSize)
        self.Bind(gridlib.EVT_GRID_COL_SIZE, self.OnColSize)

        self.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGE,  self.OnCellChange)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL,  self.OnSelectCell)

        self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN,   self.OnEditorShown)
        self.Bind(gridlib.EVT_GRID_EDITOR_HIDDEN,  self.OnEditorHidden)
        self.Bind(gridlib.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)

    #

    ###################################################################
    # Add a new reconrd to the end 
    ###################################################################
    def AppendRecord(self, row):
        self.AppendRows(1)
        i = self.GetNumberRows() - 1
        j = 0
        n = len(row)
        for j in range(n):
            if (type(row[j]) is types.IntType):
                self.SetCellValue(i, j,  str(row[j]))
            else:
                self.SetCellValue(i, j,  row[j])
            #
        #
    #


    ###################################################################
    #
    ###################################################################
    def OnCellLeftClick(self, evt):
        sys.stdout.write("OnCellLeftClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    #
    ###################################################################
    def OnCellRightClick(self, evt):
        sys.stdout.write("OnCellRightClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    #
    ###################################################################
    def OnCellLeftDClick(self, evt):
        sys.stdout.write("OnCellLeftDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        # Get the part number from the grid
        partNo = 3
        
        # Open the edit dialog
        dlg = PartsDlg.PartsDlg(self, -1, "Edit", partNo, self.db)
        dlg.CenterOnScreen()

        # Display dialog and wait for OK or Cancel
        val = dlg.ShowModal()

        # If user wants to accept the new data
        if (val == wx.ID_OK):

            # Get the new part data from the dialog
            newPart = dlg.GetPartData()
            print newPart

        elif (val == wx.ID_CANCEL):
            print "Discarding changes"
        else:
            print "Invalid return from dialog"
        #

        # Now kill the dialog processing
        dlg.Destroy()

        evt.Skip()
    #

    ###################################################################
    #
    ###################################################################
    def OnCellRightDClick(self, evt):
        sys.stdout.write("OnCellRightDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    #
    ###################################################################
    def OnLabelLeftClick(self, evt):
        sys.stdout.write("OnLabelLeftClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    #
    ###################################################################
    def OnLabelRightClick(self, evt):
        sys.stdout.write("OnLabelRightClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    #
    ###################################################################
    def OnLabelLeftDClick(self, evt):
        sys.stdout.write("OnLabelLeftDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    #
    ###################################################################
    def OnLabelRightDClick(self, evt):
        sys.stdout.write("OnLabelRightDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    #
    ###################################################################
    def OnRowSize(self, evt):
        sys.stdout.write("OnRowSize: row %d, %s\n" %
                       (evt.GetRowOrCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    #
    ###################################################################
    def OnColSize(self, evt):
        sys.stdout.write("OnColSize: col %d, %s\n" %
                       (evt.GetRowOrCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    #
    ###################################################################
    def OnRangeSelect(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        #
        sys.stdout.write("OnRangeSelect: %s  top-left %s, bottom-right %s\n" %
                           (msg, evt.GetTopLeftCoords(), evt.GetBottomRightCoords()))
        evt.Skip()
    #


    ###################################################################
    # Called when the user edits a cell
    ###################################################################
    def OnCellChange(self, evt):
        sys.stdout.write("OnCellChange: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        # Show how to stay in a cell that has bad data.  We can't just
        # call SetGridCursor here since we are nested inside one so it
        # won't have any effect.  Instead, set coordinates to move to in
        # idle time.
        value = self.GetCellValue(evt.GetRow(), evt.GetCol())

        if value == 'no good':
            self.moveTo = evt.GetRow(), evt.GetCol()
        #
    #


    ###################################################################
    #
    ###################################################################
    def OnIdle(self, evt):
        if self.moveTo != None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None
        #

        evt.Skip()
    #


    ###################################################################
    #
    ###################################################################
    def OnSelectCell(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        #
        sys.stdout.write("OnSelectCell: %s (%d,%d) %s\n" %
                       (msg, evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        # Another way to stay in a cell that has a bad value...
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()

        if self.IsCellEditControlEnabled():
            self.HideCellEditControl()
            self.DisableCellEditControl()
        #

        value = self.GetCellValue(row, col)

        if value == 'no good 2':
            return  # cancels the cell selection
        #

        evt.Skip()
    #


    ###################################################################
    #
    ###################################################################
    def OnEditorShown(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
           wx.MessageBox("Are you sure you wish to edit this cell?",
                        "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return
        #

        sys.stdout.write("OnEditorShown: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #


    ###################################################################
    #
    ###################################################################
    def OnEditorHidden(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
           wx.MessageBox("Are you sure you wish to  finish editing this cell?",
                        "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return

        sys.stdout.write("OnEditorHidden: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #


    ###################################################################
    #
    ###################################################################
    def OnEditorCreated(self, evt):
        sys.stdout.write("OnEditorCreated: (%d, %d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetControl()))
    #    
#
