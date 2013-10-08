#coding=utf-8
_metaclass_ = type
from NetCommunication import NetSocketFun
from MsgHandle import MsgHandleInterface
from GlobalData import CommonData, MagicNum, ConfigData

class SendFileBuffer(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendFileBuffer,self).__init__()
    
    def handleFileBegin(self,bufsize,session):
        "第一次发送则打开文件"
#        if not session.GetData("filename") or session.GetData("filename") != session.control.filename:
#            session.SetData("filename",session.control.filename.decode("utf8"))
        session.SetData("file",open(session.GetData("filename"),"rb"))
        import os
        session.SetData("totalbytes",os.path.getsize(session.GetData("filename")))
        
        _filename = session.GetData("filename")[-session.GetData("filename")[::-1].index("/"):].encode("utf-8")
        showmsg = "开始发送文件(" + _filename + ")..."
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
    
    def HandleMsg(self,bufsize,session):
        if not session.GetData("currentbytes") and session.threadtype != CommonData.ThreadType.CONNECTAP:
            _cfg = ConfigData.ConfigData()
            _dir = _cfg.GetMediaPath() + "/auditserver/" 
            recvbuffer = NetSocketFun.NetSocketRecv(session.GetData("sockfd"),bufsize)
            session.SetData("control.filename",_dir + NetSocketFun.NetUnPackMsgBody(recvbuffer)[0])
        if not session.GetData("currentbytes"):
            self.handleFileBegin(bufsize, session)
        _filebuffer = session.GetData("file").read(CommonData.MsgHandlec.FILEBLOCKSIZE)
        session.SetData("currentbytes",session.GetData("currentbytes") + len(_filebuffer))
        msgbody = NetSocketFun.NetPackMsgBody([_filebuffer])
        if session.GetData("currentbytes") == session.totalbytes:
            msghead = self.packetMsg(MagicNum.MsgTypec.SENDFILEOVER,len(msgbody))
            session.GetData("file").close()
            session.SetData("currentbytes",0)
            
            _filename = session.GetData("filename")[-session.GetData("filename")[::-1].index("/"):].encode("utf-8")
            filesize = float(session.GetData("totalbytes")) / (1024 * 1024)
            showmsg = "文件发送完毕:\n(1)文件名:" + _filename + "\n(2)文件大小（MB）:" + str(filesize)
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg,True)
        else:
            msghead = self.packetMsg(MagicNum.MsgTypec.SENDFILEBUFFER,len(msgbody))
        NetSocketFun.NetSocketSend(session.GetData("sockfd"), msghead + msgbody)
        