
import wx
import wx.grid  as  gridlib
import time
import sys
import types

import CategoryDlg


#######################################################################
#
#######################################################################
class CategoryTab(gridlib.Grid):

    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self, parent, db, log):

        gridlib.Grid.__init__(self, parent, -1)

        self.db = db

        self.moveTo = None

        # Get list of all field info
        part = self.db.GetCategoryTemplate()
        n    = self.db.GetNumCategoryFields()

        # Create Grid
        self.CreateGrid(0, n)  # Row, col

        # Add the column headers
        for iFld in range(n):
            self.SetColLabelValue(iFld, part.humanNames[iFld])
        #

        # Column widths
        for i in range(n):
          self.AutoSizeColumn(i)
        #

        # Set all text columns as left and bottom aligned
        self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)

        # For each item in the database
        rows = self.db.GetAllCategorys()
        iRow = 0
        for row in rows:
            self.AppendRecord(row)
            for iCol in range(len(row)):
                self.SetReadOnly(iRow, iCol, True)
            iRow = iRow + 1
        #

        
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
    # Add a new record to the end 
    ###################################################################
    def AppendRecord(self, lst):
        self.AppendRows(1)
        row = self.GetNumberRows() - 1
        self.UpdateRecord(row, lst)
    #


    ###################################################################
    # Update a record
    ###################################################################
    def UpdateRecord(self, row, lst):
        for col in range(len(lst)):
            if (type(lst[col]) is types.IntType):
                self.SetCellValue(row, col,  str(lst[col]))
            else:
                self.SetCellValue(row, col,  lst[col])
            #
        #
    #



    ###################################################################
    # Left click
    ###################################################################
    def OnCellLeftClick(self, evt):
        sys.stdout.write("OnCellLeftClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    # Right click
    ###################################################################
    def OnCellRightClick(self, evt):
        sys.stdout.write("OnCellRightClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    # Left double click
    ###################################################################
    def OnCellLeftDClick(self, evt):
        sys.stdout.write("OnCellLeftDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        selectedRow = evt.GetRow()
        selectedCol = evt.GetCol()

        categoryNo = self.GetCellValue(selectedRow, 0)

        self.EditCategory(categoryNo, selectedCol)

        evt.Skip()
    #


    ###################################################################
    # Delete category
    ###################################################################
    def DeleteCategory(self, categoryId):

        self.db.DelCategory(categoryId)

        # Make grid one row smaller
        self.DeleteRows(0, 1)

        # Redraw the grid
        self.RedrawGrid()
    #


    ###################################################################
    # Add part
    ###################################################################
    def AddCategory(self):

        # Create a blank part
        category = Category.Category()

        # Add part to database
        self.db.AddCategory(category)

        # Add entry in table
        self.AppendRows(1)

        # Redraw the grid
        row = self.RedrawGrid()

        return row-1
    #

    ###################################################################
    # Edit part (and focus on given column)
    ###################################################################
    def EditCategory(self, categoryNo, selectedCol):


        # Open the edit dialog
        dlg = CategoryDlg.CategoryDlg(self, -1, "Edit", categoryNo, selectedCol, self.db)
        dlg.CenterOnScreen()

        # Display dialog and wait for OK or Cancel
        val = dlg.ShowModal()

        # If user wants to accept the new data
        if (val == wx.ID_OK):

            # Get the new list of values from the dialog
            newLst = dlg.GetCategoryData()

            # Update the database
            self.db.UpdateCategory(categoryNo, newLst)

            # Redraw the grid
            self.RedrawGrid()

        elif (val == wx.ID_CANCEL):
            print "Discarding changes"
        else:
            print "Invalid return from dialog"
        #

        # Now kill the dialog processing
        dlg.Destroy()

    #    

    ###################################################################
    # Right double click
    ###################################################################
    def OnCellRightDClick(self, evt):
        sys.stdout.write("OnCellRightDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    # Left click on label
    ###################################################################
    def OnLabelLeftClick(self, evt):
        sys.stdout.write("OnLabelLeftClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    # Right clock on label
    ###################################################################
    def OnLabelRightClick(self, evt):

        row = evt.GetRow()
        col = evt.GetCol()

        # Right click on vertical header
        if (col == -1):

            # Pop up a Row context menu
            menu = RowContextMenu(row)
            self.PopupMenu(menu, evt.GetPosition())
            retval = menu.GetRetval()
            menu.Destroy()

            # Uninitialized
            if (retval == 0):
                print "zip"

            # Edit
            elif (retval == 1):
                categoryNo = self.GetCellValue(row, 0)
                self.EditCategory(categoryNo, col)

            # Delete
            elif (retval == 2):
                categoryNo = self.GetCellValue(row, 0)
                self.DeleteCategory(categoryNo)

            # Add
            elif (retval == 3):

                # Add the part
                row = self.AddCategory()

                # Now force it do be edited
                categoryNo = self.GetCellValue(row, 0)

                self.EditCategory(partNo, 2)

            # Bad answer
            else:
                print "???"
            #

        # Right click on horizontal header
        elif (row == -1):
            pass

        else:
            pass
        #
       
        evt.Skip()        
    #

    ###################################################################
    # Left double click on label
    ###################################################################
    def OnLabelLeftDClick(self, evt):
        sys.stdout.write("OnLabelLeftDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    # Right double clcoik on label
    ###################################################################
    def OnLabelRightDClick(self, evt):
        sys.stdout.write("OnLabelRightDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    # User resizes a row
    ###################################################################
    def OnRowSize(self, evt):
        sys.stdout.write("OnRowSize: row %d, %s\n" %
                       (evt.GetRowOrCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    # User resizes a column
    ###################################################################
    def OnColSize(self, evt):
        sys.stdout.write("OnColSize: col %d, %s\n" %
                       (evt.GetRowOrCol(), evt.GetPosition()))
        evt.Skip()
    #

    ###################################################################
    # User selects a range or rows or columns
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

        # Show how to move to a new cell
        #self.SetGridCursor(2,3)
    #


    ###################################################################
    # Nothing happening
    ###################################################################
    def OnIdle(self, evt):
        evt.Skip()
    #


    ###################################################################
    # Cell is selected or deselected
    ###################################################################
    def OnSelectCell(self, evt):

        row = evt.GetRow()
        col = evt.GetCol()

        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        #
        sys.stdout.write("OnSelectCell: %s (%d,%d) %s\n" %
                       (msg, row, col, evt.GetPosition()))

        evt.Skip()
    #


    ###################################################################
    #
    ###################################################################
    def OnEditorShown(self, evt):

        row = evt.GetRow()
        col = evt.GetCol()

        sys.stdout.write("OnEditorShown: (%d,%d) %s\n" %
                       (row, col, evt.GetPosition()))
        evt.Skip()
    #


    ###################################################################
    #
    ###################################################################
    def OnEditorHidden(self, evt):
        row = evt.GetRow()
        col = evt.GetCol()

        sys.stdout.write("OnEditorHidden: (%d,%d) %s\n" %
                       (row, col, evt.GetPosition()))
        evt.Skip()
    #


    ###################################################################
    #
    ###################################################################
    def OnEditorCreated(self, evt):
        row = evt.GetRow()
        col = evt.GetCol()
        sys.stdout.write("OnEditorCreated: (%d, %d) %s\n" %
                       (row, col, evt.GetControl()))
    #    
#


#######################################################################
#
#######################################################################
class RowContextMenu(wx.Menu):

    ###################################################################
    #
    ###################################################################
    def __init__(self, row):
        wx.Menu.__init__(self)

        self.row = row
    
        item = wx.MenuItem(self, wx.NewId(), "Edit")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnEditRow, item)

        item = wx.MenuItem(self, wx.NewId(),"Delete")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnDeleteRow, item)

        item = wx.MenuItem(self, wx.NewId(),"Add")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnAddRow, item)

        self.retval = 0
    #


    ###################################################################
    #
    ###################################################################
    def OnEditRow(self, event):
        self.retval = 1
    #


    ###################################################################
    #
    ###################################################################
    def OnDeleteRow(self, event):
        self.retval = 2
    #


    ###################################################################
    #
    ###################################################################
    def OnAddRow(self, event):
        self.retval = 3
    #

    ###################################################################
    #
    ###################################################################
    def GetRetval(self):
        return self.retval
    #
#

