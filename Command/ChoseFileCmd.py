# -*- coding: UTF-8 -*-
import wx

from CommandInterface import CommandInterface

_metaclass_ = type
class ChoseFileCmd(CommandInterface,object):
    def __init__(self,view):
        super(ChoseFileCmd,self).__init__(view)
        
    def Excute(self):
        dlg = wx.FileDialog(None, 
                            message="请选择一个文件",
                            wildcard="*" ,
                            style=wx.OPEN
                            )
        if dlg.ShowModal() == wx.ID_OK:
            self.view.filename = dlg.GetPath()
            from GlobalData import CommonData
            showmsg = "选择文件：" + self.view.filename.encode("utf8") 
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg,True)
        dlg.Destroy()