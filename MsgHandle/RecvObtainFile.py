#coding=utf-8

_metaclass_ = type
from MsgHandle import MsgHandleInterface 
from NetCommunication import NetSocketFun
from GlobalData import ConfigData, CommonData

class RecvObtainFile(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvObtainFile,self).__init__() 
        _cfg = ConfigData.ConfigData()
        self.__mediapath = _cfg.GetMediaPath()
    
    def HandleMsg(self,bufsize,fddata,th):
        "接收文件名,保存文件名"
        recvbuffer = NetSocketFun.NetSocketRecv(fddata.GetData("sockfd"),bufsize)
        fddata.SetData("threadtype",CommonData.ThreadType.ACCETPNO)
        msglist = NetSocketFun.NetUnPackMsgBody(recvbuffer.encode("utf-8"))
        fddata.SetData("filename",self.__mediapath + "/auditserver/" + msglist[0])
        showmsg = "开始为 " + msglist[1]  +" 分发文件(" + msglist[0] + ")"
        fddata.SetData("peername",msglist[1])
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg.encode("utf-8"),True)
        
        import SendDhPAndPubkey
        _sdh = SendDhPAndPubkey.SendDhPAndPubkey()
        _sdh.HandleMsg(0, fddata)
        