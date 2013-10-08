# -*- coding: UTF-8 -*-
_metaclass_ = type
import wx
from wx.lib.pubsub  import Publisher

from GlobalData import CommonData
from MsgHandle import MsgHandleInterface

class RecvRegisterFailed(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvRegisterFailed,self).__init__()
    
    def HandleMsg(self,bufsize,session):
        wx.CallAfter(Publisher().sendMessage,CommonData.ViewPublisherc.REGISTER_TRYAGAIN, "该用户名已经存在",True)