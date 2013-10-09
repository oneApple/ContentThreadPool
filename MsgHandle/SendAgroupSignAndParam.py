
# -*- coding: UTF-8 -*-
_metaclass_ = type

from NetCommunication import NetSocketFun
from MsgHandle import MsgHandleInterface
from GlobalData import CommonData, MagicNum, ConfigData
from DataBase import MediaTable
from CryptoAlgorithms import Rsa, HashBySha1

class SendAgroupSignAndParam(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendAgroupSignAndParam,self).__init__()
        _cfg = ConfigData.ConfigData()
        self.__mediapath = _cfg.GetMediaPath()
    
    def APgetAgroupHashAndParam(self,fddata):
        "得到数据库中存放的A组参数和hash"
        _db = MediaTable.MediaTable()
        _db.Connect()
        _dir = fddata.GetData("filename")
        _filename =  _dir[-_dir[::-1].index("/"):]
        _res = _db.searchMedia(_filename)
        return NetSocketFun.NetUnPackMsgBody(_res[0][1]), _res[0][2]
    
    def deltempFile(self,fddata):
        import os
        _cfg = ConfigData.ConfigData()
        _mediapath = _cfg.GetYVectorFilePath()
        _media = _mediapath + "out.ts" 
        os.remove(_media)
        _dir = _mediapath + fddata.GetData("filename")[:fddata.GetData("filename").index(".")]
        for root, dirs, files in os.walk(_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            os.rmdir(root)  
    
    def getFrameNum(self,filename):
        "获取目录下文件数即帧的数目"
        import os
        _cfg = ConfigData.ConfigData()
        _dirname = _cfg.GetYVectorFilePath() + filename[:filename.index(".")]
        _framenum = sum([len(files) for root,dirs,files in os.walk(_dirname)])
        return str(_framenum)
    
    def NOgetAgroupHashAndParam(self,fddata):
        "得到数据库中存放的A组参数和hash"
        _db = MediaTable.MediaTable()
        _db.Connect()
        _dir = fddata.GetData("filename")
        _filename =  _dir[-_dir[::-1].index("/"):]
        _res = _db.searchMedia(_filename)
        
        showmsg = "正在采样 ..."
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
        from VideoSampling import ExecuteFfmpeg,GetVideoSampling
        _meidaPath = self.__mediapath + "/auditserver/" + _dir[-_dir[::-1].index("/"):]
        _efm = ExecuteFfmpeg.ExecuteFfmpeg(_meidaPath)
        _efm.Run()
        _efm.WaitForProcess()
        
        import os
        filesize = float(os.path.getsize(_meidaPath)) / (1024 * 1024)
        showmsg = "采样完成:\n(1)总帧数：" + self.getFrameNum(_dir[-_dir[::-1].index("/"):]) + \
                  "\n(2)文件大小（MB）：" + str(filesize)
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
        
        _sparam = NetSocketFun.NetUnPackMsgBody(_res[0][1])
        import string
        _iparam = [string.atoi(s) for s in _sparam[:3]] + [string.atof(s) for s in _sparam[3:]]
        
        _cgvs = GetVideoSampling.GetVideoSampling(_filename[:_filename.index(".")],*_iparam)
        try:
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, "Ａ组采样过程:",True)
            return NetSocketFun.NetUnPackMsgBody(_res[0][1]),NetSocketFun.NetPackMsgBody(_cgvs.GetSampling())
        except:
            return NetSocketFun.NetUnPackMsgBody(_res[0][1]),""
    
    def packMsgBody(self,fddata):
        "将会话密钥与A组参数用公钥加密，将采样hash用私钥加密（签名）"
        if fddata.GetData("threadtype") == CommonData.ThreadType.CONNECTAP:
            _agroup = self.APgetAgroupHashAndParam(fddata)
        elif fddata.GetData("threadtype") == CommonData.ThreadType.ACCETPNO:
            _agroup = self.NOgetAgroupHashAndParam(fddata)
            self.deltempFile(fddata)
                      
        _cfd = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfd.GetKeyPath())
        msglist = (str(fddata.GetData("fddatakey")),) + _agroup[0]
        _plaintext = NetSocketFun.NetPackMsgBody(msglist)
        _pubkeyMsg = _rsa.EncryptByPubkey(_plaintext.encode("ascii"), fddata.GetData("peername"))
        
        _hbs = HashBySha1.HashBySha1()
        _sign = _rsa.SignByPrikey(_hbs.GetHash(_agroup[1].encode("ascii"),MagicNum.HashBySha1c.HEXADECIMAL))
        msglist = [_pubkeyMsg,_sign,_agroup[1].encode("ascii")]
        _msgbody = NetSocketFun.NetPackMsgBody(msglist)
        showmsg = "发送采样结果：\n(1)A组参数:\n(帧总数,分组参数,帧间隔位数,混沌初值,分支参数)\n(".decode("utf8") + \
                  ",".join(_agroup[0]) + ")\n(2)A组采样:".decode("utf8") + \
                  CommonData.MsgHandlec.SHOWPADDING.join(NetSocketFun.NetUnPackMsgBody(_agroup[1]))  \
                  + "\n(3)A组采样签名：".decode("utf8") + _sign 
        showmsg += "\nCP用AP的公钥加密采样参数A"
        showmsg += "\nCP用其私钥加密比特串承诺值"
        showmsg += "\nCP发送加密的A组参数和加密的比特串承诺值，以及公钥加密TID发送给AP"
        showmsg += "\n等待文件验证..."
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg,True)
        return _msgbody
    
    def HandleMsg(self,bufsize,fddata,th):
        msgbody = self.packMsgBody(fddata)
        msghead = self.packetMsg(MagicNum.MsgTypec.SENDAGROUP,len(msgbody))
        fddata.SetData("outdata",msghead + msgbody)
        th.ModifyInToOut(fddata.GetData("sockfd"))
        
if __name__ == "__main__":
    pass    
        