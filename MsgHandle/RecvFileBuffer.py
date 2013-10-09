# -*- coding: UTF-8 -*-

_metaclass_ = type
from NetCommunication import NetSocketFun

from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum,CommonData
from NetCommunication import NetSocketFun

class RecvFileBuffer(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvFileBuffer,self).__init__() 
        
    def HandleMsg(self,bufsize,fddata,th):
        if not fddata.GetData("currentbytes"):
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,"开始接收文件(" + fddata.GetData("filename") + ")")
        recvmsg = NetSocketFun.NetSocketRecv(fddata.GetData("sockfd"),bufsize)
        recvbuffer = NetSocketFun.NetUnPackMsgBody(recvmsg)[0]
        fddata.SetData("currentbytes",fddata.GetData("currentbytes") + len(recvbuffer)) 
        fddata.GetData("file").write(recvbuffer)
        msghead = self.packetMsg(MagicNum.MsgTypec.REQFILEBUFFER, 0)
        fddata.SetData("outdata",msghead)
        th.ModifyInToOut(fddata.GetData("sockfd"))
