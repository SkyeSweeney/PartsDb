#######################################################################
#
# This is the main Python module for the Parts Database application
#
#######################################################################

import wx
import os
import sys
import MyNotebook
import Database
import Log

assertMode = wx.PYAPP_ASSERT_DIALOG



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

        # Initialize the parent class
        wx.App.__init__(self)

    #


    ###################################################################
    # Called on WX initialization
    ###################################################################
    def OnInit(self):
        
        # Create a database object
        self.db = Database.Database()

        # Set up WX logger to send to Standard Error
        wx.Log.SetActiveTarget(wx.LogStderr())

        # Create a logger
        self.log = Log.Log() 
        print self.log

        # Set assertion mode
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
        self.NotebookWin = MyNotebook.MyNotebook(self.frame, -1, self)

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
# 
#######################################################################
def main():
    global appObj

    # Create the application
    appObj = TopWindow()

    # Now run the application's main loop till exit
    appObj.MainLoop()
#


#######################################################################
# 
#######################################################################
def getApp():
    global appObj
    return appObj
#

#######################################################################
# This is the main entry point
#######################################################################
if __name__ == '__main__':
    main()
#
