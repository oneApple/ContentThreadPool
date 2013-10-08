# -*- coding: UTF-8 -*-
from GlobalData import ConfigData

class GetSingleFrameSampling:
    "获取每帧的采样"
    def getFrameFileData(self,frame,filename):
        "获取文件数据"
        self.__frameData = []
        _cfg = ConfigData.ConfigData()
        _path = _cfg.GetYVectorFilePath() + filename + "/" + str(frame) + ".yvector"
        with open(_path) as f:
            for line in f.xreadlines():
                self.__frameData.append(line[:-1].split(","))
        _len = len(self.__frameData)
        del self.__frameData[_len - 1]
        del self.__frameData[_len - 2]
    
    def GetSingleSampling(self,frame,filename,region,unit):
        "获取一个帧的采样，以字符串形式输出"
        self.getFrameFileData(frame,filename)
        _rrowlen = len(self.__frameData) / 3
        _rcollen = len(self.__frameData[0]) / 3 
        _urowlen = _rrowlen / 2
        _ucollen = _rcollen / 2
        
        _rx = region % 3
        _ry = region / 3
        
        _ux = unit % 2
        _uy = unit / 2
        
        _sampling = []
        _xbegin = _rx * _rcollen + _ux * _ucollen
        _ybegin = _ry * _rrowlen + _uy * _urowlen
        for _region in range(_ybegin,_ybegin + _urowlen):
            _sampling += self.__frameData[_region][_xbegin:_xbegin + _ucollen]
        self.__samplingStr = "".join(_sampling)
        return self.__samplingStr
        
        
        

if __name__ == "__main__":
    g = GetSingleFrameSampling()
