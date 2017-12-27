#######################################################################
# 
# 
# 
#######################################################################

import wx
import time
import PartsDialog
import Part
import Parts
import MyGrid

assertMode = wx.PYAPP_ASSERT_DIALOG


#######################################################################
# 
#######################################################################
class MyNotebook(wx.Frame):
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
        log = None
        self.grid = MyGrid.MyGrid(self, self.db, log)
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
    def __init__(self):
        wx.App.__init__(self)
    #


    ###################################################################
    # 
    ###################################################################
    def OnInit(self):

        wx.Log.SetActiveTarget(wx.LogStderr())
        log = Log()

        self.SetAssertMode(assertMode)

        # Create the notebook
        frame = MyNotebook(None, "Parts Database")

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
  app = TopWindow()
  app.MainLoop()
#
