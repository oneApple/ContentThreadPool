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
    
    def verifyMsgSign(self,msg,sign,fddata,th):
        "如果验证成功则发送成功消息，否则发送验证失败并关闭该线程"
        _cfg = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfg.GetKeyPath())
        if _rsa.VerifyByPubkey(msg, sign, fddata.GetData("peername")) == False:
            msghead = self.packetMsg(MagicNum.MsgTypec.IDENTITYVERIFYFAILED, 0)
            fddata.SetData("outdata", msghead )
            th.ModifyInToOut(fddata.GetData("sockfd"))
            showmsg = "签名验证失败"
        else:
            #生成自己的会话密钥
            from CryptoAlgorithms import HashBySha1
            _hbs = HashBySha1.HashBySha1()
            fddata.SetData("fddatakey",_hbs.GetHash(str(fddata.GetData("dhkey").getKey(string.atol(msg))),MagicNum.HashBySha1c.HEXADECIMAL))
            if fddata.GetData("threadtype") == CommonData.ThreadType.CONNECTAP:
                msghead = self.packetMsg(MagicNum.MsgTypec.AUDITDHGENERATE, 0)
            else:
                msghead = self.packetMsg(MagicNum.MsgTypec.AUDITRETURNDHGENERATE, 0)
            fddata.SetData("outdata", msghead )
            th.ModifyInToOut(fddata.GetData("sockfd"))
            showmsg = "生成会话密钥：" + fddata.GetData("fddatakey")
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
    
    def HandleMsg(self,bufsize,fddata,th):
        "接受对方传来的dh参数及公钥并生成自己的dh公钥"
        recvmsg = NetSocketFun.NetSocketRecv(fddata.GetData("sockfd"),bufsize)
        dhmsg = NetSocketFun.NetUnPackMsgBody(recvmsg)
        #参数p：公钥：签名
        self.verifyMsgSign(dhmsg[0], dhmsg[1], fddata,th)
