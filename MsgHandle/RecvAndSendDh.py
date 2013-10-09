# -*- coding: UTF-8 -*-
_metaclass_ = type
import string
from NetCommunication import NetSocketFun

from MsgHandle import MsgHandleInterface
from CryptoAlgorithms import DiffieHellman, Rsa
from GlobalData import CommonData, MagicNum, ConfigData

class RecvAndSendDh(MsgHandleInterface.MsgHandleInterface,object):
    "接受对方传来的dh参数p及公钥并生成自己的dh公钥，同时计算生成会话密钥,公钥"
    def __init__(self):
        super(RecvAndSendDh,self).__init__() 
    
    def verify(self,rsa,msg,sign,fddata):
        return  rsa.VerifyByPubkey(msg, sign, fddata.GetData("peername"))
    
    def verifyMsgSign(self,msg,sign,fddata,th):
        "如果验证成功则发送公钥，否则发送验证失败并关闭该线程"
        _cfg = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfg.GetKeyPath())
        if self.verify(_rsa, msg[0], sign[0], fddata)== False or self.verify(_rsa, msg[1], sign[1], fddata)== False:
            msghead = self.packetMsg(MagicNum.MsgTypec.IDENTITYVERIFYFAILED, 0)
            fddata.SetData("outdata", msghead )
            th.ModifyInToOut(fddata.GetData("sockfd"))
        else:
            #生成自己的会话密钥
            _dhkey = DiffieHellman.DiffieHellman(string.atol(msg[0]))
            from CryptoAlgorithms import HashBySha1
            _hbs = HashBySha1.HashBySha1()
            fddata.SetData("fddatakey" ,_hbs.GetHash(str(_dhkey.getKey(string.atol(msg[1]))),MagicNum.HashBySha1c.HEXADECIMAL))
            _dhpubkey = str(_dhkey.getPubkey())
            msglist = [_dhpubkey,_rsa.SignByPrikey(_dhpubkey)]
            msgbody = NetSocketFun.NetPackMsgBody(msglist)
            msghead = self.packetMsg(MagicNum.MsgTypec.SENDDHPUBKEY, len(msgbody))
            fddata.SetData("outdata", msghead + msgbody ) 
            th.ModifyInToOut(fddata.GetData("sockfd"))
    
    def HandleMsg(self,bufsize,fddata,th):
        "接受对方传来的dh参数及公钥并生成自己的dh公钥"
        recvmsg = NetSocketFun.NetSocketRecv(fddata.GetData("sockfd"),bufsize)
        dhmsg = NetSocketFun.NetUnPackMsgBody(recvmsg)
        #参数p：公钥：签名
        self.verifyMsgSign(dhmsg[:2], dhmsg[2:], fddata,th)
        