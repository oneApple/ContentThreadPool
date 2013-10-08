# -*- coding: UTF-8 -*-
import SamplingFrameArray, GetSingleFrameSampling, RegionMap
from CryptoAlgorithms import HashBySha1
from GlobalData import MagicNum

class GetVideoSampling:
    def __init__(self,filename,framenum,gt,X,x0,u):
        self.__fnum = framenum
        self.__gt = gt
        self.__X = X
        self.__x0 = x0
        self.__u = u
        self.__filename = filename
    
    def sendViewMsg(self,showmsg):
        import wx
        from wx.lib.pubsub  import Publisher
        from GlobalData import CommonData
        msg = [showmsg,False]
        wx.CallAfter(Publisher().sendMessage,CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,msg)      
    
    def GetSampling(self):
        "第0帧不采集，帧区间是左闭又开区间，包括左边界，不包括右边界"
        _sfa = SamplingFrameArray.SamplingFrameArray(self.__fnum,self.__gt,self.__X,self.__x0,self.__u)
        _gsfs = GetSingleFrameSampling.GetSingleFrameSampling()
        _rgm = RegionMap.RegionMap()
        _hbs = HashBySha1.HashBySha1()
        _sfaArray = _sfa.SplitChaosArray()
        
        self.__videoSampling = []
        _groupindex = -1
        for _groupMap in _sfaArray:
            _groupindex += 1
            try:
                _gsampling = ""
                for _single in _groupMap:
                    _pos = _rgm.GetRegion(_groupMap[_single])
                    
                    showmsg = "采样了第" + str(_groupindex) + "组第" + str(_single) + "帧第" + str(_pos[0]) + "区第" + str(_pos[1]) + "单元"
                    self.sendViewMsg(showmsg)
                    
                    _gsampling += _gsfs.GetSingleSampling(_single, self.__filename,*_pos)
                self.__videoSampling.append(_hbs.GetHash(_gsampling,MagicNum.HashBySha1c.HEXADECIMAL))
            except:
                self.__videoSampling.append(_hbs.GetHash(_gsampling,MagicNum.HashBySha1c.HEXADECIMAL))
                break
        
        _groupborder = [x * (self.__fnum / self.__gt) for x in range(self.__gt)] + [self.__fnum]
        for _index in range(len(_groupborder)-1):
            showmsg = "组" + str(_index) +"：第" + str(_groupborder[_index]) + "帧-第"\
                      + str(_groupborder[_index + 1]) + "帧，比特串承诺值为：" + self.__videoSampling[_index]
            self.sendViewMsg(showmsg)
        
        return self.__videoSampling

if __name__ == "__main__":
    import GetSamplingParams
    s = GetSamplingParams.GetSamplingParams("gaoqing_mpeg2")
    p = s.GetSamplingParams()
    g = GetVideoSampling("gaoqing_mpeg2",*p)
                