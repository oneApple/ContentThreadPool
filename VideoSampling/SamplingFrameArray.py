# -*- coding: UTF-8 -*-
from CryptoAlgorithms import Chaos
from GlobalData import CommonData

class SamplingFrameArray:
    "获取采样帧的序列"
    def __init__(self,framenum,gt,X,x0,u):
        self.__fnum = framenum
        self.__gt = gt
        self.__X = X
        self.__x0 = x0
        self.__u = u
                
    def getChaosArray(self):
        "获取二进制的混沌序列"
        _arraylen = self.__fnum * (self.__X + CommonData.SamplingFrameArrayc.GROUPPARAMELEN)
        _c = Chaos.Chaos(_arraylen,self.__x0,self.__u)
        self.__binChaosArray = _c.getBinaryArray()
    
    def binaryToDecimal(self,binArray):
        "二进制转化为十进制"
        _bin = binArray[::-1]
        _dec = 0;
        for i,b in enumerate(_bin):
            if b == 1:
                _dec += 2**i
        return _dec
    
    def SplitChaosArray(self):
        "获取一个序列，每个元素是一组，该组是一个map，是序列号与位置的对应"
        self.getChaosArray()
        _groupborder = [x * (self.__fnum / self.__gt) for x in range(1,self.__gt)] + [self.__fnum]
        _curframe = 0
        _index = 0
        self.__groupChaosArray = []
        for border in _groupborder:
            _singlemap = {}
            while _curframe < border:
                _grouplen = CommonData.SamplingFrameArrayc.GROUPPARAMELEN + self.__X
                _singleChaos = self.__binChaosArray[_index * _grouplen : (_index + 1) * _grouplen]
                _fdata = _singleChaos[self.__X:]
                if _curframe != 0:
                    _singlemap[_curframe] = _fdata
                elif self.__X == 1:
                    _singlemap[_curframe + 1] = _fdata
                
                if self.__X == 0:
                    _fpos = 1
                else:
                    _fpos = self.binaryToDecimal(_singleChaos[:-CommonData.SamplingFrameArrayc.GROUPPARAMELEN]) + 1
                _curframe += _fpos
                _index += 1
            self.__groupChaosArray.append(_singlemap)
        return self.__groupChaosArray
    
if __name__ == "__main__":
    import GetSamplingParams
    s = GetSamplingParams.GetSamplingParams("../View/gaoqing_mpeg2")
    p = s.GetSamplingParams()
    a = SamplingFrameArray(*p)
    