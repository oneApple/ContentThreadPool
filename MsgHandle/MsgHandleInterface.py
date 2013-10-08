# -*- coding: UTF-8 -*-
_metaclass_ = type
import struct, wx
from wx.lib.pubsub  import Publisher
from NetCommunication import NetSocketFun
from GlobalData import CommonData

class MsgHandleInterface:
    "接受消息处理函数"
    def __init__(self):
        pass
        
    def sendViewMsg(self,msgtype,showmsg,changeColor=False):
        msg = [showmsg,changeColor]
        if msgtype != CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT:
            msg = showmsg
        wx.CallAfter(Publisher().sendMessage,msgtype,msg)
        
    def packetMsg(self,msgtype,msgbodysize):
        "对信息头打包"
        return struct.pack(CommonData.MsgHandlec.MSGHEADTYPE,msgtype,msgbodysize)
    
    def HandleMsg(self,recvsize,session):
        "处理接受到的信息"
        sockfd = session.GetData("sockfd")
        while True:
            recvmsg = sockfd.recv(NetSocketFun.NetSocketBufferSize)
            print "odd",sockfd.fileno(),recvmsg
            if not recvmsg:
                break