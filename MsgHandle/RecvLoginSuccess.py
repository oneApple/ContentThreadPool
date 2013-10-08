# -*- coding: UTF-8 -*-
_metaclass_ = type
from wx.lib.pubsub  import Publisher
from NetCommunication import NetSocketFun
import wx

from MsgHandle import MsgHandleInterface
from GlobalData import CommonData

class RecvLoginSuccess(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvLoginSuccess,self).__init__()
    
    def HandleMsg(self,bufsize,session):
        recvmsg = NetSocketFun.NetSocketRecv(session.GetData("sockfd"),bufsize)                                                                                       
        recvlist = NetSocketFun.NetUnPackMsgBody(recvmsg)
        wx.CallAfter(Publisher().sendMessage,CommonData.ViewPublisherc.LOGIN_SWITCH,recvlist)
        
