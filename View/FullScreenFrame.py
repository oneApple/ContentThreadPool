# -*- coding: UTF-8 -*-

import wx
from wx.lib.pubsub  import Publisher
from GlobalData import CommonData, WindowConfig


class FullScreenFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.parentFrame = parent
        self.wcfg = WindowConfig.WindowConfig()
        
        self.__showTextColor = True
        
        panel = wx.Panel(self, -1)
        
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.__showText = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY)  
        self.__showText.SetFont(self.wcfg.GetFullShowTextFont())
        self.__showText.SetBackgroundColour(self.wcfg.GetFullShowTextBackColor())
        self.__showText.Bind(wx.EVT_LEFT_DCLICK, self.evtDoubleClick)
        
        
        vbox.Add(self.__showText,-1,wx.EXPAND)
        panel.SetSizer(vbox)
        self.registerPublisher()
        
    
    def registerPublisher(self):
        Publisher().subscribe(self.appendShowTextCtrl, CommonData.ViewPublisherc.FULLFRAME_APPENDTEXT)    
        
    def appendShowTextCtrl(self, recvmsg):
        "添加新行"
        msg = recvmsg.data[0].decode("utf8")
        msg += "\n"
            
        _isChangeColor = recvmsg.data[1]
        if _isChangeColor:
            if self.__showTextColor:
                self.__showText.SetForegroundColour(self.wcfg.GetFullShowTextFontColor1())
            else:
                self.__showText.SetForegroundColour(self.wcfg.GetFullShowTextFontColor2())
            self.__showTextColor = not self.__showTextColor

        self.__showText.AppendText(msg)
    
    def evtDoubleClick(self,evt):
        self.parentFrame.Show()
        self.Hide()
    
    def clearShowText(self):
        self.__showText.Clear()    
    
    def ShowFullScreenFrame(self):
        self.Centre()
        self.Show()
        self.ShowFullScreen(True,style=wx.FULLSCREEN_ALL)
        
if __name__ == "__main__":
    app = wx.App()
    FullScreenFrame(None, -1, 'k.py')
    app.MainLoop()
