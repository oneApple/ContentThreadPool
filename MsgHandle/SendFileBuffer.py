#coding=utf-8
_metaclass_ = type
from NetCommunication import NetSocketFun
from MsgHandle import MsgHandleInterface
from GlobalData import CommonData, MagicNum, ConfigData

class SendFileBuffer(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendFileBuffer,self).__init__()
    
    def handleFileBegin(self,bufsize,fddata):
        "第一次发送则打开文件"
#        if not fddata.GetData("filename") or fddata.GetData("filename") != fddata.control.filename:
#            fddata.SetData("filename",fddata.control.filename.decode("utf8"))
        fddata.SetData("file",open(fddata.GetData("filename"),"rb"))
        import os
        fddata.SetData("totalbytes",os.path.getsize(fddata.GetData("filename")))
        
        _filename = fddata.GetData("filename")[-fddata.GetData("filename")[::-1].index("/"):].encode("utf-8")
        showmsg = "开始发送文件(" + _filename + ")..."
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
    
    def HandleMsg(self,bufsize,fddata,th):
        if not fddata.GetData("currentbytes") and fddata.threadtype != CommonData.ThreadType.CONNECTAP:
            _cfg = ConfigData.ConfigData()
            _dir = _cfg.GetMediaPath() + "/auditserver/" 
            recvbuffer = NetSocketFun.NetSocketRecv(fddata.GetData("sockfd"),bufsize)
            fddata.SetData("control.filename",_dir + NetSocketFun.NetUnPackMsgBody(recvbuffer)[0])
        if not fddata.GetData("currentbytes"):
            self.handleFileBegin(bufsize, fddata)
        _filebuffer = fddata.GetData("file").read(CommonData.MsgHandlec.FILEBLOCKSIZE)
        fddata.SetData("currentbytes",fddata.GetData("currentbytes") + len(_filebuffer))
        msgbody = NetSocketFun.NetPackMsgBody([_filebuffer])
        if fddata.GetData("currentbytes") == fddata.totalbytes:
            msghead = self.packetMsg(MagicNum.MsgTypec.SENDFILEOVER,len(msgbody))
            fddata.GetData("file").close()
            fddata.SetData("currentbytes",0)
            
            _filename = fddata.GetData("filename")[-fddata.GetData("filename")[::-1].index("/"):].encode("utf-8")
            filesize = float(fddata.GetData("totalbytes")) / (1024 * 1024)
            showmsg = "文件发送完毕:\n(1)文件名:" + _filename + "\n(2)文件大小（MB）:" + str(filesize)
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg,True)
        else:
            msghead = self.packetMsg(MagicNum.MsgTypec.SENDFILEBUFFER,len(msgbody))
        fddata.SetData("outdata", msghead + msgbody)
        th.ModifyInToOut(fddata.GetData("sockfd"))
        