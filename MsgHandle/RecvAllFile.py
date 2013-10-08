# -*- coding: UTF-8 -*-
_metaclass_ = type
from NetCommunication import NetSocketFun
from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum,CommonData


class RecvAllFile(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvAllFile,self).__init__() 
        
    def HandleMsg(self,bufsize,session):
        recvmsg = NetSocketFun.NetSocketRecv(session.GetData("sockfd"),bufsize)
        recvbuffer = NetSocketFun.NetUnPackMsgBody(recvmsg)[0]
        session.GetData("file").write(recvbuffer)
        session.GetData("file").close()
        if session.GetData("threadtype") == CommonData.ThreadType.ACCETPNO:
            msghead = self.packetMsg(MagicNum.MsgTypec.REQAGROUP, 0)
        elif session.GetData("threadtype") == CommonData.ThreadType.ACCEPTAP:
            msghead = self.packetMsg(MagicNum.MsgTypec.REQCGROUP, 0)
        
        filesize = float((session.GetData("currentbytes") + bufsize)) / (1024 * 1024)
        showmsg = "文件接收完毕:\n(1)文件名:" + session.GetData("filename") + "\n(2)文件大小（MB）:" + str(filesize)
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
        NetSocketFun.NetSocketSend(session.GetData("sockfd"),msghead)
        session.SetData("currentbytes",0)

