# -*- coding: UTF-8 -*-
from CommandInterface import CommandInterface
from VideoSampling import ExecuteFfmpeg
from GlobalData import CommonData,ConfigData

import os

_metaclass_ = type
class SamplingCmd(CommandInterface,object):
    def __init__(self,view):
        super(SamplingCmd,self).__init__(view)
    
    def getFrameNumAndFileSize(self):
        "获取目录下文件数即帧的数目"
        _cfg = ConfigData.ConfigData()
        _fullpath = self.view.filename
        _filename = _fullpath[-_fullpath[::-1].index("/"):_fullpath.index(".")]
        _dirname = _cfg.GetYVectorFilePath() + _filename
        self.__framenum = sum([len(files) for root,dirs,files in os.walk(_dirname)])
        self.__filesize = os.path.getsize(self.view.filename)
    
    def Excute(self):
        
        _e = ExecuteFfmpeg.ExecuteFfmpeg(self.view.filename)
        _e.Run()
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, ["正在采样 . . .",False])
        _e.WaitForProcess()
        
        self.getFrameNumAndFileSize()
        filesize = float(self.__filesize) / (1024 * 1024)
        showmsg = "采样完成:\n(1)总帧数：" + str(self.__framenum) + "\n(2)文件大小（MB）：" + str(filesize)
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_REWRITETEXT, [showmsg,True])

        