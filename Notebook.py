
import  sys

import  wx

import  ColorPanel
import  GridSimple
import  ScrolledWindow

#----------------------------------------------------------------------------

class TestNB(wx.Notebook):
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


    def makeColorPanel(self, color):
        p = wx.Panel(self, -1)
        win = ColorPanel.ColoredPanel(p, color)
        p.win = win
        def OnCPSize(evt, win=win):
            win.SetPosition((0,0))
            win.SetSize(evt.GetSize())
        p.Bind(wx.EVT_SIZE, OnCPSize)
        return p


    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        self.log.write('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        self.log.write('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

#----------------------------------------------------------------------------

def runTest(frame, nb, log):
    testWin = TestNB(nb, -1, log)
    return testWin

#----------------------------------------------------------------------------


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['Notebook.py'])





