# -*- coding: UTF-8 -*-
_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import CommonData

class IdentifyVerifyFailed(MsgHandleInterface.MsgHandleInterface,object):
    "身份验证失败，关闭线程"
    def __init__(self):
        super(IdentifyVerifyFailed,self).__init__() 
    
    def HandleMsg(self,bufsize,session):
        "关闭线程"
        showmsg = "对方关闭连接，此次会话结束"
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
