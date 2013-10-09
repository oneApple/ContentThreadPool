# -*- coding: UTF-8 -*-
_metaclass_ = type

from NetCommunication import NetSocketFun
from MsgHandle import MsgHandleInterface
from DataBase import NOUserTable
from GlobalData import MagicNum

class RecvDhGenerateSuccess(MsgHandleInterface.MsgHandleInterface,object):
    "身份验证成功"
    def __init__(self):
        super(RecvDhGenerateSuccess,self).__init__() 
    
    def getUserPermission(self,name):
        _db = NOUserTable.NOUserTable()
        _db.Connect()
        _res = _db.searchUser(name)
        _db.CloseCon()
        return _res[0][2]
    
    def HandleMsg(self,bufsize,fddata,th):
        _permission = self.getUserPermission(fddata.GetData("peername"))
        msgbody = NetSocketFun.NetPackMsgBody([str(_permission)])
        msghead = self.packetMsg(MagicNum.MsgTypec.LOGINSUCCESS,len(msgbody))
        fddata.SetData("outdata",msghead + msgbody)
th.ModifyInToOut(fddata.GetData("sockfd"))
        