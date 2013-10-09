# -*- coding: UTF-8 -*-
_metaclass_ = type
from NetCommunication import NetSocketFun
from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum,CommonData


class RecvAllFile(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvAllFile,self).__init__() 
        
    def HandleMsg(self,bufsize,fddata,th):
        recvmsg = NetSocketFun.NetSocketRecv(fddata.GetData("sockfd"),bufsize)
        recvbuffer = NetSocketFun.NetUnPackMsgBody(recvmsg)[0]
        fddata.GetData("file").write(recvbuffer)
        fddata.GetData("file").close()
        if fddata.GetData("threadtype") == CommonData.ThreadType.ACCETPNO:
            msghead = self.packetMsg(MagicNum.MsgTypec.REQAGROUP, 0)
        elif fddata.GetData("threadtype") == CommonData.ThreadType.ACCEPTAP:
            msghead = self.packetMsg(MagicNum.MsgTypec.REQCGROUP, 0)
        
        filesize = float((fddata.GetData("currentbytes") + bufsize)) / (1024 * 1024)
        showmsg = "文件接收完毕:\n(1)文件名:" + fddata.GetData("filename") + "\n(2)文件大小（MB）:" + str(filesize)
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
        fddata.SetData("outdata",msghead)
        th.ModifyInToOut(fddata.GetData("sockfd"))
        fddata.SetData("currentbytes",0)

