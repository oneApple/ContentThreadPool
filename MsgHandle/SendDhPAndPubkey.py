# -*- coding: UTF-8 -*-
_metaclass_ = type

from NetCommunication import NetSocketFun
from MsgHandle import MsgHandleInterface
from GlobalData import CommonData, MagicNum, ConfigData
from CryptoAlgorithms import DiffieHellman, Rsa


class SendDhPAndPubkey(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendDhPAndPubkey,self).__init__()
        
    def getDhpAndga(self,session):                                
        "获取迪菲赫尔慢公钥和大素数"
        p = DiffieHellman.GetBigPrime()
        session.SetData("dhkey", DiffieHellman.DiffieHellman(p))
        _cfg = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfg.GetKeyPath())    
        _dhpubkey = str(session.GetData("dhkey").getPubkey())
        return str(p) , _dhpubkey ,_rsa.SignByPrikey(str(p)),_rsa.SignByPrikey(_dhpubkey)
                                                                                 
    def HandleMsg(self,bufsize,session):
        "发送迪菲参数p和公钥，及该消息的签名"                
        msglist = self.getDhpAndga(session)
        msgbody = NetSocketFun.NetPackMsgBody(msglist)
        msghead = self.packetMsg(MagicNum.MsgTypec.SENDDHPANDPUBKEY ,len(msgbody))
        NetSocketFun.NetSocketSend(session.GetData("sockfd"),msghead + msgbody)
        if not session.GetData("peername"):
            session.SetData("peername","auditserver")
            
        #showmsg = "发送迪菲赫尔曼\n(1)参数p：" + _dhkeymsg[0] + "\n(2)公钥:" + _dhkeymsg[1]
        #self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)

        
