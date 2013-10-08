# -*- coding: UTF-8 -*-
import socket, struct
from NetCommunication import NetSocketFun,ComThreadManage,CommunicationThread
import NetThread
from CryptoAlgorithms import RsaKeyExchange
from GlobalData import CommonData, ConfigData, MagicNum

_metaclass_ = type
class NetConnect:
    def __init__(self,view):
        self.__Sockfd = socket.socket()
        self.view = view  
    
    def ChangeView(self,view):
        self.view = view    
        
    def ReqConnect(self,name,psw):
        "请求登录"
        msglist = [MagicNum.UserTypec.CPUSER , name , psw]
        _msgbody = NetSocketFun.NetPackMsgBody(msglist)
        _msghead = struct.pack(CommonData.MsgHandlec.MSGHEADTYPE,MagicNum.MsgTypec.REQLOGINMSG,len(_msgbody))
        NetSocketFun.NetSocketSend(self.__Sockfd,_msghead + _msgbody)
    
    def ReqRegister(self,name,psw,ip,port):
        "请求注册"
        _rke = RsaKeyExchange.RsaKeyExchange()
        _rke.GenerateRsaKey()
        _pkeystr = _rke.GetPubkeyStr("own")
        msglist = [name,psw,ip,port,_pkeystr]
        _msgbody = NetSocketFun.NetPackMsgBody(msglist)
        _msghead = struct.pack(CommonData.MsgHandlec.MSGHEADTYPE,MagicNum.MsgTypec.REQREGISTERMSG,len(_msgbody))
        NetSocketFun.NetSocketSend(self.__Sockfd,_msghead + _msgbody.decode('gbk').encode("utf-8"))
        
    def ReqAudit(self,filename):
        "请求审核" 
        self.filename = filename
        _filename = filename[-filename[::-1].index("/"):].encode("utf-8")
        _msgbody = NetSocketFun.NetPackMsgBody([_filename])
        _msghead = struct.pack(CommonData.MsgHandlec.MSGHEADTYPE,MagicNum.MsgTypec.REQAUDITMSG, len(_msgbody))
        CommunicationThread.CommunicationThread.epManage.GetSockData(self.__Sockfd.fileno()).SetData("filename",self.filename)
        NetSocketFun.NetSocketSend(self.__Sockfd,_msghead + _msgbody)
        
        import wx
        from wx.lib.pubsub  import Publisher
        wx.CallAfter(Publisher().sendMessage,CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,["请求审核文件(" + _filename + ")".encode("utf8"),False])
        
    def StartNetConnect(self):
        "连接服务器并开启网络线程"
        config = ConfigData.ConfigData()
        _auditAddress = config.GetAuditServerAddress()
        try:
            self.__Sockfd.connect((_auditAddress[0],int(_auditAddress[1])))
            print self.__Sockfd.fileno(),"confd"
            self.__netManage = ComThreadManage.ComThreadManage()
            self.__netManage.run(4)
            CommunicationThread.CommunicationThread.epManage.AddNewSockfd(self.__Sockfd,CommonData.ThreadType.CONNECTAP)
        except:
            return MagicNum.NetConnectc.NOTCONNECT
        
        
    def StopNetConnect(self):
        "发送关闭消息并关闭网络线程"
        print "send close"
        _msghead = struct.pack(CommonData.MsgHandlec.MSGHEADTYPE,MagicNum.MsgTypec.REQCLOSEMSG, 0)
        NetSocketFun.NetSocketSend(self.__Sockfd,_msghead)
#        self.__netThread.stop()
        print "netmanage.stop"
        self.__netManage.stop()
        print "all close"
        #放在主线程主执行
        
if __name__=='__main__':
    filename = "/home/keym/视频/小伙.mpg"
    _msgbody = filename[-filename[::-1].index("/"):].encode("utf-8")
