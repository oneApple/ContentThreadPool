# -*- coding: UTF-8 -*-
_metaclass_ = type
import wx
from wx.lib.pubsub  import Publisher

from GlobalData import CommonData
from MsgHandle import MsgHandleInterface

class RecvLoginFailed(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvLoginFailed,self).__init__()
    
    def HandleMsg(self,bufsize,session):
        wx.CallAfter(Publisher().sendMessage,CommonData.ViewPublisherc.LOGIN_TRYAGAIN,"用户名或密码错误",True)