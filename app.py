#######################################################################
#
#
#
#######################################################################

import wx
import os
import Notebook
import sys
import ColorPanel
import MyGrid
import Database
import Part
import FilterTab

assertMode = wx.PYAPP_ASSERT_DIALOG


#######################################################################
# Main class for the notebook
#######################################################################
class MyNotebook(wx.Notebook):

    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self, parent, id, log):

        # Create the notebook
        wx.Notebook.__init__(self, 
                             parent, 
                             id, 
                             size=(21,21), 
                             style=wx.BK_DEFAULT)
        # Save logger
        self.log = log

        # Open database
        self.db = Database.Database()
        self.db.OpenDataBase()

        # Make the Parts tab
        self.partsTab = MyGrid.MyGrid(self, self.db, log)
        self.AddPage(self.partsTab, "Parts")

        # Make the Filter tab
        self.filterTab = FilterTab.FilterTab(self)
        self.AddPage(self.filterTab, "Filter")

        # Make the Search tab
        self.searchTab = self.makeColorPanel(wx.RED)
        self.AddPage(self.searchTab, "Search")

        # Make the Category tab
        self.categoryTab = self.makeColorPanel(wx.RED)
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


#######################################################################
# Logger class
#######################################################################
class Log:

    ###################################################################
    # Write text to logger
    ###################################################################
    def WriteText(self, text):
        if text[-1:] == '\n':
            text = text[:-1]
        #
        wx.LogMessage(text)
    #


    write = WriteText
#



#######################################################################
# This is the top level class for the application
#######################################################################
class TopWindow(wx.App):

    ID_VIEW_FILTER  = 3001
    ID_VIEW_GROUP   = 3002
    ID_VIEW_SEARCH  = 3003
   

    ###################################################################
    # Constructor
    ###################################################################
    def __init__(self):
        wx.App.__init__(self)
    #


    ###################################################################
    # Called on WX initialization
    ###################################################################
    def OnInit(self):

        # Create logger
        wx.Log.SetActiveTarget(wx.LogStderr())
        log = Log()

        # Set asseriton mode
        self.SetAssertMode(assertMode)

        # Create a top level frame
        self.frame = wx.Frame(None, 
                              -1, 
                              "Notebook", 
                              pos=(50,50), 
                              size=(200,100),
                              style=wx.DEFAULT_FRAME_STYLE, 
                              name="Notebook1")

        # Create Menu Bar
        self.CreateMenuBar()

        # Create Status Bar
        self.CreateTools()

        # Create Status Bar
        self.CreateStatusBar()

        # Show the frame
        self.frame.Show(True)

        # Bind to the CloseFrame routine
        self.frame.Bind(wx.EVT_CLOSE, self.OnCloseFrame)

        # Create a notebook within this frame
        self.NotebookWin = Notebook.MyNotebook(self.frame, -1, log)

        # Set the frame to a good size for showing stuff
        self.frame.SetSize((640, 480))

        # Set the focus to the Notebook
        self.NotebookWin.SetFocus()

        # Set this to be the top Z frame
        self.SetTopWindow(self.frame)
                    
        return True
    #

    ###################################################################
    # Create MenuBar in top frame
    ###################################################################
    def CreateMenuBar(self):

        # Create the "File" menu
        fileMenu = wx.Menu()

        fileMenu.Append(wx.ID_OPEN,   "Open",    "Open a parts database")
        fileMenu.Append(wx.ID_CLOSE,  "Close",   "Close a parts database")
        fileMenu.Append(wx.ID_SAVE,   "Save",    "Save current parts database")
        fileMenu.Append(wx.ID_SAVEAS, "Save as", "Save current parts database as a new file")
        fileMenu.Append(wx.ID_EXIT,   "Exit",    "Exit without saving")

        # Bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnFileOpen,   id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnFileClose,  id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU, self.OnFileSave,   id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.OnFileSaveAs, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.OnFileExit,   id=wx.ID_EXIT)

        # Create the menubar
        menuBar = wx.MenuBar()

        # And put the menu on the menubar
        menuBar.Append(fileMenu, "&File")

        # And put the menu on the frame
        self.frame.SetMenuBar(menuBar)

    #

    ###################################################################
    # Create toolbar
    ###################################################################
    def CreateTools(self):    

        # Create toolbar under the main frame
        toolbar = self.frame.CreateToolBar()

        # Get some art work for buttons
        art_quit      = wx.ArtProvider.GetBitmap(wx.ART_QUIT, 
                                                 client=wx.ART_TOOLBAR)
        art_file_open = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, 
                                                 client=wx.ART_TOOLBAR)

        # Add artwork to tool bar
        toolOpen   = toolbar.AddLabelTool(wx.ID_ANY, 'Open',   art_file_open)
        toolQuit   = toolbar.AddLabelTool(wx.ID_ANY, 'Quit',   art_quit)

        # Draw the toolbar
        toolbar.Realize()

        # Bind methods to buttons
        self.Bind(wx.EVT_TOOL, self.OnFileExit,       toolQuit)
        self.Bind(wx.EVT_TOOL, self.OnFileOpen,       toolOpen)
        
    #

    ###################################################################
    # Create a status bar in top frame
    ###################################################################
    def CreateStatusBar(self):    
        # Create a status bar in the frame
        self.frame.CreateStatusBar()
    #

    ###################################################################
    # Called when application exits
    ###################################################################
    def OnExitApp(self, evt):
        print "OnExitApp"
        self.frame.Close(True)
    #


    ###################################################################
    # Called when frame is closed
    ###################################################################
    def OnCloseFrame(self, evt):
        print "OnCloseFrame"
        evt.Skip()
    #


    ###################################################################
    # Called to close a database file
    ###################################################################
    def OnFileExit(self, evt):
        print "OnFileExit"
        evt.Skip()
    #


    ###################################################################
    # Called when frame is closed
    ###################################################################
    def OnFileOpen(self, evt):
        print "OnFileOPen"
        evt.Skip()
    #


    ###################################################################
    # 
    ###################################################################
    def OnFileClose(self, evt):
        print "OnFileClose"
        evt.Skip()
    #


    ###################################################################
    # 
    ###################################################################
    def OnFileSave(self, evt):
        print "OnFileSave"
        evt.Skip()
    #


    ###################################################################
    # 
    ###################################################################
    def OnFileSaveAs(self, evt):
        print "OnFileSaveAs"
        evt.Skip()
    #


#

    

#######################################################################
# This is the main entry point
#######################################################################
if __name__ == '__main__':

    # Create the application
    app = TopWindow()

    # Now run the application's main loop till exit
    app.MainLoop()
#
