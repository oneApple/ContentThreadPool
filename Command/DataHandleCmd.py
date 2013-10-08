# -*- coding: UTF-8 -*-
from CommandInterface import CommandInterface
from VideoSampling import GetVideoSampling
from DataBase import MediaTable
from GlobalData import CommonData, ConfigData
from  NetCommunication import NetSocketFun

_metaclass_ = type
class DataHandleCmd(CommandInterface,object):
    "将采样数据进行hash并记录入数据库"
    def __init__(self,view,aparams,bparams):
        super(DataHandleCmd,self).__init__(view)
        _cfg = ConfigData.ConfigData()
        self.__mediapath = _cfg.GetYVectorFilePath()
        
        self.__aparams = aparams
        self.__bparams = bparams
    
    def handleParam(self,sampling):
        "将列表转化为字符串"
        _aparam = NetSocketFun.NetPackMsgBody(sampling[0])
        _ahash = NetSocketFun.NetPackMsgBody(sampling[1])
        _bparam = NetSocketFun.NetPackMsgBody(sampling[2])
        _bhash = NetSocketFun.NetPackMsgBody(sampling[3])
        return _aparam, _ahash, _bparam, _bhash 
    
    def addNewMedia(self,filename,audituser,sampling):
        "增加媒体到数据库"
        _db = MediaTable.MediaTable()
        _db.Connect()
        _value = (filename.decode("utf8"),) + sampling + (audituser.decode("utf8"),)
        if not _db.AddNewMedia(_value):
            import wx
            wx.MessageBox("该视频已存在，相关数据无法存入数据库","错误",wx.ICON_ERROR|wx.YES_DEFAULT)
        _db.CloseCon()
    
    def handleSamplingParams(self,params):
        import string
        return list(params[:3]) + [string.atof(str(s)) for s in params[3:]]
    
    def getMediaHashAndParam(self):
        "从媒体采样数据中获取hash及参数"
        _dir = self.view.filename
        _filename = _dir[-_dir[::-1].index("/"):_dir.index(".")]
        _aparam = self.handleSamplingParams(self.__aparams)
        _bparam = self.handleSamplingParams(self.__bparams)
        
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,"Ａ组采样过程:",True)
        _agvs = GetVideoSampling.GetVideoSampling(_filename,*_aparam)
        _asampling = _agvs.GetSampling()
        
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, "B组采样过程:",True)
        _bgvs = GetVideoSampling.GetVideoSampling(_filename,*_bparam)
        _bsampling = _bgvs.GetSampling()
        
        return [str(x) for x in _aparam], _asampling, [str(x) for x in _bparam], _bsampling
    
    def deltempFile(self,filename):
        import os
        _media = self.__mediapath + "out.ts" 
        os.remove(_media)
        _dir = self.__mediapath + filename[:filename.index(".")]
        for root, dirs, files in os.walk(_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            os.rmdir(root)  
    
    def Excute(self):
        _sampling = self.handleParam(self.getMediaHashAndParam())
        _dir = self.view.filename
        _filename   = _dir[-_dir[::-1].index("/"):]
        self.addNewMedia(_filename,self.view.audituser, _sampling)
        try:
            self.deltempFile(_filename)
        except Exception,e:
            print e
        self.view.netconnect.ReqAudit(_dir)