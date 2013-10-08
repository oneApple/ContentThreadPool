# -*- coding: UTF-8 -*-
import os, random

from GlobalData import CommonData, ConfigData

class GetSamplingParams:
    "获取帧数目及分组参数gt.x,x0,u"
    def __init__(self,filename):
        "分别为文件名和分组数(参数Gt)"
        _cfg = ConfigData.ConfigData()
        self.__filename = _cfg.GetYVectorFilePath() + filename
        self.__gt = CommonData.Rsac.PLAINTLEN / CommonData.HashBySha1c.HEXHASH
        
    def getFrameNum(self):
        "获取目录下文件数即帧的数目"
        _dirname = self.__filename
        self.__framenum = sum([len(files) for root,dirs,files in os.walk(self.__filename)])
        if self.__gt > self.__framenum:
            self.__gt = self.__framenum
    
    def getGroupLen(self):
        "获取分组长度(参数X),_glen是每组的帧数目"
        _glen = self.__framenum / self.__gt - 1
        self.__x = 1
        while _glen >= 2:
            _glen = _glen / 2
            self.__x += 1
        if (self.__framenum / self.__gt - 1) < 2 ** self.__x:
            self.__x -= 1
    
    def getRandomX0AndU(self):
        "获取混沌序列初始值（x0）及系数u"
        self.__x0 = random.random()
        self.__u = random.uniform(3.5699456,4.0)
    
    def GetSamplingParams(self):
        self.getFrameNum()
        self.getGroupLen()
        self.getRandomX0AndU()
        return self.__framenum,self.__gt,self.__x,self.__x0,self.__u   

if __name__ == "__main__":
    s = GetSamplingParams("../View/gaoqing_mpeg2")
