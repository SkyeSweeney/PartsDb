

import wx
import os
import Notebook
import sys
import ColorPanel
import GridSimple
import ScrolledWindow

assertMode = wx.PYAPP_ASSERT_DIALOG


#######################################################################
#
#######################################################################
class TestNB(wx.Notebook):

    ###################################################################
    #
    ###################################################################
    def __init__(self, parent, id, log):
        wx.Notebook.__init__(self, parent, id, size=(21,21), style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        self.log = log

        win = self.makeColorPanel(wx.BLUE)
        self.AddPage(win, "Blue")

        st = wx.StaticText(win.win, -1,
                          "You can put nearly any type of window here,\n"
                          "and if the platform supports it then the\n"
                          "tabs can be on any side of the notebook.",
                          (10, 10))

        st.SetForegroundColour(wx.WHITE)
        st.SetBackgroundColour(wx.BLUE)


        win = self.makeColorPanel(wx.RED)
        self.AddPage(win, "Red")

        win = ScrolledWindow.MyCanvas(self)
        self.AddPage(win, 'ScrolledWindow')

        win = GridSimple.SimpleGrid(self, log)
        self.AddPage(win, "Grid")


        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
    #


    ###################################################################
    #
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
    #
    ###################################################################
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        self.log.write('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()
    #

    ###################################################################
    #
    ###################################################################
    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        self.log.write('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()
    #


#######################################################################
#
#######################################################################
class Log:

    ###################################################################
    #
    ###################################################################
    def WriteText(self, text):
        if text[-1:] == '\n':
            text = text[:-1]
        #
        wx.LogMessage(text)
    #


    write = WriteText



#######################################################################
#
#######################################################################
class RunDemoApp(wx.App):

    ###################################################################
    #
    ###################################################################
    def __init__(self):
        wx.App.__init__(self, redirect=False)
    #


    ###################################################################
    #
    ###################################################################
    def OnInit(self):
        wx.Log.SetActiveTarget(wx.LogStderr())

        self.SetAssertMode(assertMode)

        frame = wx.Frame(None, 
                         -1, 
                         "Notebook", 
                         pos=(50,50), 
                         size=(200,100),
                         style=wx.DEFAULT_FRAME_STYLE, 
                         name="Notebook1")
        self.frame = frame
        frame.CreateStatusBar()

        menuBar = wx.MenuBar()
        menu = wx.Menu()

        item = menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q", "Exit demo")
        self.Bind(wx.EVT_MENU, self.OnExitApp, item)
        menuBar.Append(menu, "&File")

        frame.SetMenuBar(menuBar)
        frame.Show(True)
        frame.Bind(wx.EVT_CLOSE, self.OnCloseFrame)

        log = Log()
        win = Notebook.TestNB(frame, -1, log)
        self.window = win

        # Set the frame to a good size for showing stuff
        frame.SetSize((640, 480))
        win.SetFocus()
        frect = frame.GetRect()

        self.SetTopWindow(frame)
                    
        return True
    #

    ###################################################################
    #
    ###################################################################
    def OnExitApp(self, evt):
        self.frame.Close(True)
    #


    ###################################################################
    #
    ###################################################################
    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "ShutdownDemo"):
            self.window.ShutdownDemo()
        #
        evt.Skip()
    #
#

    

#----------------------------------------------------------------------------
if __name__ == '__main__':
    app = RunDemoApp()
    app.MainLoop()
#
