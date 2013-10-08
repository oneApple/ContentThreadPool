# -*- coding: UTF-8 -*-
_metaclass_ = type
import string
from NetCommunication import NetSocketFun

from MsgHandle import MsgHandleInterface
from CryptoAlgorithms import Rsa
from GlobalData import CommonData, MagicNum, ConfigData

class RecvDhPubkeyAndSendDhGenerateSuccess(MsgHandleInterface.MsgHandleInterface,object):
    "接受对方传来的dh公钥，同时计算生成会话密钥"
    def __init__(self):
        super(RecvDhPubkeyAndSendDhGenerateSuccess,self).__init__()         
    
    def verifyMsgSign(self,msg,sign,session):
        "如果验证成功则发送成功消息，否则发送验证失败并关闭该线程"
        _cfg = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfg.GetKeyPath())
        if _rsa.VerifyByPubkey(msg, sign, session.GetData("peername")) == False:
            msghead = self.packetMsg(MagicNum.MsgTypec.IDENTITYVERIFYFAILED, 0)
            NetSocketFun.NetSocketSend(session.GetData("sockfd"), msghead )
            showmsg = "签名验证失败"
        else:
            #生成自己的会话密钥
            from CryptoAlgorithms import HashBySha1
            _hbs = HashBySha1.HashBySha1()
            session.SetData("sessionkey",_hbs.GetHash(str(session.GetData("dhkey").getKey(string.atol(msg))),MagicNum.HashBySha1c.HEXADECIMAL))
            if session.GetData("threadtype") == CommonData.ThreadType.CONNECTAP:
                msghead = self.packetMsg(MagicNum.MsgTypec.AUDITDHGENERATE, 0)
            else:
                msghead = self.packetMsg(MagicNum.MsgTypec.AUDITRETURNDHGENERATE, 0)
            NetSocketFun.NetSocketSend(session.GetData("sockfd"), msghead )
            showmsg = "生成会话密钥：" + session.GetData("sessionkey")
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
    
    def HandleMsg(self,bufsize,session):
        "接受对方传来的dh参数及公钥并生成自己的dh公钥"
        recvmsg = NetSocketFun.NetSocketRecv(session.GetData("sockfd"),bufsize)
        dhmsg = NetSocketFun.NetUnPackMsgBody(recvmsg)
        #参数p：公钥：签名
        self.verifyMsgSign(dhmsg[0], dhmsg[1], session)
