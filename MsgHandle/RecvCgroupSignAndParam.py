#coding=utf-8
_metaclass_ = type
import string
from NetCommunication import NetSocketFun
from MsgHandle import MsgHandleInterface
from GlobalData import CommonData, MagicNum, ConfigData
from DataBase import MediaTable
from CryptoAlgorithms import Rsa, HashBySha1
from VideoSampling import GetVideoSampling, ExecuteFfmpeg

class RecvCgroupSignAndParam(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvCgroupSignAndParam,self).__init__()
        _cfg = ConfigData.ConfigData()
        self.__mediapath = _cfg.GetMediaPath()
    
    def getBgroupSignAndParam(self,session):
        "从数据库查询获取b组参数和hash值"
        _db = MediaTable.MediaTable()
        _db.Connect()
        _res = _db.searchMedia(session.GetData("filename"))
        self.__bparam = _res[0][3]
        self.__bhash = _res[0][4]
        _db.CloseCon()
        
    def handleDhkeyAndCgroupParam(self,msglist,session):
        "验证接收到的会话密钥是否相同，如果相同则获取C组参数和hash"
        _cfd = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfd.GetKeyPath())
        _plaintext = _rsa.DecryptByPrikey(msglist[0])
        _plist = NetSocketFun.NetUnPackMsgBody(_plaintext)
        if session.GetData("sessionkey") == _plist[0]:
            self.__cparam = _plist[1:]
            self.__csign = msglist[1]
            self.__chash = msglist[2]
            return True
        else:
            showmsg = "会话密钥验证失败：会话密钥：" + session.GetData("sessionkey")
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
            return False
    
    def verifySignleSign(self,sampling,sign,session):
        "验证C组采样是否符合收到的C组签名"
        _cfd = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfd.GetKeyPath())
        
        _hbs = HashBySha1.HashBySha1()
        return _rsa.VerifyByPubkey(_hbs.GetHash(sampling.encode("ascii"),MagicNum.HashBySha1c.HEXADECIMAL), sign, session.GetData("peername"))
    
    def getFrameNum(self,filename):
        "获取目录下文件数即帧的数目"
        import os
        _cfg = ConfigData.ConfigData()
        _dirname = _cfg.GetYVectorFilePath() + filename[:filename.index(".")]
        _framenum = sum([len(files) for root,dirs,files in os.walk(_dirname)])
        return str(_framenum)
    
    def verifySign(self,session):
        import string
        _hashlist = []
        _bparam = NetSocketFun.NetUnPackMsgBody(self.__bparam)
        
        showmsg = "正在采样 ..."
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
        _meidaPath = self.__mediapath + "/" + session.GetData("peername") + "/" + session.GetData("filename")
        _efm = ExecuteFfmpeg.ExecuteFfmpeg(_meidaPath)
        _efm.Run()
        _efm.WaitForProcess()
        
        import os
        filesize = float(os.path.getsize(_meidaPath)) / (1024 * 1024)
        showmsg = "采样完成:\n(1)总帧数：" + self.getFrameNum(session.GetData("filename")) + \
                  "\n(2)文件大小（MB）：" + str(filesize)
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
        
        showmsg = ["B组采样过程：","C组采样过程："]
        for _param in [_bparam,self.__cparam]:
            _argum = [string.atoi(s) for s in _param[:3]]
            _argum += [string.atof(s) for s in _param[3:]]
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg[len(_hashlist)],True)
            _hashlist.append(self.computeSingleSampling(session, _argum))
            
            
        self.deltempFile(session)
        
        if not self.verifySignleSign(_hashlist[1], self.__csign, session):
            self.compareSamplingHash(_hashlist[1],self.__chash)
            showmsg = "签名验证失败,该文件在传输过程中被篡改"
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
            return False
        elif self.__bhash != _hashlist[0]:
            self.compareSamplingHash(_hashlist[0],self.__bhash)
            showmsg = "文件验证失败,该文件已被审核部门修改"
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
            return False
        else:
            self.compareSamplingHash(_hashlist[1],self.__chash,title = "Ｃ组")
            showmsg = "签名验证成功,该文件在传输过程中未被篡改"
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
            self.compareSamplingHash(_hashlist[0],self.__bhash,title = "Ｂ组")
            showmsg = "文件验证成功,该文件未被审核部门修改"
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
            return True
    
    def computeSingleSampling(self,session,param):
        _filename = session.GetData("filename")[:session.GetData("filename").index(".")]
        _gvs = GetVideoSampling.GetVideoSampling(_filename,*param)
        
        return NetSocketFun.NetPackMsgBody(_gvs.GetSampling())
    
    def compareSamplingHash(self,localhash,recvhash,title = ""):
        "分组验证"
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,title + "分组进行比对:",True)
        difList = []
        localhash = NetSocketFun.NetUnPackMsgBody(localhash)
        recvlist = NetSocketFun.NetUnPackMsgBody(recvhash)
        for i in range(len(recvlist)):
            try:
                if localhash[i] != recvlist[i]:
                    difList.append(i)
                    showmsg = "第" + str(i) + "组验证失败"
                else:
                    showmsg = "第" + str(i) + "组验证成功"
                self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
            except:
                difList += [index for index in range(i,len(recvlist))]
                break
        
        import string
        _bparam = NetSocketFun.NetUnPackMsgBody(self.__bparam)
        _fnum = string.atoi(_bparam[0])
        _gt = string.atoi(_bparam[1])
        
        _groupborder = [x * (_fnum / _gt) for x in range(_gt)] + [_fnum]
        
        if len(difList) == 0:
            showmsg = "结果：采样验证成功，该文件未被篡改"
        else:
            showmsg = "结果：采样验证失败，该文件被篡改,其中"
        for _dif in difList:
            showmsg += "\n第" + str(_dif) + "组存在篡改，篡改帧区间为：" + str(_groupborder[_dif]) + "-" + str(_groupborder[_dif + 1]) +"帧"
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
    
    def deltempFile(self,session):
        import os
        _cfg = ConfigData.ConfigData()
        _mediapath = _cfg.GetYVectorFilePath()
        _media = _mediapath + "out.ts" 
        os.remove(_media)
        _dir = _mediapath + session.GetData("filename")[:session.GetData("filename").index(".")]
        for root, dirs, files in os.walk(_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            os.rmdir(root)  
    
    def HandleMsg(self,bufsize,session):
        recvbuffer = NetSocketFun.NetSocketRecv(session.GetData("sockfd"),bufsize)
        _msglist = NetSocketFun.NetUnPackMsgBody(recvbuffer)
        if self.handleDhkeyAndCgroupParam(_msglist, session) == True:
            try:
                self.getBgroupSignAndParam(session)
            except:
                import wx
                wx.MessageBox("该文件不存在","错误",wx.ICON_ERROR|wx.YES_DEFAULT)
                return
            if self.verifySign(session) == True:
                showmsg = "收到采样结果:\n(1)B组参数：" + ",".join(self.__bparam.split(CommonData.MsgHandlec.PADDING)) + "\n(2)B组采样签名：" + _msglist[1]
                showmsg += "\n(3)C组参数：" + ",".join(self.__cparam) + "\n(4)C组采样签名：" + self.__csign + "\n审核返回成功"
                self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg,True)
                msghead = self.packetMsg(MagicNum.MsgTypec.AUDITRETURNSUCCESS,0)
                NetSocketFun.NetSocketSend(session.GetData("sockfd"),msghead)
                
                
                _db = MediaTable.MediaTable()
                _db.Connect()
                _db.AlterMedia("status", MagicNum.MediaTablec.AUDIT,session.GetData("filename"))
                _db.CloseCon()
                self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_REFRESHFILETABLE,"")
                return
            
        msghead = self.packetMsg(MagicNum.MsgTypec.IDENTITYVERIFYFAILED,0)
        NetSocketFun.NetSocketSend(session.GetData("sockfd"),msghead)
        
if __name__ == "__main__":
    pass