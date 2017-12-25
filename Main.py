#######################################################################
# 
# 
# 
#######################################################################

import wxversion
wxversion.select("3.0")
import wx
import time
import PartsDialog
import Part
import Parts
import MyGrid


#######################################################################
# This is the main frame class for the application
#######################################################################
class MyFrame(wx.Frame):
    ID_VIEW_FILTER  = 3001
    ID_VIEW_GROUP   = 3002
    ID_VIEW_SEARCH  = 3003

    ###################################################################
    # This is the top level window with a menu and status bar
    ###################################################################
    def __init__(self, parent, title):

        # Call the base class constructor
        wx.Frame.__init__(self, 
                          parent, 
                          -1, 
                          title,
                          pos=(150, 150), 
                          size=(700, 500))

        # Create the menu system
        self.CreateMenu()

        # Create the toolbar
        self.CreateToolbar()

        # Create the status bar on the bottom
        self.CreateStatusBar()

        # Create the default filter
        self.filt = Part.Part()
        self.filt.setAll("*")

        self.db = Parts.Parts()
        self.db.OpenDataBase()

        # Draw grid on pane
        self.grid = MyGrid.MyGrid(self, self.db)
    #

    ###################################################################
    # 
    ###################################################################
    def CreateMenu(self):

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

        # Create the "view" menu
        viewMenu = wx.Menu()
        viewMenu.Append(self.ID_VIEW_FILTER,  "Filter",      "Filter")
        viewMenu.Append(self.ID_VIEW_GROUP,   "Group",       "Group")
        viewMenu.Append(self.ID_VIEW_SEARCH,  "Search",      "Search")

        # Bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnViewFilter,  id=self.ID_VIEW_FILTER)
        self.Bind(wx.EVT_MENU, self.OnViewGroup,   id=self.ID_VIEW_GROUP)
        self.Bind(wx.EVT_MENU, self.OnViewSearch,  id=self.ID_VIEW_SEARCH)

        # Create the menubar
        menuBar = wx.MenuBar()

        # And put the menu on the menubar
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(viewMenu, "&View")
        self.SetMenuBar(menuBar)
    #

    ###################################################################
    # 
    ###################################################################
    def CreateToolbar(self):
        #wx.ART_ADD_BOOKMARK
        #wx.ART_DEL_BOOKMARK
        #wx.ART_HELP_SIDE_PANEL
        #wx.ART_HELP_SETTINGS
        #wx.ART_HELP_BOOK
        #wx.ART_HELP_FOLDER
        #wx.ART_HELP_PAGE
        #wx.ART_GO_BACK
        #wx.ART_GO_FORWARD
        #wx.ART_GO_UP
        #wx.ART_GO_DOWN
        #wx.ART_GO_TO_PARENT
        #wx.ART_GO_HOME
        #wx.ART_FILE_OPEN
        #wx.ART_FILE_SAVE
        #wx.ART_FILE_SAVE_AS
        #wx.ART_PRINT
        #wx.ART_HELP
        #wx.ART_TIP
        #wx.ART_REPORT_VIEW
        #wx.ART_LIST_VIEW
        #wx.ART_NEW_DIR
        #wx.ART_HARDDISK
        #wx.ART_FLOPPY
        #wx.ART_CDROM
        #wx.ART_REMOVABLE
        #wx.ART_FOLDER
        #wx.ART_FOLDER_OPEN
        #wx.ART_GO_DIR_UP
        #wx.ART_EXECUTABLE_FILE
        #wx.ART_NORMAL_FILE
        #wx.ART_TICK_MARK
        #wx.ART_CROSS_MARK
        #wx.ART_ERROR
        #wx.ART_QUESTION
        #wx.ART_WARNING
        #wx.ART_INFORMATION
        #wx.ART_MISSING_IMAGE
        #wx.ART_COPY
        #wx.ART_CUT
        #wx.ART_PASTE
        #wx.ART_DELETE
        #wx.ART_NEW
        #wx.ART_UNDO
        #wx.ART_REDO
        #wx.ART_QUIT
        #wx.ART_FIND
        #wx.ART_FIND_AND_REPLACE
        art_quit      = wx.ArtProvider.GetBitmap(wx.ART_QUIT, client=wx.ART_TOOLBAR)
        art_file_open = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, client=wx.ART_TOOLBAR)

        toolbar = self.CreateToolBar()


        toolOpen   = toolbar.AddLabelTool(wx.ID_ANY, 'Open',   art_file_open)
        toolQuit   = toolbar.AddLabelTool(wx.ID_ANY, 'Quit',   art_quit)
        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.OnFileExit,       toolQuit)
        self.Bind(wx.EVT_TOOL, self.OnFileOpen,       toolOpen)
    #


    ###################################################################
    # 
    ###################################################################
    def OnFileOpen(self, evt):
      print "open"
    #


    ###################################################################
    # 
    ###################################################################
    def OnFileClose(self, evt):
      print "close"
    #


    ###################################################################
    # 
    ###################################################################
    def OnFileSave(self, evt):
      print "save"
    #


    ###################################################################
    # 
    ###################################################################
    def OnFileSaveAs(self, evt):
      print "saveas"
    #


    ###################################################################
    # 
    ###################################################################
    def OnFileExit(self, evt):
        """Event handler for the button click."""
        self.Close()
    #



    ###################################################################
    # 
    ###################################################################
    def OnViewFilter(self, evt):

      dlg = PartsDialog.PartsDialog(self, 
                       -1, 
                       "Filter", 
                       self.filt,
                       size=(350, 200),
                       style=wx.DEFAULT_DIALOG_STYLE,
                       )

      dlg.CenterOnScreen()

      # this does not return until the dialog is closed.
      val = dlg.ShowModal()
    
      if val == wx.ID_OK:
          self.filt = dlg.GetValue()
      #

      dlg.Destroy()
    #


    ###################################################################
    # 
    ###################################################################
    def OnViewGroup(self, evt):
      pass
    #


    ###################################################################
    # 
    ###################################################################
    def OnViewSearch(self, evt):
      pass
    #


    ###################################################################
    # 
    ###################################################################
    def OnFunButton(self, evt):
        """Event handler for the button click."""
        print "Having fun yet?"
    #


#######################################################################
#
#######################################################################
class TopWindow(wx.App):


    ###################################################################
    # 
    ###################################################################
    def OnInit(self):

        # Create the frame
        frame = MyFrame(None, "Parts Database")

        # Make this the top level window
        self.SetTopWindow(frame)

        # Force the frame to be shown
        frame.Show(True)

        return True
    #
#



#######################################################################
#
#######################################################################
if __name__ == "__main__":
  app = TopWindow(redirect=False)
  app.MainLoop()
#
