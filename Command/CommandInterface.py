# -*- coding: UTF-8 -*-
_metaclass_ = type

import wx
from wx.lib.pubsub  import Publisher
from GlobalData import CommonData

class CommandInterface:
    def __init__(self,view):
        self.view = view
    
    def sendViewMsg(self,msgtype,showmsg,changeColor=False):
        msg = [showmsg,changeColor]
        if msgtype != CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT:
            msg = showmsg
        wx.CallAfter(Publisher().sendMessage,msgtype,msg)
        
    def Excute(self):
        pass