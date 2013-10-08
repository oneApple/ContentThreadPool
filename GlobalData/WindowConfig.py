# -*- coding: UTF-8 -*-
class WindowConfig:
    def __init__(self):
        pass
    
    def GetFrameSize(self):
        return (1024,800)
    
    def GetSystemNameFontSize(self):
        return 15
    
    def GetSystemNameFontColor(self):
        return "blue"
    
    def GetSystemNameBackColor(self):
        return "bisque"
    
    def GetShowTextFont(self):
        import wx
        font = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL)
        return font
    
    def GetShowTextFontColor1(self):
        return "orange"
    
    def GetShowTextFontColor2(self):
        return "black"
    
    def GetShowTextBackColor(self):
        return "gainsboro"
    
    def GetFullShowTextFont(self):
        import wx
        font = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL)
        return font
    
    def GetFullShowTextFontColor1(self):
        return "green"
    
    def GetFullShowTextFontColor2(self):
        return "white"
    
    def GetFullShowTextBackColor(self):
        return "black"
    
    def GetStaticTextFont(self):
        import wx
        font = wx.Font(15, wx.NORMAL, wx.NORMAL, wx.NORMAL)
        return font
    
    def GetStaticTextFontColor(self):
        return "black"
    
    def GetPanelBackColor(self):
        return "pink"
    
    def GetTableLabelSize(self):
        return 25
    
    def GetTableChoseFontColor(self):
        return "white"
    
    def GetTableChoseBackColor(self):
        return "pink"    
    